import datetime
import math
import ephem
import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st


# ==============================================================================
# 1. CONFIGURAZIONE PAGINA & INIEZIONE CSS "iOS 17 NATIVE OLED PREMIUM"
# ==============================================================================
st.set_page_config(
    page_title="Bass Pro V2",
    page_icon="🎣",
    layout="centered",  # Ottimizzato per viewport Mobile / iPhone 15
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Nascondi Header, Menu Hamburger, Footer e Sidebar nativa di Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
    section[data-testid="stSidebar"] {display: none;}

    /* Sfondo OLED Nero Puro / Grigio Antracite iOS per contrasto sotto il sole */
    .stApp {
        background-color: #000000;
        color: #F2F2F7;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, sans-serif;
    }

    /* Riduzione padding superiore per sfruttare ogni pixel dell'iPhone 15 */
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 3rem !important;
        padding-left: 0.9rem !important;
        padding-right: 0.9rem !important;
        max-width: 520px !important; /* Simula perfettamente la colonna mobile anche su PC */
    }

    /* Tipografia maggiorata per lettura sotto luce solare diretta */
    p, li, span {
        font-size: 1.04rem !important;
        line-height: 1.5 !important;
    }

    /* Header compatto stile App iOS */
    .ios-app-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 10px;
        padding: 4px 2px;
    }
    .ios-app-title {
        font-size: 1.45rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #00E676, #29B6F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .ios-badge {
        background-color: #1C1C1E;
        border: 1px solid #2C2C2E;
        color: #00E676;
        font-size: 0.75rem !important;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 20px;
        text-transform: uppercase;
    }

    /* HERO CARD PRINCIPALE (Impatto Visivo Immediato) */
    .ios-hero-card {
        background: linear-gradient(155deg, #11261B 0%, #161618 65%, #1C1C1E 100%);
        border: 1.5px solid #00E676;
        border-radius: 20px;
        padding: 20px 18px;
        margin-top: 8px;
        margin-bottom: 16px;
        box-shadow: 0 10px 28px rgba(0, 230, 118, 0.16);
    }
    .hero-spot-label {
        color: #00E676;
        font-size: 0.82rem !important;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .hero-main-grid {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin: 6px 0 12px 0;
    }
    .hero-big-score {
        font-size: 3.7rem !important;
        font-weight: 900;
        color: #FFFFFF;
        line-height: 1.0 !important;
        letter-spacing: -1.5px;
    }
    .hero-score-caption {
        font-size: 0.85rem !important;
        color: #8E8E93;
        font-weight: 600;
        display: block;
        margin-top: 2px;
    }
    .hero-trophy-box {
        text-align: right;
        background: rgba(179, 136, 255, 0.12);
        border: 1px solid rgba(179, 136, 255, 0.4);
        border-radius: 14px;
        padding: 8px 12px;
    }
    .hero-trophy-val {
        font-size: 1.65rem !important;
        font-weight: 800;
        color: #B388FF;
        line-height: 1.1 !important;
    }
    .hero-trophy-lbl {
        font-size: 0.74rem !important;
        color: #D1C4E9;
        font-weight: 600;
        text-transform: uppercase;
    }
    .hero-pill-bar {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        padding-top: 12px;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    .hero-pill {
        background-color: rgba(255, 255, 255, 0.07);
        border-radius: 10px;
        padding: 6px 10px;
        font-size: 0.88rem !important;
        font-weight: 600;
        color: #E5E5EA;
        flex: 1 1 auto;
        text-align: center;
    }

    /* CARDS GENERICHE STILE iOS (border-radius: 15px + box-shadow) */
    .ios-card {
        background-color: #1C1C1E;
        border: 1px solid #2C2C2E;
        border-radius: 15px;
        padding: 16px 18px;
        margin-bottom: 14px;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.45);
    }
    .ios-card-title {
        font-size: 1.08rem !important;
        font-weight: 800;
        margin-bottom: 10px;
        padding-bottom: 8px;
        border-bottom: 1px solid #2C2C2E;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .accent-blue { border-left: 5px solid #29B6F6; }
    .accent-green { border-left: 5px solid #00E676; }
    .accent-amber { border-left: 5px solid #FFCA28; }
    .accent-purple { border-left: 5px solid #B388FF; }

    /* Stile Metriche Native Streamlit (Stile Widget iOS) */
    div[data-testid="stMetric"] {
        background-color: #1C1C1E;
        border: 1px solid #2C2C2E;
        border-radius: 15px;
        padding: 12px 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.35);
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.55rem !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        color: #8E8E93 !important;
        font-weight: 600 !important;
    }

    /* Stile Segmented Control per st.tabs (Touch-Friendly su iPhone) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #1C1C1E;
        padding: 5px;
        border-radius: 14px;
        border: 1px solid #2C2C2E;
    }
    .stTabs [data-baseweb="tab"] {
        flex: 1;
        justify-content: center;
        height: 44px;
        border-radius: 10px;
        font-weight: 700;
        font-size: 0.92rem !important;
        color: #8E8E93;
        padding: 0 6px !important;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2C2C2E !important;
        color: #00E676 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.4);
    }

    /* Expander "Imposta Condizioni sul Campo" */
    div[data-testid="stExpander"] {
        background-color: #1C1C1E !important;
        border: 1px solid #2C2C2E !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 14px rgba(0,0,0,0.35);
        margin-bottom: 12px;
    }
    div[data-testid="stExpander"] summary p {
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        color: #29B6F6 !important;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# CONFIGURAZIONE MORFOLOGIA SPOT (INTATTA)
# ==============================================================================
SPOT_TYPES = {
    "Cava / Lago Profondo (Sassaie, Drop-off)": {
        "history_weight": 0.88,
        "diurnal_swing": 0.6,
        "desc": "Alta inerzia termica: l'acqua si scalda e si raffredda molto lentamente."
    },
    "Lago Medio / Bacino Misto (Canneti, Punte, Legnaie)": {
        "history_weight": 0.78,
        "diurnal_swing": 1.1,
        "desc": "Inerzia termica media: le baie basse reagiscono al sole pomeridiano."
    },
    "Acqua Bassa / Canale / Palude / Bozzo (< 2.5m)": {
        "history_weight": 0.62,
        "diurnal_swing": 1.8,
        "desc": "Bassa inerzia termica: risente subito dei fronti freddi ma si scalda rapidamente al sole."
    }
}


# ==============================================================================
# MODULO 1: DATA FETCHING CON STORICO 7 GIORNI (INTATTO AL 100%)
# ==============================================================================
@st.cache_data(ttl=1800, show_spinner=False)
def geocode_location(location_name: str) -> dict:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": location_name, "count": 1, "language": "it", "format": "json"}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if "results" not in data or not data["results"]:
        raise ValueError(f"Nessuna località trovata per '{location_name}'. Verifica l'ortografia.")
    
    loc = data["results"][0]
    return {
        "name": loc.get("name", location_name),
        "admin1": loc.get("admin1", ""),
        "country": loc.get("country", ""),
        "lat": float(loc["latitude"]),
        "lon": float(loc["longitude"]),
        "timezone": loc.get("timezone", "Europe/Rome")
    }


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_thermal_and_weather_series(lat: float, lon: float, day_offset: int, spot_morphology: str) -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,surface_pressure,cloud_cover,wind_speed_10m,shortwave_radiation",
        "timezone": "auto",
        "past_days": 7,
        "forecast_days": 4
    }
    resp = requests.get(url, params=params, timeout=12)
    resp.raise_for_status()
    data = resp.json()

    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    pressures = hourly.get("surface_pressure", [])
    clouds = hourly.get("cloud_cover", [])
    winds = hourly.get("wind_speed_10m", [])
    radiations = hourly.get("shortwave_radiation", [])

    today_start_idx = 7 * 24
    target_start_idx = today_start_idx + (day_offset * 24)
    target_end_idx = target_start_idx + 24

    if len(times) < target_end_idx:
        raise ValueError("Dati storici/previsionali insufficienti per la data selezionata.")

    morph = SPOT_TYPES[spot_morphology]
    hist_w = morph["history_weight"]

    past_7d_temps = [float(t) for t in temps[target_start_idx - 168 : target_start_idx] if t is not None]
    mean_7d_air = sum(past_7d_temps) / len(past_7d_temps)

    recent_48h_mean = sum(past_7d_temps[-48:]) / 48.0
    older_96h_mean = sum(past_7d_temps[-144:-48]) / 96.0
    water_temp_trend_3d = round((recent_48h_mean - older_96h_mean) * 0.60, 2)

    day_air_temps = [float(t) for t in temps[target_start_idx:target_end_idx]]
    mean_day_air = sum(day_air_temps) / 24.0

    base_water_temp = (mean_7d_air * hist_w) + (mean_day_air * (1.0 - hist_w))

    hourly_records = []
    for idx in range(target_start_idx, target_end_idx):
        dt_str = times[idx]
        hour_int = int(dt_str.split("T")[1].split(":")[0])
        air_t = float(temps[idx])
        rad_wm2 = float(radiations[idx]) if radiations[idx] is not None else 0.0

        solar_boost = (rad_wm2 / 800.0) * 0.6 if 11 <= hour_int <= 16 else 0.0
        diurnal_wave = -morph["diurnal_swing"] * math.cos((hour_int - 3) * math.pi / 12.0)
        estimated_water_temp = round(base_water_temp + (diurnal_wave * 0.65) + solar_boost, 1)

        curr_press = float(pressures[idx])
        prev_press_3h = float(pressures[max(0, idx - 3)])
        press_delta_3h = round(curr_press - prev_press_3h, 1)

        hourly_records.append({
            "hour": hour_int,
            "time_label": f"{hour_int:02d}:00",
            "date_str": dt_str.split("T")[0],
            "air_temp": round(air_t, 1),
            "water_temp": estimated_water_temp,
            "pressure": round(curr_press, 1),
            "pressure_delta": press_delta_3h,
            "clouds": int(clouds[idx]),
            "wind": round(float(winds[idx]), 1),
            "radiation": int(rad_wm2)
        })

    return {
        "hourly": hourly_records,
        "mean_7d_air": round(mean_7d_air, 1),
        "base_water_temp": round(base_water_temp, 1),
        "thermal_trend_3d": water_temp_trend_3d
    }


def compute_astronomy(lat: float, lon: float, target_date_str: str) -> dict:
    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.lon = str(lon)
    
    y, m, d = map(int, target_date_str.split("-"))
    target_dt = datetime.datetime(y, m, d, 0, 0, 0)
    utc_offset = datetime.datetime.now() - datetime.datetime.utcnow()
    observer.date = target_dt - utc_offset

    sun = ephem.Sun()
    moon = ephem.Moon()
    moon.compute(observer)
    moon_illum = round(moon.phase, 1)

    is_major_moon = (moon_illum <= 12.0 or moon_illum >= 88.0)
    if is_major_moon:
        phase_desc = "Luna Piena / Nuova (Picco Gravitazionale)"
    elif 38 <= moon_illum <= 62:
        phase_desc = "Primo / Ultimo Quarto"
    else:
        phase_desc = "Fase Intermedia"

    try:
        sr_utc = observer.next_rising(sun).datetime()
        ss_utc = observer.next_setting(sun).datetime()
        sr_local = sr_utc + utc_offset
        ss_local = ss_utc + utc_offset

        sunrise_dec = sr_local.hour + (sr_local.minute / 60.0)
        sunset_dec = ss_local.hour + (ss_local.minute / 60.0)
        sunrise_str = sr_local.strftime("%H:%M")
        sunset_str = ss_local.strftime("%H:%M")
    except (ephem.AlwaysUpError, ephem.NeverUpError):
        sunrise_dec, sunset_dec = 6.5, 19.5
        sunrise_str, sunset_str = "06:30", "19:30"

    return {
        "sunrise_dec": sunrise_dec,
        "sunset_dec": sunset_dec,
        "sunrise_str": sunrise_str,
        "sunset_str": sunset_str,
        "moon_illum": moon_illum,
        "is_major_moon": is_major_moon,
        "phase_desc": phase_desc
    }


# ==============================================================================
# MODULO 2: MOTORE BIOLOGICO MOLTIPLICATIVO V2 (INTATTO AL 100%)
# ==============================================================================
class ProTourBiologicalEngine:

    @staticmethod
    def metabolic_potential(temp: float) -> float:
        nodi = [
            (4.0, 0.04),
            (8.0, 0.14),
            (11.5, 0.32),
            (14.0, 0.54),
            (16.5, 0.82),
            (20.5, 1.00),
            (24.0, 0.88),
            (28.0, 0.52),
            (32.5, 0.18)
        ]
        if temp <= nodi[0][0]:
            return nodi[0][1]
        if temp >= nodi[-1][0]:
            return nodi[-1][1]

        for i in range(len(nodi) - 1):
            t1, s1 = nodi[i]
            t2, s2 = nodi[i + 1]
            if t1 <= temp <= t2:
                return round(s1 + ((temp - t1) / (t2 - t1)) * (s2 - s1), 4)
        return 0.50

    @staticmethod
    def thermal_trend_multiplier(trend_3d: float, current_water_temp: float) -> float:
        if current_water_temp < 22.0:
            mod = trend_3d * 0.11
        else:
            mod = -trend_3d * 0.06

        return round(max(0.72, min(1.22, 1.0 + mod)), 4)

    @staticmethod
    def score_barometric_and_sky(press: float, delta_3h: float, clouds: int, radiation: int, water_temp: float) -> float:
        if delta_3h <= -1.0:
            p_score = 0.96
        elif -1.0 < delta_3h < -0.2:
            p_score = 0.84
        elif -0.2 <= delta_3h <= 0.4:
            p_score = 0.70
        elif 0.4 < delta_3h <= 1.2:
            p_score = 0.46
        else:
            p_score = 0.30

        if water_temp < 14.5:
            if radiation >= 220:
                sky_mod = +0.16
            elif clouds > 85 and delta_3h >= 0:
                sky_mod = -0.08
            else:
                sky_mod = +0.02
        else:
            if radiation > 600 and clouds < 30:
                sky_mod = -0.18
            elif clouds >= 60:
                sky_mod = +0.12
            else:
                sky_mod = 0.0

        return round(max(0.20, min(1.00, p_score + sky_mod)), 4)

    @staticmethod
    def score_photoperiod_dynamic(hour: int, alba_dec: float, tramonto_dec: float, moon_illum: float, water_temp: float) -> float:
        if water_temp < 14.5:
            dist_from_2pm = abs(hour - 14.0)
            if dist_from_2pm <= 3.5:
                base_sol = 0.45 + 0.55 * math.exp(- (dist_from_2pm ** 2) / 4.5)
            elif hour < alba_dec or hour > tramonto_dec + 1:
                base_sol = 0.25
            else:
                base_sol = 0.38
        else:
            dist_alba = abs(hour - alba_dec)
            dist_tramonto = abs(hour - tramonto_dec)
            min_dist = min(dist_alba, dist_tramonto)

            if min_dist <= 2.2:
                base_sol = 0.45 + 0.55 * math.exp(- (min_dist ** 2) / 1.8)
            elif alba_dec < hour < tramonto_dec:
                base_sol = 0.40
            else:
                base_sol = 0.55

        if moon_illum >= 88.0 or moon_illum <= 12.0:
            base_sol = min(1.00, base_sol + 0.06)

        return round(base_sol, 4)

    @staticmethod
    def score_vento(vento_kmh: float, water_temp: float) -> float:
        if water_temp < 12.0 and vento_kmh > 18.0:
            return 0.35

        nodi_vento = [
            (0.0, 0.50),
            (4.0, 0.60),
            (9.0, 1.00),
            (18.0, 1.00),
            (25.0, 0.62),
            (32.0, 0.28)
        ]
        if vento_kmh <= nodi_vento[0][0]:
            return nodi_vento[0][1]
        if vento_kmh >= nodi_vento[-1][0]:
            return nodi_vento[-1][1]

        for i in range(len(nodi_vento) - 1):
            v1, s1 = nodi_vento[i]
            v2, s2 = nodi_vento[i + 1]
            if v1 <= vento_kmh <= v2:
                return round(s1 + ((vento_kmh - v1) / (v2 - v1)) * (s2 - s1), 4)
        return 0.50

    @staticmethod
    def score_torbidita(torbidita_input: str) -> float:
        mappa = {"Velata": 1.00, "Non specificato": 0.85, "Limpida": 0.80, "Torbida": 0.65, "Fangosa": 0.40}
        return mappa.get(torbidita_input, 0.85)

    @staticmethod
    def estimate_strike_zone_depth(water_temp: float, radiation: int, wind: float, hour: int, alba: float, tramonto: float) -> str:
        if water_temp < 9.5:
            return "Fondale / Buche (4.0m - 8.0m+)"
        elif 9.5 <= water_temp < 14.5:
            if 11 <= hour <= 16 and radiation >= 180:
                return "Risalita su Sassaie/Scalini (1.2m - 2.5m)"
            return "Drop-off / Primo Scalino (2.5m - 4.5m)"
        elif 14.5 <= water_temp <= 23.5:
            if abs(hour - alba) <= 2 or abs(hour - tramonto) <= 2 or wind >= 10:
                return "Shallow & Superficie (0.2m - 1.5m)"
            return "Sub-superficie & Cover (0.8m - 2.2m)"
        else:
            if hour < alba + 1.5 or hour > tramonto - 1.5:
                return "Topwater / Riva (0.1m - 1.0m)"
            elif radiation > 550:
                return "Cuore delle Cover Ombreggiate o Termoclino (3.0m+)"
            return "Bordi Erbai / Ombre (1.0m - 2.5m)"

    @classmethod
    def run_pro_simulation(cls, series_data: dict, astro: dict, torbidita: str, manual_water_temp: float = None) -> dict:
        hourly_meteo = series_data["hourly"]
        trend_3d = series_data["thermal_trend_3d"]
        s_torb = cls.score_torbidita(torbidita)
        torb_label = "Velata (Stima)" if torbidita == "Non specificato" else torbidita

        timeline = []
        for row in hourly_meteo:
            if manual_water_temp is not None:
                osc = -0.6 * math.cos((row["hour"] - 3) * math.pi / 12.0)
                w_temp = round(manual_water_temp + osc, 1)
            else:
                w_temp = row["water_temp"]

            m_temp = cls.metabolic_potential(w_temp)
            c_trend = cls.thermal_trend_multiplier(trend_3d, w_temp)
            effective_metabolism = min(1.05, m_temp * c_trend)

            s_press = cls.score_barometric_and_sky(row["pressure"], row["pressure_delta"], row["clouds"], row["radiation"], w_temp)
            s_sol = cls.score_photoperiod_dynamic(row["hour"], astro["sunrise_dec"], astro["sunset_dec"], astro["moon_illum"], w_temp)
            s_vento = cls.score_vento(row["wind"], w_temp)

            env_trigger = (s_press * 0.42) + (s_sol * 0.33) + (s_vento * 0.15) + (s_torb * 0.10)

            bai_raw = effective_metabolism * (0.32 + 0.68 * env_trigger) * 100.0
            bai_pct = round(max(4.0, min(100.0, bai_raw)), 1)

            trophy_temp_factor = 1.0 if 11.5 <= w_temp <= 22.0 else (0.65 if 8.5 <= w_temp < 11.5 else 0.45)
            moon_bonus = 1.12 if astro["is_major_moon"] else 1.0
            trophy_raw = ((env_trigger * 0.65) + (trophy_temp_factor * 0.35)) * moon_bonus * 100.0
            trophy_pct = round(max(5.0, min(100.0, trophy_raw)), 1)

            depth_zone = cls.estimate_strike_zone_depth(
                w_temp, row["radiation"], row["wind"], row["hour"], astro["sunrise_dec"], astro["sunset_dec"]
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
            "thermal_trend_3d": trend_3d,
            "mean_7d_air": series_data["mean_7d_air"]
        }


# ==============================================================================
# MODULO 3: GENERATORE REPORT TATTICO STRATEGICO PRO V2 (INTATTO AL 100%)
# ==============================================================================
class TacticalAdvisorV2:

    @staticmethod
    def generate_report(sim_data: dict, torbidita: str, spot_morphology: str) -> dict:
        timeline = sim_data["timeline"]
        best = sim_data["best_hour"]
        trend_3d = sim_data["thermal_trend_3d"]

        daylight_hours = [h for h in timeline if 7 <= h["hour"] <= 19]
        avg_w_temp = round(sum(h["water_temp_used"] for h in daylight_hours) / len(daylight_hours), 1)
        avg_wind = round(sum(h["wind"] for h in daylight_hours) / len(daylight_hours), 1)
        max_rad = max(h["radiation"] for h in daylight_hours)

        surface_cond = "Increspata" if avg_wind >= 8.5 else "Piatta/Calma"
        clarity_eff = "Velata" if torbidita == "Non specificato" else torbidita

        if trend_3d >= 0.6:
            trend_desc = f"📈 **Warming Trend (+{trend_3d}°C negli ultimi 3gg):** L'acqua si sta scaldando! Questo attiva i pesci e li spinge a salire di fascia batimetrica."
        elif trend_3d <= -0.6:
            trend_desc = f"📉 **Cooling Trend / Cold Front ({trend_3d}°C negli ultimi 3gg):** L'acqua ha subito un raffreddamento. Il metabolismo ha accusato uno shock termico: i bass sono apatici, hanno la bocca chiusa e si sono ritirati sui salti di profondità."
        else:
            trend_desc = f"➡️ **Stabilità Termica ({trend_3d:+.1f}°C su 3gg):** Nessuno shock termico recente, i pesci seguono il normale ciclo stagionale."

        if avg_w_temp < 14.5:
            stagione_regola = (
                f"❄️ **Regime Acqua Fredda/Fresca ({avg_w_temp}°C - Inversione Solare Attiva):** "
                "Dimentica l'alba! Al mattino presto l'acqua superficiale è al minimo termico. "
                f"Concentra gli sforzi nelle **ore centrali/pomeridiane (Picco ore {best['time_label']})**, "
                "quando l'irraggiamento solare scalda le sponde esposte a Nord, le sassaie e i legni sommersi."
            )
        else:
            stagione_regola = (
                f"🔥 **Regime Metabolico Attivo ({avg_w_temp}°C):** "
                f"Il motore enzimatico del Bass gira ad alti regimi. Le finestre di cambio luce e il picco delle ore **{best['time_label']}** "
                "offrono la massima propensione all'attacco in *shallow water*."
            )

        approccio = (
            f"{stagione_regola}\n\n"
            f"- {trend_desc}\n"
            f"- **Fascia di Profondità Chiave (Strike Zone):** `{best['depth_zone']}`\n"
            f"- **Morfologia Spot ({spot_morphology.split('(')[0].strip()}):** Superficie **{surface_cond}** (vento medio {avg_wind} km/h, radiazione max {max_rad} W/m²)."
        )

        if avg_w_temp < 12.0 or (avg_w_temp < 15.0 and trend_3d <= -0.7):
            esche = (
                "**Assetto da Cold Front / Ipometabolismo (Bocca Chiusa):**\n"
                "Con acqua fredda o in crollo termico, le esche troppo veloci vengono ignorate dai pesci piccoli e medi:\n"
                "- **Prima Scelta (Reaction Sospesa):** *Suspending Jerkbait* (110mm) lavorato con lunghe pause tra i colpi di vetta.\n"
                "- **Fondo & Scalini:** *Football Jig / Casting Jig* compatto con trailer minimale, *Blade Bait / Metal Vibe* o *Ned Rig / Drop Shot* fermo sul posto.\n"
                "- **Ricerca Lenta:** *Flat-side Crankbait* (nuoto stretto, perfetto per acqua sotto i 14°C) o *Spinnerbait* in *slow-rolling* sul fondo."
            )
        else:
            match (clarity_eff, surface_cond):
                case ("Limpida", "Piatta/Calma"):
                    esche = (
                        "Alta penetrazione luminosa e zero increspatura: il Bass usa la vista ed è iper-selettivo.\n"
                        "- **Prima Scelta (Finesse):** *Drop Shot*, *Neko Rig*, *Wacky Rig* weightless (Senko) e *Ned Rig*.\n"
                        "- **Ricerca Stealth:** *Spybait*, *Soft Jerkbait* (Fluke) o *Swimbait/Glide Bait* realistiche.\n"
                        "- **Assetto:** Fluorocarbon sottile (6 - 10 lb) e lanci lunghi."
                    )
                case ("Limpida", "Increspata"):
                    esche = (
                        "Acqua chiara ma vento che spezza la luce: condizione top per l'attacco di reazione dei grossi esemplari.\n"
                        "- **Prima Scelta:** *Suspending Jerkbait* e *Soft Swimbait* su testina piombata.\n"
                        "- **Power Fishing:** *Spinnerbait* con doppia paletta **Willow Leaf** (massimo flash) e *Medium Crankbait*."
                    )
                case ("Velata", "Piatta/Calma"):
                    esche = (
                        "Visibilità intermedia ottimale con superficie ferma: il pesce è appoggiato alle cover.\n"
                        "- **Prima Scelta:** *Casting Jig* (3/8 - 1/2 oz) con trailer *Craw* e *Texas Rig* lanciati a *Pitching*.\n"
                        f"- **Finestra Picco ({best['time_label']}):** *Flat-side Crankbait* sui bordi o *Topwater* se l'acqua supera i 17°C."
                    )
                case ("Velata", "Increspata"):
                    esche = (
                        "Condizione da manuale: vento e acqua velata attivano sia la vista sia la linea laterale.\n"
                        "- **Prima Scelta:** *Chatterbait (Bladed Jig)* sopra gli erbai e *Spinnerbait* (Tandem Colorado/Willow).\n"
                        "- **Contatto:** *Squarebill Crankbait* fatto rimbalzare sulle rocce (*deflection*)."
                    )
                case ("Torbida" | "Fangosa", _):
                    esche = (
                        f"Con acqua **{clarity_eff}**, il Bass caccia al 100% con i meccanocettori della **linea laterale**.\n"
                        "- **Massimo Thump:** *Spinnerbait* con grossa paletta **Colorado Singola** e *Chatterbait* con trailer voluminosi.\n"
                        "- **Acustica & Cover:** *Squarebill Crankbait* con *One-Knocker* rumoroso e *Jig* Black & Blue a ridosso delle sponde."
                    )

        match clarity_eff:
            case "Limpida":
                colori = (
                    "**Strategia Natural & Translucent (Acqua Limpida):**\n"
                    "- **Softbait / Jig:** *Watermelon Seed*, *Green Pumpkin*, *Smoke Pepper*, *Cinnamon*.\n"
                    "- **Hardbait:** Livree semitrasparenti come *Ghost Minnow*, *Ayu*, *Pro Blue*, *Wakasaki*."
                )
            case "Velata":
                colori = (
                    "**Strategia Solid & Two-Tone (Acqua Velata):**\n"
                    "- **Softbait / Jig:** *Green Pumpkin/Chartreuse*, *PB&J*, *Bama Bug*.\n"
                    "- **Hardbait / Lame:** *Bianco solido (White)*, *Chartreuse/White*, *Sexy Shad*, *Red Craw*."
                )
            case "Torbida" | "Fangosa":
                colori = (
                    "**Strategia High-Contrast & Silhouette (Acqua Torbida/Fangosa):**\n"
                    "- **Softbait / Jig:** **Black & Blue** (sagoma netta), *Junebug*, *Nero solido*.\n"
                    "- **Hardbait / Lame:** **Chartreuse intenso**, **Firetiger**, *Bone (Bianco opaco)* e palette dorate."
                )

        if avg_w_temp < 10.0 or trend_3d <= -1.0:
            velocita = (
                "**Recupero Ultra-Lento e Pause Prolungate (Deadsticking):**\n"
                "Il metabolismo o lo shock termico impediscono inseguimenti rapidi. Trascina il Jig sul fondo a centimetri al secondo; "
                "col Jerkbait suspending fai **2 colpi secchi e attendi 8-12 secondi** a filo in bando prima di muovere ancora."
            )
        elif 10.0 <= avg_w_temp < 15.5:
            velocita = (
                "**Recupero Cadenzato a Contatto (Slow-Rolling & Deflection):**\n"
                "Velocità medio-bassa e costante. Fai girare le palette dello Spinnerbait al minimo sindacale vicino al fondo; "
                "se usi un Crankbait, cerca l'urto contro sassi o legni e inserisci **1-2 secondi di stop** subito dopo l'impatto."
            )
        elif 15.5 <= avg_w_temp <= 23.5:
            velocita = (
                "**Recupero Reattivo e Dinamico (Reaction Speed):**\n"
                "Il pesce ha piena energia muscolare. Alterna recuperi sostenuti per coprire acqua a brusche accelerazioni (*burn-and-stop*) "
                "per scatenare l'attacco predatorio prima che il Bass possa esaminare l'inganno."
            )
        else:
            velocita = (
                "**Recupero Bipolare Estivo:**\n"
                "Veloce e rumoroso in superficie all'alba/tramonto; lentissimo e verticale (caduta libera sul posto dentro i buchi d'ombra) nelle ore centrali."
            )

        return {
            "approccio": approccio,
            "esche": esche,
            "colori": colori,
            "velocita": velocita
        }


# ==============================================================================
# MODULO 4: GRAFICI OTTIMIZZATI PER SCHERMO VERTICALE iPHONE 15 (Zero Margini)
# ==============================================================================
def create_mobile_plotly_chart(timeline: list[dict], astro: dict, best_hour: dict, focus_hour: dict) -> go.Figure:
    hours = [r["time_label"] for r in timeline]
    bai_rates = [r["catch_rate"] for r in timeline]
    trophy_rates = [r["trophy_rate"] for r in timeline]
    water_temps = [r["water_temp_used"] for r in timeline]
    depths = [r["depth_zone"] for r in timeline]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Bande Alba e Tramonto
    sr_idx = int(round(astro["sunrise_dec"]))
    ss_idx = int(round(astro["sunset_dec"]))
    for idx, label_txt in [(sr_idx, "🌅"), (ss_idx, "🌇")]:
        if 0 <= idx <= 23:
            fig.add_vrect(
                x0=max(0, idx - 1), x1=min(23, idx + 1),
                fillcolor="rgba(255, 202, 40, 0.12)",
                layer="below", line_width=1, line_dash="dot", line_color="rgba(255, 202, 40, 0.4)",
                annotation_text=label_txt, annotation_position="top left",
                annotation_font=dict(size=12)
            )

    # Curva 1: Activity Index (BAI %)
    fig.add_trace(
        go.Scatter(
            x=hours,
            y=bai_rates,
            name="🔥 Activity %",
            mode="lines",
            line=dict(color="#00E676", width=3.5, shape="spline", smoothing=0.8),
            fill="tozeroy",
            fillcolor="rgba(0, 230, 118, 0.15)",
            customdata=list(zip(water_temps, trophy_rates, depths)),
            hovertemplate=(
                "<b>Ore %{x}</b><br>"
                "🔥 Activity: <b>%{y:.1f}%</b><br>"
                "🏆 Trophy: <b>%{customdata[1]:.1f}%</b><br>"
                "💧 Acqua: %{customdata[0]}°C<extra></extra>"
            )
        ),
        secondary_y=False
    )

    # Curva 2: Trophy Window Index (Big Bass %)
    fig.add_trace(
        go.Scatter(
            x=hours,
            y=trophy_rates,
            name="🏆 Trophy %",
            mode="lines",
            line=dict(color="#B388FF", width=2.2, dash="dash", shape="spline"),
            hoverinfo="skip"
        ),
        secondary_y=False
    )

    # Stella sul Picco di Attività
    fig.add_trace(
        go.Scatter(
            x=[best_hour["time_label"]],
            y=[best_hour["catch_rate"]],
            name="Picco",
            mode="markers+text",
            marker=dict(size=15, color="#FFCA28", symbol="star", line=dict(width=1.5, color="#FFFFFF")),
            text=[f"TOP {best_hour['catch_rate']}%"],
            textposition="top center",
            textfont=dict(color="#FFCA28", size=11, family="Arial Black"),
            hoverinfo="skip",
            showlegend=False
        ),
        secondary_y=False
    )

    # Curva 3: Temperatura Acqua
    fig.add_trace(
        go.Scatter(
            x=hours,
            y=water_temps,
            name="💧 T.Acqua",
            mode="lines",
            line=dict(color="#29B6F6", width=1.8, dash="dot", shape="spline"),
            hoverinfo="skip"
        ),
        secondary_y=True
    )

    # Layout ultra-compatto senza margini morti per iPhone 15
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1C1C1E",
        plot_bgcolor="#1C1C1E",
        margin=dict(l=4, r=4, t=36, b=8),
        height=285,
        hovermode="x unified",
        dragmode=False,  # Evita che lo scroll col pollice sull'iPhone sposti il grafico per sbaglio
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="center", x=0.5,
            font=dict(size=11)
        )
    )

    fig.update_yaxes(
        range=[0, 112],
        gridcolor="#2C2C2E",
        ticksuffix="%",
        tickfont=dict(size=10, color="#8E8E93"),
        secondary_y=False
    )
    fig.update_yaxes(
        showgrid=False,
        ticksuffix="°",
        tickfont=dict(size=10, color="#29B6F6"),
        secondary_y=True
    )
    fig.update_xaxes(
        gridcolor="#242426",
        dtick=3,  # Mostra un'etichetta ogni 3 ore (00:00, 03:00, 06:00...) per non accavallarle su mobile
        tickfont=dict(size=10, color="#AEAEB2")
    )

    return fig


def create_mobile_radar(best_hour: dict) -> go.Figure:
    categories = ["Metabolismo", "Barometro", "Fotoperiodo", "Vento", "Torbidità"]
    values = [
        min(100, best_hour["s_temp"] * 100),
        best_hour["s_press"] * 100,
        best_hour["s_sol"] * 100,
        best_hour["s_vento"] * 100,
        best_hour["s_torb"] * 100
    ]
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill="toself",
        fillcolor="rgba(0, 230, 118, 0.22)",
        line=dict(color="#00E676", width=2.2),
        marker=dict(color="#FFCA28", size=6),
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1C1C1E",
        polar=dict(
            bgcolor="#141416",
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, gridcolor="#2C2C2E"),
            angularaxis=dict(gridcolor="#2C2C2E", tickfont=dict(size=11, color="#E5E5EA"))
        ),
        showlegend=False,
        margin=dict(l=28, r=28, t=20, b=20),
        height=240,
        dragmode=False
    )
    return fig


# ==============================================================================
# MODULO 5: INTERFACCIA MOBILE-FIRST iPHONE 15 (Zero Sidebar, Expander + 3 Tabs)
# ==============================================================================
def main():
    # --- 1. TOP BAR COMPATTA STILE APP NATIVA iOS ---
    st.markdown("""
    <div class="ios-app-header">
        <div class="ios-app-title">🎣 BASS PRO V2</div>
        <div class="ios-badge">Biological Engine</div>
    </div>
    """, unsafe_allow_html=True)

    # Barra rapida per Luogo e Giorno sempre a portata di pollice
    c_loc, c_day = st.columns([6, 4])
    with c_loc:
        location_query = st.text_input(
            "📍 Spot",
            value="Mantova",
            label_visibility="collapsed",
            placeholder="📍 Cerca città o lago..."
        )
    with c_day:
        day_options = {"Oggi": 0, "Domani": 1, "Dopodomani": 2}
        selected_day_label = st.selectbox(
            "📅 Giorno",
            list(day_options.keys()),
            index=0,
            label_visibility="collapsed"
        )
        day_offset = day_options[selected_day_label]

    # --- 2. EXPANDER TATTICO (Sostituisce la scomoda Sidebar su Mobile) ---
    with st.expander("⚙️ Imposta Condizioni sul Campo", expanded=False):
        torbidita_input = st.selectbox(
            "🌊 Torbidità Acqua",
            options=["Non specificato", "Limpida", "Velata", "Torbida", "Fangosa"],
            index=0
        )
        spot_morphology = st.selectbox(
            "🏞️ Morfologia & Fondale Spot",
            options=list(SPOT_TYPES.keys()),
            index=1
        )
        st.caption(f"*{SPOT_TYPES[spot_morphology]['desc']}*")

        use_manual_temp = st.toggle("🌡️ Usa Temperatura Sonda Ecoscandaglio", value=False)
        manual_water_temp = None
        if use_manual_temp:
            manual_water_temp = st.slider(
                "Temperatura Acqua Rilevata (°C)",
                min_value=4.0, max_value=33.0, value=15.0, step=0.5
            )

    if not location_query.strip():
        st.warning("Inserisci il nome di uno spot qui sopra per calcolare i dati.")
        return

    # --- ESECUZIONE MOTORE BIOLOGICO V2 ---
    try:
        with st.spinner("Calcolo curva biologica in corso..."):
            geo = geocode_location(location_query.strip())
            series_data = fetch_thermal_and_weather_series(geo["lat"], geo["lon"], day_offset, spot_morphology)
            target_date = series_data["hourly"][0]["date_str"]
            astro = compute_astronomy(geo["lat"], geo["lon"], target_date)

            sim = ProTourBiologicalEngine.run_pro_simulation(
                series_data=series_data,
                astro=astro,
                torbidita=torbidita_input,
                manual_water_temp=manual_water_temp
            )
            report = TacticalAdvisorV2.generate_report(sim, torbidita_input, spot_morphology)

    except Exception as ex:
        st.error(f"❌ Errore: {ex}")
        return

    best = sim["best_hour"]
    best_trophy = sim["best_trophy_hour"]
    top_3 = sim["top_3"]
    trend_3d = sim["thermal_trend_3d"]

    # Se l'utente guarda "Oggi", mettiamo in primo piano anche il dato dell'ORA ATTUALE
    now_hour_int = datetime.datetime.now().hour
    current_slot = sim["timeline"][now_hour_int] if day_offset == 0 else best
    hero_mode_label = f"ADESSO (ORE {current_slot['time_label']})" if day_offset == 0 else f"PICCO PREVISTO (ORE {best['time_label']})"

    # --- 3. LA "HERO SECTION" (L'Impatto Visivo Immediato sotto il sole) ---
    st.markdown(f"""
    <div class="ios-hero-card">
        <div class="hero-spot-label">📍 {geo['name']} ({geo['admin1']}) • {hero_mode_label}</div>
        <div class="hero-main-grid">
            <div>
                <div class="hero-big-score">{current_slot['catch_rate']}%</div>
                <span class="hero-score-caption">🔥 CATCH RATE (ACTIVITY INDEX)</span>
            </div>
            <div class="hero-trophy-box">
                <div class="hero-trophy-val">👑 {current_slot['trophy_rate']}%</div>
                <div class="hero-trophy-lbl">Trophy Big Bass</div>
            </div>
        </div>
        <div style="font-size:0.92rem; color:#00E676; font-weight:700; margin-bottom:10px;">
            📏 Strike Zone: {current_slot['depth_zone']}
        </div>
        <div class="hero-pill-bar">
            <div class="hero-pill">💧 Acqua: <b>{current_slot['water_temp_used']}°C</b></div>
            <div class="hero-pill">📊 <b>{int(current_slot['pressure'])}</b> hPa ({current_slot['pressure_delta']:+.1f})</div>
            <div class="hero-pill">💨 <b>{current_slot['wind']}</b> km/h</div>
            <div class="hero-pill">🏆 Top: <b>{best['time_label']} ({best['catch_rate']}%)</b></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- 4. NAVIGAZIONE A 3 SCHEDE ORIZZONTALI CONTRO LO SCROLL INFINITO ---
    tab1, tab2, tab3 = st.tabs([
        "📊 Radar Orario",
        "🎣 Strategia & Esche",
        "🌤️ Meteo Dettagliato"
    ])

    # ==========================================================================
    # TAB 1: RADAR ORARIO (Grafico Mobile + Tabella Compatta Zero-Scroll Orizz.)
    # ==========================================================================
    with tab1:
        st.markdown(
            f"**🥇 Top 3 Finestre del Giorno:** `{top_3[0]['time_label']}` ({top_3[0]['catch_rate']}%) • "
            f"`{top_3[1]['time_label']}` ({top_3[1]['catch_rate']}%) • `{top_3[2]['time_label']}` ({top_3[2]['catch_rate']}%)"
        )

        fig_mobile = create_mobile_plotly_chart(sim["timeline"], astro, best, current_slot)
        st.plotly_chart(fig_mobile, use_container_width=True, config={"displayModeBar": False})

        st.markdown("##### 📋 Timeline 24 Ore (Tocca una colonna per ordinare)")
        # Tabella ultra-compatta a 4 colonne progettata per non sbordare mai su iPhone 15
        df_mobile = pd.DataFrame([
            {
                "Ora": f"⭐ {r['time_label']}" if r["hour"] == best["hour"] else (f"🟢 {r['time_label']}" if day_offset == 0 and r["hour"] == now_hour_int else r["time_label"]),
                "Acqua": f"{r['water_temp_used']}°",
                "Catch Rate": r["catch_rate"],
                "Big Bass": r["trophy_rate"],
            }
            for r in sim["timeline"]
        ])

        st.dataframe(
            df_mobile,
            use_container_width=True,
            hide_index=True,
            height=420,
            column_config={
                "Ora": st.column_config.TextColumn("🕒 Ora", width="small"),
                "Acqua": st.column_config.TextColumn("💧 Acqua", width="small"),
                "Catch Rate": st.column_config.ProgressColumn(
                    "🔥 Activity %",
                    format="%.0f%%",
                    min_value=0,
                    max_value=100,
                ),
                "Big Bass": st.column_config.ProgressColumn(
                    "🏆 Trophy %",
                    format="%.0f%%",
                    min_value=0,
                    max_value=100,
                ),
            }
        )

    # ==========================================================================
    # TAB 2: STRATEGIA & ESCHE (Card iOS ad alto contrasto scansionabili)
    # ==========================================================================
    with tab2:
        st.success(f"🎯 **Target Picco ({best['time_label']}):** Posizionati su **{best['depth_zone']}**")

        st.markdown(f"""
        <div class="ios-card accent-green">
            <div class="ios-card-title" style="color:#00E676;">🐟 ESCHE & RIG CONSIGLIATI</div>
        """, unsafe_allow_html=True)
        st.markdown(report["esche"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="ios-card accent-amber">
            <div class="ios-card-title" style="color:#FFCA28;">🎨 COLORAZIONI & CROMATISMO</div>
        """, unsafe_allow_html=True)
        st.markdown(report["colori"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="ios-card accent-purple">
            <div class="ios-card-title" style="color:#B388FF;">⏱️ VELOCITÀ & CADENZA RECUPERO</div>
        """, unsafe_allow_html=True)
        st.markdown(report["velocita"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="ios-card accent-blue">
            <div class="ios-card-title" style="color:#29B6F6;">🧭 APPROCCIO & ANALISI BIOLOGICA</div>
        """, unsafe_allow_html=True)
        st.markdown(report["approccio"])
        st.markdown("</div>", unsafe_allow_html=True)

    # ==========================================================================
    # TAB 3: METEO DETTAGLIATO, LUNA & TELEMETRIA 7 GIORNI
    # ==========================================================================
    with tab3:
        m1, m2 = st.columns(2)
        m1.metric("💧 Inerzia Termica 3gg", f"{trend_3d:+.1f} °C", "Riscaldamento" if trend_3d >= 0 else "Raffreddamento")
        m2.metric("🔥 Tetto Metabolico", f"{int(min(100, best['s_temp'] * 100))}%", f"Media 7gg: {sim['mean_7d_air']}°C")

        m3, m4 = st.columns(2)
        m3.metric("🌅 Alba / 🌇 Tramonto", f"{astro['sunrise_str']} - {astro['sunset_str']}", "Orari astronomici")
        m4.metric("🌙 Fase Lunare", f"{astro['moon_illum']}%", astro["phase_desc"].split("(")[0].strip())

        st.markdown("##### 🎯 Equilibrio Fattori nell'Ora di Picco")
        fig_radar = create_mobile_radar(best)
        st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})

        st.markdown("##### 🌤️ Dati Grezzi Orari (Pressione, Vento, Luce)")
        df_raw_weather = pd.DataFrame([
            {
                "Ora": r["time_label"],
                "Aria": f"{r['air_temp']}°C",
                "Press (Δ3h)": f"{int(r['pressure'])} ({r['pressure_delta']:+.1f})",
                "Vento": f"{r['wind']} km/h",
                "Sole": f"{r['radiation']} W/m²"
            }
            for r in sim["timeline"]
        ])
        st.dataframe(df_raw_weather, use_container_width=True, hide_index=True, height=300)

        st.markdown("##### 🗺️ Posizione GPS dello Spot")
        map_df = pd.DataFrame({"lat": [geo["lat"]], "lon": [geo["lon"]]})
        st.map(map_df, zoom=12, use_container_width=True)


if __name__ == "__main__":
    main()