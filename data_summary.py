import streamlit as st


# data summary method
def data_summary(df):
    st.header("Data Summary")
    st.write("Data Source : CTDMS data, Finance Data")
    st.write("Data Timeline : Jan 2023 - June 2024")
    st.write("Dataframe Shape:", df.shape)