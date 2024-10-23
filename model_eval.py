import pandas as pd
import streamlit as st
import os

def model_eval():
    st.markdown("<h3 style='text-align: center;'>Model Evaluation</h1>", unsafe_allow_html=True)
    # Load data
    script_dir = os.path.dirname(__file__)
    file_path_test = os.path.join(script_dir, "Dataset", "Test set Data Performance.xlsx") 
    df_test_data = pd.read_excel(file_path_test,parse_dates = True)
    file_path_train = os.path.join(script_dir, "Dataset", "Training set Data Performance.xlsx") 
    df_train_data = pd.read_excel(file_path_train,parse_dates = True)

    # Rename the 'Unnamed: 0' column to empty string so the label is not displayed
    df_test_data = df_test_data.rename(columns={'Unnamed: 0': ''})
    df_train_data = df_train_data.rename(columns={'Unnamed: 0': ''})
 
    select_type = st.radio(' ',('Data','Confusion Matrix'))
 
    # Radio button for selecting between test and train sets
    options = st.radio("Dataset:", ('Test', 'Train'))
 
    if select_type == 'Data':
       
        # Display the corresponding dataset
        if options == 'Test':
            st.dataframe(df_test_data, use_container_width=True,hide_index = True)
        elif options == 'Train':
            st.dataframe(df_train_data, use_container_width=True,hide_index=True)
 
    elif select_type == 'Confusion Matrix':
 
        options = st.radio('',('Logistic Regression','Decision Tree','KNN','SVC'))

