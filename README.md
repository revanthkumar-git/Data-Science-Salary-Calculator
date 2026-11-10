# Data Science Salary Calculator — Web App

This project recreates the core functionality of the supplied Excel salary calculator as an interactive Streamlit website.

## Files
- `app.py` — Streamlit web application
- `Salary_Calculator.xlsx` — Original workbook; the app reads the `Data` worksheet
- `requirements.txt` — Python dependencies

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Run `pip install -r requirements.txt`.
4. Run `streamlit run app.py`.
5. Open the local URL printed in the terminal (usually http://localhost:8501).

## Deploy
Push these files to a GitHub repository. On https://share.streamlit.io/, sign in with GitHub, create an app, select the repository and branch, and set the main file path to `app.py`.

## Notes
The app uses median and average values from the source salary columns. Yearly and hourly salary figures are kept separate. The app does not execute Excel formulas; it reads the source `Data` worksheet and calculates the displayed results in Python.
