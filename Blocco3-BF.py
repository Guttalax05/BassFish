# ==============================================================================
# MODULO 3: GENERATORE REPORT TATTICO STRATEGICO PRO V2 (COMPLETO 3A + 3B)
# ==============================================================================
class TacticalAdvisorV2:
    """
    Sistema esperto di livello Bassmaster Elite Series per la diagnostica posizionale,
    la cinetica biomeccanica di recupero, l'ingegneria del setup (canna/filo),
    la fisica ottica subacquea e la selezione chirurgica degli artificiali.
    Supporta il selettore di focus operativo ('Numeri', 'Trophy', 'Entrambi') e
    garantisce retrocompatibilità al 100% con tutte le versioni della UI.
    """

    # --------------------------------------------------------------------------
    # PARTE 3A: DIAGNOSTICA POSIZIONALE, CINETICA & SPETTRO OTTICO
    # --------------------------------------------------------------------------
    @staticmethod
    def analyze_hydro_biological_positioning(
        w_temp: float,
        macro_14d: float,
        micro_72h: float,
        do_idx: float,
        press_delta: float,
        press_12h: float,
        depth_zone: str,
        bio_state: str,
        water_level: str = "Stabile"
    ) -> dict:
        """
        1. DIAGNOSTICA FISIOLOGICA E POSIZIONAMENTO STRUTTURALE IDRO-BAROMETRICO
        Incrocia lo stato bio-energetico, il bilancio della vescica natatoria (3h x 12h),
        la tensione di ossigeno disciolto (do_idx) e l'idrometria (water_level) per
        mappare il posizionamento tridimensionale del Bass sulle strutture.
        """
        # --- A) Analisi Fisiologica: Vescica Natatoria (3h x 12h) & Ossigenazione ---
        if press_12h <= -1.8 and press_delta <= -0.6:
            baro_physio = (
                f"**Decompressione Pre-Frontale Ciclonica (Δ3h {press_delta:+.1f} / Δ12h {press_12h:+.1f} hPa):** "
                "L'espansione progressiva della vescica natatoria riduce il peso idrostatico percepito dal pesce, "
                "sbloccando lo stacco dal fondo e attivando una finestra di iper-aggressività predatoria prima del fronte."
            )
        elif press_delta >= 0.8 or press_12h >= 2.5:
            baro_physio = (
                f"**Compressione Post-Frontale Acuta (Δ3h {press_delta:+.1f} / Δ12h {press_12h:+.1f} hPa):** "
                "Il rapido innalzamento barometrico comprime la vescica natatoria, costringendo il Bass a compensare "
                "l'assetto: i pesci o si schiacciano sul substrato duro nel cuore delle cover o si sospendono immobili "
                "a mezz'acqua sui salti batimetrici con muscolatura boccale serrata (*lockjaw*)."
            )
        elif press_delta < -0.4 and press_12h > 0.5:
            baro_physio = (
                f"**Micro-Oscillazione Barometrica (Δ3h {press_delta:+.1f} su trend 12h {press_12h:+.1f} hPa):** "
                "Breve flessione depressiva temporanea che apre una micro-finestra opportunistica di 60-90 minuti "
                "per i pesci già posizionati sulle strutture primarie."
            )
        else:
            baro_physio = (
                f"**Equilibrio Idrostatico Barometrico (Δ3h {press_delta:+.1f} / Δ12h {press_12h:+.1f} hPa):** "
                "Vescica natatoria stabilizzata; gli spostamenti verticali lungo la colonna d'acqua non comportano "
                "stress pressorio e seguono fedelmente il fotoperiodo e la disponibilità di foraggio."
            )

        # Diagnostica Respiratoria ed Ematochimica (Ossigeno Disciolto vs Temperatura)
        if w_temp > 24.0 and do_idx < 0.58:
            do_physio = (
                f"⚠️ **Stress Ipossico Critico (Acqua {w_temp}°C | Indice DO {do_idx:.2f}):** "
                "La ridotta solubilità dell'O2 ad alte temperature genera acidosi lattica precoce durante gli scatti. "
                "**Ordine Tattico:** Abbandona le baie stagnanti. Cerca esclusivamente ossigeno disciolto: "
                "immissari d'acqua più fresca, sponde sottovento battute dall'onda (*wind-blown banks*), "
                "il cuore ombreggiato dei tappeti di macrofite fotosintetiche (*Ceratophyllum/Myriophyllum*) "
                "o la fascia di rottura del **termoclino**."
            )
        elif w_temp > 23.5 and do_idx >= 0.70:
            do_physio = (
                f"💨 **Compensazione Eolica Estiva (Acqua {w_temp}°C | Indice DO {do_idx:.2f}):** "
                "Nonostante il regime termico estivo, il rimescolamento superficiale mantiene alta la saturazione di O2, "
                "sostenendo il metabolismo aerobico anche fuori dalle ombre fitte."
            )
        elif w_temp < 10.5:
            do_physio = (
                f"❄️ **Ipossia Tissutale Assente ma Bradicardia Enzimatica (Acqua {w_temp}°C | DO {do_idx:.2f}):** "
                "Saturazione di ossigeno massima per la legge di Henry, ma la viscosità ematica e il rallentamento "
                "degli enzimi digestivi impongono il minimo dispendio calorico."
            )
        else:
            do_physio = (
                f"✅ **Omeostasi Aerobica Ottimale (Acqua {w_temp}°C | Indice DO {do_idx:.2f}):** "
                "Piena efficienza branchiale e rapido smaltimento dell'acido lattico post-attacco."
            )

        condizione_fisiologica = (
            f"🧬 **Stato Biologico Rilevato:** *{bio_state}*\n"
            f"- {baro_physio}\n"
            f"- {do_physio}"
        )

        # --- B) Geometria di Posizionamento & Dinamica Idrometrica (Water Level) ---
        match water_level:
            case "In Crescita":
                hydro_positioning = (
                    "🌊 **Dinamica di Flooding (Livello in Crescita — Vettore Ultra-Shallow):** "
                    "L'innalzamento idrometrico allaga sponde asciutte, erba terrestre, radici di salice e canneti interni, "
                    "rilasciando nutrienti, lombrichi e insetti. Il Bass risponde per istinto condizionato **seguendo l'acqua che sale**: "
                    "ignora le strutture al largo e batti il **bordo interno delle nuove cover appena sommerse** "
                    "(anche in 30-60 cm d'acqua), specialmente negli angoli riparati dalla corrente principale."
                )
            case "In Calo":
                hydro_positioning = (
                    "📉 **Panico Idrometrico (Livello in Calo — Ritiro su Drop-off e Drenaggi):** "
                    "Quando il livello scende, l'istinto di sopravvivenza spinge immediatamente il Bass ad abbandonare i flat bassi "
                    "e il fondo delle baie per non restare intrappolato. I pesci **scivolano all'esterno delle cover**, "
                    "posizionandosi sospesi sulle **punte primarie, sui primi drop-off verticali (scalini da 1.5m a 3.5m)** "
                    "e all'imboccatura dei **canali di drenaggio** dove il pesce foraggio è costretto a defluire."
                )
            case _:  # "Stabile" o "Non specificato"
                if micro_72h <= -0.8 and w_temp < 21.0:
                    hydro_positioning = (
                        "⚓ **Posizionamento da Shock Termico (Livello Stabile + Δ72h Negativo):** "
                        "Con livello fermo ma brusco raffreddamento recente, i pesci disertano le sponde di caccia "
                        "e si ancorano sul **lato sottovento dei drop-off**, dentro legnaie sommerse compatte o a ridosso "
                        "di sassaie verticali che rilasciano il calore latente accumulato."
                    )
                else:
                    hydro_positioning = (
                        "🎯 **Posizionamento Strutturale Canonico (Livello Stabile):** "
                        "Assenza di stress idrometrico; i pesci presidiano le rotte di migrazione standard tra le zone di "
                        "riparo (*holding cover*) e i *feeding flat* adiacenti."
                    )

        approccio_posizionale = (
            f"📏 **Strike Zone Batimetrica Primaria:** `{depth_zone}`\n"
            f"- {hydro_positioning}\n"
            f"- **Vettore Stagionale (Δ14gg {macro_14d:+.1f}°C | Δ72h {micro_72h:+.1f}°C):** "
            + (
                "Punta alle **sponde Nord/Nord-Ovest** (massima esposizione all'irraggiamento solare meridiano) e alle rocce scure."
                if w_temp < 14.5
                else "Lavora i **cambi di pendenza bruschi, i vertici delle punte ventose** e i margini d'ombra netta delle cover."
            )
        )

        return {
            "condizione_fisiologica": condizione_fisiologica,
            "approccio_posizionale": approccio_posizionale
        }

    @staticmethod
    def compute_retrieve_kinetics_and_gear(
        w_temp: float,
        micro_72h: float,
        press_delta: float,
        torbidita: str,
        wind: float,
        fishing_pressure: str = "Media",
        water_level: str = "Stabile"
    ) -> dict:
        """
        2. CINETICA BIOMECCANICA DI RECUPERO & INGEGNERIA DEL SETUP (CANNA / FILO)
        Determina la velocità angolare di recupero, i tempi di pausa (deadsticking),
        la deflessione meccanica e calibra il sistema canna/lenza in funzione della
        Pressione di Pesca (Anti-Conditioning vs Power Fishing).
        """
        clarity_eff = "Velata" if ("Velata" in torbidita or torbidita == "Non specificato") else torbidita

        # --- A) Cinetica di Presentazione (Velocità, Cadenza, Pause) ---
        if w_temp < 9.8 or (w_temp < 15.0 and micro_72h <= -0.9):
            base_kinetics = (
                "**Cinetica Inerziale / Deadsticking Estremo:** "
                "La velocità di contrazione delle fibre muscolari bianche del Bass è ridotta al minimo.\n"
                "- *Gomma / Jig sul fondo:* Trascinamento millimetrico (*bottom dragging*) con la sola pressione della canna "
                "(spostamenti di 5-10 cm), seguito da **pause statiche di 6 - 12 secondi** a filo semi-teso.\n"
                "- *Hardbait Sospese (Jerkbait):* Sequenza `Twitch-Twitch-Pause` con colpi di vetta secchi ma corti su filo in bando "
                "(*slack line*) per far spanciare l'esca sul posto senza farla avanzare, attendendo **8 - 15 secondi** tra le serie."
            )
        elif 9.8 <= w_temp < 15.5:
            base_kinetics = (
                "**Cinetica Cadenzata a Contatto (Slow-Rolling & Deflection):** "
                "Il pesce insegue solo se l'esca interseca la sua corsia a velocità sostenibile.\n"
                "- *Lame / Spinnerbait / Chatterbait:* Recupero in **Slow-Rolling** radente il fondo o il bordo superiore degli erbai, "
                "mantenendo la rotazione del mulinello appena sopra la soglia di stallo della paletta.\n"
                "- *Crankbait:* Ricerca sistematica dell'**urto meccanico (*Deflection*)** contro rocce o rami; "
                "appena la paletta sbatte, **blocca la manovella per 1.5 secondi** permettendo il galleggiamento lento (*back-up*)."
            )
        elif 15.5 <= w_temp <= 23.8:
            if press_delta <= -0.5 or wind >= 10.0:
                base_kinetics = (
                    "**Cinetica Reattiva ad Alta Velocità (Burning & Erratic Stop):** "
                    "Metabolismo al picco e finestra ambientale favorevole: togli al predatore il tempo di ispezionare l'inganno.\n"
                    "- *Reazione:* Recupero sostenuto a canna bassa alternato a **4-5 giri di manovella brucianti (*Burn*)** "
                    "e stop improvviso di 0.5 secondi per scatenare l'attacco d'istinto.\n"
                    "- *Pitching nelle Cover:* Presentazione verticale veloce; se lo strike non avviene nei **primi 3 secondi di caduta** "
                    "(*on the fall*) o ai primi 2 inviti sul fondo, recupera subito ed effettua il lancio successivo."
                )
            else:
                base_kinetics = (
                    "**Cinetica Ritmica e Finesse-Swimming (Glide & Shake):**\n"
                    "- *Softbait / Swimbait:* Nuoto lineare e fluido a mezz'acqua (*steady swimming*) o caduta libera *weightless* "
                    "davanti ai margini d'ombra, imprimendo micro-vibrazioni di vetta (*shaking*) a 3-4 Hz durante la discesa."
                )
        else:  # Acqua > 23.8°C (Pattern Estivo Bipolare)
            base_kinetics = (
                "**Cinetica Bipolare Estiva (Vertical Drop Diurno vs High-Cadence Crepuscolare):**\n"
                "- *Ore Centrali (Luce Alta):* Azzera lo spostamento orizzontale; buca la cover in verticale (*Punching / Drop*) "
                "perché il Bass accalorato attacca solo per riflesso difensivo se l'esca gli cade **a meno di 20 cm dal muso**.\n"
                "- *Alba / Tramonto / Notte:* Cadenza ritmica continua in superficie (*Walk-the-Dog* serrato o scia costante)."
            )

        # --- B) Filtro Pressione di Pesca (Protocollo Anti-Conditioning vs Power) ---
        match fishing_pressure:
            case "Alta":
                pressure_protocol = (
                    "🔇 **Protocollo Anti-Conditioning (Alta Pressione di Pesca):** "
                    "In acque battute i Bass associano i *rattle* metallici ad alta frequenza e gli splash pesanti al pericolo. "
                    "**Regole d'ingaggio:** 1) Usa esclusivamente hardbait **Silent** (senza sfere sonore) o *One-Knocker* sordi in tungsteno; "
                    "2) Arretra la posizione di lancio di almeno 4-5 metri facendo atterrare l'esca *oltre* il bersaglio per poi portarla "
                    "nella strike zone in modo furtivo; 3) Sostituisci i saltelli bruschi sul fondo con uno **scivolamento continuo (*swimming/gliding*)**."
                )
            case "Bassa":
                pressure_protocol = (
                    "💥 **Protocollo Power Fishing (Bassa Pressione di Pesca):** "
                    "Pesci non condizionati: massimizza la copertura d'acqua (*water coverage*). Usa artificiali ad **alto impatto acustico e vibratorio** "
                    "(camere rattle multiple, palette Colorado/Tandem, profili voluminosi) per richiamare i predatori anche da 3-4 metri di distanza."
                )
            case _:  # "Media"
                pressure_protocol = (
                    "⚖️ **Protocollo Bilanciato (Pressione di Pesca Media):** "
                    "Alterna una prima passata veloce con esche di ricerca (*searchbait*) sugli spot primari a una seconda passata "
                    "chirurgica di rifinitura (*clean-up bait* in gomma silenziosa) sulle cover più promettenti."
                )

        # --- C) Ingegneria del Setup: Azione Canna, Moduli in Grafite/Composito & Fisica del Filo ---
        if clarity_eff == "Limpida" and (wind < 8.0 or fishing_pressure == "Alta"):
            gear_setup = (
                "🎣 **Setup Spinning / BFS Finesse (Massima Discrezione Ottica):**\n"
                "- **Canna:** 6'8\" - 7'1\" azione *Fast / Extra-Fast* con vetta sensibile (*Solid Tip* o tubolare alto modulo) potenza ML o L.\n"
                "- **Lenza:** Madre in trecciato PE 0.6 - 0.8 (10-14 lb) collegata tramite nodo *FG* o *Alberto* a un lungo terminale (2.5 - 3.5 m) "
                "oppure **Fluorocarbon 100% in bobina da 5 - 8 lb (0.18 - 0.23 mm)** per azzerare la rifrazione luminosa e garantire l'affondamento dell'esca."
            )
        elif clarity_eff in ["Torbida", "Fangosa"] or water_level == "In Crescita":
            gear_setup = (
                "🎣 **Setup Heavy Cover & Reaction (Forza Bruta e Sensibilità in Acqua Sporca):**\n"
                "- **Canna:** Casting 7'0\" - 7'4\" potenza *Medium-Heavy (MH)* o *Heavy (H)* azione *Fast* per Jig/Texas nelle cover allagate; "
                "7'2\" *Moderate-Fast* (in fibra di vetro/composito) per Chatterbait e Squarebill.\n"
                "- **Lenza:** **Fluorocarbon ad alta resistenza all'abrasione 16 - 20 lb (0.33 - 0.37 mm)** per contatto diretto coi legni, "
                "oppure **Trecciato 8 capi diretto 40 - 65 lb** su erbai fitti e rane (in acqua torbida il pesce non vede il trecciato)."
            )
        else:
            downsize_note = " (scendi di 2 lb sul diametro per l'alta pressione di pesca)" if fishing_pressure == "Alta" else ""
            gear_setup = (
                f"🎣 **Setup Versatile da Torneo (Acqua {clarity_eff} / Vento {wind} km/h):**\n"
                "- **Combo 1 (Moving Baits & Reazione):** Canna Casting 7'0\" - 7'2\" *Moderate-Fast* (assorbe l'onda d'urto sulle ancorette "
                "evitando di slamare il pesce in salto) con **Fluorocarbon 12 - 14 lb (0.28 - 0.31 mm)**" + downsize_note + ".\n"
                "- **Combo 2 (Bottom Contact / Jig & Rig):** Canna Casting 7'1\" - 7'3\" *Fast* alto modulo per trasmettere le micro-aspirazioni "
                "sul fondo con **Fluorocarbon 14 - 16 lb (0.31 - 0.33 mm)**.\n"
                "- *Nota Topwater:* Se peschi a galla nei picchi crepuscolari, usa **Nylon (Monofilo) 12 - 15 lb** o Trecciato (il Fluorocarbon affonda e rovina il nuoto WTD!)."
            )

        return {
            "recupero_cinetica": f"{base_kinetics}\n\n{pressure_protocol}",
            "gear_e_line_setup": gear_setup
        }

    @staticmethod
    def select_chromatic_spectrum(
        torbidita: str,
        clouds: int,
        radiation: int,
        hour: int,
        alba: float,
        tramonto: float,
        forage_base: str = "Misto"
    ) -> str:
        """
        3. FISICA OTTICA SUBACQUEA, SPETTRO CROMATICO & MIMETISMO FORAGGIO
        Seleziona i pattern cromatici ufficiali da torneo in base all'assorbimento selettivo
        della luce (torbidità + W/m²), all'angolo zenitale (controluce crepuscolare) e alla preda.
        """
        clarity_eff = "Velata" if ("Velata" in torbidita or torbidita == "Non specificato") else torbidita
        h_float = float(hour)
        is_low_light = (abs(h_float - alba) <= 1.5) or (abs(h_float - tramonto) <= 1.5) or (radiation < 120)

        # --- A) Selezione Primaria per Fisica Ottica (Torbidità x Luce) ---
        match clarity_eff:
            case "Limpida":
                if radiation >= 480 and clouds < 35:
                    optical_core = (
                        "☀️ **Ottica Acqua Limpida + Alta Radiazione (Penetrazione Fotonica Massima):** "
                        "I colori opachi o pastello appaiono innaturali e finti. Sfrutta la **traslucenza interna (*Ghost/Clear*)** "
                        "e i riflessi olografici che lasciano attraversare il raggio solare:\n"
                        "- **Softbait & Jig:** `Watermelon Seed`, `Watermelon Red Flake`, `Green Pumpkin Magic`, `Smoke Shad`.\n"
                        "- **Hardbait & Swimbait:** `Ghost Minnow`, `Table Rock Shad`, `Ayu`, `Pro Blue`, `Wakasaki` (o `Sexy Chrome` se c'è vento)."
                    )
                else:
                    optical_core = (
                        "🌥️ **Ottica Acqua Limpida + Luce Diffusa / Crepuscolo:** "
                        "In assenza di abbagliamento diretto, passa da livree trasparenti a **toni naturali semi-solidi e perlati** "
                        "che definiscano il profilo senza allarmare il pesce:\n"
                        "- **Softbait & Jig:** `Green Pumpkin`, `Sungill`, `Cinnamon Blue Flake`, `Baby Bass`.\n"
                        "- **Hardbait & Swimbait:** `Matte Shad`, `Ghost Pearl`, `Tennessee Shad`, `Natural Perch`."
                    )

            case "Velata":
                optical_core = (
                    "🍵 **Ottica Acqua Velata / Stained (Diffusione del Particolato & Rifrazione Media):** "
                    "Il fitoplancton e i sedimenti leggeri filtrano le lunghezze d'onda corte: servono **colori solidi a doppio tono** "
                    "e flash metallici/chartreuse che taglino la foschia subacquea:\n"
                    "- **Softbait & Jig:** `Green Pumpkin / Chartreuse Tip`, `PB&J (Peanut Butter & Jelly)`, `Bama Bug`, `Okeechobee Craw`.\n"
                    "- **Hardbait & Lame:** `Sexy Shad`, `Chartreuse & White`, `Pearl White`, `Red Craw / Spring Craw`, palette **Nickel + Gold**."
                )

            case _:  # "Torbida" o "Fangosa"
                optical_core = (
                    f"🌑 **Ottica Acqua {clarity_eff} (Estinzione Fotonica & Silhouette Nera/Fluorescente):** "
                    "Visibilità inferiore a 30 cm: la luce viene assorbita nei primi centimetri. Funzionano solo due estremi fisici: "
                    "il **contrasto negativo assoluto** (che staglia una sagoma nera netta contro il riverbero superficiale) "
                    "o l'**emissione ad alta visibilità** per lo strike a bruciapelo:\n"
                    "- **Softbait & Jig:** **`Black & Blue Flake`** (scelta #1 assoluta), `Junebug`, `Black Neon`, `Sapphire Blue`.\n"
                    "- **Hardbait & Lame:** **`Firetiger`**, **`Hot Mustard / Chartreuse Black Back`**, **`Bone (Bianco Solido Opaco)`** "
                    "e palette verniciate **Chartreuse o Rame/Oro (*Colorado Gold*)**."
                )

        # --- B) Adattamento Specifico alla Preda Prevalente (Forage Base) ---
        if "Gamber" in forage_base or "Crostacei" in forage_base or "Craw" in forage_base or "Gobbio" in forage_base:
            forage_palette = (
                "🦞 **Mimetismo Prevalente Gambero / Gobbio (Craw & Goby Pattern):** "
                "Includi accenti ventrali arancio/rossi o chele bluastre: privilegia `Molting Craw`, `Green Pumpkin Orange`, "
                "`Brown/Purple (PB&J)`, `Dark Cinnamon` e `Bruised Okeechobee`."
            )
        elif "Pesce Foraggio" in forage_base or "Shad" in forage_base or "Alborella" in forage_base:
            forage_palette = (
                "🐟 **Mimetismo Prevalente Pesce Foraggio (Baitfish / Shad Pattern):** "
                "Punta sul contrasto dorso grigio-verde / ventre bianco perla con punto d'attacco laterale: privilegia `Sexy Shad`, "
                "`Threadfin Shad`, `Ghost Ayu`, `Smelt` e `White/Silver Flake`."
            )
        elif "Rane" in forage_base or "Insetti" in forage_base or "Persico" in forage_base or "Bluegill" in forage_base:
            forage_palette = (
                "🐸 **Mimetismo Prevalente Rane / Bluegill / Shallow:** "
                "Inserisci riflessi verde oliva, pancia gialla/arancio e punte chartreuse: privilegia `Bullfrog`, `Green Pumpkin Blue/Chartreuse`, "
                "`Bluegill`, `Tilapia Magic` e `Black/Yellow`."
            )
        else:  # "Misto"
            forage_palette = (
                "🔄 **Regola di Rotazione Foraggio Misto:** "
                "Usa livree **Shad/Bianco/Ayu** sulle esche che lavorano staccate dal fondo (a mezz'acqua) e livree "
                "**Green Pumpkin / Black & Blue / PB&J** sulle presentazioni a contatto col substrato."
            )

        # --- C) Nota Angolo Zenitale (Controluce Alba/Tramonto) ---
        zenith_tip = (
            "\n- 🌅 **Fattore Controluce Attivo (Alba/Tramonto/Bassa Luce):** Dal basso verso l'alto un'esca chiara si confonde "
            "col cielo grigio; se peschi a galla o sub-surface in questa finestra, una pancia **`Bone` (Bianco Opaco)** o **`Nera Solida`** "
            "offre al Bass il bersaglio più nitido in assoluto."
            if is_low_light else ""
        )

        return f"{optical_core}\n\n- {forage_palette}{zenith_tip}"

    # --------------------------------------------------------------------------
    # PARTE 3B: MATRICE BIOMECCANICA ESCHE, FOCUS MODE & ORCHESTRATORE
    # --------------------------------------------------------------------------
    @staticmethod
    def build_biomechanical_lure_matrix(
        w_temp: float,
        micro_72h: float,
        wind: float,
        radiation: int,
        torbidita: str,
        trophy_rate: float,
        depth_zone: str,
        forage_base: str = "Misto",
        fishing_pressure: str = "Media",
        water_level: str = "Stabile",
        target_mode: str = "Entrambi",
        trophy_hour_label: str = None,
        trophy_depth_zone: str = None
    ) -> dict:
        """
        4. MATRICE BIOMECCANICA DELLE ESCHE E STRATEGIA DEDICATA BIG BASS (> 2.0 KG)
        Implementa:
        - Sblocco reattivo in Pre-Frega tra 9.8°C e 11.8°C quando micro_72h >= 0.3 (warming trend).
        - Selettore di focus operativo ('Numeri', 'Trophy', 'Entrambi') con coordinate orarie
          e batimetriche dedicate per il picco Trophy.
        """
        clarity_eff = "Velata" if ("Velata" in torbidita or torbidita == "Non specificato") else torbidita
        is_high_pressure = (fishing_pressure == "Alta")

        # PERFEZIONAMENTO 2: Soglia is_cold_shock dinamica in Pre-Frega (9.8°C - 11.8°C)
        # Sotto i 9.8°C è sempre regime freddo/letargico.
        # Tra 9.8°C e 11.8°C, se siamo in riscaldamento (micro_72h >= 0.3) e la pressione di pesca non è Alta,
        # sblocchiamo le presentazioni di movimento lento (Slow-Rolling, Crankbait, Jig) invece di forzare il Finesse!
        is_warming_prespawn_window = (9.8 <= w_temp <= 11.8) and (micro_72h >= 0.3) and (not is_high_pressure)
        is_cold_shock = (
            (w_temp < 9.8)
            or (9.8 <= w_temp <= 11.8 and not is_warming_prespawn_window)
            or (micro_72h <= -0.9 and w_temp < 21.5)
        )

        # Nota diagnostica se siamo nella finestra di sblocco reattivo tra 9.8°C e 11.8°C
        prespawn_unlock_note = (
            "\n- 🔥 **Sblocco Reattivo Pre-Frega Attivo (9.8°C - 11.8°C con Δ72h Positivo):** "
            "L'impulso caldo su acqua fresca spinge i pesci a intercettare esche di movimento lento (*Slow-Rolling* e *Deflection*)!"
            if is_warming_prespawn_window else ""
        )

        # --- 1. SELEZIONE BASE PER FORAGGIO E REGIME AMBIENTALE ---
        if "Gamber" in forage_base or "Crostacei" in forage_base or "Gobbio" in forage_base:
            if is_cold_shock or is_high_pressure:
                primarie = (
                    "🦞 **Approccio Primario (Benthos Finesse & Tight-Wobble):**\n"
                    "- **Ned Rig & Neko Rig (Gambero/Gobide):** Innesca un piccolo *Craw* galleggiante in TPE su testina a fungo (1/10 - 1/6 oz) "
                    "o un *Creature* compatto a Neko Rig; le chele alzate in posizione difensiva durante le lunghe pause sbloccano i pesci apatici.\n"
                    "- **Finesse Football Jig (1/4 - 3/8 oz):** Gonnellino sfoltito (*living rubber* che respira anche da fermo) + *Chunk/Baby Craw* minimale, "
                    "trascinato lentamente sui sassi.\n"
                    "- **Flat-Side / Shad Crankbait:** Nuoto strettissimo (*tight action*) che va a sbattere sulle rocce del primo scalino."
                )
            else:
                primarie = (
                    "🦞 **Approccio Primario (Heavy Bottom Contact & Deflection):**\n"
                    "- **Casting / Structure Jig (3/8 - 1/2 oz):** Accoppiato a un trailer *Craw* ad alte vibrazioni (*flapping claws*), "
                    "lanciato a *Pitching* al piede dei legni o fatto saltellare lungo i drop-off rocciosi.\n"
                    "- **Texas Rig / Free Rig (Piombo in Tungsteno 7 - 10g):** Con *Creature* o *Craw* da 3.5\" - 4\"; il *Free Rig* permette "
                    "all'imitazione di gambero di planare libera in orizzontale dopo che il piombo ha toccato il fondo.\n"
                    "- **Squarebill / Medium Diving Crankbait:** Fatto letteralmente **arare sul fondale** (*bottom digging*) per alzare nuvolette di sedimento."
                    + prespawn_unlock_note
                )
            secondarie = (
                "🔄 **Backup Tattico (Crostacei):** Passa a uno **Shaky Head** con verme dritto/piccola creatura lavorato sul posto "
                "oppure a una **Chatterbait compatta** recuperata in *slow-rolling* a stretto contatto col substrato."
            )

        elif "Pesce Foraggio" in forage_base or "Alborella" in forage_base or "Shad" in forage_base:
            if is_cold_shock or is_high_pressure:
                primarie = (
                    "🐟 **Approccio Primario (Suspending & Finesse Pelagico):**\n"
                    "- **Suspending Jerkbait (110 mm / Deep 110):** L'arma letale per pesci sospesi o sotto shock termico; resta immobile "
                    "nella corsia visiva del Bass durante le pause di 8-12 secondi senza né salire né affondare.\n"
                    "- **Drop Shot & Damiki Rig (Mid-Strolling):** Innesca uno *Shad tail* sottile o un *Minnow* senza paletta (3\" - 4\") "
                    "facendolo vibrare orizzontalmente a mezz'acqua sopra i banchi sospesi.\n"
                    "- **Soft Jerkbait (Fluke) / Spybait:** Presentazione totalmente silenziosa in caduta planante o recupero lineare."
                )
            else:
                primarie = (
                    "🐟 **Approccio Primario (High-Speed Baitfish Reaction):**\n"
                    "- **Spinnerbait (Doppia Willow in acqua chiara / Tandem in acqua velata):** Recuperato a cadenza regolare appena sotto "
                    "il pelo dell'acqua o in *slow-rolling* lungo i bordi dei canneti battuti dal vento.\n"
                    "- **Soft Swimbait (Paddle-Tail 3.8\" - 4.8\"):** Innescata su testina piombata o amo *weighted swimbait hook* (1/4 oz), "
                    "fatta nuotare lungo le punte e i corridoi degli erbai.\n"
                    "- **Chatterbait (Bladed Jig) + Trailer Pintail:** Massima vibrazione su linea laterale senza l'ingombro della doppia pala."
                    + prespawn_unlock_note
                )
            secondarie = (
                "🔄 **Backup Tattico (Baitfish):** Alterna un **Lipless Crankbait** (recuperato a *yo-yo* sui margini profondi) "
                "o un **Underspin** (testina piombata con micro-paletta Willow sotto la pancia) per sbloccare i pesci che inseguono senza abboccare."
            )

        elif "Rane" in forage_base or "Insetti" in forage_base or "Shallow" in forage_base:
            if is_cold_shock or is_high_pressure:
                primarie = (
                    "🐸 **Approccio Primario (Sub-Surface Stealth & Cover Finesse):**\n"
                    "- **Wacky Rig Weightless / Neko Rig (Senko 4\" - 5\"):** Lanciato in *Skipping* fin sotto i rami bassi, i pontili "
                    "e le fronde sporgenti; la caduta orizzontale auto-vibrante vince qualsiasi diffidenza.\n"
                    "- **Finesse Jig con Skirt Tagliato (Spider Jig):** Presentato silenziosamente sui bordi esterni delle ninfee o dei canneti.\n"
                    "- **Bug / Piccola Creatura Galleggiante:** Lavorata a galla con micro-vibrazioni e lunghi stop sotto gli alberi."
                )
            else:
                primarie = (
                    "🐸 **Approccio Primario (Heavy Cover & Topwater Ambush):**\n"
                    "- **Hollow Body Frog (Rana in gomma cava):** Lavorata a *Walk-the-Dog* sopra i tappeti di vegetazione emersa "
                    "o negli spazi d'acqua libera (*pockets*) dentro il canneto.\n"
                    "- **Pitching / Flipping con Creature (Texas Pegged 10 - 21g):** Per bucare fisicamente le coperture vegetali e i rami intrecciati.\n"
                    "- **Walking the Dog / Popper / Buzzbait:** Per battere rapidamente i primi 50 cm d'acqua lungo le sponde ombreggiate."
                    + prespawn_unlock_note
                )
            secondarie = (
                "🔄 **Backup Tattico (Shallow):** Se il pesce scoppia sulla rana a vuoto senza restare allamato, rilancia immediatamente "
                "nello stesso buco un **Senko weightless a Texas** o un **Fluke** come *follow-up bait*!"
            )

        else:
            # Pattern "Misto" (Auto-adattivo completo)
            if is_cold_shock or (clarity_eff == "Limpida" and wind < 7.0 and not is_warming_prespawn_window) or is_high_pressure:
                primarie = (
                    "🎯 **Approccio Primario Auto-Adattivo (Finesse & Suspending Control):**\n"
                    "- **Colonna d'Acqua:** *Suspending Jerkbait 110mm* (se c'è un minimo d'onda) oppure *Soft Jerkbait (Fluke)* / *Mid-Strolling*.\n"
                    "- **Contatto col Fondo:** *Neko Rig* o *Drop Shot* sui salti batimetrici e *Finesse Jig (5-7g)* vicino ai ripari.\n"
                    "- **Sponda / Ombre:** *Wacky Rig Weightless* lanciato a *Skipping* nel cuore delle ombre."
                )
                secondarie = (
                    "🔄 **Backup di Ricerca:** *Flat-Side Crankbait* silenzioso o *Soft Swimbait* da 3.5\" recuperata lentamente a ridosso del primo scalino."
                )
            elif clarity_eff in ["Torbida", "Fangosa"] or wind >= 10.0 or is_warming_prespawn_window:
                primarie = (
                    "🎯 **Approccio Primario Auto-Adattivo (Power Reaction & Linea Laterale):**\n"
                    "- **Ricerca Orizzontale:** *Chatterbait (3/8 - 1/2 oz)* e *Spinnerbait* (Colorado/Tandem in acqua scura, Doppia Willow in acqua chiara ventosa).\n"
                    "- **Urto Strutturale:** *Squarebill / Flat-Side Crankbait* fatto rimbalzare contro sassi e legni sommersi (*Deflection*).\n"
                    "- **Cover Pesante:** *Casting Jig (3/8 - 1/2 oz)* con trailer *Craw* voluminoso."
                    + prespawn_unlock_note
                )
                secondarie = (
                    "🔄 **Backup di Rifinitura:** *Texas Rig* (piombo 7-10g) con *Creature/Ribbon Tail Worm* passato lentamente dove hai avuto tocchi sulle esche di reazione."
                )
            else:
                primarie = (
                    "🎯 **Approccio Primario Auto-Adattivo (All-Round Tournament Mix):**\n"
                    "- **Ricerca Attiva:** *Soft Swimbait (4\")* su amo piombato o *Medium Crankbait* lungo le punte e i margini degli erbai.\n"
                    "- **Struttura & Cover:** *Casting Jig (3/8 oz)* o *Texas Rig* lanciati a *Pitching* sugli ostacoli visibili.\n"
                    "- **Finestra Crepuscolare:** *Walking the Dog* o *Popper* nei momenti di cambio luce."
                )
                secondarie = (
                    "🔄 **Backup Finesse:** *Ned Rig* o *Wacky Rig* per insistere sulle postazioni primarie dopo il passaggio con le esche veloci."
                )

        # --- 2. MODIFICATORE IDROMETRICO OBBLIGATORIO (Water Level Override) ---
        if water_level == "In Crescita":
            hydro_lure_mod = (
                "\n\n⬆️ **Override Acqua in Crescita (Flooding):** Concentra l'80% dei lanci sul **Flipping/Pitching** "
                "(Jig o Texas con piombo bloccato da *stopper*) dentro i cespugli appena allagati e fai scorrere una **Chatterbait / Spinnerbait** "
                "tra i corridoi dell'erba terrestre sommersa."
            )
        elif water_level == "In Calo":
            hydro_lure_mod = (
                "\n\n⬇️ **Override Acqua in Calo (Drawdown):** Abbandona le esche da riva! Monta un **Carolina Rig**, "
                "un **Football Jig**, un **Deep/Medium Crankbait** o un **Drop Shot** e lavora dall'esterno verso l'interno "
                "sui primi *drop-off* e sulle punte dove i pesci si sono ritirati."
            )
        else:
            hydro_lure_mod = ""

        # --- 3. STRATEGIA DEDICATA "TROPHY BIG BASS" (Esemplari > 2.0 kg) ---
        t_depth = trophy_depth_zone if trophy_depth_zone else depth_zone
        t_hour_str = f"Ore {trophy_hour_label} | " if trophy_hour_label else ""

        if w_temp < 15.0:
            trophy_lure = (
                "**Glide Bait / Swimbait Snodata (160 - 180 mm) o Jerkbait Profondo + Jig da 1/2 oz:** "
                "Le grandi femmine in acqua fredda/fresca non sprecano energie per prede minuscole; vogliono un **unico boccone ad alto valore calorico**."
            )
            trophy_spot = "il primo salto di profondità (*drop-off* da 2m a 4.5m) adiacente alle baie esposte a Nord o i grandi alberi sommersi isolati"
        elif 15.0 <= w_temp <= 23.5:
            trophy_lure = (
                "**Soft Swimbait Mag-Style (6\" - 7\" tipo Magdraft) / Glide Bait o Jig da 1/2 - 3/4 oz con Grosso Trailer Craw:** "
                "Sfrutta l'aggressività territoriale delle femmine dominanti presentando un profilo importante vicino ai rifugi d'imboscata."
            )
            trophy_spot = "i vertici delle punte secondarie battute dal vento, i margini esterni dei canneti profondi e gli angoli più bui dei pontili"
        else:  # Acqua > 23.5°C (Estate)
            trophy_lure = (
                "**Texas / Carolina con Big Ribbon-Tail Worm (7\" - 10\"), Punching Rig (1 oz+) o Grossa Rana / Wakebait all'Alba:** "
                "Col caldo i pesci sopra i 2 kg evitano la luce diretta e si alimentano o nel cuore più fresco dei tappeti d'erba o nelle finestre di buio."
            )
            trophy_spot = "le zone a ridosso del termoclino (3.5m+), le sorgenti/immissari ossigenati e le cover vegetali più spesse"

        trophy_strategy = (
            f"👑 **Strategia Big Bass (> 2.0 kg | {t_hour_str}Picco Trophy: {trophy_rate}%):**\n"
            f"- **Artificiale da Trofeo:** {trophy_lure}\n"
            f"- **Target Strutturale Esatto:** Lancia su **{trophy_spot}** (Strike Zone Trophy: `{t_depth}`). "
            + (
                "Con alta pressione di pesca, effettua lanci lunghissimi e recupera l'esca da Big a velocità lentissima e costante senza mai fermarla bruscamente."
                if is_high_pressure
                else "Insisti sui 2-3 spot strutturali migliori esattamente nei 45 minuti a cavallo del picco Trophy."
            )
        )

        # PERFEZIONAMENTO 1: Adattamento in base al target_mode ("Numeri", "Trophy", "Entrambi")
        if target_mode == "Trophy":
            # In modalità Trophy pura, la strategia da Big Bass diventa l'approccio primario assoluto!
            return {
                "esche_primarie": f"{trophy_strategy}{hydro_lure_mod}",
                "esche_secondarie": f"🎯 **Alternativa Tecnica per Big Sospettosi:**\n{primarie}",
                "strategia_trophy_big_bass": trophy_strategy
            }
        elif target_mode == "Numeri":
            # In modalità Numeri pura, focalizziamo tutto sul ritmo d'azione senza appesantire col Trophy
            return {
                "esche_primarie": primarie + hydro_lure_mod,
                "esche_secondarie": secondarie,
                "strategia_trophy_big_bass": ""
            }
        else:  # "Entrambi"
            return {
                "esche_primarie": primarie + hydro_lure_mod,
                "esche_secondarie": secondarie,
                "strategia_trophy_big_bass": trophy_strategy
            }

    @classmethod
    def generate_pro_report(
        cls,
        best_hour: dict,
        trend_3d: float,
        astro: dict,
        sim_results: dict = None,
        water_level: str = "Stabile",
        forage_base: str = "Misto",
        fishing_pressure: str = "Media",
        target_mode: str = "Entrambi"
    ) -> dict:
        """
        5. ORCHESTRATORE CENTRALE DEL REPORT TATTICO (Con Selettore Modalità Numeri / Trophy / Entrambi)
        - Se target_mode == 'Trophy': usa 'best_trophy_hour' come dizionario primario di riferimento.
        - Se target_mode == 'Numeri': usa 'best_hour' ed esclude il blocco Big Bass da esche_secondarie.
        - Se target_mode == 'Entrambi': usa 'best_hour' per l'analisi generale ma passa i dati esatti
          di 'best_trophy_hour' al box Strategia Big Bass.
        """
        # Estrazione di best_trophy_hour da sim_results (con fallback sicuro a best_hour)
        best_trophy_dict = best_hour
        if sim_results and isinstance(sim_results, dict) and "best_trophy_hour" in sim_results:
            best_trophy_dict = sim_results["best_trophy_hour"] or best_hour

        # Se l'utente ha scelto la modalità esclusiva "Trophy", l'intero report si ancora all'ora del picco Trophy!
        active_hour = best_trophy_dict if target_mode == "Trophy" else best_hour

        # Estrazione sicura dei parametri dall'ora attiva selezionata
        w_temp = float(active_hour.get("water_temp_used", active_hour.get("water_temp", 16.0)))
        wind = float(active_hour.get("wind", 8.0))
        clouds = int(active_hour.get("clouds", 40))
        radiation = int(active_hour.get("radiation", 350))
        press_delta = float(active_hour.get("pressure_delta", 0.0))
        press_12h = float(active_hour.get("pressure_trend_12h", press_delta * 2.5))
        do_idx = float(active_hour.get("do_saturation_index", 0.85))
        torbidita = str(active_hour.get("torbidita_label", "Velata")).replace(" (Stima)", "")
        depth_zone = str(active_hour.get("depth_zone", "Sub-Superficie & Cover (1.0m - 2.5m)"))
        catch_rate = float(active_hour.get("catch_rate", 65.0))
        hour_int = int(active_hour.get("hour", 14))
        time_label = str(active_hour.get("time_label", f"{hour_int:02d}:00"))

        # Dati specifici del picco Trophy (utilizzati sia in modalità "Trophy" sia in "Entrambi")
        trophy_rate_peak = float(best_trophy_dict.get("trophy_rate", active_hour.get("trophy_rate", 60.0)))
        trophy_hour_label = str(best_trophy_dict.get("time_label", time_label))
        trophy_depth_zone = str(best_trophy_dict.get("depth_zone", depth_zone))

        if sim_results and isinstance(sim_results, dict):
            macro_14d = float(sim_results.get("macro_trend_14d", trend_3d))
            micro_72h = float(sim_results.get("micro_trend_72h", trend_3d))
            bio_state = str(sim_results.get("biological_state", "Omeostasi Termica Consolidata"))
        else:
            macro_14d = float(trend_3d)
            micro_72h = float(trend_3d)
            bio_state = (
                f"Shock Post-Frontale ({w_temp}°C)" if micro_72h <= -0.8
                else (f"Warming Trend Attivo ({w_temp}°C)" if micro_72h >= 0.6 else f"Stabilità Termica ({w_temp}°C)")
            )

        alba_dec = float(astro.get("sunrise_dec", 6.5))
        tramonto_dec = float(astro.get("sunset_dec", 19.5))

        # --- Esecuzione dei 4 Sub-Moduli Specialistici (3A + 3B) ---
        pos_data = cls.analyze_hydro_biological_positioning(
            w_temp=w_temp,
            macro_14d=macro_14d,
            micro_72h=micro_72h,
            do_idx=do_idx,
            press_delta=press_delta,
            press_12h=press_12h,
            depth_zone=depth_zone,
            bio_state=bio_state,
            water_level=water_level
        )

        kin_gear = cls.compute_retrieve_kinetics_and_gear(
            w_temp=w_temp,
            micro_72h=micro_72h,
            press_delta=press_delta,
            torbidita=torbidita,
            wind=wind,
            fishing_pressure=fishing_pressure,
            water_level=water_level
        )

        chromatic_txt = cls.select_chromatic_spectrum(
            torbidita=torbidita,
            clouds=clouds,
            radiation=radiation,
            hour=hour_int,
            alba=alba_dec,
            tramonto=tramonto_dec,
            forage_base=forage_base
        )

        lure_data = cls.build_biomechanical_lure_matrix(
            w_temp=w_temp,
            micro_72h=micro_72h,
            wind=wind,
            radiation=radiation,
            torbidita=torbidita,
            trophy_rate=trophy_rate_peak,
            depth_zone=depth_zone,
            forage_base=forage_base,
            fishing_pressure=fishing_pressure,
            water_level=water_level,
            target_mode=target_mode,
            trophy_hour_label=trophy_hour_label,
            trophy_depth_zone=trophy_depth_zone
        )

        # --- Sintesi Bio-Alert e Composizione Condizionale per Modalità ---
        if target_mode == "Numeri":
            bio_alert = f"🔥 Focus Numeri & Azione — Picco Ore {time_label} (BAI {catch_rate}%) — {bio_state}"
            # In modalità Numeri NON appendiamo strategia_trophy_big_bass
            esche_secondarie_final = lure_data["esche_secondarie"]
            esche_completo = f"{lure_data['esche_primarie']}\n\n{lure_data['esche_secondarie']}"
        elif target_mode == "Trophy":
            bio_alert = f"👑 Focus Esclusivo Big Bass — Picco Trophy Ore {trophy_hour_label} ({trophy_rate_peak}%) — {bio_state}"
            esche_secondarie_final = lure_data["esche_secondarie"]
            esche_completo = f"{lure_data['esche_primarie']}\n\n---\n{lure_data['esche_secondarie']}"
        else:  # "Entrambi"
            bio_alert = (
                f"🔥 Picco Azione Ore {time_label} ({catch_rate}%) | "
                f"👑 Picco Trophy Ore {trophy_hour_label} ({trophy_rate_peak}%) — {bio_state}"
            )
            esche_secondarie_final = (
                f"{lure_data['esche_secondarie']}\n\n"
                f"---\n"
                f"{lure_data['strategia_trophy_big_bass']}"
            )
            esche_completo = f"{lure_data['esche_primarie']}\n\n{esche_secondarie_final}"

        recupero_arricchito = (
            f"{kin_gear['recupero_cinetica']}\n\n"
            f"---\n"
            f"{kin_gear['gear_e_line_setup']}"
        )

        approccio_completo = f"{pos_data['condizione_fisiologica']}\n\n{pos_data['approccio_posizionale']}"

        return {
            # Chiavi storiche granulari
            "condizione": pos_data["condizione_fisiologica"],
            "approccio": approccio_completo,
            "esche_primarie": lure_data["esche_primarie"],
            "esche_secondarie": esche_secondarie_final,
            "colore": chromatic_txt,
            "recupero": recupero_arricchito,
            "strike_zone": depth_zone,
            # Nuove chiavi dedicate Pro V2
            "gear_setup": kin_gear["gear_e_line_setup"],
            "strategia_trophy": lure_data["strategia_trophy_big_bass"],
            "bio_alert": bio_alert,
            "target_mode": target_mode,
            # Alias per la UI a 4 card ('approccio', 'esche', 'colori', 'velocita')
            "esche": esche_completo,
            "colori": chromatic_txt,
            "velocita": recupero_arricchito
        }

    @classmethod
    def generate_report(
        cls,
        sim_data: dict,
        torbidita: str = "Non specificato",
        spot_morphology: str = "",
        water_level: str = "Stabile",
        forage_base: str = "Misto",
        fishing_pressure: str = "Media",
        target_mode: str = "Entrambi",
        astro: dict = None
    ) -> dict:
        """
        Wrapper di retrocompatibilità diretta con stima astronomica dinamica di fallback:
        Se 'astro' non viene passato, stima dinamicamente Alba e Tramonto in funzione
        del regime termico stagionale (base_water_temp / mean_7d_air) evitando orari fissi estivi in inverno.
        """
        best = sim_data.get("best_hour", {})
        trend_3d = float(sim_data.get("micro_trend_72h", sim_data.get("thermal_trend_3d", 0.0)))

        # PERFEZIONAMENTO 3: Stima dinamica stagionale di alba/tramonto se astro è None
        if astro is not None and isinstance(astro, dict) and "sunrise_dec" in astro:
            astro_to_use = astro
        else:
            ref_temp = float(
                sim_data.get(
                    "base_water_temp",
                    best.get("water_temp_used", sim_data.get("mean_7d_air", 15.0))
                )
            )
            # Frazione stagionale continua [0.0 in pieno inverno <= 7°C, 1.0 in piena estate >= 25°C]
            season_factor = max(0.0, min(1.0, (ref_temp - 7.0) / 18.0))
            # Alba: oscilla da ~07:36 (7.6) in inverno a ~05:42 (5.7) in estate
            est_sunrise = round(7.6 - (1.9 * season_factor), 2)
            # Tramonto: oscilla da ~16:54 (16.9) in inverno a ~20:48 (20.8) in estate
            est_sunset = round(16.9 + (3.9 * season_factor), 2)
            astro_to_use = {"sunrise_dec": est_sunrise, "sunset_dec": est_sunset}

        return cls.generate_pro_report(
            best_hour=best,
            trend_3d=trend_3d,
            astro=astro_to_use,
            sim_results=sim_data,
            water_level=water_level,
            forage_base=forage_base,
            fishing_pressure=fishing_pressure,
            target_mode=target_mode
        )