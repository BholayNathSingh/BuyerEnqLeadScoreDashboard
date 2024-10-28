# model_eval.py
import pandas as pd
import streamlit as st
from confusion_matrix import test_matrix, train_matrix
import os

def model_eval():
    st.markdown("<h3 style='text-align: center;'>Model Evaluation</h3>", unsafe_allow_html=True)
    
    # Load data
    file_path = os.path.join(os.getcwd(), "Dataset", "Model Data Performance.xlsx")
    
    try:
        df_test_data = pd.read_excel(file_path, sheet_name='Sheet1', parse_dates=True)
        df_test_metrix = pd.read_excel(file_path, sheet_name='Test', parse_dates=True)
        df_train_metrix = pd.read_excel(file_path, sheet_name='Train', parse_dates=True)
    except FileNotFoundError:
        st.error("The file 'Model Data Performance.xlsx' was not found in the 'Dataset' folder.")
        return
    
    if 'Unnamed: 0' in df_test_data.columns:
        df_test_data = df_test_data.rename(columns={'Unnamed: 0': 'Metrics'})
    else:
        st.error("The dataset does not contain the expected 'Unnamed: 0' column.")
        return
    
    df_test_data.insert(0, 'S.No.', range(1, len(df_test_data) + 1))
    
    if len(df_test_data.columns) >= 10:
        df_test_data.columns = [
            'S.No.', 'Metrics', 'LR (Test)', 'LR (Train)', 'DT (Test)', 
            'DT (Train)', 'KNN (Test)', 'KNN (Train)', 'SVC (Test)', 'SVC (Train)'
        ]
    else:
        st.error("Not enough columns in the dataset to rename correctly.")
        return
    
    cols_to_modify = ['LR (Test)', 'LR (Train)', 'DT (Test)', 'DT (Train)', 
                      'KNN (Test)', 'KNN (Train)', 'SVC (Test)', 'SVC (Train)']
    df_test_data[cols_to_modify] = df_test_data[cols_to_modify].apply(lambda x: (x * 100).round(2))
    df_test_data[cols_to_modify] = df_test_data[cols_to_modify].applymap("{:.2f}".format)
    df_test_data = df_test_data.head(6)
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        view = st.radio("View", ("Table", "Matrix"))

    if view == "Matrix":
        with col2:
            data_type = st.radio("Data", ("Train", "Test"))

    if view == "Table":
        st.markdown("""
            <style>
            thead th { text-align: center !important; }
            tbody td { text-align: center; }
            </style>
        """, unsafe_allow_html=True)
        
        st.dataframe(df_test_data.style.set_properties(**{'text-align': 'center'}), hide_index=True)
        
    elif view == "Matrix":
        
        if data_type == "Test":
            df_test_metrix.set_index('Unnamed: 0', inplace=True)
            with col3:
                model_type = st.radio("Select Model", df_test_metrix.columns.tolist())
            with col4:
                value_type = st.radio("Format:", ('Number', 'Percentage'))
            test_matrix(df_test_metrix,model_type,value_type)

        elif data_type == "Train":
            df_train_metrix.set_index('Unnamed: 0', inplace=True)
            with col3:
                model_type = st.radio("Select Model",df_train_metrix.columns.to_list())
            with col4:
                value_type = st.radio("Foramt:", ('Number', 'Percentage'))
            train_matrix(df_train_metrix,model_type,value_type)
