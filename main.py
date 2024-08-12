#loading the header/library files
import streamlit as st
import pandas as pd
import os
from data_summary import data_summary
from feature_significance import feature_significance
from corr_heatmap import corr_heatmap
from bivariate_charts import bivariate_charts
from stacked_bar import stacked_bar


# Set page configuration
st.set_page_config(
    page_title="Buyer Enquiry Dashboard",
    page_icon="",
    layout="wide",
)

# Set up sidebar
st.sidebar.subheader("Select EDA Options")

# Create radio buttons for Particular EDA
particular_eda_options = [
    'Data Summary',
    'Feature Significance',
    'Correlation',
    'Bivariate Charts',
    'Stacked Bar Charts'
]
particular_eda_selected = st.sidebar.radio("EDA Options", particular_eda_options)

# Load data
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "Dataset", "df_success_dropped.xlsx") 
df_demand_supply = pd.read_excel(file_path,parse_dates = True)


# Display dashboard title
st.markdown("<h1 style='text-align: center;'>Buyer Enquiry Dashboard</h1>", unsafe_allow_html=True)


def plot_data_summary():
    data_summary(df_demand_supply)

def plot_feature_significance():
    feature_significance(df_demand_supply)

def plot_corr_heatmap():
    corr_heatmap(df_demand_supply)

def plot_bivariate_charts():
    bivariate_charts(df_demand_supply)

def plot_stacked_bar():
    stacked_bar(df_demand_supply)



# Call functions based on selected options
if particular_eda_selected == 'Data Summary':
    plot_data_summary()
elif particular_eda_selected == 'Feature Significance':
    plot_feature_significance()
elif particular_eda_selected == 'Correlation':
    plot_corr_heatmap()
elif particular_eda_selected == 'Bivariate Charts':
    plot_bivariate_charts()
elif particular_eda_selected == 'Stacked Bar Charts':
    plot_stacked_bar()