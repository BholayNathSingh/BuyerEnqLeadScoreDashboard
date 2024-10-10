import streamlit as st
import pandas as pd
from scipy.stats import chi2_contingency, f_oneway
import plotly.express as px

def feature_significance(df):
    st.markdown("<h3 style='text-align: center;'>P-Values for Feature Significance</h1>", unsafe_allow_html=True)
    graph_options = [
        'Feature Significance of Categorical features',
        'Feature Significance of Numerical features'
    ]
    selected_graph = st.selectbox('Select a graph:', graph_options)

    ## Feature significance for categorical features
    def pvalue_cat_features():
        categorical_features = df.select_dtypes(include=['object']).columns
        results = []
        for feature in categorical_features:
            if feature != 'Enquiry Status':
                contingency_table = pd.crosstab(df['Enquiry Status'], df[feature])
                chi2, p, _, _ = chi2_contingency(contingency_table)
                results.append([feature, p])

        # Create a DataFrame, remove empty rows, and add a Serial Number column
        results_df = pd.DataFrame(results, columns=['Feature', 'P-Value']).dropna(how='any')

        # Sort the DataFrame by P-Value
        results_df = results_df.sort_values(by='P-Value')

        # Add serial numbers
        results_df['S.No.'] = range(1, len(results_df) + 1)

        # Reorder columns to show serial number first
        results_df = results_df[['S.No.', 'Feature', 'P-Value']]
        results_df.dropna(inplace=True)

        # Create columns for side-by-side layout
        col1, col2 = st.columns([2, 1])

        # Plotting in the left column
        with col1:
            fig = px.bar(results_df.sort_values(by='P-Value', ascending=False), 
                         x='Feature', y='P-Value', 
                         title='Chi-square Test P-Values for Categorical Features',
                         labels={'Feature': 'Categorical Features', 'P-Value': 'P-Value'},
                         color_discrete_sequence=['blue'])
            
            fig.add_hline(y=0.05, line_dash='dash', line_color='red', 
                          annotation_text='Significance Level = 0.05', 
                          annotation_position='top left')
            
            fig.update_layout(xaxis_tickangle=45, xaxis_title_standoff=10)
            fig.update_layout(margin=dict(l=10, r=10, t=50, b=10))
            st.plotly_chart(fig, use_container_width=True)
        
        # Displaying the table in the right column
        with col2:
            st.dataframe(results_df, width=None, hide_index=True)

    ## feature significance for numerical features
    def pvalue_num_features():
        continuous_features = df.select_dtypes(include=['int', 'float']).columns
        anova_results = []
        for feature in continuous_features:
            # Perform ANOVA test
            group1 = df[df['Enquiry Status'] == 'Dropped'][feature]
            group2 = df[df['Enquiry Status'] == 'Success'][feature]
            _, p = f_oneway(group1, group2)
            anova_results.append([feature, p])

        # Create a DataFrame, remove empty rows, and add a Serial Number column
        anova_results_df = pd.DataFrame(anova_results, columns=['Feature', 'P-Value']).dropna(how='any')

        # Sort the DataFrame by P-Value
        anova_results_df = anova_results_df.sort_values(by='P-Value')

        # Add serial numbers
        anova_results_df['S.No.'] = range(1, len(anova_results_df) + 1)

        # Reorder columns to show serial number first
        anova_results_df = anova_results_df[['S.No.', 'Feature', 'P-Value']]
        anova_results_df.dropna(inplace=True)

        # Create columns for side-by-side layout
        col1, col2 = st.columns([2, 1])

        # Plotting in the left column
        with col1:
            fig = px.bar(anova_results_df.sort_values(by='P-Value', ascending=False), 
                         x='Feature', y='P-Value', 
                         color_discrete_sequence=['blue'])
            
            fig.add_hline(y=0.05, line_dash='dash', line_color='red', 
                          annotation_text='Significance Level = 0.05')
            
            fig.update_layout(title='ANOVA Test P-Values for Numerical Features',
                              xaxis_title='Numerical Features',
                              yaxis_title='P-Value',
                              xaxis_tickangle=-45)
            
            st.plotly_chart(fig, use_container_width=True)

        # Displaying the table in the right column
        with col2:
            st.dataframe(anova_results_df, width=None, hide_index=True)

    if selected_graph == 'Feature Significance of Categorical features':
        pvalue_cat_features()
    elif selected_graph == 'Feature Significance of Numerical features':
        pvalue_num_features()
