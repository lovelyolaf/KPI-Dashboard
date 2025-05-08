# inspect_data.py
import pandas as pd
import chardet

def inspect_csv(file_path):
    # Detect encoding
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(10000))
    encoding = result['encoding']
    print(f"Detected encoding: {encoding}")
    
    # Read the CSV file
    df = pd.read_csv(file_path, encoding=encoding)
    
    # Print basic info
    print("\nBasic DataFrame Info:")
    print(f"Shape: {df.shape}")
    print("\nFirst few rows:")
    print(df.head())
    
    # Inspect the OEE data section
    print("\nOEE Summary Section (rows 10-15):")
    oee_summary = df.iloc[10:16, :6].dropna()
    print(oee_summary)
    
    # Print data types
    print("\nData Types:")
    print(oee_summary.dtypes)
    
    # Try to convert OEE column to numeric and see what happens
    print("\nTrying to convert OEE column to numeric:")
    try:
        oee_summary.columns = ['Month', 'Availability (%)', 'Performance (%)', 'Quality (%)', 'OEE (%)', 'TEEP (%)']
        print(pd.to_numeric(oee_summary['OEE (%)']))
    except Exception as e:
        print(f"Error: {e}")
        print(f"OEE (%) values: {oee_summary['OEE (%)'].values}")

if __name__ == "__main__":
    inspect_csv('./data/OEE_Data.csv')
