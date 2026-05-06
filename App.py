import streamlit as st
import pandas as pd

st.set_page_config(layout="centered")
st.title("Klimatförbättrad bettong")
st.markdown("""
<style>
div[data-baseweb="select"] * {
    cursor: pointer !important;
}

div[data-baseweb="select"] {
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HJÄLPFUNKTION (NY)
# =========================
def visa_resultat(row, kolumner, rubrik="Resultat"):
    st.subheader(rubrik)

    cols = st.columns(2)

    for i, (label, col) in enumerate(kolumner.items()):

        # 🔹 Om flera möjliga kolumnnamn
        if isinstance(col, list):
            value = "Saknas"
            for c in col:
                if c in row:
                    value = row[c]
                    break
        else:
            value = row.get(col, "Saknas")

        cols[i % 2].metric(label, value)

# =========================
# KOLUMN-DEFINITIONER (NYA)
# =========================
kol_bjalklag_7d = {
    "Slaggmängd": "Slagg mängd",
    "Gjuttemperatur": "Gjuttemperatur",
    "Temperatur motgjutningsyta": "Temperatur motgjutningsyta",
    "Väderskydd / uppvärmning": "Väderskydd, uppvärmning (ingen vind)",
    "Täckning [mm]": "Täckning [mm]",
    "<7 d och >70% [Dagar]": "<7 d och >70 % [Dagar]"
}

kol_bjalklag_14d = {
    "Slaggmängd": "Slagg mängd",
    "Gjuttemperatur": "Gjuttemperatur",
    "Temperatur motgjutningsyta": "Temperatur motgjutningsyta",
    "Väderskydd / uppvärmning": "Väderskydd, uppvärmning (ingen vind)",
    "Täckning [mm]": "Täckning [mm]",
    "<14 d och >70% [Dagar]": "<14 d och >70 % [Dagar]"
}

kol_miljo_7d = {
    "Kvalitet": "Kvalitet",
    "Gjuttemperatur": "Gjuttemperatur",
    "Temperatur motgjutningsyta": "Temperatur motgjutningsyta",
    "Väderskydd / uppvärmning": "Väderskydd, uppvärmning (ingen vind)",
    "Täckning [mm]": "Täckning [mm]",
    "<7 d och >70% [Dagar]": "<7 d och >70 % [Dagar]"
}

kol_miljo_14d = {
    "Kvalitet": "Kvalitet",
    "Gjuttemperatur": "Gjuttemperatur",
    "Temperatur motgjutningsyta": "Temperatur motgjutningsyta",
    "Väderskydd / uppvärmning": "Väderskydd, uppvärmning (ingen vind)",
    "Täckning [mm]": "Täckning [mm]",
    "<14 d och >70% [Dagar]": "<14 d och >70 % [Dagar]"
}

kol_vagg = {
    "Slagg/Kvalitet": ["Slaggmängd", "Kvalitet"],
    "Gjuttemperatur": "Gjuttemperatur",
    "Temperatur motgjutningsyta": "Temperatur motgjutningsyta",
    "Värmekabel": "Värmekabel",
    "Antal värmekablar": "Antal värmekablar",
    "Täckning": "Täckning [mm]",
    "Formisolering": "Formisolering [mm]",
    "<17h och >6 MPa": "<17 Timmar och >6 Mpa"
}

# =========================
# 1. KONSTRUKTION
# =========================
val_konstruktion = st.selectbox(
    "Välj konstruktion",
    ["Bjälklag", "Vägg"]
)

# =========================
# 2. TYP
# =========================
val_typ = st.selectbox(
    "Välj (Kvalitet eller Miljö)",
    ["Kvalitet", "Miljö"]
)

# =========================
# FILVAL
# =========================
if val_konstruktion == "Bjälklag" and val_typ == "Kvalitet":
    fil_7d = "Bjälklag_Kvalitet_7d.xlsx"
    fil_14d = "Bjälklag_Kvalitet_14d.xlsx"

elif val_konstruktion == "Bjälklag" and val_typ == "Miljö":
    fil = "Bjälklag_Miljo.xlsx"

elif val_konstruktion == "Vägg" and val_typ == "Kvalitet":
    fil = "Vägg_Hållfasthet_17H.xlsx"

elif val_konstruktion == "Vägg" and val_typ == "Miljö":
    fil = "Vägg_slagg_17H.xlsx"

# =========================
# VAL AV SHEET
# =========================
sheet_name = None

if val_typ == "Kvalitet":

    if val_konstruktion == "Bjälklag":
        sheets = {
            "C20/25": "Bjälklag (C20-25)",
            "C25/30": "Bjälklag (C25-30)",
            "C28/35": "Bjälklag (C28-35)",
            "C30/37": "Bjälklag (C30-37)",
            "C32/40": "Bjälklag (C32-40)",
            "C35/45": "Bjälklag (C35-45)",
            "C40/50": "Bjälklag (C40-50)"
        }

    else:  # Vägg
        sheets = {
            "C20/25": "Vägg (C20-25)",
            "C25/30": "Vägg (C25-30)",
            "C28/35": "Vägg (C28-35)",
            "C30/37": "Vägg (C30-37)",
            "C32/40": "Vägg (C32-40)",
            "C35/45": "Vägg (C35-45)",
            "C40/50": "Vägg (C40-50)"
        }

    val_sheet = st.selectbox("Välj betongkvalitet", list(sheets.keys()))
    sheet_name = sheets[val_sheet]


elif val_typ == "Miljö":

    if val_konstruktion == "Bjälklag":
        miljo_sheets = {
            "10%": "Bjälklag (10% slagg)",
            "20%": "Bjälklag (20% slagg)",
            "30%": "Bjälklag (30% slagg)",
            "40%": "Bjälklag (40% slagg)"
        }
    else:
        miljo_sheets = {
            "10%": "Vägg (10% slagg)",
            "20%": "Vägg (20% slagg)",
            "30%": "Vägg (30% slagg)",
            "40%": "Vägg (40% slagg)"
        }

    val_miljo = st.selectbox("Välj slagg (%)", list(miljo_sheets.keys()))
    sheet_name = miljo_sheets[val_miljo]

# =========================
# TEMP + VIND
# =========================
temperaturer = {
    "20": 0,
    "15": 5,
    "10": 10,
    "5": 15,
    "0": 20,
    "-5": 25,
    "-10": 30,
    "-15": 35,
    "-20": 40
}

vindar = {
    "0": 0, "2": 1, "7": 2, "12": 3, "20": 4
}

col1, col2 = st.columns(2)

with col1:
    temp = st.selectbox("Temperatur", list(temperaturer.keys()))

with col2:
    vind = st.selectbox("Vindhastighet", list(vindar.keys()))



# =========================
# KNAPP
# =========================
if st.button("Beräkna"):

    rad = temperaturer[temp] + vindar[vind]

    # ===== KVALITET =====
    if val_typ == "Kvalitet":

        try:
            if val_konstruktion == "Bjälklag":
                df_7d = pd.read_excel(fil_7d, sheet_name=sheet_name)
                df_14d = pd.read_excel(fil_14d, sheet_name=sheet_name)
            else:
                df = pd.read_excel(fil, sheet_name=sheet_name)

        except Exception as e:
            st.error(f"Fel vid läsning av Excel: {e}")
            st.stop()

        # ===== Kontroll rad =====
        if val_konstruktion == "Bjälklag":
            out_of_range = rad < 0 or rad >= len(df_7d)
        else:
            out_of_range = rad < 0 or rad >= len(df)

        if out_of_range:
            st.error("Rad utanför tabell")

        else:
            st.success(f"Resultat rad {rad}")

            if val_konstruktion == "Bjälklag":

                # ===== 7 DAGAR =====
                st.markdown("""
                <h2 style='margin-top:30px;'>7 dagar</h2>
                """, unsafe_allow_html=True)

                row_7d = df_7d.iloc[rad]
                visa_resultat(row_7d, kol_bjalklag_7d)
    
                st.divider()

                # ===== 14 DAGAR =====
                st.markdown("""
                <h2 style='margin-top:30px;'>14 dagar</h2>
                """, unsafe_allow_html=True)

                row_14d = df_14d.iloc[rad]
                visa_resultat(row_14d, kol_bjalklag_14d)
            else:
                row = df.iloc[rad]
                visa_resultat(row, kol_vagg, "Resultat")

    # ===== MILJÖ =====
    else:
        df = pd.read_excel(fil, sheet_name=sheet_name)

        if rad < 0 or rad >= len(df):
            st.error("Rad utanför tabell")
        else:
            st.success(f"Resultat rad {rad}")

        row = df.iloc[rad]

        if val_konstruktion == "Bjälklag":
            visa_resultat(row, kol_miljo_14d, "Resultat")
        else:
            visa_resultat(row, kol_vagg, "Resultat")
