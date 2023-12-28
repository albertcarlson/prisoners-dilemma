# Prisoner's Dilemma Simulation

This repository contains a simulation of the prisoner's dilemma with various strategies, inspired by [this Veritasium video](https://www.youtube.com/watch?v=mScpHTIi-kM&t=995s), which is based on [Robert Axelrod's research](https://en.wikipedia.org/wiki/Robert_Axelrod).

## The Prisoner's Dilemma
The prisoner's dilemma is a game where two players have to decide whether to cooperate or defect. If both players cooperate, they both get a small reward. If both players defect, they both get a medium reward. If one player cooperates and the other defects, the cooperator gets a large penalty and the defector gets a large reward.

You can change the `config.ini` file to change the rewards and penalties for each outcome.

## Project Structure

- `README.md`: This file.
- `config.ini`: Configuration file for the simulation.
- `contest.py`: Contains a simple, one-round, contest to battle different strategies against once each other.
- `ecological_simulation.py`: Contains the logic for the ecological simulation, which is the main simulation of multiple generations where strategies that perform well grow in numbers and others go extinct.
- `catalogue/`: Contains the different species that can be used in the simulation.
- `utils/`: Contains utility functions and data types for the simulation.
- `tests/`: Contains unit tests for the simulation.
- `tmp/`: Contains temporary files generated during the simulation (might be removed later).

## Running the Simulation

To run the simulation, execute the `contest.py` or `ecological_simulation.py` script.

## Running the Tests

To run the tests to make sure everything works correctly, use the following command:

```sh
pytest
```