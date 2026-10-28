# ==============================================================================
# CONFIGURAZIONE MORFOLOGIA SPOT (Parametri Limnologici & Coefficienti Energetici)
# ==============================================================================
SPOT_TYPES = {
    "Cava / Lago Profondo (Sassaie, Drop-off)": {
        "alpha": 0.06,          # Alta inerzia termica (EMA 30gg): grande volume ipolimnico
        "rad_factor": 0.16,     # Guadagno radiativo orario contenuto (°C per 1000 W/m²)
        "sensible_k": 0.012,    # Coefficiente di scambio convettivo aria-acqua ridotto
        "evap_factor": 0.04,    # Perdita per calore latente/evaporazione minima
        "ir_loss": 0.035,       # Perdita radiativa infrarossa notturna (onde lunghe)
        "max_swing": 1.10,      # Escursione diurna massima fisicamente ammissibile (picco-picco)
        "desc": "Alta inerzia termica (α=0.06): massa d'acqua profonda, risente pochissimo degli sbalzi giornalieri."
    },
    "Lago Medio / Bacino Misto (Canneti, Punte, Legnaie)": {
        "alpha": 0.12,          # Inerzia termica intermedia
        "rad_factor": 0.30,     # Risposta moderata delle fasce litorali all'irraggiamento
        "sensible_k": 0.022,    # Scambio termico sensibile intermedio
        "evap_factor": 0.08,    # Raffreddamento evaporativo moderato sotto vento
        "ir_loss": 0.060,       # Perdita infrarossa notturna media
        "max_swing": 2.10,      # Escursione diurna moderata (picco-picco ~2.1°C)
        "desc": "Inerzia termica media (α=0.12): equilibrio tra massa pelagica e zone di acqua bassa."
    },
    "Acqua Bassa / Canale / Palude / Bozzo (< 2.5m)": {
        "alpha": 0.22,          # Bassa inerzia termica: colonna d'acqua ridotta, risposta rapida
        "rad_factor": 0.48,     # Alto assorbimento fotonico sul fondale basso e scuro
        "sensible_k": 0.038,    # Forte accoppiamento convettivo con la temperatura dell'aria
        "evap_factor": 0.14,    # Forte dispersione per calore latente in presenza di vento
        "ir_loss": 0.095,       # Rapido raffreddamento notturno per irraggiamento
        "max_swing": 3.40,      # Forte escursione tra alba e tardo pomeriggio
        "desc": "Bassa inerzia termica (α=0.22): risponde rapidamente sia alle insolazioni sia ai fronti freddi."
    }
}


# ==============================================================================
# MODULO 1: STIMATORE LIMNOLOGICO E INTEGRATORE TERMODINAMICO ORARIO
# ==============================================================================
@st.cache_data(ttl=1800, show_spinner=False)
def fetch_thermal_and_weather_series(lat: float, lon: float, day_offset: int, spot_morphology: str) -> dict:
    """
    Scarica 30 giorni di storico + 3 giorni di previsione da Open-Meteo.
    Implementa:
    1. Raggruppamento giornaliero esatto e calcolo EMA con asintoto di densità massima (3.8°C - 4.0°C)
       e Radiative Night Cooling per le notti serene (< 25% nuvole).
    2. Integratore energetico orario ricorsivo (accumulo solare + calore sensibile - evaporazione - IR)
       privo di sinusoidi fittizie, centrato attorno a base_water_temp.
    3. Metriche multi-scala: pressure_delta (3h), pressure_trend_12h (12h) e do_saturation_index (Ossigeno Disciolto).
    4. Matrice dello Stato Biologico termo-consapevole (ancorata a base_water_temp).
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,surface_pressure,cloud_cover,wind_speed_10m,shortwave_radiation",
        "timezone": "auto",
        "past_days": 30,
        "forecast_days": 3
    }
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    pressures = hourly.get("surface_pressure", [])
    clouds = hourly.get("cloud_cover", [])
    winds = hourly.get("wind_speed_10m", [])
    radiations = hourly.get("shortwave_radiation", [])

    if not times or len(times) < (30 + day_offset + 1) * 24:
        raise ValueError("Serie storica/previsionale incompleta per la data selezionata.")

    morph = SPOT_TYPES.get(spot_morphology, list(SPOT_TYPES.values())[1])
    alpha_base = morph["alpha"]

    # --------------------------------------------------------------------------
    # 1. RAGGRUPPAMENTO GIORNALIERO ESATTO & EMA CON LIMITE DENSITÀ (3.8°C)
    # --------------------------------------------------------------------------
    # Raggruppiamo per data calendario effettiva ("YYYY-MM-DD") garantendo blocchi allineati
    days_map = {}
    for idx, dt_str in enumerate(times):
        d_key = dt_str.split("T")[0]
        if d_key not in days_map:
            days_map[d_key] = []
        days_map[d_key].append(idx)

    sorted_dates = sorted(days_map.keys())
    # Indice 30 = Oggi (dopo i 30 past_days: indici 0..29)
    target_day_pos = min(30 + day_offset, len(sorted_dates) - 1)
    target_date_str = sorted_dates[target_day_pos]

    daily_air_means = []
    daily_cloud_means = []

    for d_idx in range(target_day_pos + 1):
        d_key = sorted_dates[d_idx]
        hour_indices = days_map[d_key]
        valid_t = [float(temps[i]) for i in hour_indices if temps[i] is not None]
        valid_c = [float(clouds[i]) for i in hour_indices if clouds[i] is not None]
        
        daily_air_means.append(sum(valid_t) / len(valid_t) if valid_t else 15.0)
        daily_cloud_means.append(sum(valid_c) / len(valid_c) if valid_c else 50.0)

    # Inizializzazione del seme EMA sui primi 3 giorni (rispettando il pavimento di 3.8°C)
    seed_temp = sum(daily_air_means[:3]) / 3.0
    current_ema = max(3.8, seed_temp)
    ema_water_history = []

    for d_idx in range(len(daily_air_means)):
        t_air_d = daily_air_means[d_idx]
        c_cov_d = daily_cloud_means[d_idx]

        # A) Radiative Night Cooling: se la copertura nuvolosa media giornaliera è < 25%,
        # il corpo idrico subisce una maggiore dispersione infrarossa notturna verso il cielo sereno
        radiative_night_cooling = 0.0
        if c_cov_d < 25.0:
            radiative_night_cooling = ((25.0 - c_cov_d) / 25.0) * (0.45 * (alpha_base / 0.12))

        t_forcing = t_air_d - radiative_night_cooling

        # B) Asimmetria di Densità dell'Acqua Dolce (< 8.0°C):
        # Avvicinandosi a 4.0°C (massima densità dell'H2O), il rimescolamento convettivo
        # rallenta il raffreddamento. Smorziamo alpha e comprimiamo la forzante verso l'asintoto 3.8°C
        if current_ema < 8.0 and t_forcing < current_ema:
            density_damping = max(0.18, (current_ema - 3.8) / 4.2)
            eff_alpha = alpha_base * density_damping
            if t_forcing < 3.8:
                # L'aria sottozero cede freddo molto più lentamente grazie allo strato limite superficiale
                t_forcing = 3.8 - ((3.8 - t_forcing) * 0.15)
        else:
            eff_alpha = alpha_base

        current_ema = (eff_alpha * t_forcing) + ((1.0 - eff_alpha) * current_ema)

        # Barriera fisica invalicabile di congelamento/densità di fondo a 3.8°C
        if current_ema < 3.8:
            current_ema = 3.8 + 0.05 * math.exp(current_ema - 3.8)
        current_ema = max(3.8, current_ema)

        ema_water_history.append(current_ema)

    base_water_temp = round(ema_water_history[-1], 2)

    # --------------------------------------------------------------------------
    # 2. VETTORI TERMICI MULTI-SCALA (MACRO 14GG & MICRO 72H)
    # --------------------------------------------------------------------------
    recent_3d_water_mean = sum(ema_water_history[-3:]) / 3.0
    past_14d_slice = ema_water_history[-16:-13] if len(ema_water_history) >= 16 else ema_water_history[:3]
    past_14d_water_mean = sum(past_14d_slice) / len(past_14d_slice)
    macro_trend_14d = round(recent_3d_water_mean - past_14d_water_mean, 2)

    target_hour_indices = days_map[target_date_str][:24]
    target_start_idx = target_hour_indices[0]
    target_end_idx = target_start_idx + 24

    ema_delta_72h = ema_water_history[-1] - ema_water_history[max(0, len(ema_water_history) - 4)]
    air_last_24h = sum(float(t) for t in temps[max(0, target_start_idx - 24) : target_start_idx] if t is not None) / 24.0
    air_72h_ago = sum(float(t) for t in temps[max(0, target_start_idx - 96) : max(24, target_start_idx - 72)] if t is not None) / 24.0
    
    # Se siamo vicino a 3.8°C e l'aria scende, l'impulso superficiale è frenato dal pavimento fisico
    shallow_damping = 0.25 if (base_water_temp < 5.5 and air_last_24h < air_72h_ago) else 1.0
    shallow_impulse_72h = (air_last_24h - air_72h_ago) * (alpha_base * 1.5) * shallow_damping
    micro_trend_72h = round((ema_delta_72h * 0.65) + (shallow_impulse_72h * 0.35), 2)

    # --------------------------------------------------------------------------
    # 3. INTEGRATORE TERMICO ORARIO CUMULATIVO (Bilancio Energetico Ricorsivo)
    # --------------------------------------------------------------------------
    # Simuliamo l'accumulo e il rilascio di calore ora dopo ora: T_w(h) = T_w(h-1) + dT_net(h).
    # In questo modo l'acqua mantiene memoria termica: se passa una nuvola per un'ora non crolla,
    # e il picco termico cade naturalmente nel tardo pomeriggio (15:00 - 17:00).
    raw_trace = []
    # Partiamo all'ora 00:00 leggermente sotto la media giornaliera (raffreddamento notturno in corso)
    sim_tw = max(3.8, base_water_temp - (morph["max_swing"] * 0.25))

    for idx in range(target_start_idx, target_end_idx):
        air_t = float(temps[idx]) if temps[idx] is not None else base_water_temp
        wind_kmh = float(winds[idx]) if winds[idx] is not None else 0.0
        rad_wm2 = float(radiations[idx]) if radiations[idx] is not None else 0.0
        cloud_pct = float(clouds[idx]) if clouds[idx] is not None else 50.0

        # 1) Guadagno per Irraggiamento Solare ad Onda Corta (dT_solar >= 0)
        dt_solar = (rad_wm2 / 1000.0) * morph["rad_factor"]

        # 2) Scambio Termico Convettivo Sensibile (dT_sensible):
        # Dipende strettamente da (T_air - T_water)! Se il vento è più caldo dell'acqua, cede calore all'acqua;
        # se il vento è più freddo dell'acqua, sottrae calore. Amplificato moderatamente dalla velocità del vento.
        wind_conv_boost = 1.0 + min(1.5, wind_kmh / 20.0)
        dt_sensible = morph["sensible_k"] * (air_t - sim_tw) * wind_conv_boost

        # 3) Perdita per Calore Latente di Evaporazione (dT_evap >= 0):
        # Attiva per vento > 10 km/h. È accentuata se l'acqua è calda (alta tensione di vapore)
        # o se l'aria è più fredda dell'acqua. Fortemente ridotta se l'aria è molto più calda dell'acqua (condensazione/stabilità).
        if wind_kmh > 10.0:
            wind_excess = min(2.0, (wind_kmh - 10.0) / 18.0)
            vapor_factor = max(0.15, min(1.8, (sim_tw - 4.0) / 18.0))
            delta_aw_factor = 1.35 if air_t < sim_tw else max(0.20, 1.0 - ((air_t - sim_tw) * 0.12))
            dt_evap = morph["evap_factor"] * wind_excess * vapor_factor * delta_aw_factor
        else:
            dt_evap = 0.0

        # 4) Perdita Radiativa Infrarossa ad Onda Lunga (dT_ir):
        # Costante perdita verso l'atmosfera, massima con cielo sereno, schermata dalle nuvole
        clear_sky_factor = 1.0 - (0.65 * (cloud_pct / 100.0))
        dt_ir = morph["ir_loss"] * clear_sky_factor

        # Passo di integrazione oraria (Metodo di Eulero sul bilancio energetico)
        dt_net = dt_solar + dt_sensible - dt_evap - dt_ir
        sim_tw = max(3.8, sim_tw + dt_net)
        raw_trace.append(sim_tw)

    # Centratura e normalizzazione della curva cumulativa attorno a base_water_temp:
    # Elimina qualsiasi deriva netta artificiale a fine giornata preservando la forma fisica reale
    # dell'accumulo pomeridiano e limitando l'escursione massima ai limiti fisici del corpo idrico
    trace_mean = sum(raw_trace) / 24.0
    centered_trace = [t - trace_mean for t in raw_trace]
    current_span = max(centered_trace) - min(centered_trace)

    if current_span > morph["max_swing"] and current_span > 0:
        scale_ratio = morph["max_swing"] / current_span
        centered_trace = [d * scale_ratio for d in centered_trace]

    final_hourly_water_temps = [round(max(3.8, base_water_temp + d), 1) for d in centered_trace]

    # --------------------------------------------------------------------------
    # 4. COSTRUZIONE RECORD ORARI E INDICE DI SATURAZIONE OSSIGENO (DO)
    # --------------------------------------------------------------------------
    hourly_records = []
    for h_pos, idx in enumerate(range(target_start_idx, target_end_idx)):
        dt_str = times[idx]
        hour_int = int(dt_str.split("T")[1].split(":")[0])
        air_t = round(float(temps[idx]), 1)
        w_temp = final_hourly_water_temps[h_pos]
        wind_kmh = round(float(winds[idx]), 1)
        rad_wm2 = int(float(radiations[idx])) if radiations[idx] is not None else 0
        cloud_pct = int(clouds[idx])

        # Variazioni barometriche a 3 ore (trigger acuto) e a 12 ore (fronte sinottico strutturato)
        curr_press = float(pressures[idx])
        prev_press_3h = float(pressures[max(0, idx - 3)])
        prev_press_12h = float(pressures[max(0, idx - 12)])
        press_delta_3h = round(curr_press - prev_press_3h, 1)
        press_trend_12h = round(curr_press - prev_press_12h, 1)

        # Calcolo Indice di Saturazione Ossigeno Disciolto (do_saturation_index: 0.0 -> 1.0):
        # Segue la legge fisica di solubilità di Henry (l'acqua fredda trattiene molto più O2 dell'acqua calda).
        # Sopra i 24°C la solubilità cala criticamente, ma il rimescolamento eolico (onde) e la fotosintesi diurna ossigenano lo strato.
        if w_temp <= 14.0:
            base_do = 0.96
        elif w_temp <= 22.0:
            base_do = 0.96 - ((w_temp - 14.0) / 8.0) * 0.20  # Scende gradualmente da 0.96 a 0.76
        else:
            base_do = 0.76 - ((w_temp - 22.0) / 11.0) * 0.56 # Cala da 0.76 fino a 0.20 a 33°C

        # Rimescolamento meccanico superficiale da vento/onde (più incisivo quando l'acqua è calda e ipossica)
        wind_reaeration = min(0.22, (wind_kmh / 25.0) * (0.20 if w_temp > 22.0 else 0.07))
        # Contributo fotosintetico diurno vs respirazione vegetale notturna (critico in acque calde ricche di erbai)
        photo_mod = 0.04 if rad_wm2 > 250 else (-0.06 if (rad_wm2 == 0 and w_temp > 24.0) else 0.0)

        do_saturation_index = round(max(0.10, min(1.00, base_do + wind_reaeration + photo_mod)), 3)

        hourly_records.append({
            "hour": hour_int,
            "time_label": f"{hour_int:02d}:00",
            "date_str": dt_str.split("T")[0],
            "air_temp": air_t,
            "water_temp": w_temp,
            "pressure": round(curr_press, 1),
            "pressure_delta": press_delta_3h,
            "pressure_trend_12h": press_trend_12h,
            "clouds": cloud_pct,
            "wind": wind_kmh,
            "radiation": rad_wm2,
            "do_saturation_index": do_saturation_index
        })

    # --------------------------------------------------------------------------
    # 5. MATRICE STATO BIOLOGICO TERMO-CONSAPEVOLE (Ancorata a base_water_temp)
    # --------------------------------------------------------------------------
    # Scaglione 1: Regime Invernale / Ipometabolico (< 10.5°C)
    if base_water_temp < 10.5:
        if micro_trend_72h >= 0.7:
            biological_state = (
                f"Finestra di Risveglio Invernale ({base_water_temp}°C, Δ72h {micro_trend_72h:+.1f}°C: "
                "anomalia tiepida che sblocca brevi risalite pomeridiane sui primi scalini)"
            )
        elif micro_trend_72h <= -0.7 or macro_trend_14d <= -1.2:
            biological_state = (
                f"Letargo Termico Invernale ({base_water_temp}°C: "
                "metabolismo ai minimi storici e stazionamento passivo nelle buche più profonde)"
            )
        else:
            biological_state = (
                f"Stasi Ipometabolica Invernale ({base_water_temp}°C: "
                "acqua fredda stabilizzata, micro-finestra di attività solo nelle ore di massima insolazione)"
            )

    # Scaglione 2: Regime di Transizione Primaverile o Autunnale (10.5°C <= T < 16.0°C)
    elif 10.5 <= base_water_temp < 16.0:
        if macro_trend_14d >= 0.5 and micro_trend_72h <= -0.9:
            biological_state = (
                f"Primavera Ingannevole / Cold Front ({base_water_temp}°C, Δ72h {micro_trend_72h:+.1f}°C: "
                "brusco stop post-riscaldamento, pesci sospesi sui drop-off e bocca chiusa)"
            )
        elif macro_trend_14d <= -0.5 and micro_trend_72h >= 0.8:
            biological_state = (
                f"Falsa Estate Autunnale / Indian Summer ({base_water_temp}°C, Δ72h {micro_trend_72h:+.1f}°C: "
                "inversione calda temporanea che riattiva la caccia shallow nelle ore centrali)"
            )
        elif macro_trend_14d >= 0.6 and micro_trend_72h >= 0.4:
            biological_state = (
                f"Warming Trend di Pre-Frega ({base_water_temp}°C: "
                "riscaldamento progressivo ottimale, grandi femmine in risalita aggressiva verso le baie)"
            )
        elif macro_trend_14d <= -0.8 and micro_trend_72h <= -0.5:
            biological_state = (
                f"Crollo Termico Autunnale ({base_water_temp}°C: "
                "raffreddamento rapido, i banchi abbandonano le rive e si compattano sulle strutture verticali)"
            )
        else:
            biological_state = (
                f"Transizione Termica Stabile ({base_water_temp}°C: "
                "pesci attivi lungo i corridoi di migrazione tra fondale e acqua bassa)"
            )

    # Scaglione 3: Regime Metabolico Ottimale / Temperato-Caldo (16.0°C <= T <= 24.5°C)
    elif 16.0 <= base_water_temp <= 24.5:
        if micro_trend_72h <= -1.2:
            biological_state = (
                f"Shock Post-Frontale in Finestra Ottimale ({base_water_temp}°C, Δ72h {micro_trend_72h:+.1f}°C: "
                "calo termico repentino che rende il Bass selettivo e rintanato nel fitto delle cover)"
            )
        elif micro_trend_72h >= 0.8 or macro_trend_14d >= 1.0:
            biological_state = (
                f"Picco Metabolico in Spinta ({base_water_temp}°C: "
                "enzimologia e ossigeno al 100%, massima aggressività territoriale e caccia in acqua bassa)"
            )
        else:
            biological_state = (
                f"Omeostasi nella Finestra d'Oro ({base_water_temp}°C: "
                "equilibrio termico perfetto, attività predatoria governata dai picchi barometrici e solunari)"
            )

    # Scaglione 4: Regime Estivo / Stress Termico e Ipossia (> 24.5°C)
    else:
        if micro_trend_72h <= -0.6:
            biological_state = (
                f"Rinfrescamento Estivo Ossigenante ({base_water_temp}°C, Δ72h {micro_trend_72h:+.1f}°C: "
                "il calo termico spezza l'ipossia estiva e scatena una forte finestra di caccia attiva!)"
            )
        elif micro_trend_72h >= 0.7 or base_water_temp >= 28.0:
            biological_state = (
                f"Allarme Stress Termico & Ipossia ({base_water_temp}°C: "
                "carenza di ossigeno disciolto diurna, attività confinata all'alba/notte, correnti o ombre fitte)"
            )
        else:
            biological_state = (
                f"Pattern Estivo Consolidato ({base_water_temp}°C: "
                "picchi esplosivi ai crepuscoli e stazionamento profondo sul termoclino o sotto i tappeti d'erba di giorno)"
            )

    mean_7d_air = round(sum(daily_air_means[-7:]) / min(7, len(daily_air_means)), 1)

    return {
        "base_water_temp": round(base_water_temp, 1),
        "macro_trend_14d": macro_trend_14d,
        "micro_trend_72h": micro_trend_72h,
        "biological_state": biological_state,
        "hourly": hourly_records,
        # Chiavi alias di retrocompatibilità per il resto dell'app
        "thermal_trend_3d": micro_trend_72h,
        "mean_7d_air": mean_7d_air
    }