import streamlit as st
import plotly.express as px
import pandas as pd

def open_enq_frq():
    data_file = 'Dataset/open cumsum.xlsx'
    df = pd.read_excel(data_file)
    
    # Streamlit UI for inputs
    st.title("Enquiry Frequency Plot")
    
    # User selects end date
    End_Date = st.date_input("Select End Date")
    
    # User inputs make and model
    IBB_Make = st.text_input("Enter IBB Make")
    IBB_Model = st.text_input("Enter IBB Model")
    
    # Calculate the StartDate as 1 month back from End_Date
    StartDate = pd.to_datetime(End_Date) - pd.DateOffset(months=1)
    
    # Filter the dataframe based on the input values
    filtered_df = df[(df['Enquiry Date'] >= StartDate) & 
                     (df['Enquiry Date'] <= pd.to_datetime(End_Date)) & 
                     (df['IBB_Make'] == IBB_Make) & 
                     (df['IBB_Model'] == IBB_Model)]
    
    # Create a new dataframe with the required columns
    plot_df = filtered_df[['Enquiry Date', 'cumulativeOpenEnq', 'nOpenEnq']]
    
    # Radio button selection for chart type
    chart_type = st.radio("Select Chart Type:", 
                          ('Stacked Bar Chart', 'Bar Chart for nOpenEnq', 'Bar Chart for cumulativeOpenEnq'), 
                          horizontal=True)

    # Plotting based on selected chart type
    if chart_type == 'Stacked Bar Chart':
        # Stacked bar chart (Both nOpenEnq and cumulativeOpenEnq together)
        fig = px.bar(plot_df,
                     x='Enquiry Date',
                     y=['cumulativeOpenEnq', 'nOpenEnq'],
                     barmode='overlay',  # Stacked bar mode
                     opacity=0.8,   # Adjust opacity
                     color_discrete_map={'cumulativeOpenEnq':'blue','nOpenEnq':'red'}
                     )  

        fig.update_layout(
            xaxis=dict(tickangle=-45),
            title='Stacked Enquiry Data: Open Enq and Cumulative Open Enq vs Date',
            yaxis=dict(range=[0, plot_df[['cumulativeOpenEnq', 'nOpenEnq']].max() * 1.1])  # Adjust for better visibility
        )
        
    elif chart_type == 'Bar Chart for nOpenEnq':
        # Line chart for nOpenEnq
        fig_nOpenEnq = px.line(
            plot_df,
            x='Enquiry Date',
            y='nOpenEnq',
            title='Open Enquiries (nOpenEnq) vs Date',
            labels={'nOpenEnq': 'Number of Open Enquiries'},
            line_shape='linear',
            markers=True  # Add markers for better visibility
        )
        # Update the layout of both figures to tilt x-axis labels
        fig_nOpenEnq.update_layout(
            xaxis=dict(tickangle=-45),
            yaxis=dict(range=[0, plot_df['nOpenEnq'].max() * 1.1])
        )
        st.plotly_chart(fig_nOpenEnq)

        
    elif chart_type == 'Bar Chart for cumulativeOpenEnq':
        # Bar chart for cumulativeOpenEnq only
        fig = px.bar(plot_df,
                     x='Enquiry Date',
                     y='cumulativeOpenEnq',
                     opacity=0.8,
                     labels={'cumulativeOpenEnq': 'Cumulative Open Enquiries'})

        fig.update_layout(
            xaxis=dict(tickangle=-45),
            title='Cumulative Open Enquiries (cumulativeOpenEnq) vs Date',
            yaxis=dict(range=[0, plot_df['cumulativeOpenEnq'].max() * 1.1])  # Adjust for better visibility
        )
    
    # Show the plot in Streamlit
    st.plotly_chart(fig)