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
    fil_7d = "Vagg_Kvalitet_7d.xlsx"
    fil_14d = "Vagg_Kvalitet_14d.xlsx"

else:
    fil = "Vagg_Miljo.xlsx"

# =========================
# VAL AV SHEET
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
# KOLUMNER DU VILL VISA
# =========================
visa_kolumner = st.multiselect(
    "Välj vilka kolumner du vill visa",
    ["Cementhalt", "Hållfasthet", "CO2", "Slump"],  # <-- ÄNDRA DENNA
    default=["Cementhalt", "Hållfasthet"]
)

# =========================
# KNAPP
# =========================
if st.button("Beräkna"):

    rad = temperaturer[temp] + vindar[vind]

    # ===== KVALITET =====
    if val_typ == "Kvalitet":

        df_7d = pd.read_excel(fil_7d, sheet_name=sheet_name)
        df_14d = pd.read_excel(fil_14d, sheet_name=sheet_name)

        if rad < 0 or rad >= len(df_7d):
            st.error("Rad utanför tabell")
        else:
            st.success(f"Resultat rad {rad}")

            result_7d = df_7d.iloc[rad]
            result_14d = df_14d.iloc[rad]

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("7 dagar")

                for col in visa_kolumner:
                    st.markdown(f"""
                    <div style="
                        padding:10px;
                        border-radius:10px;
                        background-color:#f0f2f6;
                        margin-bottom:6px;
                    ">
                        <b>{col}</b><br>{result_7d[col]}
                    </div>
                    """, unsafe_allow_html=True)

            with col2:
                st.subheader("14 dagar")

                for col in visa_kolumner:
                    st.markdown(f"""
                    <div style="
                        padding:10px;
                        border-radius:10px;
                        background-color:#f0f2f6;
                        margin-bottom:6px;
                    ">
                        <b>{col}</b><br>{result_14d[col]}
                    </div>
                    """, unsafe_allow_html=True)

    # ===== MILJÖ =====
    else:

        df = pd.read_excel(fil, sheet_name=sheet_name)

        if rad < 0 or rad >= len(df):
            st.error("Rad utanför tabell")
        else:
            st.success(f"Resultat rad {rad}")

            result = df.iloc[rad]

            for col in visa_kolumner:
                st.markdown(f"""
                <div style="
                    padding:10px;
                    border-radius:10px;
                    background-color:#f0f2f6;
                    margin-bottom:6px;
                ">
                    <b>{col}</b><br>{result[col]}
                </div>
                """, unsafe_allow_html=True)
