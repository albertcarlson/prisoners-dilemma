from utils import PAYOFF_MATRIX, STARTING_POPULATION, Action, Player, Population, Strategy
from catalogue import EXAMPLE_SPECIES
from collections.abc import Iterable
import streamlit as st
import pandas as pd
import time



SPECIES: dict[str, Strategy] = EXAMPLE_SPECIES  # Change this if you want to use a different set of species



st.title("Prisoner's Dilemma Ecological Simulation")


st.subheader("Species to include")
st.write("Make your own species in `catalogue/example_species.py` (or make a new file here replicating the current pattern).")
species = st.multiselect("Select species", SPECIES)

# Drop-down menu with explanations of the species (from their docstrings)
with st.expander("Species explanations"):
    # A table with the species and their docstrings
    df = pd.DataFrame({
        "Species": [species_name for species_name in SPECIES],
        "Description": [SPECIES[species_name].__doc__ or "(No description, add a docstring)" for species_name in SPECIES],
    }).set_index("Species")
    st.table(df)

st.subheader("Payoff matrix")

st.write("The payoff matrix below shows your reward for the different outcomes. \
         The opponent's reward is mirrored (transposed). \
         A higher score is better for the player.")
df = pd.DataFrame({
    "Your Reward": ["You COOP", "You DEFECT"],
    "Opponent COOPS": [PAYOFF_MATRIX.get_reward(Action.COOP, Action.COOP)[0], PAYOFF_MATRIX.get_reward(Action.DEFECT, Action.COOP)[0]],
    "Opponent DEFECTS": [PAYOFF_MATRIX.get_reward(Action.COOP, Action.DEFECT)[0], PAYOFF_MATRIX.get_reward(Action.DEFECT, Action.DEFECT)[0]],
}).set_index("Your Reward")
st.table(df)
st.info("*At the moment, you need to change `config.ini` to adjust with the payoff matrix.*")



st.subheader("Simulation parameters")
advanced = st.checkbox("Advanced")
col1, col2, col3 = st.columns(3)
starting_population = col1.number_input("Starting population per species", value=STARTING_POPULATION, min_value=1, max_value=100, step=1, disabled=True)

rounds = col2.number_input("Rounds per battle", value=50, min_value=1, max_value=1000, step=5, disabled=not advanced)
overall_food = col3.number_input("Overall food available", value=100, min_value=0, max_value=2_000, step=25)
matchup_rate = col1.number_input("Matchup rate", value=1.0, min_value=0.0, max_value=1.0, step=0.01, disabled=not advanced)
mutation_rate = col2.number_input("Mutation rate", value=0.01, min_value=0.0, max_value=1.0, step=0.01)
can_mutate_parent = col3.checkbox("Can mutate parent", value=False)
can_mutate_into_extinct = col3.checkbox("Can mutate into extinct species", value=True, disabled=True)  # TODO: Implement this feature

st.write("Adjust overall food mid-game to introduce famines or periods of plenty.")
st.write("Adjust mutation rate to increase the probability that offspring uses a different strategy than its parent.")

st.write("\n")
st.write("***")
st.write("\n")



def generate_new_population(
        starting_population: int = starting_population, 
        species: Iterable[Strategy] = SPECIES.values()
) -> Population:
    players = []
    for strategy in species:
        for _ in range(starting_population):
            players.append(Player(strategy))
    return Population([players])


if len(species) == 0:
    st.info("To begin the simulation, select at least one species.")
    st.stop()


if "generation" not in st.session_state:
    st.session_state.generation = 0

if st.session_state.generation == 0:
    st.session_state.population = generate_new_population(species=[SPECIES[strategy] for strategy in species])


col1, col2 = st.columns(2)


# Initialize the last click time in session state if it doesn't exist
if 'last_click_time' not in st.session_state:
    st.session_state.last_click_time = 0


run_generation = col1.button("Run 1 generation")

if run_generation:
    
    current_time = time.time()
    # Check if enough time has passed since the last click,
    # to prevent threading issues (or something?)
    # with stqdm(total=1, desc="Running generation", key="generation") as progress:
    if current_time - st.session_state.last_click_time > 2:
        st.session_state.last_click_time = current_time
        st.session_state.generation += 1
        st.session_state.population.do_generation(
            matchup_rate=matchup_rate, 
            mutation_probability=mutation_rate, 
            mutation_strategies=[SPECIES[strategy] for strategy in species],
            rounds=rounds, 
            overall_food=overall_food,
            can_mutate_parent=can_mutate_parent,
        )
    else:
        st.warning("Please wait a few seconds before clicking the button simulation again. \
                    Quickly pressing causes issues with the function being called multiple \
                    times simultaneously, probably due to Streamlit's threading.")
        st.stop()


if col2.button("Reset simulation"):
    st.session_state.generation = 0
    st.session_state.population = generate_new_population(species=[SPECIES[strategy] for strategy in species])


st.write(f"Generation: {st.session_state.generation}")
st.write(f"Total population: {st.session_state.population.population_size}")
st.write(f"Population average age: {st.session_state.population.population_average_age:.2f}")


st.markdown("<h4 style='text-align: center;'>Current population counts</h4>", unsafe_allow_html=True)
st.bar_chart(st.session_state.population.get_population_counts(), x_label="Species", y_label="Count")

# Stacked area chart of population counts
if st.session_state.generation > 0:
    st.markdown("<h4 style='text-align: center;'>Development of population</h4>", unsafe_allow_html=True)
    # TODO: Add possibility of nicer coloring, e.g. color=["#0f4cd1", "#a8324a", "#32a852"][:(len(species))]
    st.area_chart([st.session_state.population.get_population_counts(gen) for gen in range(1, st.session_state.generation)], x_label="Generation", y_label="Count") 


