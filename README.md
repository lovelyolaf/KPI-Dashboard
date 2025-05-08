# Manufacturing KPI Dashboards

This project implements three interactive KPI dashboards for manufacturing performance monitoring.

## Dashboards Included

1. **Overall Equipment Effectiveness (OEE) Dashboard**
   - KPIs: OEE (%), TEEP (%), Downtime Cost
   - Formulas:
     - OEE = Availability × Performance × Quality
     - TEEP = Utilization × OEE
   - Filters: Month selection

2. **Cost of Poor Quality (COPQ) Dashboard**
   - KPIs: Total COPQ, Defect Rate, COPQ as % of Revenue
   - Formulas:
     - COPQ = Scrap Cost + Rework Cost + Warranty Cost
     - Defect Rate = (Defective Units / Total Units) × 100
   - Filters: Month, Defect Type

3. **Manufacturing Cost per Unit Dashboard**
   - KPIs: Cost per Unit, Labor Efficiency, Material Yield
   - Formulas:
     - Cost per Unit = (Materials + Labor + Overhead) / Units Produced
     - Labor Efficiency = (Standard Hours / Actual Hours) × 100
   - Filters: Month, Cost Type

## Setup Instructions

1. Clone the repository
2. Install requirements: `pip install -r requirements.txt`
3. Run the application: `streamlit run main.py`

## Data Requirements

Place your data files in the `data/` directory with the following names:
- OEE data: `OEE_Data.csv`
- COPQ data: `COPQ.csv`
- Cost per Unit data: `Manufacturing_Cost_per_Unit_Calculator.csv`

## Assumptions

1. Data files follow the exact format of the provided sample files
2. All currency values are in GBP (£)
3. Time periods are monthly