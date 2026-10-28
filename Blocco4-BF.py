# ==============================================================================
# MODULO 4 (v2): MOTORE GRAFICO PLOTLY MOBILE — LETTURA IMMEDIATA (iPhone / OLED)
# ==============================================================================
# Cosa cambia rispetto alla v1 (solo grafica: i Blocchi 1-2-3 NON vengono toccati):
#   * Una curva = un grafico. Attività (BAI) e Trophy stanno in righe separate, ognuna con la
#     propria scala. Via il doppio asse, via la legenda con le emoji, via la linea "DO %".
#   * Le informazioni chiave sono SCRITTE sopra ogni grafico ("picco 06:00", "ore migliori:
#     05:00–08:00 · 18:00–20:00"): non bisogna leggerle dalla curva con le dita.
#   * Un solo punto etichettato con l'ora per il picco + fasce evidenziate per le ore migliori.
#   * Se una curva è piatta (es. Trophy fisso al minimo) NON viene disegnato un picco finto:
#     il grafico lo dice a parole. Risolve il caso "picco Trophy alle 00:00" visto in estate.
#   * Testi più grandi (11-13 px) e spazi calcolati in pixel. Verificato con un rendering reale
#     (Chromium + plotly.js 2.35 / 3.0 / 4.1, larghezze 320-393 px): nessun testo si sovrappone,
#     esce dal riquadro o viene attraversato dalla curva.
#   * Al tocco compare UN riquadro: ora, valore di ogni serie (Attività, Trophy, Acqua) e
#     contesto in grigio (vento, pressione, O₂, zona). Nessuna etichetta extra sull'asse.
#   * Il valore di ossigeno NON viene più mostrato come "%" (era un indice euristico, non una
#     saturazione): nel tooltip compare come "O₂ indice 0.40", oppure "O₂ 7.2 mg/L" se il
#     Blocco 1 fornirà la chiave `do_actual_mg_l`.
#   * Radar riordinato (etichette con il valore, niente semaforo a soglie) + nuove barre dei
#     fattori, più rapide da leggere del radar.
#
# FUNZIONI PUBBLICHE (firme retrocompatibili con la v1)
#   create_mobile_plotly_chart(sim, astro, target_mode="Entrambi", focus_hour=None)
#   create_mobile_radar(best_hour, target_mode="Entrambi")            # accetta anche l'intero `sim`
#   create_mobile_factors_chart(best_hour, target_mode="Entrambi")    # NUOVO: barre orizzontali
#   check_block4_contract(sim)                                        # NUOVO: controllo del contratto dati
#   MOBILE_PLOTLY_CONFIG                                              # NUOVO: config consigliata per st.plotly_chart
#
# USO CONSIGLIATO IN STREAMLIT
#   st.plotly_chart(fig, use_container_width=True, config=MOBILE_PLOTLY_CONFIG)
#   Nota: Streamlit applica un proprio tema ai grafici Plotly; se colori o font risultassero
#   diversi da quelli previsti, aggiungere theme=None (non verificato qui: Streamlit non era
#   disponibile nell'ambiente di test).
#
# DATI LETTI (chiavi del timeline dei Blocchi 1-2; tutte tranne `hour` sono opzionali):
#   hour, time_label, date_str, catch_rate, trophy_rate, water_temp_used | water_temp, wind,
#   pressure_delta, depth_zone, do_saturation_index (| do_actual_mg_l), s_temp, s_press, s_sol,
#   s_vento, s_torb. In `sim`: best_hour, best_trophy_hour (| no_good_window, window_quality).
#
# LIMITI NOTI (da dichiarare)
#   * Tutto ciò che il grafico mostra sono gli indici del Blocco 2 (relativi, non calibrati):
#     il Blocco 4 li rende leggibili ma non li rende più affidabili.
#   * best_trophy_hour del Blocco 2 vale ore 00:00 quando il Trophy è piatto (bug del Blocco 2):
#     qui viene ignorato se si passa l'intero `sim`; passando la sola riga resta a carico del chiamante.
#   * Provato con Chromium e dati meteo sintetici, non su Safari/iPhone né dentro Streamlit.
#
# Nota sugli import: se i blocchi vengono incollati in un unico file, questi import possono
# restare duplicati senza problemi (datetime è importato con alias per non sovrascrivere
# eventuali `from datetime import datetime` presenti altrove).
# ==============================================================================
import math
import datetime as _b4_dt
import textwrap as _b4_tw

import plotly.graph_objects as go


# ------------------------------------------------------------------------------
# COSTANTI DI STILE
# ------------------------------------------------------------------------------
# Palette verificata con validate_palette.js (modo dark, superficie #14181c): banda di
# luminosità, croma, contrasto >= 3:1 e separazione per daltonici (deutan ΔE 8.5) tutti PASS.
B4_COL_BAI = "#0fa874"       # Attività / Numeri
B4_COL_TROPHY = "#a855f7"    # Trophy
B4_COL_WATER = "#2b9fe0"     # Temperatura dell'acqua
B4_INK_1 = "#F2F2F7"         # testo primario
B4_INK_2 = "#AEAEB2"         # testo secondario
B4_INK_3 = "#8E8E93"         # assi e didascalie
B4_SURFACE = "#14181c"       # colore del pannello (anello attorno ai marker)
B4_PANEL = "rgba(18, 22, 26, 0.75)"
B4_GRID = "rgba(255, 255, 255, 0.08)"
B4_DAYLIGHT = "rgba(250, 204, 21, 0.055)"    # velo caldo sulle ore di luce
B4_FONT = "-apple-system, SF Pro Text, Helvetica Neue, Helvetica, Arial, sans-serif"

# Config consigliata per st.plotly_chart(..., config=MOBILE_PLOTLY_CONFIG): niente barra
# strumenti, niente zoom con la rotella, niente doppio tocco che resetta il grafico.
MOBILE_PLOTLY_CONFIG = {
    "displayModeBar": False,
    "scrollZoom": False,
    "doubleClick": False,
    "showTips": False,
    "responsive": True,
}

# Geometria in pixel (pensata per ~360-393 px di larghezza utile)
B4_MARGIN_L = 34
B4_MARGIN_R = 10
B4_MARGIN_T = 2
B4_MARGIN_B = 44
B4_ROW_H_SINGLE = 140        # altezza del grafico quando c'è una sola curva
B4_ROW_H_DUAL = 108          # altezza di ciascun grafico in modalità "Entrambi"
B4_STRIP_H = 34              # striscia della temperatura dell'acqua
B4_HEADER_H = 50             # spazio per il titolo a due righe sopra ogni grafico (aria inclusa)
B4_STRIP_HEADER_H = 30       # spazio per il titolo a una riga sopra la striscia
B4_HEADER_GAP = 7            # distanza tra il titolo e il bordo alto del grafico
B4_STRIP_GAP = 5

# Soglie di PRESENTAZIONE (IPOTESI: servono solo a decidere cosa evidenziare, non hanno
# alcun significato biologico e non influenzano il modello).
B4_FLAT_SPAN = 1.0           # escursione minima (punti indice) sotto cui la curva è "piatta"
B4_WINDOW_FRAC = 0.80        # "ore migliori" = ore con valore >= minimo + 80% dell'escursione
B4_MAX_WINDOWS = 2           # al massimo due fasce evidenziate per grafico (alba e tramonto)
B4_PEAK_TOL = 0.5            # tolleranza per accettare il picco indicato dal Blocco 2
B4_Y_ADAPTIVE = True         # True: scala verticale adattata ai valori; False: sempre 0-100
B4_FOOTER_NOTE = "indici relativi, non probabilità"   # "" per toglierlo
B4_BARS_XMAX = 114           # estremo destro dell'asse delle barre (la colonna dei numeri sta oltre il 100)

_B4_DOW = ("lun", "mar", "mer", "gio", "ven", "sab", "dom")
_B4_MON = ("gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic")
_B4_MODES = {"numeri": "Numeri", "trophy": "Trophy", "entrambi": "Entrambi"}


# ------------------------------------------------------------------------------
# UTILITÀ
# ------------------------------------------------------------------------------
def _b4_f(value, default=0.0):
    """float sicuro: None / testo / NaN / inf -> default."""
    try:
        x = float(value)
    except (TypeError, ValueError):
        return default
    if math.isnan(x) or math.isinf(x):
        return default
    return x


def _b4_rgba(hex_color, alpha):
    h = hex_color.lstrip("#")
    return "rgba(%d, %d, %d, %s)" % (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), alpha)


def _b4_esc(text):
    """Escape minimo per i testi di Plotly (nomi di zona ecc. arrivano da altri blocchi)."""
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _b4_wrap_html(text, width=34, max_lines=2, prefix=""):
    lines = _b4_tw.wrap(prefix + str(text), width=width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(" ,.;:&(") + "…"
    return "<br>".join(_b4_esc(line) for line in lines)


def _b4_norm_mode(target_mode):
    return _B4_MODES.get(str(target_mode).strip().lower(), "Entrambi")


def _b4_hhmm(hour):
    total = int(round(_b4_f(hour, 0.0) * 60.0))
    hh, mm = divmod(total, 60)
    return "%02d:%02d" % (hh % 24, mm)


def _b4_hour_from_label(label):
    try:
        hh, mm = str(label).split(":")[:2]
        return int(hh) + int(mm) / 60.0
    except (ValueError, TypeError):
        return None


def _b4_parse_day(date_str):
    try:
        return _b4_dt.datetime.strptime(str(date_str)[:10], "%Y-%m-%d")
    except (ValueError, TypeError):
        return None


def _b4_ts(day, hour):
    """Timestamp 'YYYY-MM-DD HH:MM:SS' per un'ora decimale (anche fuori 0-24: scavalca il giorno)."""
    dt = day + _b4_dt.timedelta(minutes=int(round(hour * 60.0)))
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def _b4_time_ticks(day, hours, step_h, fmt):
    """Tick dell'asse dei tempi: (valori, testi), uno ogni `step_h` ore dalla mezzanotte del primo giorno.

    Li calcoliamo noi (invece di dtick/tick0) per due motivi: l'ultimo tick viene tolto se la sua
    etichetta uscirebbe dal riquadro (con dati ogni 15 minuti, o fino alle 24:00, "00:00" sporgeva
    di qualche pixel a destra) e con pochissimi dati le etichette sono le ore stesse.
    """
    lo_h, hi_h = hours[0] - 0.5, hours[-1] + 0.5
    edge_h = 0.03 * (hi_h - lo_h)      # ~8-10 px sui 276-349 px utili di uno schermo da telefono

    def label(h):
        return (day + _b4_dt.timedelta(minutes=int(round(h * 60.0)))).strftime(fmt)

    vals, texts = [], []
    k = int(math.ceil(lo_h / step_h - 1e-9))
    while len(vals) < 60:
        h = k * step_h
        if h > hi_h - edge_h + 1e-9:
            break
        vals.append(_b4_ts(day, h))
        texts.append(label(h))
        k += 1
    if len(vals) < 2:                  # serie cortissima: nessun multiplo di step_h cade nei dati
        picks = list(hours) if len(hours) <= 6 else [hours[i * (len(hours) - 1) // 5] for i in range(6)]
        vals = [_b4_ts(day, h) for h in picks]
        texts = [label(h) for h in picks]
    return vals, texts


def _b4_day_label(day):
    try:
        return "%s %d %s" % (_B4_DOW[day.weekday()], day.day, _B4_MON[day.month - 1])
    except (AttributeError, IndexError):
        return ""


def _b4_hour_of(obj):
    """Ora (float) da un dict-riga, da un numero o da un 'HH:MM'. None se non interpretabile."""
    if isinstance(obj, dict):
        h = _b4_f(obj.get("hour"), None)
        if h is None:
            h = _b4_hour_from_label(obj.get("time_label"))
        return h
    h = _b4_f(obj, None)
    if h is None:
        h = _b4_hour_from_label(obj)
    return h


def _b4_cont_hour(obj, day0):
    """Ora continua (float) di una riga/numero: conta dal giorno 0 se la riga ha una `date_str`."""
    h = _b4_hour_of(obj)
    if h is None:
        return None
    if isinstance(obj, dict) and day0 is not None:
        d = _b4_parse_day(obj.get("date_str"))
        if d is not None:
            h += (d - day0).days * 24.0
    return h


def _b4_chrono(raw_rows):
    """
    Righe (solo dict) in ordine cronologico -> (giorno_0 oppure None, [(ora_continua, riga), ...]).
    L'ora è continua dal primo giorno: se il timeline copre più giorni (hour 0-23 ripetuto con
    `date_str` diversa) i punti restano nell'ordine giusto invece di mescolarsi.
    """
    items = []
    for i, r in enumerate(raw_rows):
        if not isinstance(r, dict):
            continue
        h = _b4_hour_of(r)
        items.append((_b4_parse_day(r.get("date_str")), float(i) if h is None else h, r))
    days = [d for d, _, _ in items if d is not None]
    day0 = min(days) if days else None
    out = []
    for d, h, r in items:
        if day0 is not None and d is not None:
            h += (d - day0).days * 24.0
        out.append((h, r))
    out.sort(key=lambda t: t[0])
    return day0, out


def _b4_ticks(peak):
    """Scala verticale: tick a 0 / metà / cima + limite superiore con spazio per l'etichetta del picco."""
    if B4_Y_ADAPTIVE:
        tick_top = 100.0
        for cand in (20.0, 30.0, 40.0, 60.0, 80.0, 100.0):
            if peak <= cand:
                tick_top = cand
                break
        else:
            tick_top = float(math.ceil(peak / 10.0) * 10.0)
    else:
        tick_top = 100.0
    range_top = max(tick_top, peak * 1.38)
    return [0.0, tick_top / 2.0, tick_top], range_top


def _b4_find_peak(hours, vals, preferred_hour, twilights):
    """Indice del picco, oppure None se la curva è piatta (nessuna ora si distingue)."""
    if not vals:
        return None
    lo, hi = min(vals), max(vals)
    if (hi - lo) < B4_FLAT_SPAN:
        return None
    # 1) picco indicato dal Blocco 2 (coerenza col report testuale), se è davvero in cima
    if preferred_hour is not None:
        for i, h in enumerate(hours):
            if abs(h - preferred_hour) < 1e-6 and vals[i] >= hi - B4_PEAK_TOL:
                return i
    # 2) picco locale con spareggio deterministico: vicino a alba/tramonto, poi ora più bassa
    cands = [i for i, v in enumerate(vals) if v >= hi - 1e-9]
    cands.sort(key=lambda i: (min([abs(hours[i] - t) for t in twilights] or [0.0]), hours[i]))
    return cands[0]


def _b4_windows(hours, vals):
    """Fasce di ore consecutive nella parte alta della curva: [(ora_inizio, ora_fine), ...]."""
    if not vals:
        return [], 1.0
    lo, hi = min(vals), max(vals)
    diffs = sorted(b - a for a, b in zip(hours, hours[1:]) if b - a > 1e-9)
    step = diffs[len(diffs) // 2] if diffs else 1.0
    if (hi - lo) < B4_FLAT_SPAN:
        return [], step
    thr = lo + B4_WINDOW_FRAC * (hi - lo)
    runs, cur = [], []
    for h, v in zip(hours, vals):
        if v >= thr - 1e-12:
            if cur and (h - cur[-1][0]) > step * 1.01:
                runs.append(cur)
                cur = []
            cur.append((h, v))
        elif cur:
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    runs.sort(key=lambda run: max(v for _, v in run), reverse=True)
    runs = runs[:B4_MAX_WINDOWS]
    runs.sort(key=lambda run: run[0][0])
    return [(run[0][0], run[-1][0]) for run in runs], step


def _b4_windows_text(windows):
    parts = []
    for h0, h1 in windows:
        if abs(h1 - h0) < 1e-9:
            parts.append(_b4_hhmm(h0))
        else:
            parts.append("%s–%s" % (_b4_hhmm(h0), _b4_hhmm(h1)))
    return " · ".join(parts)


def _b4_vtxt(v):
    """Valore di un indice: intero da 10 in su, un decimale sotto (niente falsa precisione)."""
    return ("%.0f" % v) if abs(v) >= 10 else ("%.1f" % v)


def _b4_details(r):
    """Righe di contesto per il tooltip (lista; solo ciò che esiste davvero nella riga)."""
    lines = []
    bits = []
    wind = _b4_f(r.get("wind"), None)
    if wind is not None:
        bits.append("Vento %.0f km/h" % wind)
    dp = _b4_f(r.get("pressure_delta"), None)
    if dp is not None:
        bits.append("Pressione %+.1f hPa/3h" % dp)
    if bits:
        lines.append(" · ".join(bits))
    mg = _b4_f(r.get("do_actual_mg_l"), None)
    if mg is not None:
        lines.append("O₂ %.1f mg/L" % mg)
    else:
        di = _b4_f(r.get("do_saturation_index"), None)
        if di is not None:
            lines.append("O₂ indice %.2f" % di)
    zone = r.get("depth_zone")
    if zone not in (None, "", "-"):
        lines.extend(_b4_wrap_html(zone, prefix="Zona: ").split("<br>"))
    return lines


def _b4_empty_figure(message, height=110):
    return go.Figure(layout=dict(
        template="plotly_dark",
        height=height,
        margin=dict(l=8, r=8, t=8, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=B4_PANEL,
        font=dict(family=B4_FONT, size=13, color=B4_INK_2),
        dragmode=False,
        xaxis=dict(visible=False, fixedrange=True),
        yaxis=dict(visible=False, fixedrange=True),
        annotations=[dict(text=_b4_esc(message), x=0.5, y=0.5, xref="paper", yref="paper",
                          showarrow=False, font=dict(size=13, color=B4_INK_2))],
    ))


def _b4_dot(color):
    return '<span style="color:%s">●</span>' % color


def _b4_muted(text):
    return '<span style="color:%s">%s</span>' % (B4_INK_2, text)


# ------------------------------------------------------------------------------
# INGRESSO: normalizzazione degli input (dict sim | lista legacy | 3° argomento dict)
# ------------------------------------------------------------------------------
def _b4_prepare(sim, astro, target_mode):
    legacy_best = None
    if isinstance(target_mode, dict):     # vecchia UI: create_mobile_plotly_chart(tl, astro, best_hour)
        legacy_best = target_mode
        target_mode = "Entrambi"
    mode = _b4_norm_mode(target_mode)

    best_hour = best_trophy = None
    flags = {"no_good_window": False, "window_quality": ""}
    if isinstance(sim, dict):
        raw_rows = sim.get("timeline") or []
        if isinstance(sim.get("best_hour"), dict):
            best_hour = sim["best_hour"]
        if isinstance(sim.get("best_trophy_hour"), dict):
            best_trophy = sim["best_trophy_hour"]
        flags["no_good_window"] = bool(sim.get("no_good_window", False))
        flags["window_quality"] = str(sim.get("window_quality") or "").strip().lower()
    elif isinstance(sim, (list, tuple)):
        raw_rows = list(sim)
    else:
        raw_rows = []
    if legacy_best is not None:
        best_hour = legacy_best

    day0, chrono = _b4_chrono(raw_rows)
    rows = [{"h": h, "r": r} for h, r in chrono]

    return {
        "rows": rows,
        "day0": day0,
        "mode": mode,
        "astro": astro if isinstance(astro, dict) else {},
        "best_hour": best_hour,
        "best_trophy_hour": best_trophy,
        "flags": flags,
    }


# ------------------------------------------------------------------------------
# GRAFICO 1 — TELEMETRIA ORARIA
# ------------------------------------------------------------------------------
def create_mobile_plotly_chart(
    sim: dict,
    astro: dict,
    target_mode: str = "Entrambi",
    focus_hour: dict = None
) -> go.Figure:
    """
    Telemetria oraria a righe separate, leggibile a colpo d'occhio su iPhone.

    target_mode:
        "Numeri"   -> una riga: Attività (BAI)
        "Trophy"   -> una riga: Trophy (big bass > 2 kg)
        "Entrambi" -> due righe (BAI sopra, Trophy sotto), ciascuna con la propria scala
    In fondo c'è sempre una striscia sottile con la temperatura dell'acqua (se disponibile).

    sim:        dict del Blocco 2 (con 'timeline', 'best_hour', 'best_trophy_hour') oppure, come
                nella v1, la sola lista timeline.
    astro:      dict con 'sunrise_dec' e 'sunset_dec' (ore decimali). Facoltativo: None va bene.
    focus_hour: facoltativo. Riga oraria (dict) o ora numerica da evidenziare con una linea
                verticale (es. l'ora scelta dall'utente o l'ora attuale). Nella v1 era ignorato.

    Ogni riga mostra: titolo + picco, "ore migliori" evidenziate, curva con area. Se la curva è
    piatta non si disegna alcun picco. Se `sim` contiene no_good_window=True (chiave futura del
    Blocco 2) il titolo lo dice e non vengono evidenziate finestre.
    """
    ctx = _b4_prepare(sim, astro, target_mode)
    rows = ctx["rows"]
    if not rows:
        return _b4_empty_figure("Nessun dato orario disponibile")

    mode = ctx["mode"]
    flags = ctx["flags"]
    astro = ctx["astro"]
    recs = [d["r"] for d in rows]
    hours = [d["h"] for d in rows]

    # --- asse dei tempi: vero asse "date" (ticks ogni 3 ore, tooltip con l'ora) ---
    day_first = ctx["day0"]
    has_date = day_first is not None
    if day_first is None:
        day_first = _b4_dt.datetime(2000, 1, 10)
    xs = [_b4_ts(day_first, h) for h in hours]
    x_lo = _b4_ts(day_first, hours[0] - 0.5)
    x_hi = _b4_ts(day_first, hours[-1] + 0.5)
    span_h = hours[-1] - hours[0]       # ticks ogni 3 h per un giorno; più radi se i dati coprono più giorni
    tick_step_h = 3 if span_h <= 30 else (6 if span_h <= 54 else (12 if span_h <= 100 else 24))
    tick_fmt = "%d/%m" if tick_step_h >= 24 else "%H:%M"
    tickvals_x, ticktext_x = _b4_time_ticks(day_first, hours, tick_step_h, tick_fmt)
    first_k = int(math.floor(hours[0] / 24.0))
    n_days = int(math.floor(hours[-1] / 24.0)) - first_k + 1
    day_ks = list(range(first_k, first_k + max(1, min(n_days, 8))))

    # --- alba / tramonto ---
    sr = _b4_f(astro.get("sunrise_dec"), None)
    ss = _b4_f(astro.get("sunset_dec"), None)
    sun_ok = sr is not None and ss is not None and 0.0 <= sr < ss <= 24.0
    twilights = []
    if sun_ok:
        for dk in day_ks:
            twilights += [24.0 * dk + sr, 24.0 * dk + ss]

    # --- curve da mostrare ---
    metrics = []
    if mode in ("Numeri", "Entrambi"):
        metrics.append({"key": "catch_rate", "title": "Attività (BAI)", "short": "Attività",
                        "color": B4_COL_BAI, "symbol": "star", "psize": 13,
                        "best": ctx["best_hour"]})
    if mode in ("Trophy", "Entrambi"):
        metrics.append({"key": "trophy_rate", "title": "Trophy (big bass >2 kg)", "short": "Trophy",
                        "color": B4_COL_TROPHY, "symbol": "diamond", "psize": 12,
                        "best": ctx["best_trophy_hour"]})
    row_h = B4_ROW_H_DUAL if len(metrics) > 1 else B4_ROW_H_SINGLE

    # --- temperatura dell'acqua (striscia) ---
    water = [_b4_f(r.get("water_temp_used", r.get("water_temp")), None) for r in recs]
    water_ok = sum(1 for w in water if w is not None) >= 2

    # --- piano dei blocchi (dall'alto in basso) ---
    blocks = []
    for m in metrics:
        vals = [_b4_f(r.get(m["key"]), 0.0) for r in recs]
        best_h = _b4_cont_hour(m["best"], ctx["day0"]) if m["best"] else None
        idx = _b4_find_peak(hours, vals, best_h, twilights)
        wins, step = _b4_windows(hours, vals)
        m.update({"vals": vals, "peak": idx, "wins": [] if flags["no_good_window"] else wins, "step": step})
        blocks.append({"kind": "main", "m": m, "header_h": B4_HEADER_H, "plot_h": row_h})
    if water_ok:
        blocks.append({"kind": "strip", "header_h": B4_STRIP_HEADER_H, "plot_h": B4_STRIP_H})

    # --- tooltip: UNA lettura completa dell'ora (ora + tutte le serie + contesto), uguale su ogni grafico ---
    labels = [str(r.get("time_label") or _b4_hhmm(h)) for r, h in zip(recs, hours)]
    readout_rows = []
    for b in blocks:
        if b["kind"] == "main":
            readout_rows.append((b["m"]["short"], b["m"]["color"], [_b4_vtxt(v) for v in b["m"]["vals"]]))
    if water_ok:
        readout_rows.append(("Acqua", B4_COL_WATER, [("%.1f °C" % w) if w is not None else None for w in water]))
    readouts = []
    for i, r in enumerate(recs):
        lines = ["<b>%s</b>" % _b4_esc(labels[i])]
        for name, rcolor, texts in readout_rows:
            if texts[i] is not None:
                lines.append("%s %s <b>%s</b>" % (_b4_dot(rcolor), name, texts[i]))
        lines.extend(_b4_muted(t) for t in _b4_details(r))
        readouts.append("<br>".join(lines))

    y_px = 0.0
    for b in blocks:
        y_px += b["header_h"]
        b["top_px"] = y_px
        y_px += b["plot_h"]
        b["bot_px"] = y_px
    plot_total = y_px
    fig_h = int(round(B4_MARGIN_T + plot_total + B4_MARGIN_B))
    for b in blocks:
        b["y_top"] = 1.0 - b["top_px"] / plot_total
        b["y_bot"] = 1.0 - b["bot_px"] / plot_total

    # --- focus: linea verticale opzionale ---
    focus_h = _b4_cont_hour(focus_hour, ctx["day0"]) if focus_hour is not None else None

    traces, shapes, annotations = [], [], []
    layout_axes = {}
    n = len(blocks)

    for k, b in enumerate(blocks, start=1):
        xid = "x" if k == 1 else "x%d" % k
        yid = "y" if k == 1 else "y%d" % k
        xkey = "xaxis" if k == 1 else "xaxis%d" % k
        ykey = "yaxis" if k == 1 else "yaxis%d" % k
        last = (k == n)

        # fascia "luce del giorno" (velo caldo) su ogni riga
        if sun_ok:
            for dk in day_ks:
                shapes.append(dict(type="rect", xref=xid, yref="paper",
                                   x0=_b4_ts(day_first, 24.0 * dk + sr), x1=_b4_ts(day_first, 24.0 * dk + ss),
                                   y0=b["y_bot"], y1=b["y_top"], fillcolor=B4_DAYLIGHT,
                                   line=dict(width=0), layer="below"))

        if b["kind"] == "main":
            m = b["m"]
            vals = m["vals"]
            peak_val = max(vals) if vals else 0.0
            tickvals, range_top = _b4_ticks(peak_val)
            color = m["color"]

            # ore migliori: fasce evidenziate
            for h0, h1 in m["wins"]:
                shapes.append(dict(type="rect", xref=xid, yref="paper",
                                   x0=_b4_ts(day_first, h0 - m["step"] / 2.0),
                                   x1=_b4_ts(day_first, h1 + m["step"] / 2.0),
                                   y0=b["y_bot"], y1=b["y_top"],
                                   fillcolor=_b4_rgba(color, 0.16), line=dict(width=0), layer="below"))

            # linea di focus
            if focus_h is not None:
                shapes.append(dict(type="line", xref=xid, yref="paper",
                                   x0=_b4_ts(day_first, focus_h), x1=_b4_ts(day_first, focus_h),
                                   y0=b["y_bot"], y1=b["y_top"],
                                   line=dict(color="rgba(242, 242, 247, 0.80)", width=1.6)))

            # curva (tooltip completo al tocco)
            traces.append(go.Scatter(
                x=xs, y=vals, xaxis=xid, yaxis=yid, mode="lines", name=m["short"],
                line=dict(color=color, width=2.6, shape="linear"),
                fill="tozeroy", fillcolor=_b4_rgba(color, 0.12),
                customdata=readouts,
                hovertemplate="%{customdata}<extra></extra>", showlegend=False))

            # picco: un solo punto con l'ora
            pk = m["peak"]
            if pk is not None and not flags["no_good_window"]:
                px = hours[pk]
                span = (hours[-1] - hours[0]) or 1.0
                rel = (px - hours[0]) / span
                tpos = "top right" if rel < 0.08 else ("top left" if rel > 0.92 else "top center")
                traces.append(go.Scatter(
                    x=[xs[pk]], y=[vals[pk]], xaxis=xid, yaxis=yid, mode="markers+text",
                    marker=dict(size=m["psize"], symbol=m["symbol"], color=B4_INK_1,
                                line=dict(width=2, color=B4_SURFACE)),
                    text=[_b4_hhmm(px)], textposition=tpos,
                    textfont=dict(size=12, color=B4_INK_1), cliponaxis=False,
                    hoverinfo="skip", showlegend=False))

            # titolo a due righe sopra il grafico
            head = "%s <b>%s</b>" % (_b4_dot(color), m["title"])
            if pk is None:
                l1 = head + " · nessun picco"
                l2 = "andamento piatto: nessuna ora si distingue"
            elif flags["no_good_window"]:
                l1 = head + " · poco favorevole"
                l2 = "nessuna finestra buona oggi"
            else:
                l1 = head + " · picco <b>%s</b> (%.0f)" % (_b4_hhmm(hours[pk]), vals[pk])
                l2 = ("ore migliori: " + _b4_windows_text(m["wins"])) if m["wins"] else ""
                if flags["window_quality"] == "scarsa":
                    l2 = (l2 + " · " if l2 else "") + "qualità scarsa"
            annotations.append(dict(
                text=l1 + ("<br>" + _b4_muted(l2) if l2 else ""),
                xref="paper", yref="paper", x=0, y=b["y_top"], xanchor="left", yanchor="bottom",
                xshift=-(B4_MARGIN_L - 6), yshift=B4_HEADER_GAP, align="left", showarrow=False,
                font=dict(size=13, color=B4_INK_1)))

            layout_axes[ykey] = dict(
                domain=[b["y_bot"], b["y_top"]], anchor=xid, range=[0, range_top], automargin=False,
                tickvals=tickvals, tickformat=".0f", ticks="", showgrid=True, gridcolor=B4_GRID,
                gridwidth=1, zeroline=False, showline=False, fixedrange=True,
                tickfont=dict(size=11, color=B4_INK_3))
        else:
            ws = [w for w in water if w is not None]
            lo, hi = min(ws), max(ws)
            pad = max(1.0, 0.5 * (hi - lo))
            traces.append(go.Scatter(
                x=xs, y=[w if w is not None else None for w in water], xaxis=xid, yaxis=yid,
                mode="lines", name="Acqua", connectgaps=True,
                line=dict(color=B4_COL_WATER, width=2.2, shape="linear"),
                customdata=readouts,
                hovertemplate="%{customdata}<extra></extra>",
                showlegend=False))
            rng = ("%.1f–%.1f" % (lo, hi)) if (hi - lo) >= 0.05 else ("%.1f" % hi)
            annotations.append(dict(
                text="%s Acqua <b>%s</b> °C" % (_b4_dot(B4_COL_WATER), rng),
                xref="paper", yref="paper", x=0, y=b["y_top"], xanchor="left", yanchor="bottom",
                xshift=-(B4_MARGIN_L - 6), yshift=B4_STRIP_GAP, align="left", showarrow=False,
                font=dict(size=12, color=B4_INK_2)))
            layout_axes[ykey] = dict(
                domain=[b["y_bot"], b["y_top"]], anchor=xid, range=[lo - pad, hi + pad], automargin=False,
                showticklabels=False, ticks="", showgrid=False, zeroline=False, showline=False,
                fixedrange=True)

        layout_axes[xkey] = dict(
            type="date", domain=[0, 1], anchor=yid, range=[x_lo, x_hi], automargin=False,
            tickmode="array", tickvals=tickvals_x, ticktext=ticktext_x, hoverformat="%H:%M",
            showticklabels=last, ticks="outside", ticklen=6, tickcolor="rgba(0, 0, 0, 0)", tickangle=0,
            showgrid=True, gridcolor=B4_GRID, gridwidth=1,
            zeroline=False, showline=False, fixedrange=True,
            tickfont=dict(size=11, color=B4_INK_3),
            showspikes=True, spikemode="across", spikesnap="data", spikedash="solid",
            spikethickness=1, spikecolor="rgba(242, 242, 247, 0.35)")

    # piè di pagina: data, alba/tramonto, avvertenza sulla scala
    foot = []
    if has_date:
        foot.append(_b4_day_label(day_first))
    if sun_ok:
        foot.append("☀ %s–%s" % (_b4_hhmm(sr), _b4_hhmm(ss)))
    if B4_FOOTER_NOTE:
        foot.append(B4_FOOTER_NOTE)
    foot = [f for f in foot if f]
    if foot:
        annotations.append(dict(
            text=_b4_esc(" · ").join(_b4_esc(f) for f in foot),
            xref="paper", yref="paper", x=0, y=0, xanchor="left", yanchor="top",
            xshift=-(B4_MARGIN_L - 6), yshift=-28, align="left", showarrow=False,
            font=dict(size=10.5, color=B4_INK_3)))

    layout = dict(
        template="plotly_dark", height=fig_h,
        margin=dict(l=B4_MARGIN_L, r=B4_MARGIN_R, t=B4_MARGIN_T, b=B4_MARGIN_B, autoexpand=False),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=B4_PANEL,
        font=dict(family=B4_FONT, size=12, color=B4_INK_1),
        hovermode="closest", hoverdistance=-1, spikedistance=-1, dragmode=False, showlegend=False,
        hoverlabel=dict(bgcolor="rgba(15, 18, 22, 0.96)", bordercolor="rgba(255, 255, 255, 0.18)",
                        font=dict(size=12, color=B4_INK_1, family=B4_FONT), align="left"),
        shapes=shapes, annotations=annotations)
    layout.update(layout_axes)
    return go.Figure(data=traces, layout=layout)


# ------------------------------------------------------------------------------
# FATTORI DELL'ORA DI PICCO (usati da radar e barre)
# ------------------------------------------------------------------------------
# (nome mostrato, chiave nella riga oraria). Tutti i punteggi sono 0-1 "più alto = più favorevole".
_B4_FACTORS = (
    ("Metabolismo", "s_temp"),
    ("Barometro", "s_press"),
    ("Luce", "s_sol"),
    ("Vento", "s_vento"),
    ("Torbidità", "s_torb"),
    ("Ossigeno", "do_saturation_index"),
)


def _b4_resolve_hour(obj, mode):
    """
    Riga oraria da mostrare in radar/barre -> (riga, nota).
    * Se `obj` è già una riga oraria: la usa così com'è (nota vuota).
    * Se `obj` è l'intero `sim`: sceglie lo stesso picco del grafico orario. In modalità Trophy,
      se la curva Trophy è piatta (nessuna ora si distingue) usa l'ora migliore per l'Attività e
      lo dice nel titolo, invece di mostrare un'ora "migliore" che non lo è.
    """
    if isinstance(obj, dict) and isinstance(obj.get("timeline"), (list, tuple)):
        day0, pairs = _b4_chrono(obj["timeline"])
        hours = [p[0] for p in pairs]
        recs = [p[1] for p in pairs]

        def pick(rate_key, best_key):
            best = obj.get(best_key)
            vals = [_b4_f(r.get(rate_key), 0.0) for r in recs]
            idx = _b4_find_peak(hours, vals, _b4_cont_hour(best, day0) if isinstance(best, dict) else None, [])
            return recs[idx] if idx is not None else None

        if mode == "Trophy":
            rec = pick("trophy_rate", "best_trophy_hour")
            if rec is not None:
                return rec, ""
            rec = pick("catch_rate", "best_hour")
            if rec is not None:
                return rec, "Trophy piatto: ora migliore dell'Attività"
        else:
            rec = pick("catch_rate", "best_hour")
            if rec is not None:
                return rec, ""
        fallback = obj.get("best_hour")
        if not isinstance(fallback, dict):
            fallback = obj.get("best_trophy_hour")
        if isinstance(fallback, dict):
            return fallback, "andamento piatto: ora indicativa"
        return (recs[0] if recs else {}), ""
    return (obj if isinstance(obj, dict) else {}), ""


def _b4_factor_list(rec):
    """[(nome, punteggio 0-100 oppure None se la chiave manca)]."""
    out = []
    for name, key in _B4_FACTORS:
        v = _b4_f(rec.get(key), None) if isinstance(rec, dict) else None
        out.append((name, None if v is None else max(0.0, min(100.0, v * 100.0))))
    return out


def _b4_hour_label(rec):
    if not isinstance(rec, dict):
        return ""
    label = rec.get("time_label")
    if label:
        return str(label)
    h = _b4_hour_of(rec)
    return _b4_hhmm(h) if h is not None else ""


def _b4_extremes_text(facts):
    """Riga di sintesi sotto il titolo: quale fattore frena di più l'ora mostrata."""
    valid = [(n, v) for n, v in facts if v is not None]
    if len(valid) < 2:
        return ""
    lo_v = min(v for _, v in valid)
    hi_v = max(v for _, v in valid)
    if hi_v - lo_v < 5.0:
        return "fattori tutti allineati"
    lows = [n for n, v in valid if v <= lo_v + 0.5]
    if len(lows) == 1:
        return "più debole: %s" % lows[0]
    if len(lows) == 2:
        return "più deboli: %s e %s" % (lows[0], lows[1])
    return "più deboli: %s e altri %d" % (lows[0], len(lows) - 1)


def _b4_factor_header(rec, facts, title, note=""):
    hl = _b4_hour_label(rec)
    l1 = "<b>%s</b>" % title + ((" alle <b>%s</b>" % hl) if hl else "")
    l2 = note or _b4_extremes_text(facts)
    return l1 + ("<br>" + _b4_muted(_b4_esc(l2)) if l2 else "")


# ------------------------------------------------------------------------------
# GRAFICO 2 — ESAGONO DEI FATTORI (radar)
# ------------------------------------------------------------------------------
def create_mobile_radar(best_hour: dict, target_mode: str = "Entrambi") -> go.Figure:
    """
    Esagono a 6 assi con il punteggio (0-100) di ogni fattore nell'ora di picco.

    best_hour:   riga oraria del Blocco 2 oppure l'intero `sim` (in modalità "Trophy" usa
                 automaticamente best_trophy_hour: non serve più scegliere l'ora a mano).
    target_mode: "Trophy" -> viola; "Numeri"/"Entrambi" -> verde. Il colore indica la modalità,
                 NON un giudizio: la v1 usava un semaforo a soglie (70/45) che col BAI reale
                 risultava quasi sempre rosso anche nelle ore migliori.
    I valori sono scritti sotto il nome di ogni asse (non servono dita sul grafico) e il titolo
    indica il fattore più debole, cioè ciò che frena quell'ora. "n/d" = chiave assente nei dati.
    Per una lettura ancora più rapida su telefono vedi create_mobile_factors_chart().
    """
    mode = _b4_norm_mode(target_mode)
    rec, note = _b4_resolve_hour(best_hour, mode)
    facts = _b4_factor_list(rec)
    if all(v is None for _, v in facts):
        return _b4_empty_figure("Fattori non disponibili per questa ora", height=120)

    color = B4_COL_TROPHY if mode == "Trophy" else B4_COL_BAI
    n = len(facts)
    theta = [i * 360.0 / n for i in range(n)]
    r_vals = [0.0 if v is None else v for _, v in facts]
    custom = [[nm, "n/d" if v is None else "%.0f su 100" % v] for nm, v in facts]
    ticktext = ["%s<br><b>%s</b>" % (nm, "n/d" if v is None else "%d" % int(round(v))) for nm, v in facts]

    top, bottom, side, height = 72, 36, 64, 306
    fig = go.Figure(
        data=[go.Scatterpolar(
            r=r_vals + [r_vals[0]], theta=theta + [360.0], thetaunit="degrees",
            mode="lines+markers", fill="toself", fillcolor=_b4_rgba(color, 0.22),
            line=dict(color=color, width=2.6),
            marker=dict(size=9, color=color, line=dict(width=2, color=B4_SURFACE)),
            customdata=custom + [custom[0]],
            hovertemplate="<b>%{customdata[0]}</b>: %{customdata[1]}<extra></extra>",
            showlegend=False)],
        layout=dict(
            template="plotly_dark", height=height,
            margin=dict(l=side, r=side, t=top, b=bottom, autoexpand=False),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family=B4_FONT, size=12, color=B4_INK_1),
            dragmode=False, showlegend=False,
            hoverlabel=dict(bgcolor="rgba(15, 18, 22, 0.96)", bordercolor="rgba(255, 255, 255, 0.18)",
                            font=dict(size=12, color=B4_INK_1, family=B4_FONT), align="left"),
            polar=dict(
                bgcolor=B4_PANEL,
                radialaxis=dict(range=[0, 112], tickvals=[25, 50, 75, 100], showticklabels=False,
                                ticks="", showline=False, gridcolor="rgba(255, 255, 255, 0.12)"),
                angularaxis=dict(type="linear", thetaunit="degrees", rotation=90, direction="clockwise",
                                 tickmode="array", tickvals=theta, ticktext=ticktext, ticks="",
                                 tickfont=dict(size=12, color=B4_INK_1),
                                 gridcolor="rgba(255, 255, 255, 0.12)", showline=False)),
            annotations=[dict(
                text=_b4_factor_header(rec, facts, "Fattori", note),
                xref="paper", yref="paper", x=0, y=1, xanchor="left", yanchor="top",
                xshift=-(side - 6), yshift=top - 4, align="left", showarrow=False,
                font=dict(size=13, color=B4_INK_1))]))
    return fig


# ------------------------------------------------------------------------------
# GRAFICO 3 — BARRE DEI FATTORI (alternativa più immediata al radar)
# ------------------------------------------------------------------------------
def create_mobile_factors_chart(best_hour: dict, target_mode: str = "Entrambi") -> go.Figure:
    """
    Stessi 6 fattori del radar ma in barre orizzontali, con i valori in una colonna a destra.
    Confrontare lunghezze è molto più rapido che confrontare vertici di un poligono: la barra
    più corta è subito "ciò che frena" quell'ora. Colore unico per modalità (verde / viola):
    la lunghezza porta già il valore, non serve ricolorare le barre.

    best_hour / target_mode: come in create_mobile_radar (accetta anche l'intero `sim`).
    """
    mode = _b4_norm_mode(target_mode)
    rec, note = _b4_resolve_hour(best_hour, mode)
    facts = _b4_factor_list(rec)
    if all(v is None for _, v in facts):
        return _b4_empty_figure("Fattori non disponibili per questa ora", height=120)

    color = B4_COL_TROPHY if mode == "Trophy" else B4_COL_BAI
    n = len(facts)
    names = [nm for nm, _ in facts]
    vals = [0.0 if v is None else v for _, v in facts]
    texts = ["n/d" if v is None else "%d" % int(round(v)) for _, v in facts]
    custom = ["n/d" if v is None else "%.0f su 100" % v for _, v in facts]

    left, right, top, bottom, slot = 100, 10, 44, 8, 30
    height = top + n * slot + bottom

    track = go.Bar(x=[100] * n, y=names, orientation="h",
                   marker=dict(color="rgba(255, 255, 255, 0.07)"),
                   hoverinfo="skip", showlegend=False)
    bar_kw = dict(x=vals, y=names, orientation="h",
                  customdata=custom, hovertemplate="<b>%{y}</b> · %{customdata}<extra></extra>",
                  showlegend=False)
    try:    # angoli arrotondati: disponibile solo nelle versioni recenti di Plotly
        bars = go.Bar(marker=dict(color=color, cornerradius=4), **bar_kw)
    except ValueError:
        bars = go.Bar(marker=dict(color=color), **bar_kw)
    # numeri in una colonna a destra, allineati: si confrontano senza inseguire la punta delle barre
    numbers = go.Scatter(x=[B4_BARS_XMAX] * n, y=names, mode="text", text=texts,
                         textposition="middle left", textfont=dict(size=13, color=B4_INK_1),
                         cliponaxis=False, hoverinfo="skip", showlegend=False)

    return go.Figure(
        data=[track, bars, numbers],
        layout=dict(
            template="plotly_dark", height=height,
            margin=dict(l=left, r=right, t=top, b=bottom, autoexpand=False),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family=B4_FONT, size=12, color=B4_INK_1),
            barmode="overlay", bargap=0.42, dragmode=False, showlegend=False, hovermode="closest",
            hoverlabel=dict(bgcolor="rgba(15, 18, 22, 0.96)", bordercolor="rgba(255, 255, 255, 0.18)",
                            font=dict(size=12, color=B4_INK_1, family=B4_FONT), align="left"),
            xaxis=dict(range=[0, B4_BARS_XMAX], visible=False, fixedrange=True, automargin=False),
            yaxis=dict(autorange="reversed", categoryorder="array", categoryarray=names, automargin=False,
                       tickfont=dict(size=12.5, color=B4_INK_1), ticks="outside", ticklen=8,
                       tickcolor="rgba(0, 0, 0, 0)", showgrid=False,
                       zeroline=False, showline=False, fixedrange=True),
            annotations=[dict(
                text=_b4_factor_header(rec, facts, "Fattori", note),
                xref="paper", yref="paper", x=0, y=1, xanchor="left", yanchor="top",
                xshift=-(left - 6), yshift=top - 4, align="left", showarrow=False,
                font=dict(size=13, color=B4_INK_1))]))


# ------------------------------------------------------------------------------
# CONTROLLO DEL CONTRATTO DATI (utile per i test di integrazione tra i blocchi)
# ------------------------------------------------------------------------------
B4_ROW_KEYS_REQUIRED = ("hour", "catch_rate", "trophy_rate")
B4_ROW_KEYS_OPTIONAL = (
    "time_label", "date_str", "water_temp_used", "water_temp", "wind", "pressure_delta",
    "depth_zone", "do_saturation_index", "s_temp", "s_press", "s_sol", "s_vento", "s_torb",
)


def check_block4_contract(sim):
    """
    Verifica che `sim` (o la sola lista timeline) contenga ciò che il Blocco 4 legge.
    Ritorna una lista di avvisi in italiano; lista vuota = tutto in ordine.
    Non solleva mai eccezioni: pensata per i test di integrazione tra Blocco 2 e Blocco 4.
    """
    rows = sim.get("timeline") if isinstance(sim, dict) else sim
    if not isinstance(rows, (list, tuple)) or not rows:
        return ["timeline assente o vuota: il grafico mostrerà solo un messaggio"]
    problems = []
    dict_rows = [r for r in rows if isinstance(r, dict)]
    if len(dict_rows) != len(rows):
        problems.append("%d righe del timeline non sono dizionari (ignorate)" % (len(rows) - len(dict_rows)))
    for key in B4_ROW_KEYS_REQUIRED:
        missing = sum(1 for r in dict_rows if r.get(key) is None)
        if missing:
            problems.append("chiave '%s' mancante in %d/%d righe (obbligatoria)" % (key, missing, len(dict_rows)))
    for key in B4_ROW_KEYS_OPTIONAL:
        if dict_rows and all(r.get(key) is None for r in dict_rows):
            problems.append("(opzionale) '%s' assente: il grafico ne omette la parte relativa" % key)
    if isinstance(sim, dict):
        for key in ("best_hour", "best_trophy_hour"):
            if not isinstance(sim.get(key), dict):
                problems.append("(opzionale) '%s' assente: il picco verrà ricalcolato dal timeline" % key)
    return problems
