# Dice Roll

This repository contains a revision of one of my early programming projects, which involves generating random numbers using Python code and displaying them through either a graph or a web interface built with Django. This project also includes an optional feature that allows users to introduce a "bias" when rolling the dice, based on the comparison between the theoretical probability distribution of all possible outcomes and the actual distribution of past results.

## WebUI

The '**web**' directory contains the source code for a simple Django server that exposes both an API endpoint and a minimalist web page for generating random numbers. Users can run the server locally or use the docker compose file included in the root directory.

## Code

The '**src**' directory contains a standalone script written entirely in Python. Specifically, it includes functions for generating random numbers and visualizing their distributions using the Matplotlib library.

Additionally, it offers the ability to apply a "bias" to the generation process, whereby the probabilities of certain outcomes are adjusted based on historical data.

### Bias Mechanism

The bias mechanism works by comparing two probability distributions:

1. **All Outcome Distribution**: This represents the expected probability distribution of all possible outcomes if the generator were truly random (i.e., unbiased).

1. **Real Life Result Distribution**: This reflects the actual frequency at which specific outcomes have occurred in the past.

   > For example, if the last ten rolls resulted in five ones, four twos, and one three, then the distribution would show higher likelihood for those values compared to others.

By normalizing these distributions, users can observe how variations impact the generated numbers while still maintaining knowledge of the odd of each outcomes.

## Archive

Lastly, the archive directory stores snippets from the original implementation of this project. These files serve as documentation for future reference, allowing us to track progress made since its initial creation and providing valuable insights into potential improvements moving forward.

## Tips

For more guidance on operating this project, execute:

```bash
bash run.sh -h
```
