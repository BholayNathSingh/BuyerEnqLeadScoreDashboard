import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


def stacked_bar(df):
    # Stacked bar for Success Dropped wrt Mfg Year
    st.markdown("<h3 style='text-align: center;'>Stacked bar for Success and Dropped</h1>", unsafe_allow_html=True)

    # Create a dropdown menu
    graph_options = [
        'Stacked bar for Success and Dropped wrt Mfg Year',
        'Stacked bar graph for Success and Dropped wrt (top 30) Budget From',
        'Stacked bar graph for Success and Dropped wrt (top 30) Budget To'
    ]
    selected_graph = st.selectbox('Select a Stacked bar graph:', graph_options)

    def stackedbar_mfg_yr():
        grouped_data = df.groupby(['Manufacturing Year', 'Enquiry Status'], sort=True).size().reset_index(name='Count')
        pivot_table = grouped_data.pivot_table(index='Manufacturing Year', columns='Enquiry Status', values='Count', fill_value=0)
        desired_order = ['Dropped', 'Success']
        pivot_table = pivot_table[desired_order]
        fig = go.Figure(data=[
            go.Bar(x=pivot_table.index.astype(str), y=pivot_table['Dropped'], name='Dropped', marker_color='#ff7f00'),
            go.Bar(x=pivot_table.index.astype(str), y=pivot_table['Success'], name='Success', marker_color='#1f78b4')
        ])
        fig.update_layout(
            barmode='stack',
            title='Enquiry Status by Manufacturing Year',
            xaxis=dict(title='Manufacturing Year', tickangle=45),
            yaxis=dict(title='Count'),
            legend=dict(title='Enquiry Status', x=1.05, y=1),
            plot_bgcolor='rgba(0,0,0,0)',
            bargap=0.15,
            bargroupgap=0.1
        )
        st.plotly_chart(fig, use_container_width=True)

    # Stacked bar graph for Success Dropped wrt (top 30) Budget From
    def stackedbar_budget_from():
        df['Budget From (Lakhs)'] = df['Budget From'] / 100000  # Convert to lakhs
        grouped_data = df.groupby(['Budget From (Lakhs)', 'Enquiry Status'], sort=True).size().reset_index(name='Count')
        pivot_table = grouped_data.pivot_table(index='Budget From (Lakhs)', columns='Enquiry Status', values='Count', fill_value=0)
        desired_order = ['Dropped', 'Success']
        pivot_table = pivot_table[desired_order]
        top_30_budgets = pivot_table.sum(axis=1).nlargest(30).index
        pivot_table = pivot_table.loc[top_30_budgets]
        fig = px.bar(pivot_table, x=pivot_table.index, y=pivot_table.columns, color_discrete_sequence=['#ff7f00', '#1f78b4'])
        fig.update_layout(
            title='Budget From (Lakhs) vs Enquiry Status',
            xaxis_title='Budget From (Lakhs)',
            yaxis_title='Count',
            legend_title='Enquiry Status',
            bargap=0.2,
            bargroupgap=0.1
        )
        st.plotly_chart(fig, use_container_width=True)

    # Stacked bar graph for Success Dropped wrt (top 30) Budget To
    def stackedbar_budget_to():
        df['Budget To (Lakhs)'] = df['Budget To'] / 100000  # Convert to lakhs
        grouped_data = df.groupby(['Budget To (Lakhs)', 'Enquiry Status'], sort=True).size().reset_index(name='Count')
        pivot_table = grouped_data.pivot_table(index='Budget To (Lakhs)', columns='Enquiry Status', values='Count', fill_value=0)
        desired_order = ['Dropped', 'Success']
        pivot_table = pivot_table[desired_order]
        top_30_budgets = pivot_table.sum(axis=1).nlargest(30).index
        pivot_table = pivot_table.loc[top_30_budgets]
        fig = px.bar(pivot_table, x=pivot_table.index, y=pivot_table.columns, color_discrete_sequence=['#ff7f00', '#1f78b4'])
        fig.update_layout(
            title='Budget To (Lakhs) vs Enquiry Status',
            xaxis_title='Budget To (Lakhs)',
            yaxis_title='Count',
            legend_title='Enquiry Status',
            bargap=0.2,
            bargroupgap=0.1
        )
        st.plotly_chart(fig, use_container_width=True)

    if selected_graph == 'Stacked bar for Success and Dropped wrt Mfg Year':
        stackedbar_mfg_yr()
    elif selected_graph == 'Stacked bar graph for Success and Dropped wrt (top 30) Budget From':
        stackedbar_budget_from()
    elif selected_graph == 'Stacked bar graph for Success and Dropped wrt (top 30) Budget To':
        stackedbar_budget_to()
