import os
import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup

def main():
    
    # 📁 Padinstellingen
    base_folder = r"C:\Users\Rob Vermeer\OneDrive\Documenten\Sports Interactive\Football Manager 2024\8. Python export data"
    scouting_html_folder = os.path.join(base_folder, "Scouting_exports")
    role_profile_folder = os.path.join(base_folder, "Role_Profiles")

    html_file = os.path.join(scouting_html_folder, "Player_Scouting.html")
    roles_file = os.path.join(role_profile_folder, "Value per role FM24.xlsx")

    # 🔄 HTML naar Excel - Robuust inlezen en opschonen
    with open(html_file, "r", encoding="latin1", errors="replace") as f:
        raw_html = f.read()

    # HTML opschonen met BeautifulSoup
    soup = BeautifulSoup(raw_html, "lxml")  # lxml parser voor reparatie
    clean_html = str(soup)

    # 📥 Tabellen uitlezen - probeer eerst lxml, dan fallback html5lib
    try:
        tables = pd.read_html(clean_html, flavor="lxml")
    except Exception:
        tables = pd.read_html(clean_html, flavor="html5lib")

    df_html = tables[0]
    scouting_df = df_html.copy()

    # 📄 Rollen inlezen
    roles_df = pd.read_excel(roles_file, header=None)
    attribute_map = roles_df.iloc[1].dropna().tolist()

    # 🗺️ Rolmapping: volledige naam ➜ afkorting
    role_name_col = 0
    role_code_col = 1
    role_map = dict(zip(roles_df.iloc[2:, role_name_col], roles_df.iloc[2:, role_code_col]))

    # 🎛️ UI
    st.title("🧠 Football Manager 24 - Scouting Dashboard")
    st.markdown("Selecteer tot **11 rollen** die je wilt analyseren")

    role_choices = roles_df.iloc[2:, role_name_col].dropna().unique().tolist()
    selected_roles = st.multiselect("Kies rollen (max. 11)", role_choices, max_selections=11)

    # 🧮 Functies
    def get_role_weights(role_name):
        row = roles_df[roles_df.iloc[:, role_name_col] == role_name].iloc[0]
        weights = {attr: row[i + 2] for i, attr in enumerate(attribute_map) if pd.notnull(row[i + 2]) and row[i + 2] > 0}
        return weights

    def calculate_score(row, weights):
        total = sum(weights.values())
        score = sum(row[attr] * w for attr, w in weights.items() if attr in row and pd.notnull(row[attr]))
        return round(score / total, 2) if total > 0 else 0

    # 📊 Berekenen rolscores
    short_role_names = []
    for role in selected_roles:
        weights = get_role_weights(role)
        short_name = role_map.get(role, role)
        scouting_df[short_name] = scouting_df.apply(lambda row: calculate_score(row, weights), axis=1)
        short_role_names.append(short_name)

    # 📊 Resultaat tonen
    meta_cols = ["Name", "Age", "Position", "Club", "Wage", "Transfer Value", "Nat", "Expires"]
    display_df = scouting_df[meta_cols + short_role_names].sort_values(by=short_role_names[0], ascending=False) if short_role_names else scouting_df[meta_cols]

    st.dataframe(display_df, use_container_width=True)
    
    # 🧼 Verwijder Excelbestand na gebruik
    try:
        os.remove(excel_file)  # directe poging; als het weg is, komt FileNotFoundError
    except FileNotFoundError:
        pass  # al weg: niets te doen
    except PermissionError as e:
        st.warning(f"Bestand is nog geopend in een ander programma: {e}")
    except Exception as e:
        st.warning(f"Onbekende fout bij verwijderen: {e}")

# Alleen uitvoeren als dit bestand direct gestart wordt
if __name__ == "__main__":
    main()