import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder



# data summary method
def data_summary(df):
    st.markdown("<h1 style='text-align: center;'>Buyer Enquiry Leadscore Analysis</h1>", unsafe_allow_html=True)
    st.header("Data Summary")
    st.write("Note")
    st.write("1. Removed rows with >30% missing columns")
    st.write("2. Dropped columns with >80% missing rows")
    st.write("3. Resulting dataset: **14715** data points, **26** variables.")

    # Load the data from the Excel file
    data_file = 'Dataset/Data_Summary_Unclean.xlsx'
    try:
        data = pd.read_excel(data_file)
        #st.write(data.to_string(index=False))
        #st.dataframe(data, width=None, height=None, hide_index=True)
        numeric_cols = ["nData","nVar","nVar with <30% missing","nVar with 30%-80% missing","nVar with 80%-100% missing"]
        gb = GridOptionsBuilder.from_dataframe(data)
        for col in numeric_cols:
            gb.configure_column(col,type=["numericColumn","numberColumnFilter"],align='right')
            
        gb.configure_grid_options(autoSizeColumnsMode='autoSizeColumns')
        AgGrid(data,gridOptions=gb.build(),width=None,height=None)
        #st.write(data)
    except FileNotFoundError:
        st.error(f"File not found: {data_file}")
    except Exception as e:
        st.error(f"Error loading data: {e}")