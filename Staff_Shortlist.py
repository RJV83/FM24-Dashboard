import streamlit as st
import pandas as pd
from io import StringIO

st.set_page_config(page_title="FM24 Coach Stars", layout="wide")
st.title("⭐ FM24 Coach Sterrenscores per Rol")

# ⭐ Conversiefunctie: score ➜ sterwaarde
def convert_score_to_star(score):
    thresholds = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270]
    stars = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    for i in reversed(range(len(thresholds))):
        if score >= thresholds[i]:
            return stars[i]
    return 0.5

def main():
    
    # 📂 Bestandspaden
    html_path = r"C:\Users\Rob Vermeer\OneDrive\Documenten\Sports Interactive\Football Manager 2024\8. Python export data\Staff_Shortlist_Export\Staff_Shortlist.html"
    excel_path = r"C:\Users\Rob Vermeer\OneDrive\Documenten\Sports Interactive\Football Manager 2024\8. Python export data\Role_Profiles\Coaching value per role FM24.xlsx"

    try:
        with open(html_path, encoding='utf-8') as f:
            html_content = f.read()
        staff_df = pd.read_html(StringIO(html_content))[0]
        weights_df = pd.read_excel(excel_path)

        st.success("✔️ Bestand succesvol ingelezen!")

        # 🧠 Alleen sterrenscores berekenen
        def calculate_score(row, role_weights):
            return sum(row[attr] * role_weights[attr] for attr in role_weights.index)

        all_roles = weights_df.iloc[:, 0].dropna().unique()

        for role in all_roles:
            role_weights = weights_df[weights_df.iloc[:, 0] == role].iloc[0, 1:].astype(float)

            for attr in role_weights.index:
                staff_df[attr] = pd.to_numeric(staff_df[attr], errors='coerce')

            staff_df.fillna(0, inplace=True)
            score = staff_df.apply(lambda row: calculate_score(row, role_weights), axis=1)
            staff_df[f"{role} Stars"] = score.apply(convert_score_to_star)

        # 🧩 Toevoegen van aangepaste velden
        extra_fields = [
            "Name", "Age", "Preferred Job", "Club", "Wage", "Expires",
            "Preferred Formation", "Second Preferred Formation",
            "Youth", "Tac Knw", "Judge A", "Judge P", "Media Handling"
        ]
        available_fields = [col for col in extra_fields if col in staff_df.columns]
        star_cols = [col for col in staff_df.columns if col.endswith("Stars")]

        result_df = staff_df[available_fields + star_cols]

        st.subheader("📋 Sterrenscores per Coach incl. Extra Eigenschappen")
        st.dataframe(result_df.sort_values(by=star_cols[0], ascending=False), use_container_width=True)

        # 📥 Download-optie
        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button("📤 Download Coach Sterrenscores als CSV", data=csv, file_name="Coach_Stars.csv", mime="text/csv")

    except Exception as e:
        st.error(f"🚨 Fout bij inladen van bestanden:\n{e}")

if __name__ == "__main__":
    main()
    