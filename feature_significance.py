import streamlit as st
import pandas as pd
from scipy.stats import chi2_contingency,f_oneway
import plotly.express as px




def feature_significance(df):
        st.markdown("<h3 style='text-align: center;'>P-Values for Feature Significance</h1>", unsafe_allow_html=True)
        ## Feature significance for categorical features
        graph_options = [
            'Feature Significance of Categorical features',
            'Feature Significance of Numerical features']
        selected_graph = st.selectbox('Select a graph:', graph_options)


        def pvalue_cat_features():
                categorical_features = df.select_dtypes(include=['object']).columns
                results = []
                for feature in categorical_features:
                    if feature != 'Enquiry Status':
                        contingency_table = pd.crosstab(df['Enquiry Status'], df[feature])
                        chi2, p, _, _ = chi2_contingency(contingency_table)
                        results.append([feature, p])
                results_df = pd.DataFrame(results, columns=['Feature', 'P-Value'])                
                results_df.set_index('Feature', inplace=True)
                # Plotting
                results_df = pd.DataFrame(results, columns=['Feature', 'P-Value'])
                results_df = results_df.sort_values(by='P-Value')
                # Plotting
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
                st.write(results_df)


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
                anova_results_df = pd.DataFrame(anova_results, columns=['Feature', 'P-Value'])
                anova_results_df = anova_results_df.sort_values(by='P-Value')
                # Set the 'Feature' column as the index of the DataFrame
                anova_results_df.set_index('Feature', inplace=True)
                # Plotting
                p_values_df_sorted = anova_results_df.sort_values(by='P-Value', ascending=False)
                anova_results_df = anova_results_df.sort_values(by='P-Value', ascending=False)
                fig = px.bar(p_values_df_sorted, x=p_values_df_sorted.index, y='P-Value', color_discrete_sequence=['blue'])
                fig.add_hline(y=0.05, line_color='red', line_dash='dash', annotation_text='Significance Level = 0.05')
                fig.update_layout(title='ANOVA Test P-Values for Numerical Features',
                                xaxis_title='Numerical Features',
                                yaxis_title='P-Value',
                                xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
                st.write(anova_results_df)
        if selected_graph == 'Feature Significance of Categorical features':
            pvalue_cat_features()
        elif selected_graph == 'Feature Significance of Numerical features':
            pvalue_num_features()
