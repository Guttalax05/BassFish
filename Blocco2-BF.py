# ==============================================================================
# MODULO 2: MOTORE BIOLOGICO CONTINUO V2 (Bio-Energetica, Trigger & Trophy Model)
# ==============================================================================
class ProTourBiologicalEngine:
    """
    Motore bio-matematico continuo (C^1 differenziabile) per il Micropterus salmoides.
    Unisce:
    - Parte 2A: Cinetica enzimatica aerobica (Two-Piece Gaussian + O2) e matrice vettoriale dT.
    - Parte 2B: Trigger ambientali accoppiati (barometro 3h x 12h, termo-fotonica, fotoperiodo).
    - Parte 2C: Orchestratore orario con curve separate per Azione/Numeri (BAI) e Big Bass (>2kg).
    """

    # --------------------------------------------------------------------------
    # PARTE 2A: BIO-ENERGETICA CONTINUA & CINETICA DI ACCLIMATAZIONE
    # --------------------------------------------------------------------------
    @staticmethod
    def metabolic_potential(temp: float, do_index: float = 0.85) -> float:
        """
        Modella la curva continua di performance aerobica (Aerobic Scope) del Micropterus salmoides.
        Integra una distribuzione Gaussiana Bipartita (Two-Piece Gaussian) centrata su T_opt = 21.2°C
        con un modulatore sigmoideo di saturazione dell'ossigeno disciolto (do_index).
        Zero discontinuità o scalini artificiali: funzione C^1 differenziabile su tutto il dominio.
        """
        t_opt = 21.2
        sigma_cold = 6.7
        sigma_hot = 5.2

        # 1. Curva Termica Primaria (Two-Piece Gaussian continua in T = 21.2°C dove vale 1.00)
        sigma = sigma_cold if temp <= t_opt else sigma_hot
        base_thermal = math.exp(-((temp - t_opt) ** 2) / (2.0 * (sigma ** 2)))

        # 2. Compressione Asintotica Ipometabolica Invernale (< 6.0°C -> asintoto basale 0.045)
        cold_blend = 0.5 * (1.0 - math.tanh((temp - 5.8) / 1.4))
        basal_floor = 0.045
        thermal_curve = (base_thermal * (1.0 - 0.55 * cold_blend)) + (basal_floor * cold_blend)

        # 3. Accoppiamento Ipossico Reale (Modulazione da Ossigeno Disciolto per T > 22.5°C)
        high_temp_gate = 0.5 * (1.0 + math.tanh((temp - 23.5) / 1.6))
        do_deviation = math.tanh((do_index - 0.635) / 0.11)
        
        # Asimmetria fisiologica: l'ipossia severa penalizza il metabolismo (-45%) più di quanto
        # l'iper-ossigenazione meccanica possa salvarlo (+22%) ad alte temperature
        hypoxia_asymmetry = 0.22 if do_deviation >= 0.0 else 0.45
        do_modifier = 1.0 + (high_temp_gate * hypoxia_asymmetry * do_deviation)

        final_potential = thermal_curve * do_modifier
        return round(max(0.04, min(1.00, final_potential)), 4)

    @staticmethod
    def trend_matrix_multiplier(
        macro_14d: float,
        micro_72h: float,
        current_water_temp: float,
        do_index: float = 0.85
    ) -> float:
        """
        Calcola il moltiplicatore dinamico di acclimatazione e shock termico [0.42, 1.35].
        Sostituisce le matrici a soglia fissa con campi vettoriali continui basati su math.tanh,
        catturando l'inversione di polarità estiva, il blocco da Pre-Spawn Cold Front e l'Indian Summer.
        """
        # A) Polarità Termica Continua (da +1.0 sotto i 22°C fino a -0.65 sopra i 24.5°C)
        raw_transition = -math.tanh((current_water_temp - 23.8) / 2.2)
        thermal_polarity = 0.175 + (0.825 * raw_transition)

        # B) Vettore Combinato (Inerzia Stagionale 35% + Impulso Acuto 65%)
        macro_norm = math.tanh(macro_14d / 2.5)
        micro_norm = math.tanh(micro_72h / 1.4)
        combined_vector = (0.35 * macro_norm) + (0.65 * micro_norm)
        directional_effect = 0.26 * thermal_polarity * combined_vector

        # C) Shock da Dissonanza / Pre-Spawn Cold Front (macro > 0 ma micro < 0 sotto i 21°C)
        sub_21_gate = 0.5 * (1.0 - math.tanh((current_water_temp - 21.0) / 1.8))
        macro_pos_strength = math.tanh(max(0.0, macro_14d) / 1.2)
        micro_neg_strength = math.tanh(abs(min(0.0, micro_72h)) / 1.0)
        dissonance_shock_penalty = 0.46 * sub_21_gate * macro_pos_strength * micro_neg_strength

        # D) Finestra Opportunistica (Indian Summer / Riscaldamento Invernale Repentino)
        cold_water_gate = 0.5 * (1.0 - math.tanh((current_water_temp - 13.5) / 2.0))
        cooling_season_gate = math.tanh(abs(min(0.0, macro_14d)) / 1.3)
        opportunistic_context = cold_water_gate + cooling_season_gate - (cold_water_gate * cooling_season_gate)
        
        micro_pos_strength = math.tanh(max(0.0, micro_72h) / 1.1)
        opportunistic_boost = 0.24 * opportunistic_context * micro_pos_strength

        # E) Sinergia Ossigeno durante i Rinfrescamenti Estivi
        summer_gate = 0.5 * (1.0 + math.tanh((current_water_temp - 24.5) / 1.5))
        do_synergy = 0.08 * summer_gate * math.tanh((do_index - 0.65) / 0.15) * micro_neg_strength

        raw_multiplier = (
            1.00
            + directional_effect
            - dissonance_shock_penalty
            + opportunistic_boost
            + do_synergy
        )

        return round(max(0.42, min(1.35, raw_multiplier)), 4)

    # --------------------------------------------------------------------------
    # PARTE 2B: TRIGGER AMBIENTALI ACCOPPIATI & BATIMETRIA DINAMICA
    # --------------------------------------------------------------------------
    @staticmethod
    def score_barometric_and_sky(
        press: float,
        delta_3h: float,
        clouds: int,
        radiation: int,
        water_temp: float,
        trend_12h: float = 0.0
    ) -> float:
        """
        1. TRIGGER BAROMETRICO MULTI-SCALA (3h x 12h) & ACCOPPIAMENTO TERMO-FOTONICO
        Modella la distensione/compressione della vescica natatoria incrociando l'impulso
        barometrico acuto (3h) con il fronte sinottico strutturato (12h) tramite funzioni
        continue (tanh), ed esegue il blending termo-fotonico continuo centrato a 15.0°C.
        """
        # --- A) Dinamica della Vescica Natatoria (Multi-Scala 3h x 12h) ---
        acute_3h_signal = -math.tanh((delta_3h + 0.15) / 1.1)
        synoptic_12h_signal = -math.tanh((trend_12h + 0.40) / 2.2)
        baro_combined = (0.60 * acute_3h_signal) + (0.40 * synoptic_12h_signal)

        # Sinergia Pre-Frontale Ciclonica (calo sincronizzato a 3h e 12h)
        falling_3h_gate = 0.5 * (1.0 - math.tanh((delta_3h + 0.5) / 0.5))
        falling_12h_gate = 0.5 * (1.0 - math.tanh((trend_12h + 1.2) / 0.9))
        pre_frontal_synergy = 0.10 * falling_3h_gate * falling_12h_gate

        # Blocco Post-Frontale Anticiclonico (Rimbalzo Barometrico + Cielo Sereno + Alta Pressione)
        rising_bounce_gate = max(
            0.5 * (1.0 + math.tanh((delta_3h - 0.75) / 0.45)),
            0.5 * (1.0 + math.tanh((trend_12h - 2.4) / 1.0))
        )
        clear_sky_gate = 0.5 * (1.0 - math.tanh((clouds - 25.0) / 12.0))
        high_abs_press_gate = 0.5 * (1.0 + math.tanh((press - 1021.0) / 3.5))
        post_frontal_lock = 0.18 * rising_bounce_gate * clear_sky_gate * (0.5 + 0.5 * high_abs_press_gate)

        abs_press_mod = -0.05 * math.tanh((press - 1014.5) / 6.0)
        base_baro_score = 0.70 + (0.24 * baro_combined) + pre_frontal_synergy - post_frontal_lock + abs_press_mod

        # --- B) Accoppiamento Termo-Fotonico Continuo (Blending tra 14.0°C e 16.0°C) ---
        warm_photon_weight = 0.5 * (1.0 + math.tanh((water_temp - 15.0) / 0.95))
        cold_photon_weight = 1.0 - warm_photon_weight

        # 1) Effetto Fotonico in Acqua Fredda (< 14°C): il sole scalda le cover (+0.16)
        solar_warming_gain = 0.16 * (0.5 * (1.0 + math.tanh((radiation - 220.0) / 110.0)))
        cold_overcast_drag = 0.07 * (0.5 * (1.0 + math.tanh((clouds - 80.0) / 10.0))) * (1.0 - falling_3h_gate)
        cold_light_effect = solar_warming_gain - cold_overcast_drag

        # 2) Effetto Fotonico in Acqua Calda (> 16°C): fotofobia da sole diretto (-0.18), bonus nuvole (+0.15)
        intense_glare_gate = (
            0.5 * (1.0 + math.tanh((radiation - 520.0) / 130.0))
            * 0.5 * (1.0 - math.tanh((clouds - 32.0) / 14.0))
        )
        overcast_roaming_gate = 0.5 * (1.0 + math.tanh((clouds - 62.0) / 16.0))
        warm_light_effect = (0.15 * overcast_roaming_gate) - (0.18 * intense_glare_gate)

        thermo_photonic_mod = (cold_photon_weight * cold_light_effect) + (warm_photon_weight * warm_light_effect)
        final_score = base_baro_score + thermo_photonic_mod

        return round(max(0.20, min(1.00, final_score)), 4)

    @staticmethod
    def score_photoperiod_dynamic(
        hour: int,
        alba_dec: float,
        tramonto_dec: float,
        moon_illum: float,
        water_temp: float
    ) -> float:
        """
        2. FOTOPERIODO DINAMICO CON BLENDING CONTINUO (Soglia di Transizione 13.8°C)
        Unisce senza discontinuità la campana termica monomodale invernale (picco ore 14:30)
        con la distribuzione bimodale crepuscolare dei bastoncelli retinici (Alba+0.4h / Tramonto-0.3h)
        e il boost gravitazionale continuo dei sizigi lunari.
        """
        h_float = float(hour)
        w_warm = 0.5 * (1.0 + math.tanh((water_temp - 13.8) / 1.15))
        w_cold = 1.0 - w_warm

        # --- A) Regime Freddo / Invernale (< 13.8°C): Campana Monomodale Pomeridiana (14:30) ---
        dist_afternoon_peak = h_float - 14.5
        cold_afternoon_bell = math.exp(-((dist_afternoon_peak ** 2) / (2.0 * (2.35 ** 2))))
        dawn_chill_dip = 0.08 * math.exp(-(((h_float - alba_dec) ** 2) / 2.0))
        score_cold_regime = 0.24 + (0.72 * cold_afternoon_bell) - dawn_chill_dip

        # --- B) Regime Temperato / Caldo (>= 13.8°C): Curva Bimodale Crepuscolare ---
        dawn_peak_center = alba_dec + 0.4
        dusk_peak_center = tramonto_dec - 0.3

        dawn_bell = math.exp(-(((h_float - dawn_peak_center) ** 2) / (2.0 * (1.35 ** 2))))
        dusk_bell = math.exp(-(((h_float - dusk_peak_center) ** 2) / (2.0 * (1.45 ** 2))))
        crepuscular_peaks = max(dawn_bell, dusk_bell)

        is_daytime_smooth = (
            0.5 * (1.0 + math.tanh((h_float - alba_dec) / 0.6))
            * 0.5 * (1.0 - math.tanh((h_float - tramonto_dec) / 0.6))
        )
        summer_night_gate = 0.5 * (1.0 + math.tanh((water_temp - 23.0) / 1.6))
        night_baseline = 0.46 + (0.16 * summer_night_gate)
        day_baseline = 0.38 - (0.05 * summer_night_gate)

        ambient_baseline = (is_daytime_smooth * day_baseline) + ((1.0 - is_daytime_smooth) * night_baseline)
        score_warm_regime = ambient_baseline + ((0.96 - ambient_baseline) * crepuscular_peaks)

        blended_photoperiod = (w_cold * score_cold_regime) + (w_warm * score_warm_regime)

        # --- C) Boost Gravitazionale Solunare Continuo (Sizigi: Luna Piena >= 82% o Nuova <= 18%) ---
        dist_to_syzygy = min(moon_illum, 100.0 - moon_illum)
        syzygy_boost = 0.08 * math.exp(-((dist_to_syzygy ** 2) / (2.0 * (11.5 ** 2))))

        final_solunar = blended_photoperiod + syzygy_boost
        return round(max(0.18, min(1.00, final_solunar)), 4)

    @staticmethod
    def score_vento(vento_kmh: float, water_temp: float, do_index: float = 0.85) -> float:
        """
        3. IDRODINAMICA DI SUPERFICIE, ROTTURA CONO DI SNELL & RI-OSSIGENAZIONE EOLICA
        Valuta l'azione meccanica del vento in funzione del regime termico e del deficit di O2.
        """
        warm_wind_gate = 0.5 * (1.0 + math.tanh((water_temp - 12.75) / 1.1))
        cold_wind_gate = 1.0 - warm_wind_gate

        # --- A) Regime Freddo (< 11.5°C): Conservazione della Micro-Stratificazione ---
        cold_breeze_optimum = 0.62 + 0.18 * math.exp(-(((vento_kmh - 5.5) ** 2) / (2.0 * (3.8 ** 2))))
        cold_mixing_penalty = 0.52 * (0.5 * (1.0 + math.tanh((vento_kmh - 14.5) / 4.5)))
        score_wind_cold = max(0.22, cold_breeze_optimum - cold_mixing_penalty)

        # --- B) Regime Temperato/Caldo (> 14.0°C): Attivazione Linea Laterale & Rottura Luce ---
        mirror_calm_climb = 0.50 + 0.48 * (0.5 * (1.0 + math.tanh((vento_kmh - 5.2) / 2.2)))
        gale_force_drop = 0.73 * (0.5 * (1.0 + math.tanh((vento_kmh - 26.5) / 3.8)))
        score_wind_warm = mirror_calm_climb - gale_force_drop

        # Premio di Ri-Ossigenazione Meccanica Estiva (T > 24.0°C)
        summer_reaeration_gate = 0.5 * (1.0 + math.tanh((water_temp - 24.0) / 1.4))
        active_wave_window = (
            0.5 * (1.0 + math.tanh((vento_kmh - 7.5) / 2.5))
            * 0.5 * (1.0 - math.tanh((vento_kmh - 25.0) / 3.5))
        )
        reaeration_bonus = 0.12 * summer_reaeration_gate * active_wave_window * (1.1 - 0.3 * do_index)

        combined_wind = (cold_wind_gate * score_wind_cold) + (warm_wind_gate * (score_wind_warm + reaeration_bonus))
        return round(max(0.22, min(1.00, combined_wind)), 4)

    @staticmethod
    def score_torbidita(torbidita_input: str) -> float:
        """
        4. COEFFICIENTE OTTICO E SICUREZZA PREDATORIA
        Restituisce i pesi ottici di penetrazione luminosa e confidenza in acqua bassa.
        """
        mappa_ottica = {
            "Velata": 1.00,
            "Non specificato": 0.85,
            "Limpida": 0.80,
            "Torbida": 0.65,
            "Fangosa": 0.40
        }
        return mappa_ottica.get(torbidita_input, 0.85)

    @staticmethod
    def estimate_strike_zone_depth(
        water_temp: float,
        radiation: int,
        wind: float,
        hour: int,
        alba: float,
        tramonto: float,
        micro_72h: float,
        do_index: float = 0.85
    ) -> str:
        """
        5. STIMATORE BATIMETRICO E STRUTTURALE DELLA STRIKE ZONE
        Incrocia temperatura, shock termico a 72h (Cold Front), saturazione di ossigeno (ipossia),
        radiazione solare e moto ondoso per localizzare il posizionamento tridimensionale del Bass.
        """
        h_float = float(hour)
        is_crepuscular = (abs(h_float - alba) <= 1.8) or (abs(h_float - tramonto) <= 1.8)
        is_night = (h_float < alba - 0.5) or (h_float > tramonto + 0.8)

        if water_temp < 9.0:
            if 12 <= hour <= 16 and radiation >= 220 and wind < 10.0 and micro_72h >= -0.3:
                return "Sassaie & Pareti Nord Insolate (2.0m - 4.0m)"
            return "Buche Invernali & Fondale Primario (4.5m - 8.5m+)"

        if micro_72h <= -0.9 and water_temp < 22.0:
            if radiation > 450 and wind < 7.0:
                return "Incollati nel Cuore delle Cover / Legnaie (1.5m - 3.5m)"
            return "Sospesi sui Drop-off / Primo Scalino (2.5m - 5.0m)"

        if 9.0 <= water_temp < 14.5:
            if 11 <= hour <= 16 and (radiation >= 200 or micro_72h >= 0.5):
                return "Risalita su Flat Bassi, Sassaie & Legni (1.0m - 2.2m)"
            elif wind >= 12.0:
                return "Punte Secondarie & Scalini Battuti dall'Onda (1.8m - 3.5m)"
            return "Staging sui Drop-off & Margini Erbai (2.5m - 4.5m)"

        if 14.5 <= water_temp <= 23.5:
            if is_crepuscular or (wind >= 9.0 and radiation < 450):
                return "Shallow Attivo, Sponde Ventose & Superficie (0.2m - 1.5m)"
            elif radiation >= 600 and wind < 6.0:
                return "Ombra Fitta: Pontili, Canneti & Alberi Sommersi (0.8m - 2.5m)"
            return "Sub-Superficie, Punte & Bordi Cover (1.0m - 2.5m)"

        if do_index < 0.55:
            if is_night or is_crepuscular:
                return "Micro-Strato Superficiale & Immissari (0.1m - 1.0m)"
            return "Sotto Tappeti d'Erba Ossigenati (Punching) o Termoclino (3.5m+)"
        else:
            if is_crepuscular or is_night:
                return "Topwater & Basso Fondale Litorale (0.1m - 1.2m)"
            elif wind >= 11.0:
                return "Punte Esterne & Sponde Ossigenate dall'Onda (1.2m - 3.0m)"
            elif radiation >= 550:
                return "Ombre Profonde, Erbai Fitti & Salti Batimetrici (2.0m - 4.5m)"
            return "Bordi Vegetazione & Strutture di Media Acqua (1.5m - 3.2m)"

    # --------------------------------------------------------------------------
    # PARTE 2C: ORCHESTRATORE ORARIO E MODELLO DIFFERENZIATO (BAI vs TROPHY >2KG)
    # --------------------------------------------------------------------------
    @classmethod
    def run_pro_simulation(
        cls,
        series_data: dict,
        astro: dict,
        torbidita: str,
        manual_water_temp: float = None
    ) -> dict:
        """
        Esegue la simulazione bio-energetica sulle 24 ore integrando i vettori termodinamici
        del Blocco 1 e separando matematicamente il Catch Rate generale (BAI - Azione/Numeri)
        dal modello etologico per il Trophy Rate (Big Bass > 2.0 kg).
        """
        hourly_meteo = series_data["hourly"]
        base_model_temp = float(series_data.get("base_water_temp", 15.0))
        macro_14d = float(series_data.get("macro_trend_14d", 0.0))
        micro_72h = float(series_data.get("micro_trend_72h", series_data.get("thermal_trend_3d", 0.0)))
        bio_state = series_data.get("biological_state", "Omeostasi Termica")
        mean_7d_air = float(series_data.get("mean_7d_air", 15.0))

        s_torb = cls.score_torbidita(torbidita)
        torb_label = "Velata (Stima)" if torbidita == "Non specificato" else torbidita

        timeline = []
        for row in hourly_meteo:
            # 1. Estrazione sicura con fallback dei parametri fisici avanzati del Blocco 1
            trend_12h = float(row.get("pressure_trend_12h", 0.0))
            do_idx = float(row.get("do_saturation_index", 0.85))
            rad_wm2 = int(row.get("radiation", 0))
            wind_kmh = float(row.get("wind", 0.0))
            clouds_pct = int(row.get("clouds", 50))

            # 2. Conservazione della Curva Termodinamica Oraria anche con Sonda Manuale:
            # Applichiamo l'anomalia oraria fisica calcolata dall'integratore del Blocco 1
            # (row["water_temp"] - base_model_temp) direttamente sopra la lettura della sonda!
            if manual_water_temp is not None:
                physical_hourly_delta = float(row["water_temp"]) - base_model_temp
                w_temp = round(max(3.8, float(manual_water_temp) + physical_hourly_delta), 1)
            else:
                w_temp = float(row["water_temp"])

            # 3. Sub-Scores Bio-Energetici e Trigger Ambientali
            m_temp = cls.metabolic_potential(w_temp, do_idx)
            c_trend = cls.trend_matrix_multiplier(macro_14d, micro_72h, w_temp, do_idx)
            effective_metabolism = max(0.05, min(1.18, m_temp * c_trend))

            s_press = cls.score_barometric_and_sky(
                row["pressure"], row["pressure_delta"], clouds_pct, rad_wm2, w_temp, trend_12h
            )
            s_sol = cls.score_photoperiod_dynamic(
                row["hour"], astro["sunrise_dec"], astro["sunset_dec"], astro["moon_illum"], w_temp
            )
            s_vento = cls.score_vento(wind_kmh, w_temp, do_idx)

            # Trigger ambientale ponderato (Barometro/Cielo 38%, Fotoperiodo 32%, Vento 20%, Torbidità 10%)
            env_trigger = (s_press * 0.38) + (s_sol * 0.32) + (s_vento * 0.20) + (s_torb * 0.10)

            # ==================================================================
            # 4. CALCOLO "CATCH RATE" GENERALE (BAI - Azione e Numero di Catture)
            # Accoppiamento non-lineare: quando effective_metabolism è alto, un ottimo
            # env_trigger esplode verso il 100%; in caso di shock termico/letargo,
            # il tetto biologico impedisce falsi positivi anche col meteo migliore.
            # ==================================================================
            non_linear_synergy = 0.14 * (effective_metabolism ** 1.25) * (env_trigger ** 1.40)
            bai_raw = (effective_metabolism * (0.28 + 0.64 * env_trigger) + non_linear_synergy) * 100.0
            bai_pct = round(max(4.0, min(100.0, bai_raw)), 1)

            # ==================================================================
            # 5. MODELLO BIO-ENERGETICO INDIPENDENTE PER IL "TROPHY RATE" (Big Bass > 2.0 kg)
            # ==================================================================
            # A) Curva Termica delle Grandi Femmine (T_opt_big = 16.2°C):
            # Grazie alla massa corporea superiore sono già in piena spinta tra 10.0°C e 14.5°C,
            # ma sopra i 24.5°C soffrono drasticamente il fabbisogno di ossigeno (sigma_hot = 4.1).
            t_opt_big = 16.2
            sigma_big = 5.4 if w_temp <= t_opt_big else 4.1
            big_thermal_base = math.exp(-((w_temp - t_opt_big) ** 2) / (2.0 * (sigma_big ** 2)))

            # Bonus Pre-Frega / Risalita Stagionale per le Big Mama tra 9.5°C e 15.5°C se macro_14d >= 0
            prespawn_window = math.exp(-(((w_temp - 12.5) ** 2) / (2.0 * (2.2 ** 2))))
            prespawn_trend_gate = 0.5 * (1.0 + math.tanh((macro_14d + 0.2) / 0.8))
            big_thermal_curve = min(1.00, big_thermal_base + (0.20 * prespawn_window * prespawn_trend_gate))

            # B) Vulnerabilità Critica all'Ipossia Estiva (> 25.0°C):
            # Un pesce di 2.5 - 3.5 kg richiede molto più O2 disciolto; se do_idx cala, si blocca di giorno.
            big_heat_gate = 0.5 * (1.0 + math.tanh((w_temp - 24.8) / 1.3))
            big_do_factor = 1.0 + big_heat_gate * (0.48 * math.tanh((do_idx - 0.68) / 0.10))
            big_do_factor = max(0.32, min(1.12, big_do_factor))

            # C) Selettività Sensoriale e Cautela dei Pesci Anziani (Anti-Spook Filter):
            # Con sole alto (> 500 W/m²), acqua piatta (< 4 km/h) e visibilità alta, una Big non esce in scoperto.
            high_sun_exposure = 0.5 * (1.0 + math.tanh((rad_wm2 - 460.0) / 110.0))
            flat_calm_exposure = 0.5 * (1.0 - math.tanh((wind_kmh - 4.2) / 1.6))
            clear_water_exposure = 1.0 if torbidita == "Limpida" else (0.65 if torbidita == "Non specificato" else 0.20)
            caution_penalty = 0.48 * high_sun_exposure * flat_calm_exposure * clear_water_exposure

            # D) Finestra del Predatore Apicale (Fronte in Calo + Vento 8-22 km/h + Crepuscolo/Notte + Sizigi):
            baro_drop_boost = 0.5 * (1.0 + math.tanh((s_press - 0.76) / 0.08))
            crepuscular_boost = 0.5 * (1.0 + math.tanh((s_sol - 0.76) / 0.10))
            wave_cover_boost = (
                0.5 * (1.0 + math.tanh((wind_kmh - 7.5) / 2.2))
                * 0.5 * (1.0 - math.tanh((wind_kmh - 23.0) / 3.5))
            )
            apex_feeding_burst = 0.24 * (
                (0.40 * baro_drop_boost) + (0.35 * crepuscular_boost) + (0.25 * wave_cover_boost)
            )

            # Moltiplicatore Lunare Gravitazionale (le grandi femmine sono fortemente legate ai sizigi)
            moon_dist = min(astro["moon_illum"], 100.0 - astro["moon_illum"])
            big_moon_mult = 1.0 + (0.14 * math.exp(-((moon_dist ** 2) / (2.0 * (12.0 ** 2)))))

            # Smorzamento per shock post-frontale acuto (c_trend vale < 1.0 nei cold front severi)
            big_shock_damping = max(0.50, min(1.15, 0.25 + 0.75 * c_trend))

            trophy_core_potential = big_thermal_curve * big_do_factor * big_shock_damping
            trophy_env_drive = (0.30 + (0.70 * env_trigger) + apex_feeding_burst - caution_penalty)
            trophy_raw = trophy_core_potential * trophy_env_drive * big_moon_mult * 100.0
            trophy_pct = round(max(3.0, min(98.0, trophy_raw)), 1)

            # 6. Stima Fascia Batimetrica e Strutturale (Strike Zone)
            depth_zone = cls.estimate_strike_zone_depth(
                w_temp, rad_wm2, wind_kmh, row["hour"],
                astro["sunrise_dec"], astro["sunset_dec"],
                micro_72h, do_idx
            )

            timeline.append({
                **row,
                "water_temp_used": w_temp,
                "torbidita_label": torb_label,
                "s_temp": round(effective_metabolism, 3),
                "s_press": s_press,
                "s_sol": s_sol,
                "s_vento": s_vento,
                "s_torb": s_torb,
                "env_trigger": round(env_trigger * 100.0, 1),
                "catch_rate": bai_pct,
                "trophy_rate": trophy_pct,
                "depth_zone": depth_zone
            })

        best_hour = max(timeline, key=lambda x: x["catch_rate"])
        best_trophy_hour = max(timeline, key=lambda x: x["trophy_rate"])
        avg_bai = round(sum(x["catch_rate"] for x in timeline) / 24.0, 1)
        top_3_hours = sorted(timeline, key=lambda x: x["catch_rate"], reverse=True)[:3]

        return {
            "timeline": timeline,
            "best_hour": best_hour,
            "best_trophy_hour": best_trophy_hour,
            "top_3": top_3_hours,
            "avg_rate": avg_bai,
            "macro_trend_14d": macro_14d,
            "micro_trend_72h": micro_72h,
            "biological_state": bio_state,
            "thermal_trend_3d": micro_72h,
            "mean_7d_air": mean_7d_air
        }