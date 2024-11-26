# Project Ice

[![Lint](https://github.com/jncraton/ice/actions/workflows/lint.yml/badge.svg)](https://github.com/jncraton/ice/actions/workflows/lint.yml)
[![Flask Tests](https://github.com/jncraton/ice/actions/workflows/test_flask.yml/badge.svg)](https://github.com/jncraton/ice/actions/workflows/test_flask.yml)
[![Static HTML Tests](https://github.com/jncraton/ice/actions/workflows/test_default.yml/badge.svg)](https://github.com/jncraton/ice/actions/workflows/test_default.yml)
[![Deploy to Pages](https://github.com/jncraton/ice/actions/workflows/pages.yml/badge.svg)](https://github.com/jncraton/ice/actions/workflows/pages.yml)

Project Ice or the Integrated Coding Experience is a new way to teach and practice programming in the classroom. The goals of project Ice are as follows:

1. Provide a tool for instructors to present, demonstrate, and build interactive activity to enhance their students learning
2. Provide a way for students' to practice their programming skills through instructor made activities or in a sandbox environment
3. Allow for a more integrated way to demonstrate programming skills

## Example Presentation

An [example presentation](https://jncraton.github.io/slide-decks/python-for) is provided that shows three different embedded interactive coding exercises within a larger learning segment focused on `for` loops in Python.

## Running

You can view a live version of the page at https://jncraton.github.io/ice/

## Install

1. Clone this repository
2. Open the command prompt in the project directory
3. Navigate to the app directory (`cd www`)
4. Run the command: `flask --app ../app/app.py run --port 8000`
5. Open your browser and navigate to [localhost:8000](localhost:5000)

## Running With Stats

1. Navigate to the website's directory (`cd www`)
2. Run the command: `flask --app ../app/app.py run --port 8000`
3. Open your browser and navigate to [localhost:8000](localhost:8000)

## Running Without Stats

1. Navigate to the website's directory (`cd www`)
2. Run the command: `python -m http.server`
3. Open your browser and navigate to [localhost:8000](localhost:8000)

## Testing

We use Playwright and PyTest to run unit tests.

1. (Optional) Create a new Python Virtual Environment (venv or conda works)
2. Install dependencies from `requirements.txt`
3. Open your command line in your project directory and run the following command
   `playwright install`
4. Run the server using the "running" directions above.
5. Navigate back to the project directory
6. Run `pytest`
