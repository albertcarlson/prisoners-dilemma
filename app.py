from utils import PAYOFF_MATRIX, STARTING_POPULATION, Action, Player, Population, Strategy
from catalogue import EXAMPLE_SPECIES
from collections.abc import Iterable
#from stqdm import stqdm
import streamlit as st
import pandas as pd
#import time




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
st.info("*At the moment, you need to change `config.ini` to adjust with the payoff matrix.*")



st.subheader("Simulation parameters")
advanced = st.checkbox("Advanced")
col1, col2, col3 = st.columns(3)
starting_population = col1.number_input("Starting population per species", value=STARTING_POPULATION, min_value=1, max_value=100, step=1, disabled=True)

rounds = col2.number_input("Rounds per battle", value=50, min_value=1, max_value=1000, step=5, disabled=not advanced)
overall_food = col3.number_input("Overall food available", value=100, min_value=0, max_value=2_000, step=25)
matchup_rate = col2.number_input("Matchup rate", value=1.0, min_value=0.0, max_value=1.0, step=0.01, disabled=not advanced)
mutation_rate = col3.number_input("Mutation rate", value=0.01, min_value=0.0, max_value=1.0, step=0.01)

st.write("Adjust overall food mid-game to introduce famines or periods of plenty.")
st.write("Adjust mutation rate to increase the probability that offspring uses a different strategy than its parent.")

st.write("\n")
st.write("***")
st.write("\n")



def generate_new_population(
        starting_population: int = starting_population, 
        species: Iterable[Strategy] = EXAMPLE_SPECIES.values()
) -> Population:
    players = []
    for strategy in species[:1]:
        for _ in range(starting_population):
            players.append(Player(strategy))
    return Population([players])


if len(species) == 0:
    st.info("To begin the simulation, select at least one species.")
    st.stop()


if "generation" not in st.session_state:
    st.session_state.generation = 0

if st.session_state.generation == 0:
    st.session_state.population = generate_new_population(species=[EXAMPLE_SPECIES[strategy] for strategy in species])


col1, col2, col3 = st.columns(3)


if col1.button("Run 1 generation"):
    st.session_state.generation += 1
    st.session_state.population.do_generation(
        matchup_rate=matchup_rate, 
        mutation_probability=mutation_rate, 
        mutation_strategies=[EXAMPLE_SPECIES[strategy] for strategy in species],
        rounds=rounds, 
        overall_food=overall_food
    )

if col2.button("Run 5 generations"):
    st.session_state.generation += 5
    for _ in range(5):
        st.session_state.population.do_generation(
            matchup_rate=matchup_rate, 
            mutation_probability=mutation_rate, 
            mutation_strategies=[EXAMPLE_SPECIES[strategy] for strategy in species],
            rounds=rounds, 
            overall_food=overall_food
        )

if col3.button("Reset simulation"):
    st.session_state.generation = 0
    st.session_state.population = generate_new_population(species=[EXAMPLE_SPECIES[strategy] for strategy in species])

st.write(f"Generation: {st.session_state.generation}")
st.write(f"Total population: {st.session_state.population.population_size}")
st.write(f"Population average age: {st.session_state.population.population_average_age}")

st.write(f"Mutation probability: {mutation_rate}, Matchup rate: {matchup_rate}, Rounds per battle: {rounds}, Overall food: {overall_food}")

st.markdown("<h4 style='text-align: center;'>Current population counts</h4>", unsafe_allow_html=True)
st.bar_chart(st.session_state.population.get_population_counts(), x_label="Species", y_label="Count")


# Stacked area chart of population counts
if st.session_state.generation > 0:
    st.markdown("<h4 style='text-align: center;'>Development of population</h4>", unsafe_allow_html=True)
    st.area_chart([st.session_state.population.get_population_counts(gen) for gen in range(1, st.session_state.generation)], x_label="Generation", y_label="Count")

