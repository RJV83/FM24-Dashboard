import os
import pandas as pd
import streamlit as st

def main():
    
    # 📁 Padinstellingen
    base_folder = r"C:\Users\Rob Vermeer\OneDrive\Documenten\Sports Interactive\Football Manager 2024\8. Python export data"
    role_profile_folder = os.path.join(base_folder, "Role_Profiles")
    roles_file = os.path.join(role_profile_folder, "Value per role FM24.xlsx")

    # 📥 Inlezen van data
    roles_df = pd.read_excel(roles_file, header=None)
    role_map = dict(zip(roles_df.iloc[2:, 0], roles_df.iloc[2:, 1]))  # volledige naam ➜ afkorting

    # 🧠 Attribuutcategorieën en afkortingen
    categorie_attributen = {
        "Technisch": {
            'Afstandsschoten': 'Lon',
            'Afwerken': 'Fin',
            'Dribbelen': 'Dri',
            'Eerste balcontact': 'Fir',
            'Hoekschoppen': 'Cor',
            'Koppen': 'Hea',
            'Mandekken': 'Mar',
            'Passing': 'Pas',
            'Strafschoppen': 'Pen',
            'Tackelen': 'Tck',
            'Techniek': 'Tec',
            'Verre Inworpen': 'LTh',
            'Voorzetten': 'Cro',
            'Vrije Trappen': 'Fre'
        },
        "Mentaal": {
            'Anticiperen': 'Ant',
            'Beslissingen': 'Dec',
            'Concentratie': 'Cnt',
            'Felheid': 'Agg',
            'Flair': 'Fla',
            'Inzet': 'Wor',
            'Inzicht': 'Vis',
            'Kalmte': 'Cmp',
            'Lef': 'Bra',
            'Leiderschap': 'Ldr',
            'Positie Kiezen': 'Pos',
                'Teamgeest': 'Tea',
            'Vastberadenheid': 'Det',
            'Zonder Bal': 'OtB'
        },
        "Keepen": {
            'Baas in Strafschopgebied': 'Cmd',
            'Balvastigheid': 'Han',
            'Communicatie': 'Com',
            'Een-tegen-een': '1v1',
            'Eerste balcontact': 'Fir',
            'Excentriciteit': 'Ecc',
            'Hoge Ballen': 'Aer',
            'Passing': 'Pas',
            'Reflexen': 'Ref',
            'Uitkomen (neiging)': 'TRO',
            'Uittrappen': 'Kic',
            'Uitwerpen': 'Thr',
            'Wegboksen (neiging)': 'Pun'
        },
        "Fysiek": {
            'Behendigheid': 'Agi',
            'Evenwicht': 'Bal',
            'Kracht': 'Str',
            'Natuurlijke fitheid': 'Nat2',
            'Snelheid': 'Pac',
            'Sprongkracht': 'Jum',
            'Uithoudingsvermogen': 'Sta',
            'Versnelling': 'Acc'
        }
    }

    # 🧬 Verzameling van waarden
    attribute_values = {}

    # 🔄 Switch voor spelertype
    rol_type = st.radio("🔄 Kies Spelertype", ["Veldspeler", "Keeper"])

    # 🎛️ Toon categorieën en inputs
    def toon_categorie(naam):
        st.subheader(naam)
        for attrib, code in categorie_attributen[naam].items():
            waarde = st.text_input(attrib, key=code)
            attribute_values[code] = waarde

    if rol_type == "Keeper":
        toon_categorie("Keepen")
        toon_categorie("Mentaal")
        toon_categorie("Fysiek")
    
    else:
        toon_categorie("Technisch")
        toon_categorie("Mentaal")
        toon_categorie("Fysiek")
    
    # ✅ Bereken totale score per rol
    if st.button("✅ Analyseer attributen"):
        st.subheader("🔎 Totale score per geselecteerde rol")

    def bereken_score_per_rol(rol_afkorting, attribute_values):
        # Zoek de rij in de Excel die bij deze rol hoort
        rol_data = roles_df[roles_df.iloc[:, 1] == rol_afkorting]
    
        if rol_data.empty:
            return "❌ Rol niet gevonden in Excel"

        # Neem alleen de attribuutcodes en bijbehorende wegingen
        attribuut_codes = roles_df.iloc[1, 2:].dropna().tolist()
        wegingen = rol_data.iloc[0, 2:2+len(attribuut_codes)].tolist()

        score = 0
        totaal_gewicht = 0

        for code, gewicht in zip(attribuut_codes, wegingen):
            try:
                waarde = float(attribute_values.get(code, 0))
                score += waarde * gewicht
                totaal_gewicht += gewicht
            except ValueError:
                pass  # negeer niet-numerieke invoer

        if totaal_gewicht == 0:
            return "⚠️ Geen relevante attributen ingevoerd"

        gemiddelde_score = score / totaal_gewicht
        return f"{gemiddelde_score:.2f}"


    # 📐 Structuur van formatie: aantal posities per rij
    formatie_structuur = [1, 5, 5, 5, 5, 3]

    # 📋 Positienamen uit je Excel (leeg = geen rol)
    positie_namen = [
        ["DM"],
        ["VR", "VC", "VC", "VC", "VL"],
        ["VVR", "VM", "VM", "VM", "VVL"],
        ["MR", "MC", "MC", "MC", "ML"],
        ["AMR", "AMC", "AMC", "AMC", "AML"],
        ["SC", "SC", "SC"]
    ]

    st.markdown("## 🧠 Dynamisch Formatieoverzicht")

    # 🔄 Loop door elke rij in de formatie
    rolafkortingen = [""] + roles_df.iloc[2:, 1].dropna().tolist()

    for rij_index, rij in enumerate(positie_namen):
        kolommen = st.columns(len(rij))
        for kol_index, positie in enumerate(rij):
            with kolommen[kol_index]:
                unieke_key = f"rol_{positie}_{rij_index}_{kol_index}"
                rol = st.selectbox("", rolafkortingen, key=unieke_key)

                # ⛳ Positienaam gecentreerd
                st.markdown(
                    f"<div style='text-align:center'><b>{positie}</b></div>",
                    unsafe_allow_html=True
                )

                # 🎯 Score of melding gecentreerd
                if rol in ["", "Geen rol"]:
                    st.markdown("<div style='text-align:center'>—</div>", unsafe_allow_html=True)
                else:
                    score_raw = bereken_score_per_rol(rol, attribute_values)
                    try:
                        score_float = float(score_raw)
                        st.markdown(f"<div style='text-align:center'>{score_float:.2f}</div>", unsafe_allow_html=True)
                    except:
                        st.markdown(f"<div style='text-align:center'>{score_raw}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    



