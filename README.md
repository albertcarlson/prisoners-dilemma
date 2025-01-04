# Prisoner's Dilemma Simulation

This repository contains a simulation of the prisoner's dilemma with various strategies, inspired by [this Veritasium video](https://www.youtube.com/watch?v=mScpHTIi-kM&t=995s), which is based on [Robert Axelrod's research](https://en.wikipedia.org/wiki/Robert_Axelrod).

## The Prisoner's Dilemma
I've always found the prisoner's dilemma fascinating. Since the Nash Equilibrium is not the best outcome, what is then the "best" thing to do? That, of course, depends on what others are doing. But does there still exist a reasonable definition of a strategy being "oftentimes better" than others? Maybe we can simulate it to get a better intuition for this problem (or at least have fun)? Well... that is the purpose of this repository. To simulate an ecosystem where various strategies ("species") compete and grow or decline in numbers, and maybe go extinct. They play multiple rounds against each other, remembering the opponent's previous moves and acting accordingly (depending on their `Strategy`).

You can change the `config.ini` file to change the rewards and penalties for each outcome (payoff matrix).

## Project Structure

- `config.ini`: Adjust payoff matrix and starting population.
- `catalogue/`: Contains the different prisoner's dilemma strategies ("species") that can be used in the simulation.
- `utils/`: Contains utility functions and data types for the simulation, such as Strategy, Player and Population classes.
- `tests/`: Contains functional, unit and integration tests for the simulation.
- `app.py`: The main streamlit application for running the simulation.

## Example

Below, I ran the simulation with only two possible strategies ("species“):
- Cooperators, who always cooperate no matter what; and
- Defectors, who always defect no matter what.

I started with a population of just 300 cooperators, with a mutation rate of 0.01.
As is evident in the screenshot (taken from the streamlit application), eventually
a defector appeared from mutation and begins to exploit the cooperators (due to how
the payoff matrix is structured), so it reproduces and grows in numbers. Eventually
the cooperators go extinct.

Furthermore, the overall population shrinks, since the defectors are "less efficient
overall" (as long as you specify the DEFECT-DEFECT reward in the payoff matrix to be
less than the COOP-COOP reward). This demonstrates the prisoner's dilemma and the
tragedy of the commons.

![Example of Cooperation vs Defection](images/example_coop_defect.png)

However, when we introduce a new species to the mix:

- Tit for Tat, who simply repeat the opponent's last move,

the defectors are suddenly challenged and end up going extinct, since they cannot
exploit these in the same way: When two Tit-for-Tats meet each other, they are so
productive cooperating with each other that they are able to get a high enough
score to outweigh the constant low scores against defectors. Interestingly, as
shown in the screenshot, it took quite a few generations for there to be enough
Tit-for-Tats for them to have enough others they could be productive with.

![Example of Cooperation vs Defection](images/example_coop_defect_titfortat.png)

(If you're wondering, the reason for the population increase around generation 30
to 40 was because I increased the overall food available in hopes it would speed
up the overtake of the Tit-for-Tats.)

## Running the Simulation

You need to have `uv` installed in your system. See instructions
[here](https://docs.astral.sh/uv/getting-started/installation/).
Thereafter, run 
```sh
uv run streamlit run app.py
```
to open the streamlit application with the simulation.
`uv` will automatically take care of dependencies.

## Testing

To run the tests to make sure everything works correctly, use the following command:
```sh
uv run pytest
```
Although I have set up a CI/CD pipeline with GitHub Actions, which runs the tests automatically on every push, but if you want you can run them locally to make sure everything works as expected.