# Market Data Validation Pipeline

**A professional Python-based tool for validating and cleaning high-frequency market data**  
Built as a portfolio project to demonstrate skills required for the **Analyst (with Python)** role in quantitative trading firms.

This end-to-end pipeline simulates real-world tasks performed by analysts supporting quantitative researchers:
- Discovering and profiling raw tick-level data
- Detecting anomalies and data quality issues
- Cleaning datasets with traceability and audit logs
- Delivering research-ready data via an interactive web tool

## Key Features

- Realistic synthetic HFT tick data generation (timestamp, exchange, price, volume) with injected real-world errors
- Comprehensive initial profiling and anomaly detection (missing values, outliers, negatives, duplicates, timestamp gaps)
- Robust cleaning pipeline with interpolation, outlier capping, deduplication, and invalid row handling
- Full audit trail with dynamic reports and logs
- Interactive **Streamlit web app** for ad-hoc data validation and cleaning (upload → profile → clean → download)

## Tech Stack

- **Python** – core scripting and automation
- **Pandas** & **NumPy** – data manipulation, numerical computations, statistical validation
- **Matplotlib** – visualization in reports
- **Streamlit** – interactive dashboard for exploratory analysis and tool delivery
