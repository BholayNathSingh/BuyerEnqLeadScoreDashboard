import streamlit as st
import pandas as pd

# data summary method
def data_reduction():
    st.header("Data Reduction")
    # Load the data from the Excel file
    data_file = 'Dataset/Data_Reduction.xlsx'
    try:
        # Load the data and reset the index
        data = pd.read_excel(data_file, index_col=False)
        
        # Drop the 'Unnamed: 0' column if it exists
        if 'Unnamed: 0' in data.columns:
            data = data.drop(columns=['Unnamed: 0'])
        
        st.dataframe(data, width=None, height=None, hide_index=True)
    except FileNotFoundError:
        st.error(f"File not found: {data_file}")
    except Exception as e:
        st.error(f"Error loading data: {e}")
