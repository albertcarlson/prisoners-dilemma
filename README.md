# Prisoner's Dilemma Simulation

This repository contains a simulation of the prisoner's dilemma with various strategies, inspired by [this Veritasium video](https://www.youtube.com/watch?v=mScpHTIi-kM&t=995s), which is based on [Robert Axelrod's research](https://en.wikipedia.org/wiki/Robert_Axelrod).

## The Prisoner's Dilemma
I've always found the prisoner's dilemma fascinating due to its intricate mathematical dynamics. The nuanced interplay of cooperation, defection, and the resulting rewards and penalties adds a captivating layer of complexity to the decision-making process, where the Nash Equilibrium is not the best outcome.

You can change the `config.ini` file to change the rewards and penalties for each outcome, experimenting with stuff like asymmetric rewards.

## Project Structure

- `README.md`: This file.
- `config.ini`: Configuration file for the simulation.
- `contest.py`: Contains a simple, one-round, contest to battle different strategies against each other.
- `ecological_simulation.py`: Contains the logic for the ecological simulation, which is the main simulation of multiple generations where strategies that perform well grow in numbers and others go extinct.
- `catalogue/`: Contains the different species that can be used in the simulation.
- `utils/`: Contains utility functions and data types for the simulation.
- `tests/`: Contains functional, unit and integration tests for the simulation.
- `tmp/`: Contains temporary files generated during the simulation (might be removed later).

## Running the Simulation

To run the simulations, execute the `contest.py` or `ecological_simulation.py` scripts.

## Running the Tests

To run the tests to make sure everything works correctly, use the following command:

```sh
pytest
```

Although I have set up a CI/CD pipeline with GitHub Actions, which runs the tests automatically on every push, but if you want you can run them locally to make sure everything works as expected.