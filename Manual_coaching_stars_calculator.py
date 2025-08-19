import streamlit as st
import pandas as pd

 # ⭐ Conversiefunctie: score ➜ sterwaarde
def convert_score_to_star(score):
    thresholds = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270]
    stars = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    for i in reversed(range(len(thresholds))):
        if score >= thresholds[i]:
            return stars[i]
    return 0.5
    
def main():
        
    # 📊 Laad de Exceldata met wegingsfactoren
    excel_path = r"C:\Users\Rob Vermeer\OneDrive\Documenten\Sports Interactive\Football Manager 2024\8. Python export data\Role_Profiles\Coaching value per role FM24.xlsx"
    df_weights = pd.read_excel(excel_path, sheet_name="Sheet1", index_col=0)

    # 🏷️ Mapping van korte labels naar leesbare namen
    attribute_labels = {
      'Att': 'Aanvallend',
        'Dis': 'Discipline',
        'Fit': 'Conditie',
        'Mot': 'Motiveren',
        'Men': 'Mentaal',
        'Det': 'Vastberadenheid',
        'SPC': 'Standaardsituaties',
        'GkD': 'DM Baldistributie',
        'TCo': 'Tactiek',
        'GkS': 'DM Ballen Tegenhouden',
        'Tec': 'Techniek',
        'GkH': 'BM Balvastigheid',
        'Def': 'Verdedigend',
    }

    st.title("🎯 FM24 Trainingsformulier")

    # 📥 Invoerwaarden via formulier
    col1, col2 = st.columns(2)
    attribute_values = {}
    for i, (key, label) in enumerate(attribute_labels.items()):
        input_widget = col1.number_input if i % 2 == 0 else col2.number_input
        attribute_values[key] = input_widget(label, min_value=1, max_value=20, value=10, step=1)

    # ✅ Bereken totale score per trainingsonderdeel
    if st.button("✅ Analyseer attributen"):
        st.subheader("🔎 Totale score per trainingsonderdeel")

        for onderdeel in df_weights.index:
            wegingsrij = df_weights.loc[onderdeel]
            totaal_score = sum(attribute_values.get(attr, 0) * wegingsrij.get(attr, 0) for attr in attribute_labels)
            sterren_score = convert_score_to_star(totaal_score)

            st.write(f"▶️ {onderdeel}: {totaal_score:.2f} punten → ⭐ {sterren_score} / 5")

# Alleen uitvoeren als dit bestand direct gestart wordt
if __name__ == "__main__":
    main()
