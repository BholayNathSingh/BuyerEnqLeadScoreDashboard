import streamlit as st
import pandas as pd
import plotly.express as px

path_to_df_success_dropped = 'Dataset/df_success_dropped.xlsx'
path_to_df_Buyer = 'Dataset/df_Buyer.xlsx'

# Load the datasets (replace with actual file paths)
df_success_dropped = pd.read_excel(path_to_df_success_dropped)
df_buyer = pd.read_excel(path_to_df_Buyer)

# Method to display data distribution
def data_distribution():
    st.title('Enquiry Status Distribution')

    # Create two columns for radio buttons to be side by side
    col1, col2 = st.columns([1, 3])
    
    # Radio buttons placed in the first column
    with col1:
        data_selection = st.radio("Select Data", ['All Data', 'Success and Dropped'], horizontal=True)

    # Filter the data based on the radio button selection
    if data_selection == 'All Data':
        df = df_buyer
        st.subheader("Distribution for All Data")
    else:
        df = df_success_dropped
        st.subheader("Distribution for Only Success and Dropped")

    # Get the value counts of "Enquiry Status"
    enquiry_status_counts = df['Enquiry Status'].value_counts()
    enquiry_status_percent = df['Enquiry Status'].value_counts(normalize=True) * 100

    # Combine count and percentage into a DataFrame and add serial number
    distribution_df = pd.DataFrame({
        'S.No.': range(1, len(enquiry_status_counts) + 1),
        'Enquiry Status': enquiry_status_counts.index,
        'Count': enquiry_status_counts.values,
        'Percentage (%)': enquiry_status_percent.values
    })

    # Create two columns for pie chart and table to be side by side
    chart_col, table_col = st.columns(2)

    # Pie chart in the first column
    with chart_col:
        # Plot the pie chart using Plotly
        fig = px.pie(distribution_df, names='Enquiry Status', values='Count',
                     title=f'Enquiry Status Distribution ({data_selection})',
                     hover_data=['Count', 'Percentage (%)'], 
                     labels={'Percentage (%)': 'Percentage'},
                     hole=0.3)  # Hole for a donut-style chart (optional)

        fig.update_traces(textinfo='percent+label', hovertemplate='Enquiry Status: %{label}<br>Count: %{value}<br>Percentage: %{percent}')

        # Display the pie chart using Streamlit
        st.plotly_chart(fig)

    # Distribution table in the second column
    with table_col:
        st.subheader(f"Enquiry Status Distribution Table \n({data_selection})")
        st.dataframe(distribution_df,hide_index=True)