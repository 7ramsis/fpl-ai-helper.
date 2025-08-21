import streamlit as st
import pandas as pd
import requests
import numpy as np

# --- FPL Data Fetch ---
FPL_BOOTSTRAP = "https://fantasy.premierleague.com/api/bootstrap-static/"
FPL_FIXTURES = "https://fantasy.premierleague.com/api/fixtures/"

@st.cache_data
def load_data():
    players = requests.get(FPL_BOOTSTRAP).json()["elements"]
    teams = requests.get(FPL_BOOTSTRAP).json()["teams"]
    fixtures = requests.get(FPL_FIXTURES).json()
    return pd.DataFrame(players), pd.DataFrame(teams), pd.DataFrame(fixtures)

# --- Basic Player Selection (simplified) ---
def recommend_team(budget=100.0):
    players, teams, fixtures = load_data()
    df = pd.DataFrame(players)
    df["now_cost_m"] = df["now_cost"] / 10
    df["value"] = df["total_points"] / df["now_cost_m"]
    squad = df.sort_values("value", ascending=False).head(15)
    return squad[["web_name","now_cost_m","total_points","form"]]

# --- Streamlit UI ---
st.title("⚽ Fantasy Premier League AI Helper")
st.write("Get smart squad recommendations based on live FPL stats.")

budget = st.number_input("Enter your budget (£m)", min_value=90.0, max_value=120.0, value=100.0, step=0.5)

if st.button("Build My Squad"):
    squad = recommend_team(budget)
    st.subheader("Recommended Squad")
    st.dataframe(squad)
