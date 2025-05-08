import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

def cost_per_unit_dashboard():
    st.title("Manufacturing Cost per Unit Dashboard")
    
    # Load data
    df = load_data('./data/Manufacturing_Cost_per_Unit_Calculator.csv')
    
    # Extract monthly production data
    production_data = df.iloc[3:8, :6].dropna()
    production_data.columns = ['Metric', 'January', 'February', 'March', 'April', 'May']
    
    # Extract direct material costs
    material_costs = df.iloc[10:19, :7].dropna()
    material_costs.columns = ['Cost Type', 'January', 'February', 'March', 'April', 'May', 'Unnamed']
    
    # Extract direct labor costs
    labor_costs = df.iloc[21:34, :7].dropna()
    labor_costs.columns = ['Cost Type', 'January', 'February', 'March', 'April', 'May', 'Unnamed']
    
    # Extract manufacturing overhead
    overhead_costs = df.iloc[36:46, :7].dropna()
    overhead_costs.columns = ['Cost Type', 'January', 'February', 'March', 'April', 'May', 'Unnamed']
    
    # Extract total manufacturing cost
    total_cost = df.iloc[48:53, :7].dropna()
    total_cost.columns = ['Cost Type', 'January', 'February', 'March', 'April', 'May', 'Unnamed']
    
    # Extract cost distribution
    cost_distribution = df.iloc[55:60, :7].dropna()
    cost_distribution.columns = ['Category', 'January', 'February', 'March', 'April', 'May', 'Unnamed']
    
    # Extract productivity metrics
    productivity = df.iloc[62:66, :7].dropna()
    productivity.columns = ['Metric', 'January', 'February', 'March', 'April', 'May', 'Unnamed']
    
    # Extract cost efficiency
    cost_efficiency = df.iloc[68:72, :7].dropna()
    cost_efficiency.columns = ['Metric', 'January', 'February', 'March', 'April', 'May', 'Unnamed']
    
    # Extract cost variance
    cost_variance = df.iloc[74:79, :7].dropna()
    cost_variance.columns = ['Month', 'Actual', 'Budget', 'Variance (£)', 'Variance (%)', 'Unnamed1', 'Unnamed2']
    
    # Sidebar filters
    st.sidebar.header("Filters")
    selected_months = st.sidebar.multiselect(
        "Select Months",
        options=['January', 'February', 'March', 'April', 'May'],
        default=['January', 'February', 'March', 'April', 'May']
    )
    
    selected_cost_types = st.sidebar.multiselect(
        "Select Cost Types",
        options=['Direct Material', 'Direct Labor', 'Manufacturing Overhead'],
        default=['Direct Material', 'Direct Labor', 'Manufacturing Overhead']
    )
    
    # Prepare data for visualization
    months = ['January', 'February', 'March', 'April', 'May']
    
    # Get cost per unit data
    cost_per_unit = total_cost[total_cost['Cost Type'].str.strip() == 'Manufacturing Cost per Unit (£)']
    cost_per_unit = cost_per_unit.melt(id_vars='Cost Type', 
                                     value_vars=months,
                                     var_name='Month', 
                                     value_name='Cost per Unit (£)')
    
    # Filter based on selection
    cost_per_unit_filtered = cost_per_unit[cost_per_unit['Month'].isin(selected_months)]
    
    # KPI Cards
    st.subheader("Key Performance Indicators")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if not cost_per_unit_filtered.empty:
            avg_cost = pd.to_numeric(cost_per_unit_filtered['Cost per Unit (£)'], errors='coerce').mean()
            st.metric("Average Cost per Unit", f"£{avg_cost:.2f}")
        else:
            st.metric("Average Cost per Unit", "N/A")
    
    # More robust matching with strip and lower, to prevent whitespace/case issues
    with col2:
        labor_efficiency = cost_efficiency[cost_efficiency['Metric'].str.strip().str.lower() == 'labor efficiency (%)']
        if not labor_efficiency.empty:
            avg_labor_efficiency = pd.to_numeric(labor_efficiency[selected_months].values.flatten(), errors='coerce').mean()
            st.metric("Average Labor Efficiency", f"{avg_labor_efficiency:.2f}%")
        else:
            st.metric("Average Labor Efficiency", "N/A")
    
    with col3:
        material_yield = cost_efficiency[cost_efficiency['Metric'].str.strip().str.lower() == 'material yield (%)']
        if not material_yield.empty:
            avg_material_yield = pd.to_numeric(material_yield[selected_months].values.flatten(), errors='coerce').mean()
            st.metric("Average Material Yield", f"{avg_material_yield:.2f}%")
        else:
            st.metric("Average Material Yield", "N/A")
    
    # Cost per Unit Trend
    st.subheader("Manufacturing Cost per Unit Trend")
    fig = px.line(cost_per_unit_filtered, x='Month', y='Cost per Unit (£)', 
                  markers=True, title='Cost per Unit Over Time')
    st.plotly_chart(fig, use_container_width=True)
    
    # Cost Breakdown
    st.subheader("Cost Breakdown")
    dist_data = cost_distribution[cost_distribution['Category'].str.contains(r'Direct Material|Direct Labor|Manufacturing Overhead', case=False, na=False)]
    dist_data = dist_data.melt(id_vars='Category', 
                             value_vars=selected_months,
                             var_name='Month', 
                             value_name='Percentage')
    dist_data['Category'] = dist_data['Category'].str.replace(' (% of Total)', '', regex=False)
    
    fig = px.bar(dist_data, x='Month', y='Percentage', color='Category', 
                title='Cost Distribution by Category')
    st.plotly_chart(fig, use_container_width=True)
    
    # Cost Variance Analysis
    st.subheader("Cost Variance Analysis")
    fig = px.bar(cost_variance, x='Month', y='Variance (£)', 
                title='Variance from Budget (Actual - Budget)')
    st.plotly_chart(fig, use_container_width=True)
    
    # Productivity Metrics
    st.subheader("Productivity Metrics")
    prod_metrics = productivity[productivity['Metric'].str.strip().isin(['Labor Hours per Unit', 'Material Cost per Labor Hour', 'Value Added per Labor Hour (£)'])]
    prod_metrics = prod_metrics.melt(id_vars='Metric', 
                                    value_vars=selected_months,
                                    var_name='Month', 
                                    value_name='Value')
    fig = px.line(prod_metrics, x='Month', y='Value', color='Metric',
                 markers=True, title='Productivity Metrics Over Time')
    st.plotly_chart(fig, use_container_width=True)