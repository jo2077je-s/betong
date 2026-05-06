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
    fil_7d = "Vägg_Hållfasthet_17H.xlsx"
    fil_14d = "Vägg_slagg_17H.xlsx"

else:
    fil = "Vagg_Miljo.xlsx"

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

    miljo_sheets = {
        "10%": "Bjälklag (10% slagg)",
        "20%": "Bjälklag (20% slagg)",
        "30%": "Bjälklag (30% slagg)",
        "40%": "Bjälklag (40% slagg)"
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

    # ===== KVALITET (7d + 14d) =====
    if val_typ == "Kvalitet":

        df_7d = pd.read_excel(fil_7d, sheet_name=sheet_name)
        df_14d = pd.read_excel(fil_14d, sheet_name=sheet_name)

        if rad < 0 or rad >= len(df_7d):
            st.error("Rad utanför tabell")
        else:
            st.success(f"Resultat rad {rad}")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("7 dagar")
                st.dataframe(df_7d.iloc[[rad]])

            with col2:
                st.subheader("14 dagar")
                st.dataframe(df_14d.iloc[[rad]])

    # ===== MILJÖ =====
    else:
        df = pd.read_excel(fil, sheet_name=sheet_name)

        if rad < 0 or rad >= len(df):
            st.error("Rad utanför tabell")
        else:
            st.success(f"Resultat rad {rad}")
            st.dataframe(df.iloc[[rad]])
