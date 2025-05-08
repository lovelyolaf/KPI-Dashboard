# main.py
import streamlit as st
from dashboards.oee_dashboard import show_oee_dashboard
# from dashboards.copq_dashboard import show_copq_dashboard
# from dashboards.cost_per_unit_dashboard import show_cost_per_unit_dashboard

# Set page config once at the start of the app
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
    page_title="Manufacturing KPI Dashboards"
)

def main():
    st.sidebar.title("Manufacturing KPI Dashboards")
    
    dashboard_options = {
        "Overall Equipment Effectiveness (OEE)": show_oee_dashboard,
        # "Cost of Poor Quality (COPQ)": show_copq_dashboard,
        # "Manufacturing Cost per Unit": show_cost_per_unit_dashboard
    }
    
    selected_dashboard = st.sidebar.selectbox(
        "Select Dashboard",
        list(dashboard_options.keys())
    )
    
    # Call the selected dashboard function
    dashboard_options[selected_dashboard]()

if __name__ == "__main__":
    main()