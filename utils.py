# utils.py
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import chardet

def load_data(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(10000))
    encoding = result['encoding']
    df = pd.read_csv(file_path, encoding=encoding)
    df = df.dropna(how='all')
    return df

# def load_data(file_path):
#     # Use cp1252 to handle £ and other symbols from Excel
#     return pd.read_csv(file_path, encoding='cp1252')

def create_time_series_chart(df, x_col, y_col, title, y_label, color=None):
    """Create a time series line chart"""
    fig = px.line(df, x=x_col, y=y_col, title=title, 
                  color=color if color else None,
                  markers=True)
    fig.update_layout(yaxis_title=y_label)
    return fig

def create_bar_chart(df, x_col, y_col, title, x_label, y_label):
    """Create a bar chart"""
    fig = px.bar(df, x=x_col, y=y_col, title=title)
    fig.update_layout(xaxis_title=x_label, yaxis_title=y_label)
    return fig

def create_pie_chart(df, names_col, values_col, title):
    """Create a pie chart"""
    fig = px.pie(df, names=names_col, values=values_col, title=title)
    return fig

def create_gauge_chart(value, min_val, max_val, title):
    """Create a gauge chart"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={'axis': {'range': [min_val, max_val]},
               'bar': {'color': "darkblue"},
               'steps': [
                   {'range': [min_val, min_val + (max_val-min_val)*0.33], 'color': "red"},
                   {'range': [min_val + (max_val-min_val)*0.33, min_val + (max_val-min_val)*0.66], 'color': "yellow"},
                   {'range': [min_val + (max_val-min_val)*0.66, max_val], 'color': "green"}]}
    ))
    return fig