# Prisoner's Dilemma Simulation

This repository contains a simulation of the prisoner's dilemma with various strategies, inspired by [this Veritasium video](https://www.youtube.com/watch?v=mScpHTIi-kM&t=995s), which is based on [Robert Axelrod's research](https://en.wikipedia.org/wiki/Robert_Axelrod).

## The Prisoner's Dilemma
I've always found the prisoner's dilemma fascinating. Since the Nash Equilibrium is not the best outcome, what is then the "best" thing to do? That, of course, depends on what others are doing (for a given strategy there always exists another strategy that is at least as good, so the "better than"-relation is intransitive). But does there still exist a reasonable definition of a strategy being "oftentimes better" than others? Maybe we can simulate it to get a better intuition for this problem (or at least have fun)? Well... that is the purpose of this repository. To simulate an ecosystem with various strategies ("species") compete and grow or decline in numbers, maybe going extinct. (Although they don't evovle -- I have to scope this project somewhere.)

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

Fortunately, unlike most other repositories, in this one you don't need to set up any `credentials.json` or API key environment variables etc. to run the code. You can just clone the repository and run!

## Running the Simulation

To run the simulations, execute the `contest.py` or `ecological_simulation.py` scripts.

## Running the Tests

To run the tests to make sure everything works correctly, use the following command:

```sh
pytest
```

Although I have set up a CI/CD pipeline with GitHub Actions, which runs the tests automatically on every push, but if you want you can run them locally to make sure everything works as expected.