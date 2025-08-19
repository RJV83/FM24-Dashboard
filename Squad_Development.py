import os
import pandas as pd
import streamlit as st

def main():
    
    # 📁 Padinstellingen
    base_folder = r"C:\Users\Rob Vermeer\OneDrive\Documenten\Sports Interactive\Football Manager 2024\8. Python export data"
    squad_html_folder = os.path.join(base_folder, "Squad_exports")
    role_profile_folder = os.path.join(base_folder, "Role_Profiles")

    html_file = os.path.join(squad_html_folder, "Squad.html")
    excel_file = html_file.replace(".html", ".xlsx")
    roles_file = os.path.join(role_profile_folder, "Value per role FM24.xlsx")

    # 🔄 HTML naar Excel (met tekencorrectie)
    if not os.path.exists(excel_file):
        tables = pd.read_html(html_file)
        df_html = tables[0]
        for col in df_html.select_dtypes(include='object').columns:
            df_html[col] = df_html[col].apply(lambda x: x.encode('latin1').decode('utf8') if isinstance(x, str) else x)
        df_html.to_excel(excel_file, index=False)

    # 📥 Inlezen van data
    squad_df = pd.read_excel(excel_file)
    roles_df = pd.read_excel(roles_file, header=None)
    attribute_map = roles_df.iloc[1].dropna().tolist()

    # 🗺️ Rolmapping: volledige naam (kolom A) ➜ afkorting (kolom B)
    role_name_col = 0  # volledige naam
    role_code_col = 1  # afkorting
    role_map = dict(zip(roles_df.iloc[2:, role_name_col], roles_df.iloc[2:, role_code_col]))

    # 🎛️ UI: Selecteer maximaal 11 rollen
    st.title("🧠 Football Manager 24 - Scouting Dashboard")
    st.markdown("Selecteer tot **11 rollen** die je wilt analyseren voor je squad")

    role_choices = roles_df.iloc[2:, role_name_col].dropna().unique().tolist()
    selected_roles = st.multiselect("Kies rollen (max. 11)", role_choices, max_selections=11)

    # 🧮 Bereken scores per rol 
    def get_role_weights(role_name):
        row = roles_df[roles_df.iloc[:, role_name_col] == role_name].iloc[0]
        weights = {attr: row[i + 2] for i, attr in enumerate(attribute_map) if pd.notnull(row[i + 2]) and row[i + 2] > 0}
        return weights

    def calculate_score(row, weights):
        total = sum(weights.values())
        score = sum(row[attr] * w for attr, w in weights.items() if attr in row and pd.notnull(row[attr]))
        return round(score / total, 2) if total > 0 else 0

    # 🧠 Rolscores berekenen met afkorting als kolomtitel
    short_role_names = []
    for role in selected_roles:
        weights = get_role_weights(role)
        short_name = role_map.get(role, role)
        squad_df[short_name] = squad_df.apply(lambda row: calculate_score(row, weights), axis=1)
        short_role_names.append(short_name)

    # 📊 Toon eindresultaat
    meta_cols = ["Name", "Age", "Position", "Wage", "Transfer Value", "Nat", "Av Rat"]
    display_df = squad_df[meta_cols + short_role_names].sort_values(by=short_role_names[0], ascending=False)

    st.dataframe(display_df, use_container_width=True)

    # 🧼 Opruimen: verwijder Excelbestand na gebruik
    try:
        if os.path.exists(excel_file):
            os.remove(excel_file)
    except:
        pass

if __name__ == "__main__":
    main()

