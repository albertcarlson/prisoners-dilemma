from utils import PAYOFF_MATRIX, Action
from catalogue import EXAMPLE_SPECIES
import streamlit as st
import random



st.title("Prisoner's Dilemma Simulation")



small_example_keys = random.sample(sorted(EXAMPLE_SPECIES), 6)
small_example = {k: EXAMPLE_SPECIES[k] for k in small_example_keys}


st.subheader("Species to include")
species = st.multiselect("Select species", EXAMPLE_SPECIES, default=small_example)



st.subheader("Initial population counts")
col1, col2, col3 = st.columns(3)
counts = {}
for specie in species[::3]:
    counts[specie] = col1.number_input(specie, value=10, min_value=0, max_value=100, step=1)
for specie in species[1::3]:
    counts[specie] = col2.number_input(specie, value=10, min_value=0, max_value=100, step=1)
for specie in species[2::3]:
    counts[specie] = col3.number_input(specie, value=10, min_value=0, max_value=100, step=1)



st.subheader("Payoff matrix")
st.warning("*This interface doesn't work yet. Adjust `config.ini` to change with the payoff matrix.*")
st.write("A higher score is better for the player.")
col1, col2 = st.columns(2)
payoff_CC = col1.number_input("You COOP, Opponent COOPS",     value=PAYOFF_MATRIX[(Action.COOP, Action.COOP)][0], min_value=-10, max_value=10, step=1, disabled=True)
payoff_CD = col2.number_input("You COOP, Opponent DEFECTS",   value=PAYOFF_MATRIX[(Action.COOP, Action.DEFECT)][0], min_value=-10, max_value=10, step=1, disabled=True)
payoff_DC = col1.number_input("You DEFECT, Opponent COOPS",   value=PAYOFF_MATRIX[(Action.DEFECT, Action.COOP)][0], min_value=-10, max_value=10, step=1, disabled=True)
payoff_DD = col2.number_input("You DEFECT, Opponent DEFECTS", value=PAYOFF_MATRIX[(Action.DEFECT, Action.DEFECT)][0], min_value=-10, max_value=10, step=1, disabled=True)



st.subheader("Rounds per generation")
rounds = st.number_input("Number of rounds per generation", value=50, min_value=1, max_value=1000, step=5)
st.write("The scoring is normalized, i.e. is an average for the rounds.")


st.write("\n")
st.write("***")
st.write("\n")



col1, col2 = st.columns(2)
generation = st.session_state.get("generation", 0)
col1.button("Run 1 generation")
col2.button("Run 5 generations")

st.write(f"Generation: {generation}")
st.write(f"Total population: {sum(counts.values())}")



st.markdown("<h3 style='text-align: center;'>Population counts</h3>", unsafe_allow_html=True)
st.bar_chart(counts, x_label="Species", y_label="Count")