import os
import pandas as pd
import streamlit as st

def main():
    
    try:
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

        # 🗺️ Rolmapping: volledige naam ➜ afkorting
        role_name_col = 0
        role_code_col = 1
        role_map = dict(zip(roles_df.iloc[2:, role_name_col], roles_df.iloc[2:, role_code_col]))

        # 🎛️ UI
        st.title("🧠 Football Manager 24 - Scouting Dashboard")
        st.markdown("Selecteer tot **11 rollen** die je wilt analyseren voor je squad")

        role_choices = roles_df.iloc[2:, role_name_col].dropna().unique().tolist()
        selected_roles = st.multiselect("Kies rollen (max. 11)", role_choices, max_selections=11)

        if selected_roles:
            def get_role_weights(role_name):
                row = roles_df[roles_df.iloc[:, role_name_col] == role_name].iloc[0]
                return {attr: row[i + 2] for i, attr in enumerate(attribute_map) if pd.notnull(row[i + 2]) and row[i + 2] > 0}

            def calculate_score(row, weights):
                total = sum(weights.values())
                score = sum(row[attr] * w for attr, w in weights.items() if attr in row and pd.notnull(row[attr]))
                return round(score / total, 2) if total > 0 else 0

            short_role_names = []
            for role in selected_roles:
                weights = get_role_weights(role)
                short_name = role_map.get(role, role)
                squad_df[short_name] = squad_df.apply(lambda row: calculate_score(row, weights), axis=1)
                short_role_names.append(short_name)
    
            meta_cols = ["Name", "Age", "Position", "Wage", "Transfer Value", "Nat", "Av Rat"]
            display_df = squad_df[meta_cols + short_role_names].sort_values(by=short_role_names[0], ascending=False)
            st.dataframe(display_df, use_container_width=True)
        else:
            st.info("⬅️ Selecteer één of meerdere rollen om resultaten te tonen.")

        # 🧼 Verwijder Excelbestand na gebruik
        try:
            os.remove(excel_file)  # directe poging; als het weg is, komt FileNotFoundError
        except FileNotFoundError:
            pass  # al weg: niets te doen
        except PermissionError as e:
            st.warning(f"Bestand is nog geopend in een ander programma: {e}")
        except Exception as e:
            st.warning(f"Onbekende fout bij verwijderen: {e}")

    except Exception as e:
        st.error("❌ Er is een fout opgetreden in het script.")
        st.exception(e)

if __name__ == "__main__":
    main()
