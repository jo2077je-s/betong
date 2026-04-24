import streamlit as st
import pandas as pd

st.title("Beräkningsapp")

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
    fil = "Bjälklag_Kvalitet.xlsx"

elif val_konstruktion == "Bjälklag" and val_typ == "Miljö":
    fil = "Bjälklag_Miljo.xlsx"

elif val_konstruktion == "Vägg" and val_typ == "Kvalitet":
    fil = "Vagg_Kvalitet.xlsx"

else:
    fil = "Vagg_Miljo.xlsx"

# =========================
# VAL AV SHEET (NY DEL)
# =========================
sheet_name = None

if val_typ == "Kvalitet":

    sheets = {
        "C20/25": "Bjälklag (C20-25)",
        "C25/30": "Bjälklag (C25-30)",
        "C28/35": "Bjälklag (C28-35)",
        "C30/37": "Bjälklag (C30-37)",
        "C32/40": "Bjälklag (C32-40)",
        "C35/45": "Bjälklag (C35-45)",
        "C40/50": "Bjälklag (C40-50)"
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
    "-20": 40, "-15": 35, "-10": 30, "-5": 25,
    "0": 20, "5": 15, "10": 10, "15": 5, "20": 0
}

vindar = {
    "0": 0, "2": 1, "7": 2, "12": 3, "20": 4
}

temp = st.selectbox("Temperatur", list(temperaturer.keys()))
vind = st.selectbox("Vindhastighet", list(vindar.keys()))

# =========================
# KNAPP
# =========================
if st.button("Beräkna"):

    df = pd.read_excel(fil, sheet_name=sheet_name)

    rad = temperaturer[temp] + vindar[vind]

    if rad < 0 or rad >= len(df):
        st.error("Rad utanför tabell")
    else:
        st.success(f"Resultat rad {rad}")
        st.dataframe(df.iloc[[rad]])
