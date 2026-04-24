import streamlit as st
import pandas as pd
#python -m streamlit run App.py
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
# FILVAL (EXAKT SOM DIN LOGIK)
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
# GEMENSAM LOGIK
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
# KNAPP (istället för direkt körning)
# =========================
if st.button("Beräkna"):

    rad = temperaturer[temp] + vindar[vind]

    df = pd.read_excel(fil)

    if rad < 0 or rad >= len(df):
        st.error("Rad utanför tabell")
    else:
        st.success(f"Resultat från rad {rad}")
        st.dataframe(df.iloc[[rad]])