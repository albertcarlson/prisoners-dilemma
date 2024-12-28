from utils import PAYOFF_MATRIX, STARTING_POPULATION, Action
from catalogue import EXAMPLE_SPECIES
from stqdm import stqdm
import streamlit as st
import pandas as pd
import time

st.title("Prisoner's Dilemma Ecological Simulation")


st.subheader("Species to include")
st.write("Make your own species in `catalogue/example_species.py` (or make a new file here replicating the current pattern).")
species = st.multiselect("Select species", EXAMPLE_SPECIES)



st.subheader("Payoff matrix")

st.write("The payoff matrix below shows your reward for the different outcomes. \
         The opponent's reward is mirrored (transposed). \
         A higher score is better for the player.")
df = pd.DataFrame({
    "Your Reward": ["You COOP", "You DEFECT"],
    "Opponent COOPS": [PAYOFF_MATRIX[(Action.COOP, Action.COOP)][0], PAYOFF_MATRIX[(Action.DEFECT, Action.COOP)][0]],
    "Opponent DEFECTS": [PAYOFF_MATRIX[(Action.COOP, Action.DEFECT)][0], PAYOFF_MATRIX[(Action.DEFECT, Action.DEFECT)][0]],
}).set_index("Your Reward")
st.table(df)
st.write("*At the moment, you need to change `config.ini` to adjust with the payoff matrix.*")



st.subheader("Simulation parameters")
col1, col2, col3, col4 = st.columns(4)
starting_population = col1.number_input("Starting population per species", value=STARTING_POPULATION, min_value=1, max_value=100, step=1, disabled=True)

rounds = col2.number_input("Rounds per battle", value=50, min_value=1, max_value=1000, step=5)
st.write("The scoring is normalized, i.e. is an average for the rounds. Therefore, 100 and 500 rounds are probably the same.")

overall_food = col3.number_input("Overall food available", value=1_000, min_value=0, max_value=10_000, step=100)

matchup_rate = col4.number_input("Matchup rate", value=1.0, min_value=0.0, max_value=1.0, step=0.01)
st.write("Adjust overall food mid-game to introduce famines or periods of plenty.")

st.write("*At the moment, you need to change `config.ini` to adjust the starting population per species.*")


st.write("\n")
st.write("***")
st.write("\n")



col1, col2 = st.columns(2)
generation = st.session_state.get("generation", 0)
col1.button("Run 1 generation")
col2.button("Run 5 generations")

st.write(f"Generation: {generation}")
# st.write(f"Total population: {sum(counts.values())}")



st.markdown("<h4 style='text-align: center;'>Current population counts</h4>", unsafe_allow_html=True)
st.bar_chart([5, 3, 7, 2, 6], x_label="Species", y_label="Count")