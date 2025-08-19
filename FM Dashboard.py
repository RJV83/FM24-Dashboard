import streamlit as st 

# Import van losse scripts
from Manual_coaching_stars_calculator import main as Manual_coaching_calculator
from coaching_stars import main as coaching_stars_analyser
from staff_Shortlist import main as staff_shortlist_analyser
from Manual_Playerrole_Calculator import main as Manual_Playerrole_calculator
from Squad_Development import main as squad_development
from Players_Scouting_Analyse import main as player_scouting_analyser
from team_lineup import main as team_lineup_planner

# Sidebar Navigatie
st.sidebar.title("⚽ FM Analyse Menu")"
keuze = st.sidebar.radio(
    "Kies een module:",
    [
        "Manual Coaching Calculator",
        "Coaching Stars Analyser",
        "Staff Shortlist",
        "Manual Playerrole Calculator",
        "Squad Development",
        "Player Scouting",
        "Team Lineup team_lineup_planner"
    ]
)

# Script koppelen naar navigatie knoppen
if keuze == "Manual Coaching Calculator":
    Manual_coaching_calculator()

elif keuze == "Coaching Stars Analyser":
    coaching_stars_analyser()
    
elif keuze == "Staff Shortlist":
    staff_shortlist_analyser()
    
elif keuze == "manual Playerrole Calculator":
    Manual_Playerrole_calculator()
    
elif keuze == "Squad Development":
    squad_development()
    
elif keuze == "Player scouting":
    player_scouting_analyser()
    
elif keuze == "Team Lineup Planner":
    team_lineup_planner()
    
