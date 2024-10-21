# Project Ice

Project Ice or the Integrated Coding Experience is a new way to teach and practice programming in the classroom. The goals of project Ice are as follows:

1. Provide a tool for instructors to present, demonstrate, and build interactive activity to enhance their students learning
2. Provide a way for students' to practice their programming skills through instructor made activities or in a sandbox environment
3. Allow for a more integrated way to demonstrate programming skills

## Install and Run

1. Clone this repository 
2. Open the command prompt in the project directory
3. Run `python -m http.server`
4. Navigate to [localhost:8000](localhost:8000)

## Testing

We use Playwright and PyTest to run unit tests.

1. (Optional) Create a new Python Virtual Environment (venv or conda works)
2. Install dependencies from `requirements.txt`
3. Open your command line in your project directory and run the following command
   `playwright install`
4. Run `pytest`
