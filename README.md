# Data Science Salary Calculator

An interactive web application that explores data science salaries across job titles, countries, and employment types. The app is built with **Python**, **Streamlit**, **Pandas**, and **Plotly**, using the supplied Excel workbook as its data source.

## Live app

Once deployed, add your Streamlit Community Cloud URL here:

`https://<your-app-name>.streamlit.app`

## Dashboard features

- **Salary estimate:** View median and average salary plus the number of matching records for the selected job title, country, and employment type.
- **Interactive filters:** Filter by job title, country, employment type, and salary basis.
- **Yearly or hourly salaries:** Switch between yearly and hourly salary columns when the source data contains values.
- **World salary map:** Compare median salaries by country for the selected job title and employment type.
- **Salary comparisons:** Explore median salary by job title in the selected country and by employment type in that country.
- **Matching records:** Inspect the filtered job records and download them as a CSV file.

## Project files

```text
Data-Science-Salary-Calculator/
├── app.py                  # Streamlit application
├── Salary_Calculator.xlsx  # Source Excel workbook
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## Dataset

The application reads the `Data` worksheet from `Salary_Calculator.xlsx`.

The supplied workbook contains job-posting salary information, including job titles, countries, employment schedules, and yearly/hourly salary fields. The app calculates summary statistics from the available records.

**Data note:** Salary values are displayed in the currency represented by the source dataset. Missing salary values are excluded from the relevant salary calculations. Salary estimates are descriptive summaries of the supplied records, not guaranteed offers or official market rates.

## Run locally

### 1. Install Python

Install Python 3.10 or newer.

### 2. Download the project

Clone the repository:

```bash
git clone https://github.com/revanthkumar-git/Data-Science-Salary-Calculator.git
cd Data-Science-Salary-Calculator
```

Alternatively, download the repository as a ZIP file from GitHub and extract it.

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start the application

```bash
python -m streamlit run app.py
```

Open the local URL shown in the terminal. It is usually:

`http://localhost:8501`

## Deploy on Streamlit Community Cloud

1. Push `app.py`, `Salary_Calculator.xlsx`, and `requirements.txt` to a GitHub repository.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/).
3. Sign in with GitHub and choose **Create app**.
4. Select this repository and the `main` branch.
5. Set **Main file path** to `app.py`.
6. Select **Deploy**.

Streamlit installs the packages listed in `requirements.txt` and launches the application. The Excel workbook must remain in the repository alongside `app.py`, because the application reads it at startup.

## Technologies used

- **Python** — application logic
- **Streamlit** — web application interface
- **Pandas** — Excel data loading, filtering, and aggregation
- **Plotly Express** — interactive charts and world choropleth map
- **OpenPyXL** — reading the Excel workbook

## Important implementation notes

- The app reads the source `Data` worksheet; it does not run Excel formulas or reproduce Excel macros.
- The web filters and visualizations are implemented in Python and update based on the selected options.
- Yearly and hourly salary fields are treated separately.
- Country names in the workbook need to be recognized by Plotly's country-name map to appear on the choropleth.
- Do not commit confidential, personal, or licensed data to a public repository. Make sure you have permission to publish the workbook.

## Author

**Revanth Kumar**

GitHub: [@revanthkumar-git](https://github.com/revanthkumar-git)
