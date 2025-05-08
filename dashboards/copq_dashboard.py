# dashboards/copq_dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, create_time_series_chart, create_bar_chart, create_pie_chart

def copq_dashboard():
    st.title("Cost of Poor Quality (COPQ) Dashboard")
    
    # Load data
    df = load_data('./data/COPQ.csv')
    
    # Extract basic production data
    production_data = df.iloc[3:8, :4].dropna()
    production_data.columns = ['Metric', 'Value', 'Unnamed1', 'Unnamed2']
    
    # Extract scrap costs
    scrap_costs = df.iloc[10:17, :4].dropna()
    scrap_costs.columns = ['Metric', 'Value', 'Unnamed1', 'Unnamed2']
    
    # Extract rework costs
    rework_costs = df.iloc[19:27, :4].dropna()
    rework_costs.columns = ['Metric', 'Value', 'Unnamed1', 'Unnamed2']
    
    # Extract warranty costs
    warranty_costs = df.iloc[29:37, :4].dropna()
    warranty_costs.columns = ['Metric', 'Value', 'Unnamed1', 'Unnamed2']
    
    # Extract total COPQ
    total_copq = df.iloc[39:44, :4].dropna()
    total_copq.columns = ['Metric', 'Value', 'Unnamed1', 'Unnamed2']
    
    # Extract cost breakdown
    cost_breakdown = df.iloc[46:51, :4].dropna()
    cost_breakdown.columns = ['Category', 'Cost (£)', '% of Total COPQ', '% of Revenue']
    
    # Extract monthly tracking
    monthly_tracking = df.iloc[53:60, :5].dropna()
    monthly_tracking.columns = ['Month', 'Total Units', 'Defective Units', 'COPQ (£)', 'COPQ % of Revenue']
    
    # Extract defect categories
    defect_categories = df.iloc[72:77, :4].dropna()
    defect_categories.columns = ['Defect Type', 'Number of Occurrences', '% of Total Defects', 'Associated Cost (£)']
    
    # Sidebar filters
    st.sidebar.header("Filters")
    selected_months = st.sidebar.multiselect(
        "Select Months",
        options=monthly_tracking['Month'].unique(),
        default=monthly_tracking['Month'].unique()
    )
    
    selected_defect_types = st.sidebar.multiselect(
        "Select Defect Types",
        options=defect_categories['Defect Type'].unique(),
        default=defect_categories['Defect Type'].unique()
    )
    
    # Filter data based on selection
    monthly_tracking_filtered = monthly_tracking[monthly_tracking['Month'].isin(selected_months)]
    defect_categories_filtered = defect_categories[defect_categories['Defect Type'].isin(selected_defect_types)]
    
    # KPI Cards
    st.subheader("Key Performance Indicators")
    col1, col2, col3 = st.columns(3)

    with col1:
        avg_copq = pd.to_numeric(monthly_tracking_filtered['COPQ (£)'], errors='coerce').mean()
        st.metric("Average COPQ", f"£{avg_copq:,.2f}" if not pd.isna(avg_copq) else "N/A")

    with col2:
        total_units = pd.to_numeric(monthly_tracking_filtered['Total Units'], errors='coerce').sum()
        defective_units = pd.to_numeric(monthly_tracking_filtered['Defective Units'], errors='coerce').sum()
        if total_units != 0:
            avg_defect_rate = (defective_units / total_units) * 100
            st.metric("Average Defect Rate", f"{avg_defect_rate:.2f}%")
        else:
            st.metric("Average Defect Rate", "N/A")

    with col3:
        avg_copq_percent = pd.to_numeric(monthly_tracking_filtered['COPQ % of Revenue'], errors='coerce').mean()
        st.metric("COPQ as % of Revenue", f"{avg_copq_percent:.2f}%" if not pd.isna(avg_copq_percent) else "N/A")
    
    # COPQ Trend
    st.subheader("COPQ Trend Over Time")
    fig = px.line(monthly_tracking_filtered, x='Month', y=['COPQ (£)', 'COPQ % of Revenue'], 
                  markers=True, title='COPQ Over Time')
    st.plotly_chart(fig, use_container_width=True)
    
    # Cost Breakdown
    st.subheader("COPQ Breakdown")
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(cost_breakdown, names='Category', values='Cost (£)', title='COPQ by Category')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(defect_categories_filtered, x='Defect Type', y='Associated Cost (£)', 
                    title='Cost by Defect Type')
        st.plotly_chart(fig, use_container_width=True)
    
    # Defect Analysis
    st.subheader("Defect Analysis")
    fig = px.bar(defect_categories_filtered, x='Defect Type', y='Number of Occurrences',
                title='Defect Occurrences by Type')
    st.plotly_chart(fig, use_container_width=True)
    
    # Cost Details
    st.subheader("Cost Details")
    
    scrap_total = float(scrap_costs[scrap_costs['Metric'] == 'Total Scrap Cost (£)']['Value'].values[0])
    rework_total = float(rework_costs[rework_costs['Metric'] == 'Total Rework Cost (£)']['Value'].values[0])
    warranty_total = float(warranty_costs[warranty_costs['Metric'] == 'Total Warranty Cost (£)']['Value'].values[0])
    
    cost_df = pd.DataFrame({
        'Category': ['Scrap', 'Rework', 'Warranty'],
        'Cost (£)': [scrap_total, rework_total, warranty_total]
    })
    
    fig = px.bar(cost_df, x='Category', y='Cost (£)', title='Detailed Cost Breakdown')
    st.plotly_chart(fig, use_container_width=True)