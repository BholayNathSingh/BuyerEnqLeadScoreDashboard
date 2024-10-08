import streamlit as st
import pandas as pd


# data summary method
def data_summary(df):
    st.markdown("<h1 style='text-align: center;'>Buyer Enquiry Lead Score Dashboard</h1>", unsafe_allow_html=True)
    st.header("Data Summary")
    st.write("Note")
    st.write("1. We have dropped rows with more than 30% missing columns.")
    st.write("2. We have dropped columns with more than 80% missing rows.")
    st.write("3. Using the below mentioned datasets we have obtained **14715** data points and **26** Variables.")

    # Load the data from the Excel file
    data_file = 'Dataset/Data_Summary_Unclean.xlsx'
    try:
        data = pd.read_excel(data_file)
        #st.write(data.to_string(index=False))
        st.dataframe(data, width=None, height=None, hide_index=True)
        #st.write(data)
    except FileNotFoundError:
        st.error(f"File not found: {data_file}")
    except Exception as e:
        st.error(f"Error loading data: {e}")