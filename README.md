## Polling Average Model

A program that generates a polling average, weighted by sample size, poll age, and quality score for the pollster.

## Setup

1. clone this repository
2. create a virtual environment:
   `python -m venv venv`
3. activate the virtual environment:
   - windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. install dependencies:
   `pip install -r requirements.txt`
5. run the model
   `python3 -m models.main --state [STATE]`
   (optionally, include --step-days [DAYS], which defaults to 1)

## Data

Polls last updated 11/5 - Data from FiveThirtyEight, Pollscore from 538

## Example State Average

![Polling Average](https://github.com/user-attachments/assets/633234cf-272b-4925-ae79-f0c0e967a279)
