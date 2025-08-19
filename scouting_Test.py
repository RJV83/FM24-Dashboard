import os
import pandas as pd
import streamlit as st

# 📁 Padinstellingen
base_folder = r"C:\Users\Rob Vermeer\OneDrive\Documenten\Sports Interactive\Football Manager 2024\8. Python export data"
scouting_html_folder = os.path.join(base_folder, "Scouting_exports")

html_file = os.path.join(scouting_html_folder, "Player_Scouting.html")
excel_file = html_file.replace(".html", ".xlsx")

# 🔄 HTML naar Excel (met tekencorrectie)
if not os.path.exists(excel_file):
    tables = pd.read_html(html_file)
    df_html = tables[0]
 #   for col in df_html.select_dtypes(include='object').columns:
 #       df_html[col] = df_html[col].apply(lambda x: x.encode('latin1').decode('utf8') if isinstance(x, str) else x)
    df_html.to_excel(excel_file, index=False)

# 📥 Inlezen van data
scouting_df = pd.read_excel(excel_file)

st.write("📋 Kolomnamen in scouting_df:")
st.write(scouting_df.columns.tolist())
