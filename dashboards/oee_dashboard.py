# dashboards/oee_dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from utils import load_data, create_gauge_chart

def clean_percentage_column(series):
    """Remove percentage signs and convert to float"""
    return series.str.replace('%', '').astype(float)

def create_hybrid_layout(is_mobile):
    """Create a responsive layout that works on both mobile and desktop"""
    if is_mobile:
        return {'chart_height': 300, 'cols': 1, 'margin': dict(l=20, r=20, t=40, b=20)}
    else:
        return {'chart_height': 400, 'cols': 2, 'margin': dict(l=50, r=50, t=80, b=50)}

def detect_mobile():
    """Check if user is on mobile device"""
    try:
        user_agent = st.get_option('browser.userAgent').lower()
    except:
        user_agent = ""
    mobile_keywords = ['mobile', 'android', 'iphone']
    return any(keyword in user_agent for keyword in mobile_keywords)

def show_oee_dashboard():
    """Main function to display the OEE dashboard"""
    # Initialize mobile detection
    is_mobile = detect_mobile()
    layout = create_hybrid_layout(is_mobile)
    
    st.title("Advanced OEE Analytics Dashboard")
    
    # Load and preprocess data
    @st.cache_data
    def load_and_preprocess_data():
        df = load_data('data/OEE_Data.csv')
        
        # Enhanced data with simulated shift/line/operator data
        months = ['January', 'February', 'March', 'April', 'May']
        shifts = ['A', 'B', 'C']
        lines = ['Line 1', 'Line 2', 'Line 3']
        operators = ['OP1', 'OP2', 'OP3', 'OP4', 'OP5']
        
        # Create detailed synthetic data
        detailed_data = []
        for month in months:
            for shift in shifts:
                for line in lines:
                    for operator in operators:
                        detailed_data.append({
                            'Month': month,
                            'Shift': shift,
                            'Line': line,
                            'Operator': operator,
                            'Availability': round(80 + (np.random.rand() * 15), 2),
                            'Performance': round(85 + (np.random.rand() * 10), 2),
                            'Quality': round(95 + (np.random.rand() * 4), 2),
                            'Downtime': round(30 + (np.random.rand() * 120), 0),
                            'Defects': round(np.random.rand() * 50, 0)
                        })
        
        detailed_df = pd.DataFrame(detailed_data)
        detailed_df['OEE'] = (detailed_df['Availability'] * detailed_df['Performance'] * detailed_df['Quality']) / 1000000
        
        # Add root cause data
        root_causes = [
            'Machine Breakdown', 'Changeover', 'Material Shortage', 
            'Operator Error', 'IT Issues', 'Power Outage', 'PM Delay'
        ]
        detailed_df['Root Cause'] = np.random.choice(root_causes, size=len(detailed_df))
        
        return df, detailed_df
    
    df, detailed_df = load_and_preprocess_data()
    
    # Sidebar filters - enhanced with drill-down options
    st.sidebar.header("Drill-Down Filters")
    
    # Date range filter (simulated)
    min_date = datetime(2023, 1, 1)
    max_date = datetime(2023, 5, 31)
    selected_dates = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Multi-level filters
    selected_months = st.sidebar.multiselect(
        "Select Months",
        options=detailed_df['Month'].unique(),
        default=detailed_df['Month'].unique()
    )
    
    selected_shifts = st.sidebar.multiselect(
        "Select Shifts",
        options=detailed_df['Shift'].unique(),
        default=detailed_df['Shift'].unique()
    )
    
    selected_lines = st.sidebar.multiselect(
        "Select Production Lines",
        options=detailed_df['Line'].unique(),
        default=detailed_df['Line'].unique()
    )
    
    selected_operators = st.sidebar.multiselect(
        "Select Operators",
        options=detailed_df['Operator'].unique(),
        default=detailed_df['Operator'].unique()
    )
    
    # Apply filters
    filtered_df = detailed_df[
        (detailed_df['Month'].isin(selected_months)) &
        (detailed_df['Shift'].isin(selected_shifts)) &
        (detailed_df['Line'].isin(selected_lines)) &
        (detailed_df['Operator'].isin(selected_operators))
    ]
    
    # KPI Section - Hybrid layout with gauges and metrics
    st.subheader("Overall Equipment Effectiveness")
    
    if layout['cols'] == 2:
        col1, col2, col3, col4 = st.columns(4)
    else:
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
    
    with col1:
        avg_oee = filtered_df['OEE'].mean() * 100
        st.plotly_chart(
            create_gauge_chart(avg_oee, 0, 100, "Average OEE"),
            use_container_width=True,
            height=layout['chart_height']
        )
    
    with col2:
        avg_availability = filtered_df['Availability'].mean()
        st.plotly_chart(
            create_gauge_chart(avg_availability, 0, 100, "Average Availability"),
            use_container_width=True,
            height=layout['chart_height']
        )
    
    with col3:
        avg_performance = filtered_df['Performance'].mean()
        st.plotly_chart(
            create_gauge_chart(avg_performance, 0, 100, "Average Performance"),
            use_container_width=True,
            height=layout['chart_height']
        )
    
    with col4:
        avg_quality = filtered_df['Quality'].mean()
        st.plotly_chart(
            create_gauge_chart(avg_quality, 0, 100, "Average Quality"),
            use_container_width=True,
            height=layout['chart_height']
        )
    
    # Trend Analysis Section
    st.subheader("Trend Analysis")
    
    # Create trend data
    trend_data = filtered_df.groupby('Month').agg({
        'OEE': 'mean',
        'Availability': 'mean',
        'Performance': 'mean',
        'Quality': 'mean',
        'Downtime': 'sum',
        'Defects': 'sum'
    }).reset_index()
    
    if layout['cols'] == 2:
        trend_col1, trend_col2 = st.columns(2)
    else:
        trend_col1 = st.columns(1)[0]
        trend_col2 = st.columns(1)[0]
    
    with trend_col1:
        fig = px.line(trend_data, x='Month', y=['OEE', 'Availability', 'Performance', 'Quality'],
                     title='OEE Components Trend', markers=True)
        fig.update_layout(height=layout['chart_height'], margin=layout['margin'])
        st.plotly_chart(fig, use_container_width=True)
    
    with trend_col2:
        fig = px.bar(trend_data, x='Month', y='Downtime', 
                    title='Total Downtime by Month', color='Month')
        fig.update_layout(height=layout['chart_height'], margin=layout['margin'])
        st.plotly_chart(fig, use_container_width=True)
    
    # Root Cause Analysis - Pareto Chart
    st.subheader("Root Cause Analysis")
    
    root_cause_data = filtered_df.groupby('Root Cause').agg({
        'Downtime': 'sum',
        'Defects': 'sum'
    }).reset_index().sort_values('Downtime', ascending=False)
    
    root_cause_data['Cumulative %'] = (root_cause_data['Downtime'].cumsum() / root_cause_data['Downtime'].sum()) * 100
    
    if layout['cols'] == 2:
        pareto_col1, pareto_col2 = st.columns(2)
    else:
        pareto_col1 = st.columns(1)[0]
        pareto_col2 = st.columns(1)[0]
    
    with pareto_col1:
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=root_cause_data['Root Cause'],
            y=root_cause_data['Downtime'],
            name='Downtime (min)',
            marker_color='indianred'
        ))
        
        fig.add_trace(go.Scatter(
            x=root_cause_data['Root Cause'],
            y=root_cause_data['Cumulative %'],
            name='Cumulative %',
            yaxis='y2',
            line=dict(color='royalblue', width=2)
        ))
        
        fig.update_layout(
            title='Downtime Pareto Analysis',
            yaxis=dict(title='Downtime (minutes)'),
            yaxis2=dict(
                title='Cumulative %',
                overlaying='y',
                side='right',
                range=[0, 100]
            ),
            height=layout['chart_height'],
            margin=layout['margin']
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with pareto_col2:
        fig = px.sunburst(
            filtered_df,
            path=['Root Cause', 'Line', 'Shift'],
            values='Defects',
            title='Defect Distribution by Root Cause'
        )
        fig.update_layout(height=layout['chart_height'], margin=layout['margin'])
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed Data View
    st.subheader("Detailed Performance Data")
    st.dataframe(
        filtered_df.sort_values('OEE', ascending=False),
        height=400,
        use_container_width=True
    )
    
    # Download button for filtered data
    st.download_button(
        label="Download Filtered Data",
        data=filtered_df.to_csv(index=False).encode('utf-8'),
        file_name='oee_filtered_data.csv',
        mime='text/csv'
    )