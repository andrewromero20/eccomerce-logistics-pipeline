# E-Commerce Logistics Pipeline & Delay Prediction App

An end-to-end data engineering, analytics, and machine learning pipeline built to optimize e-commerce logistics and predict delivery delays using the **Olist Brazilian E-Commerce Dataset** (+100k real-world orders).


## Project Architecture

1. **Data Ingestion & ETL (`src/etl.py`)**: Ingested and integrated a relational schema of 9 separate CSV tables into a local SQLite database using `SQLAlchemy` and `Pandas`.
2. **Exploratory Data Analysis & SQL (`notebooks/01_eda.ipynb`)**: Executed complex SQL joins and aggregations to analyze logistics SLAs, delivery performance, and customer satisfaction metrics.
3. **Predictive Modeling**: Trained a `Random Forest` classification model engineered to identify orders at high risk of shipping delays (achieving a **0.67 ROC-AUC** score).
4. **Interactive Web App (`app/app.py`)**: Built and deployed a dynamic dashboard using `Streamlit` featuring real-time KPI tracking and a machine learning risk simulator for new orders.


## Tech Stack & Tools

* **Language:** Python 3.10+
* **Database & ORM:** SQLite, SQLAlchemy
* **Data Processing & Analytics:** Pandas, NumPy
* **Data Visualization:** Plotly Express
* **Machine Learning:** Scikit-Learn, Joblib
* **Deployment & UI:** Streamlit


## Key Business Insights

* **Delay Rate:** Exactly **8.11%** of fulfilled orders experienced logistics delays beyond the promised delivery date.
* **Customer Satisfaction Impact:** Order delays severely impact customer retention, dropping average review scores from **~4.2 stars** (on-time) down to **~2.4 stars** (delayed).
* **Feature Importance:** Freight ratio (shipping cost relative to item price), package volume ($\text{length} \times \text{width} \times \text{height}$), and product price were identified as the strongest predictors of delivery delays.

## Repository Structure

eccomerce_olist_pipeline/app/app.py #Streamlit web aplication & simulator
eccomerce_olist_pipeline/data/raw/  #Source CSV files (Olist dataset)
eccomerce_olist_pipeline/data/model_rf.joblib     # Serialized Random Forest model
eccomerce_olist_pipeline/notebook/01_eda.ipynb        # Data exploration, SQL queries & ML training
eccomerce_olist_pipeline/src/etl.py              # Automated ETL script for SQLite ingestion
eccomerce_olist_pipeline/requirements.txt             # Python package dependencies
