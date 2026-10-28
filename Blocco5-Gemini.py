# ==============================================================================
# MACRO-BLOCCO 5: STREAMLIT iOS MOBILE-FIRST UI & ORCHESTRAZIONE PIPELINE V2
# ==============================================================================
def inject_ios_oled_css() -> None:
    """
    Inietta il foglio di stile iOS 17 Dark OLED calibrato per schermi iPhone 15
    e coerente con le superfici (#000000 / #14181c) del Motore Grafico Blocco 4 v2.
    """
    st.markdown("""
    <style>
        /* Rimozione cromature e menu di default di Streamlit */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid="stHeader"] {display: none;}
        [data-testid="collapsedControl"] {display: none;}
        section[data-testid="stSidebar"] {display: none;}

        /* Tema base OLED Nero Puro & Tipografia Apple SF Pro */
        .stApp {
            background-color: #000000;
            color: #F2F2F7;
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Segoe UI", Roboto, sans-serif;
        }

        /* Contenitore mobile-first centrato (ottimale per 393px su iPhone 15 e pulito su Desktop) */
        .block-container {
            padding-top: 0.9rem !important;
            padding-bottom: 3.2rem !important;
            padding-left: 0.85rem !important;
            padding-right: 0.85rem !important;
            max-width: 540px !important;
        }

        /* Leggibilità outdoor ad alto contrasto */
        p, li {
            font-size: 0.98rem !important;
            line-height: 1.52 !important;
            color: #E5E5EA;
        }

        /* Top Navigation Bar nativa iOS */
        .ios-navbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 4px 2px 10px 2px;
            border-bottom: 1px solid #1F242A;
            margin-bottom: 12px;
        }
        .ios-brand {
            font-size: 1.38rem;
            font-weight: 900;
            letter-spacing: -0.6px;
            background: linear-gradient(90deg, #10b981 0%, #38bdf8 55%, #a855f7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
        }
        .ios-version-pill {
            background-color: #14181c;
            border: 1px solid #262C34;
            color: #10b981;
            font-size: 0.72rem !important;
            font-weight: 800;
            padding: 4px 10px;
            border-radius: 999px;
            letter-spacing: 0.6px;
            text-transform: uppercase;
        }

        /* Stile Segmented Radio per il Selettore Focus (Entrambi / Numeri / Trophy) */
        div[role="radiogroup"] {
            background-color: #14181c;
            border: 1px solid #262C34;
            border-radius: 14px;
            padding: 4px;
            display: flex;
            justify-content: space-between;
            gap: 4px;
        }
        div[role="radiogroup"] > label {
            flex: 1;
            justify-content: center;
            background-color: transparent;
            border-radius: 10px;
            padding: 7px 6px !important;
            margin: 0 !important;
            transition: all 0.18s ease;
        }
        div[role="radiogroup"] > label[data-checked="true"] {
            background-color: #232A31 !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
        }

        /* HERO SUMMARY CARD ADATTIVA */
        .hero-card {
            background: linear-gradient(160deg, #14181c 0%, #0d1114 100%);
            border-radius: 18px;
            padding: 18px 16px;
            margin: 10px 0 14px 0;
            box-shadow: 0 10px 28px rgba(0, 0, 0, 0.65);
        }
        .hero-border-dual { border: 1.5px solid #10b981; }
        .hero-border-numeri { border: 1.5px solid #10b981; }
        .hero-border-trophy { border: 1.5px solid #a855f7; }

        .hero-header-line {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.78rem !important;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: #94A3B8;
            margin-bottom: 10px;
        }
        .hero-kpi-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 12px;
        }
        .hero-kpi-single {
            display: block;
            margin-bottom: 12px;
        }
        .kpi-box-green {
            background: rgba(16, 185, 129, 0.10);
            border: 1px solid rgba(16, 185, 129, 0.35);
            border-radius: 14px;
            padding: 12px 14px;
        }
        .kpi-box-purple {
            background: rgba(168, 85, 247, 0.11);
            border: 1px solid rgba(168, 85, 247, 0.38);
            border-radius: 14px;
            padding: 12px 14px;
        }
        .kpi-big-num {
            font-size: 2.35rem !important;
            font-weight: 900;
            line-height: 1.05 !important;
            letter-spacing: -1px;
            color: #FFFFFF;
        }
        .kpi-sub-label {
            font-size: 0.76rem !important;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 4px;
            display: block;
        }
        .bio-state-banner {
            background-color: rgba(56, 189, 248, 0.09);
            border-left: 3.5px solid #38bdf8;
            border-radius: 8px;
            padding: 8px 11px;
            font-size: 0.85rem !important;
            color: #E2E8F0;
            margin-bottom: 12px;
        }
        .telemetry-pills {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 6px;
            padding-top: 10px;
            border-top: 1px solid #222830;
        }
        .t-pill {
            background-color: #1B2026;
            border: 1px solid #283038;
            border-radius: 10px;
            padding: 6px 4px;
            text-align: center;
            font-size: 0.78rem !important;
            color: #CBD5E1;
        }
        .t-pill b {
            display: block;
            font-size: 0.90rem !important;
            color: #FFFFFF;
            margin-top: 1px;
        }

        /* TACTICAL CARDS (#14181c coerente col Blocco 4) */
        .tactical-box {
            background-color: #14181c;
            border: 1px solid #242B33;
            border-radius: 15px;
            padding: 15px 16px;
            margin-bottom: 13px;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.45);
        }
        .tactical-box-header {
            font-size: 0.96rem !important;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding-bottom: 8px;
            margin-bottom: 10px;
            border-bottom: 1px solid #242B33;
        }
        .b-emerald { border-left: 4.5px solid #10b981; }
        .b-cyan    { border-left: 4.5px solid #38bdf8; }
        .b-purple  { border-left: 4.5px solid #a855f7; }
        .b-amber   { border-left: 4.5px solid #f59e0b; }
        .b-rose    { border-left: 4.5px solid #f472b6; }

        /* Stile Tabs Principali (Segmented Control iOS) */
        .stTabs [data-baseweb="tab-list"] {
            gap: 5px;
            background-color: #14181c;
            padding: 5px;
            border-radius: 14px;
            border: 1px solid #242B33;
        }
        .stTabs [data-baseweb="tab"] {
            flex: 1;
            justify-content: center;
            height: 42px;
            border-radius: 10px;
            font-weight: 700;
            font-size: 0.86rem !important;
            color: #94A3B8;
            padding: 0 4px !important;
            border: none !important;
        }
        .stTabs [aria-selected="true"] {
            background-color: #242B33 !important;
            color: #10b981 !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.45);
        }

        /* Expander Configurazione Spot */
        div[data-testid="stExpander"] {
            background-color: #14181c !important;
            border: 1px solid #242B33 !important;
            border-radius: 14px !important;
            margin-bottom: 10px;
        }
        div[data-testid="stExpander"] summary p {
            font-size: 0.96rem !important;
            font-weight: 700 !important;
            color: #38bdf8 !important;
        }
    </style>
    """, unsafe_allow_html=True)


def render_tactical_card(title: str, body_md: str, accent_class: str, title_color: str) -> None:
    """Renderizza una card tattica iOS incapsulando il contenuto Markdown in una superficie #14181c."""
    st.markdown(
        f'<div class="tactical-box {accent_class}">'
        f'<div class="tactical-box-header" style="color:{title_color};">{title}</div>',
        unsafe_allow_html=True
    )
    st.markdown(body_md)
    st.markdown("</div>", unsafe_allow_html=True)


def render_adaptive_hero_card(
    geo: dict,
    target_date: str,
    sim: dict,
    target_mode: str,
    day_offset: int
) -> None:
    """
    Costruisce la Hero Summary Card sopra le Tab, adattando il layout visivo
    in base al target_mode selezionato ('Entrambi', 'Numeri', 'Trophy').
    """
    best_bai = sim["best_hour"]
    best_trophy = sim.get("best_trophy_hour", best_bai)
    base_tw = sim.get("base_water_temp", best_bai["water_temp_used"])
    macro_14d = sim.get("macro_trend_14d", 0.0)
    micro_72h = sim.get("micro_trend_72h", 0.0)
    bio_state = sim.get("biological_state", "Omeostasi Termica")

    now_h = datetime.datetime.now().hour
    now_slot = sim["timeline"][now_h] if (day_offset == 0 and len(sim["timeline"]) == 24) else best_bai
    do_pct_now = round(float(now_slot.get("do_saturation_index", 0.85)) * 100)

    if target_mode == "Numeri":
        border_cls = "hero-border-numeri"
        mode_badge = "🔥 FOCUS AZIONE & NUMERI"
        kpi_html = f"""
        <div class="hero-kpi-single kpi-box-green">
            <div style="display:flex; justify-content:space-between; align-items:baseline;">
                <div class="kpi-big-num" style="color:#10b981;">{best_bai['catch_rate']:.1f}%</div>
                <div style="font-size:1.15rem; font-weight:800; color:#facc15;">★ Picco Ore {best_bai['time_label']}</div>
            </div>
            <span class="kpi-sub-label" style="color:#A7F3D0;">
                Massima Frenesia Alimentare (BAI) • Strike Zone: {best_bai['depth_zone']}
            </span>
        </div>
        """
    elif target_mode == "Trophy":
        border_cls = "hero-border-trophy"
        mode_badge = "👑 CACCIA ESCLUSIVA BIG BASS (>2KG)"
        kpi_html = f"""
        <div class="hero-kpi-single kpi-box-purple">
            <div style="display:flex; justify-content:space-between; align-items:baseline;">
                <div class="kpi-big-num" style="color:#c084fc;">{best_trophy['trophy_rate']:.1f}%</div>
                <div style="font-size:1.15rem; font-weight:800; color:#f472b6;">👑 Finestra Ore {best_trophy['time_label']}</div>
            </div>
            <span class="kpi-sub-label" style="color:#E9D5FF;">
                Finestra Predatore Apicale • Target: {best_trophy['depth_zone']}
            </span>
        </div>
        """
    else:  # "Entrambi"
        border_cls = "hero-border-dual"
        mode_badge = "⚖️ TELEMETRIA COMPLETA (BAI + TROPHY)"
        kpi_html = f"""
        <div class="hero-kpi-grid">
            <div class="kpi-box-green">
                <div class="kpi-big-num" style="color:#10b981;">{best_bai['catch_rate']:.1f}%</div>
                <span class="kpi-sub-label" style="color:#A7F3D0;">★ Picco BAI ({best_bai['time_label']})</span>
            </div>
            <div class="kpi-box-purple">
                <div class="kpi-big-num" style="color:#c084fc;">{best_trophy['trophy_rate']:.1f}%</div>
                <span class="kpi-sub-label" style="color:#E9D5FF;">👑 Picco Big ({best_trophy['time_label']})</span>
            </div>
        </div>
        """

    st.markdown(f"""
    <div class="hero-card {border_cls}">
        <div class="hero-header-line">
            <span>📍 {geo['name']} ({geo['admin1']}) • {target_date}</span>
            <span style="color:#38bdf8;">{mode_badge}</span>
        </div>
        {kpi_html}
        <div class="bio-state-banner">
            🧬 <b>Stato Biologico:</b> {bio_state}
        </div>
        <div class="telemetry-pills">
            <div class="t-pill">💧 T.Acqua Base<b>{base_tw:.1f}°C</b></div>
            <div class="t-pill">📈 Δ14gg Macro<b>{macro_14d:+.1f}°C</b></div>
            <div class="t-pill">⚡ Δ72h Micro<b>{micro_72h:+.1f}°C</b></div>
            <div class="t-pill">🫧 Ossigeno O₂<b>{do_pct_now}%</b></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def main():
    # Configurazione pagina (Eseguita in modo sicuro se non già invocata a inizio script)
    try:
        st.set_page_config(
            page_title="Bass Pro V2 - LiveScope Telemetry",
            page_icon="🎣",
            layout="centered",
            initial_sidebar_state="collapsed"
        )
    except Exception:
        pass

    inject_ios_oled_css()

    # --- 0. TOP BAR NATIVA iOS ---
    st.markdown("""
    <div class="ios-navbar">
        <div class="ios-brand">🎣 BASS PRO TOUR V2</div>
        <div class="ios-version-pill">Bio-Engine v2.4</div>
    </div>
    """, unsafe_allow_html=True)

    # --- 1. SELETTORE RAPIDO IN PRIMO PIANO (TARGET MODE) ---
    mode_labels = {
        "Entrambi": "⚖️ Vista Completa",
        "Numeri": "🔥 Azione & Numeri",
        "Trophy": "👑 Caccia al Big Bass"
    }
    target_mode = st.radio(
        "Seleziona Obiettivo Tattico",
        options=["Entrambi", "Numeri", "Trophy"],
        format_func=lambda x: mode_labels[x],
        horizontal=True,
        label_visibility="collapsed"
    )

    # --- 2. PANNELLO CONFIGURAZIONE SPOT & CONDIZIONI SUL CAMPO (EXPANDER MOBILE) ---
    with st.expander("⚙️ Configura Spot, Idrometria & Condizioni sul Campo", expanded=False):
        c_loc, c_day = st.columns([6, 4])
        with c_loc:
            spot_query = st.text_input(
                "📍 Località / Lago / Spot",
                value="Mantova",
                placeholder="Es. Mantova, Bolsena, Sarzana..."
            )
        with c_day:
            day_map = {"Oggi": 0, "Domani": 1, "Dopodomani": 2}
            day_label = st.selectbox("📅 Giorno", options=list(day_map.keys()), index=0)
            day_offset = day_map[day_label]

        spot_morphology = st.selectbox(
            "🏞️ Morfologia & Inerzia Termica Spot",
            options=list(SPOT_TYPES.keys()),
            index=1
        )
        st.caption(f"*{SPOT_TYPES[spot_morphology]['desc']}*")

        col_t1, col_t2 = st.columns(2)
        with col_t1:
            torbidita_input = st.selectbox(
                "🌊 Torbidità Acqua",
                options=["Non specificato", "Limpida", "Velata", "Torbida", "Fangosa"],
                index=0
            )
            water_level = st.selectbox(
                "📏 Livello Idrometrico",
                options=["Stabile", "In Crescita", "In Calo"],
                index=0
            )
        with col_t2:
            forage_base = st.selectbox(
                "🐟 Foraggio Prevalente",
                options=[
                    "Misto",
                    "Pesce Foraggio (Alborella / Shad)",
                    "Gamberi / Crostacei / Gobbio",
                    "Rane / Insetti / Shallow"
                ],
                index=0
            )
            fishing_pressure = st.selectbox(
                "Boats / Pressione di Pesca",
                options=["Media", "Bassa", "Alta"],
                index=0
            )

        st.divider()
        use_manual_temp = st.toggle("🌡️ Attiva Sonda Temperatura Acqua Manuale", value=False)
        manual_water_temp = None
        if use_manual_temp:
            manual_water_temp = st.slider(
                "Temperatura Acqua Rilevata dall'Ecoscandaglio (°C)",
                min_value=4.0,
                max_value=33.0,
                value=16.0,
                step=0.5
            )

    if not spot_query.strip():
        st.warning("Inserisci il nome di una località o di un bacino nell'expander qui sopra.")
        return

    # --- 3. ESECUZIONE PIPELINE (BLOCCO 1 -> BLOCCO 2 -> BLOCCO 3) ---
    try:
        with st.spinner(f"Calcolo modello termodinamico a 30gg (EMA) per '{spot_query}'..."):
            geo = geocode_location(spot_query.strip())
            series = fetch_thermal_and_weather_series(
                geo["lat"], geo["lon"], day_offset, spot_morphology
            )
            target_date = series["hourly"][0]["date_str"]
            astro = compute_astronomy(geo["lat"], geo["lon"], target_date)

            sim = ProTourBiologicalEngine.run_pro_simulation(
                series, astro, torbidita_input, manual_water_temp
            )

            tactics = TacticalAdvisorV2.generate_pro_report(
                best_hour=sim["best_hour"],
                trend_3d=sim["micro_trend_72h"],
                astro=astro,
                sim_results=sim,
                water_level=water_level,
                forage_base=forage_base,
                fishing_pressure=fishing_pressure,
                target_mode=target_mode
            )
    except Exception as ex:
        st.error(f"❌ Errore durante l'elaborazione telemetrica: {ex}")
        return

    # --- 4. HERO SUMMARY CARD ADATTIVA ---
    render_adaptive_hero_card(geo, target_date, sim, target_mode, day_offset)

    # --- 5. NAVIGAZIONE MOBILE A 3 TAB ---
    tab_telemetry, tab_tactics, tab_schedule = st.tabs([
        "📈 Telemetria & Fattori",
        "🎯 Piano Tattico",
        "🕒 Cronologia 24h"
    ])

    # ==========================================================================
    # TAB 1: TELEMETRIA ORARIA & ANALISI DEI 6 FATTORI (BLOCCO 4 V2)
    # ==========================================================================
    with tab_telemetry:
        top_3 = sim["top_3"]
        st.caption(
            f"🥇 **Top 3 Finestre Azione:** `{top_3[0]['time_label']}` ({top_3[0]['catch_rate']}%) • "
            f"`{top_3[1]['time_label']}` ({top_3[1]['catch_rate']}%) • "
            f"`{top_3[2]['time_label']}` ({top_3[2]['catch_rate']}%)  |  "
            f"🌅 Alba `{astro['sunrise_str']}` • 🌇 Tramonto `{astro['sunset_str']}`"
        )

        # Grafico Principale Multi-Traccia (Blocco 4 v2) con theme=None obbligatorio
        fig_main = create_mobile_plotly_chart(
            sim, astro, target_mode=target_mode, focus_hour=None
        )
        st.plotly_chart(
            fig_main,
            use_container_width=True,
            config=MOBILE_PLOTLY_CONFIG,
            theme=None
        )

        st.markdown("##### ⚡ Spinta Bio-Energetica dei 6 Fattori nell'Ora di Picco")
        show_radar_view = st.toggle(
            "Passa a Vista Esagono Polare (Radar 6 Assi)",
            value=False
        )

        if not show_radar_view:
            # Grafico a barre orizzontali ad alta leggibilità su mobile (prioritario)
            fig_factors = create_mobile_factors_chart(sim, target_mode=target_mode)
            st.plotly_chart(
                fig_factors,
                use_container_width=True,
                config=MOBILE_PLOTLY_CONFIG,
                theme=None
            )
        else:
            # Vista alternativa Esagono Polare (accetta direttamente l'intero 'sim')
            fig_radar = create_mobile_radar(sim, target_mode=target_mode)
            st.plotly_chart(
                fig_radar,
                use_container_width=True,
                config=MOBILE_PLOTLY_CONFIG,
                theme=None
            )

    # ==========================================================================
    # TAB 2: PIANO TATTICO & SETUP (BLOCCO 3 V2)
    # ==========================================================================
    with tab_tactics:
        st.info(tactics["bio_alert"])

        # 1. Diagnostica Idro-Biologica & Posizionamento
        render_tactical_card(
            title="🧭 1. Diagnostica Idro-Biologica & Posizionamento",
            body_md=tactics["approccio"],
            accent_class="b-cyan",
            title_color="#38bdf8"
        )

        # 2. Selezione Artificiali Primari & Backup
        lures_combined_md = (
            f"{tactics['esche_primarie']}\n\n"
            f"---\n"
            f"{tactics['esche_secondarie']}"
            if target_mode == "Numeri"
            else f"{tactics['esche_primarie']}\n\n{tactics['esche_secondarie'].split('---')[0].strip()}"
        )
        render_tactical_card(
            title="🪝 2. Artificiali Primari & Piano di Backup",
            body_md=lures_combined_md,
            accent_class="b-emerald",
            title_color="#10b981"
        )

        # 3. Strategia Dedicata Big Bass > 2.0 kg (Visibile in "Entrambi" e "Trophy")
        if target_mode in ["Entrambi", "Trophy"] and tactics.get("strategia_trophy"):
            render_tactical_card(
                title="👑 3. Strategia Dedicata Big Bass (> 2.0 kg)",
                body_md=tactics["strategia_trophy"],
                accent_class="b-purple",
                title_color="#c084fc"
            )

        # 4. Spettro Cromatico Consigliato
        render_tactical_card(
            title="🎨 4. Spettro Cromatico & Ottica Subacquea",
            body_md=tactics["colore"],
            accent_class="b-amber",
            title_color="#f59e0b"
        )

        # 5. Cinetica di Recupero & Ingegneria Setup Canna/Filo
        kinetics_only = tactics["recupero"].split("---")[0].strip()
        render_tactical_card(
            title="⚙️ 5. Cinetica di Recupero & Setup Canna/Filo",
            body_md=f"{kinetics_only}\n\n---\n{tactics['gear_setup']}",
            accent_class="b-rose",
            title_color="#f472b6"
        )

    # ==========================================================================
    # TAB 3: CRONOLOGIA 24H & DIAGNOSTICA CONTRATTO DATI
    # ==========================================================================
    with tab_schedule:
        st.caption(
            f"🌙 **Fase Lunare:** {astro['moon_illum']}% ({astro['phase_desc']}) • "
            f"Tocca l'intestazione di una colonna per ordinare le 24 ore."
        )

        best_h_int = sim["best_hour"]["hour"]
        best_tr_int = sim.get("best_trophy_hour", sim["best_hour"])["hour"]

        schedule_rows = []
        for r in sim["timeline"]:
            h_int = r["hour"]
            tag = ""
            if h_int == best_h_int and h_int == best_tr_int:
                tag = "★👑 "
            elif h_int == best_h_int:
                tag = "★ "
            elif h_int == best_tr_int:
                tag = "👑 "

            schedule_rows.append({
                "Ora": f"{tag}{r['time_label']}",
                "BAI %": r["catch_rate"],
                "Trophy %": r["trophy_rate"],
                "Acqua °C": r["water_temp_used"],
                "O₂ Indice": round(float(r.get("do_saturation_index", 0.85)) * 100),
                "ΔP 3h": f"{r['pressure_delta']:+.1f} hPa",
                "Vento": f"{r['wind']:.0f} km/h",
                "Strike Zone": r["depth_zone"]
            })

        df_24h = pd.DataFrame(schedule_rows)

        st.dataframe(
            df_24h,
            use_container_width=True,
            hide_index=True,
            height=460,
            column_config={
                "Ora": st.column_config.TextColumn("🕒 Ora", width="small"),
                "BAI %": st.column_config.ProgressColumn(
                    "🔥 BAI %", format="%.0f%%", min_value=0, max_value=100
                ),
                "Trophy %": st.column_config.ProgressColumn(
                    "👑 Trophy %", format="%.0f%%", min_value=0, max_value=100
                ),
                "Acqua °C": st.column_config.NumberColumn("💧 Acqua", format="%.1f°C"),
                "O₂ Indice": st.column_config.NumberColumn("🫧 O₂%", format="%d%%"),
                "ΔP 3h": st.column_config.TextColumn("📊 ΔP 3h", width="small"),
                "Vento": st.column_config.TextColumn("💨 Vento", width="small"),
                "Strike Zone": st.column_config.TextColumn("📏 Strike Zone")
            }
        )

        # Expander di certificazione e validazione del Contratto Dati (Blocco 4 v2)
        with st.expander("🛠️ Diagnostica Sistema & Contratto Dati Blocco 4", expanded=False):
            contract_status = check_block4_contract(sim)
            st.write("**Esito Validazione `check_block4_contract(sim)`:**", contract_status)
            st.json({
                "spot": geo["name"],
                "coordinates": f"{geo['lat']:.4f}, {geo['lon']:.4f}",
                "target_mode_active": target_mode,
                "base_water_temp_ema30": sim.get("base_water_temp"),
                "macro_trend_14d": sim.get("macro_trend_14d"),
                "micro_trend_72h": sim.get("micro_trend_72h"),
                "peak_bai_hour": sim["best_hour"]["time_label"],
                "peak_trophy_hour": sim.get("best_trophy_hour", {}).get("time_label")
            })


if __name__ == "__main__":
    main()