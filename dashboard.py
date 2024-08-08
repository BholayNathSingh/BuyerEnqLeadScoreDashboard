import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px
from scipy.stats import chi2_contingency
from scipy.stats import f_oneway
import plotly.graph_objects as go
from plotly.subplots import make_subplots



st.set_page_config(
    page_title="my dashboard",
    page_icon="",
    layout="wide",
)

st.markdown("<h1 style='text-align: center;'>Buyer Enquiry Dashboard</h1>", unsafe_allow_html=True)



file_path = r'.\Dataset\df_success_dropped.xlsx'
df_demand_supply = pd.read_excel(file_path,parse_dates = True)



# Display the dataframe
st.dataframe(df_demand_supply)


# Display dataframe shape
st.write("Dataframe Shape:",df_demand_supply.shape)


#Display the dataframe summary
st.header("Data Summary")
st.write("Data Source : CTDMS data, Finance Data")
st.write("Data Timeline : Jan 2023 - June 2024")


# Target col distribution in Donut chart
st.markdown("<h3 style='text-align: center;'>Target Column Distribution</h3>",unsafe_allow_html=True)
target = df_demand_supply['Enquiry Status'].value_counts()
df = pd.DataFrame({'Enquiry Status': target.index, 'Count': target.values})
fig = px.pie(df, names='Enquiry Status', values='Count', hole=0.7)
fig.update_layout(
    font_size=14,
    font_family='Arial',
    margin=dict(l=0, r=0, t=50, b=0)
)
st.plotly_chart(fig, use_container_width=True)


## Feature significance for categorical features
st.markdown("<h3 style='text-align: center;'>P-Values for Feature Significance</h1>", unsafe_allow_html=True)

graph_options = [
    'Feature Significance of Categorical features',
    'Feature Significance of Numerical features']
selected_graph = st.selectbox('Select a graph:', graph_options)


def pvalue_cat_features():
        categorical_features = df_demand_supply.select_dtypes(include=['object']).columns
        results = []
        for feature in categorical_features:
            if feature != 'Enquiry Status':
                contingency_table = pd.crosstab(df_demand_supply['Enquiry Status'], df_demand_supply[feature])
                chi2, p, _, _ = chi2_contingency(contingency_table)
                results.append([feature, p])

        results_df = pd.DataFrame(results, columns=['Feature', 'P-Value'])
        
        results_df.set_index('Feature', inplace=True)
        # Plotting
        results_df = pd.DataFrame(results, columns=['Feature', 'P-Value'])

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
        continuous_features = df_demand_supply.select_dtypes(include=['int', 'float']).columns
        anova_results = []

        for feature in continuous_features:
            # Perform ANOVA test
            group1 = df_demand_supply[df_demand_supply['Enquiry Status'] == 'Dropped'][feature]
            group2 = df_demand_supply[df_demand_supply['Enquiry Status'] == 'Success'][feature]
            _, p = f_oneway(group1, group2)
            anova_results.append([feature, p])
        anova_results_df = pd.DataFrame(anova_results, columns=['Feature', 'P-Value'])
        # Set the 'Feature' column as the index of the DataFrame
        anova_results_df.set_index('Feature', inplace=True)

        # Plotting
        p_values_df_sorted = anova_results_df.sort_values(by='P-Value', ascending=False)

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



#Correlation Heatmap
numeric_df = df_demand_supply.select_dtypes(include=['number'])
corr_matrix = numeric_df.corr()
fig = px.imshow(corr_matrix, text_auto=True, color_continuous_scale='Blues')
fig.update_layout(title='Correlation Matrix',
                  xaxis_title='',
                  yaxis_title='')
st.plotly_chart(fig, use_container_width=True)




#Target distribution bar chart
class_counts = df_demand_supply['Enquiry Status'].value_counts()
fig = px.bar(x=class_counts.index, y=class_counts.values, color_discrete_sequence=['blue', 'orange'])
fig.update_layout(title='Class Distribution of Enquiry Status',
                  xaxis_title='Enquiry Status',
                  yaxis_title='Count')
for i, v in enumerate(class_counts.values):
    fig.add_annotation(x=class_counts.index[i], y=v, text=str(v), showarrow=False, yshift=10)
st.plotly_chart(fig, use_container_width=True)






st.markdown("<h3 style='text-align: center;'>Bi-Variate charts</h1>", unsafe_allow_html=True)

# Create a dropdown menu
graph_options = [
    'IBB_Make Distribution and Success Rate',
    'IBB_Model Distribution and Success Rate',
    'Source Type and Success Rate',
    'Fuel Type and Success Rate',
    'KM Range and Success Rate',
    'Mfg Year and Success Rate'
]
selected_graph = st.selectbox('Select a graph:', graph_options)

def graph_ibb_make():
        model_enq_grouped = df_demand_supply.groupby(['IBB_Make', 'Enquiry Status']).size().unstack(fill_value=0)
        model_enq_grouped['Success Rate'] = (model_enq_grouped['Success'] / model_enq_grouped.sum(axis=1)) * 100
        model_enq_grouped['Total'] = model_enq_grouped[['Dropped', 'Success']].sum(axis=1)
        model_enq_grouped = model_enq_grouped.sort_values(by='Total', ascending=False)
        model_enq_grouped = model_enq_grouped.iloc[:30]
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=model_enq_grouped.index, y=model_enq_grouped['Total'], name='Total'), secondary_y=False)
        fig.add_trace(go.Scatter(x=model_enq_grouped.index, y=model_enq_grouped['Success Rate'], name='Success Rate', mode='lines+markers', line=dict(color='orange')), secondary_y=True)
        fig.update_layout(title='IBB_Make Distribution and Success Rate',
                        xaxis_title='IBB_Make',
                        yaxis_title='Count',
                        yaxis2_title='Success Rate (%)')
        count_of_model = df_demand_supply['IBB_Make'].value_counts()[:30]
        for i, v in enumerate(count_of_model):
            fig.add_annotation(x=model_enq_grouped.index[i], y=v, text=str(v), showarrow=False, yshift=10)
        st.plotly_chart(fig, use_container_width=True)









#Model and Success rate
def graph_ibb_model():
        model_enq_grouped = df_demand_supply.groupby(['IBB_Model', 'Enquiry Status']).size().unstack(fill_value=0)
        model_enq_grouped['Success Rate'] = (model_enq_grouped['Success'] / model_enq_grouped.sum(axis=1)) * 100
        model_enq_grouped['Total'] = model_enq_grouped[['Dropped', 'Success']].sum(axis=1)
        model_enq_grouped = model_enq_grouped.sort_values(by='Total', ascending=False)
        model_enq_grouped = model_enq_grouped.iloc[:30]
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=model_enq_grouped.index, y=model_enq_grouped['Total'], name='Total'), secondary_y=False)
        fig.add_trace(go.Scatter(x=model_enq_grouped.index, y=model_enq_grouped['Success Rate'], name='Success Rate', mode='lines+markers', line=dict(color='orange')), secondary_y=True)
        fig.update_layout(title='IBB_Model Distribution and Success Rate',
                        xaxis_title='Model',
                        yaxis_title='Count',
                        yaxis2_title='Success Rate (%)')
        count_of_model = df_demand_supply['IBB_Model'].value_counts()[:30]
        for i, v in enumerate(count_of_model):
            fig.add_annotation(x=model_enq_grouped.index[i], y=v, text=str(v), showarrow=False, yshift=10)
        st.plotly_chart(fig, use_container_width=True)










#Source type and success rate bivariate
def graph_source_type():
        model_enq_grouped = df_demand_supply.groupby(['Source Type', 'Enquiry Status']).size().unstack(fill_value=0)
        model_enq_grouped['Success Rate'] = (model_enq_grouped['Success'] / model_enq_grouped.sum(axis=1)) * 100
        model_enq_grouped['Total'] = model_enq_grouped[['Dropped', 'Success']].sum(axis=1)
        model_enq_grouped = model_enq_grouped.sort_values(by='Total', ascending=False)
        model_enq_grouped = model_enq_grouped.iloc[:30]
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=model_enq_grouped.index, y=model_enq_grouped['Total'], name='Total'), secondary_y=False)
        fig.add_trace(go.Scatter(x=model_enq_grouped.index, y=model_enq_grouped['Success Rate'], name='Success Rate', mode='lines+markers', line=dict(color='orange')), secondary_y=True)
        fig.update_layout(title='Source Type and Success Rate',
                        xaxis_title='Source Type',
                        yaxis_title='Count',
                        yaxis2_title='Success Rate (%)')
        count_of_model = df_demand_supply['Source Type'].value_counts()[:30]
        for i, v in enumerate(count_of_model):
            fig.add_annotation(x=model_enq_grouped.index[i], y=v, text=str(v), showarrow=False, yshift=10)
        st.plotly_chart(fig, use_container_width=True)







#Fuel type and Success Rate bivariate
def graph_fuel_type():
        model_enq_grouped = df_demand_supply.groupby(['Fuel Type', 'Enquiry Status']).size().unstack(fill_value=0)
        model_enq_grouped['Success Rate'] = (model_enq_grouped['Success'] / model_enq_grouped.sum(axis=1)) * 100
        model_enq_grouped['Total'] = model_enq_grouped[['Dropped', 'Success']].sum(axis=1)
        model_enq_grouped = model_enq_grouped.sort_values(by='Total', ascending=False)
        model_enq_grouped = model_enq_grouped.iloc[:30]
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=model_enq_grouped.index, y=model_enq_grouped['Total'], name='Total'), secondary_y=False)
        fig.add_trace(go.Scatter(x=model_enq_grouped.index, y=model_enq_grouped['Success Rate'], name='Success Rate', mode='lines+markers', line=dict(color='orange')), secondary_y=True)
        fig.update_layout(title='Fuel Type and Success Rate',
                        xaxis_title='Source Type',
                        yaxis_title='Count',
                        yaxis2_title='Success Rate (%)')
        count_of_model = df_demand_supply['Fuel Type'].value_counts()[:30]
        for i, v in enumerate(count_of_model):
            fig.add_annotation(x=model_enq_grouped.index[i], y=v, text=str(v), showarrow=False, yshift=10)
        st.plotly_chart(fig, use_container_width=True)







#KM Range and Success Rate bivariate
def graph_km_range():
        model_enq_grouped = df_demand_supply.groupby(['KM Range', 'Enquiry Status']).size().unstack(fill_value=0)
        model_enq_grouped['Success Rate'] = (model_enq_grouped['Success'] / model_enq_grouped.sum(axis=1)) * 100
        model_enq_grouped['Total'] = model_enq_grouped[['Dropped', 'Success']].sum(axis=1)
        model_enq_grouped = model_enq_grouped.sort_values(by='Total', ascending=False)
        model_enq_grouped = model_enq_grouped.iloc[:30]
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=model_enq_grouped.index, y=model_enq_grouped['Total'], name='Total'), secondary_y=False)
        fig.add_trace(go.Scatter(x=model_enq_grouped.index, y=model_enq_grouped['Success Rate'], name='Success Rate', mode='lines+markers', line=dict(color='orange')), secondary_y=True)
        fig.update_layout(title='KM Range and Success Rate',
                        xaxis_title='Source Type',
                        yaxis_title='Count',
                        yaxis2_title='Success Rate (%)')
        count_of_kmrange = df_demand_supply['KM Range'].value_counts()[:30]
        for i, v in enumerate(count_of_kmrange):
            fig.add_annotation(x=model_enq_grouped.index[i], y=v, text=str(v), showarrow=False, yshift=10)
        st.plotly_chart(fig, use_container_width=True)










#Mfg Year and Success Rate bivariate
def graph_mfg_year():
        year_enq_grouped = df_demand_supply.groupby(['Manufacturing Year', 'Enquiry Status']).size().unstack(fill_value=0)
        year_enq_grouped['Success Rate'] = (year_enq_grouped['Success'] / year_enq_grouped.sum(axis=1)) * 100
        year_enq_grouped['Total'] = year_enq_grouped[['Dropped', 'Success']].sum(axis=1)
        year_enq_grouped = year_enq_grouped.iloc[:30]
        year_enq_grouped.index = year_enq_grouped.index.astype('str')
        fig = go.Figure(data=[
            go.Bar(x=year_enq_grouped.index, y=year_enq_grouped['Total'], name='Total'),
            go.Scatter(x=year_enq_grouped.index, y=year_enq_grouped['Success Rate'], name='Success Rate', mode='lines+markers', line=dict(color='orange'), yaxis='y2')
        ])
        fig.update_layout(
            title='Manufacturing Year vs Total and Success Rate',
            xaxis_title='Manufacturing Year',
            yaxis_title='Count',
            yaxis=dict(title='Count'),
            yaxis2=dict(title='Success Rate', overlaying='y', side='right', range=[0, 105], tickformat=".0f"),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )
        for i, v in enumerate(year_enq_grouped['Total']):
            fig.add_annotation(x=year_enq_grouped.index[i], y=v, text=str(v), showarrow=False, yshift=10)
        st.plotly_chart(fig, use_container_width=True)



if selected_graph == 'IBB_Make Distribution and Success Rate':
    graph_ibb_make()
elif selected_graph == 'IBB_Model Distribution and Success Rate':
    graph_ibb_model()
elif selected_graph == 'Source Type and Success Rate':
    graph_source_type()
elif selected_graph == 'Fuel Type and Success Rate':
    graph_fuel_type()
elif selected_graph == 'KM Range and Success Rate':
    graph_km_range()
elif selected_graph == 'Mfg Year and Success Rate':
    graph_mfg_year()










#Stacked bar for Success Dropped wrt Mfg Year
st.markdown("<h3 style='text-align: center;'>Stacked bar for Success Dropped</h1>", unsafe_allow_html=True)


# Create a dropdown menu
graph_options = [
    'Stacked bar for Success Dropped wrt Mfg Year',
    'Stacked bar graph for Success Dropped wrt (top 30) Budget From',
    'Stacked bar graph for Success Dropped wrt (top 30) Budget To'
]
selected_graph = st.selectbox('Select a graph:', graph_options)

def stackedbar_mfg_yr():
        grouped_data = df_demand_supply.groupby(['Manufacturing Year', 'Enquiry Status'], sort=True).size().reset_index(name='Count')
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









#Stacked bar graph for Success Dropped wrt (top 30) Budget From
def stackedbar_budget_from():
        grouped_data = df_demand_supply.groupby(['Budget From', 'Enquiry Status'], sort=True).size().reset_index(name='Count')
        pivot_table = grouped_data.pivot_table(index='Budget From', columns='Enquiry Status', values='Count', fill_value=0)
        desired_order = ['Dropped', 'Success']
        pivot_table = pivot_table[desired_order]
        top_30_budgets = pivot_table.sum(axis=1).nlargest(30).index
        pivot_table = pivot_table.loc[top_30_budgets]
        fig = px.bar(pivot_table, x=pivot_table.index, y=pivot_table.columns, color_discrete_sequence=['#ff7f00', '#1f78b4'])
        fig.update_layout(title='Budget From vs Enquiry Status',xaxis_title='Budget From',yaxis_title='Count',legend_title='Enquiry Status',bargap=0.2,bargroupgap=0.1)
        st.plotly_chart(fig, use_container_width=True)





#Stacked bar graph for Success Dropped wrt (top 30) Budget To
def stackedbar_budget_to():
        grouped_data = df_demand_supply.groupby(['Budget To', 'Enquiry Status'], sort=True).size().reset_index(name='Count')
        pivot_table = grouped_data.pivot_table(index='Budget To', columns='Enquiry Status', values='Count', fill_value=0)
        desired_order = ['Dropped', 'Success']
        pivot_table = pivot_table[desired_order]
        top_30_budgets = pivot_table.sum(axis=1).nlargest(30).index
        pivot_table = pivot_table.loc[top_30_budgets]
        fig = px.bar(pivot_table, x=pivot_table.index, y=pivot_table.columns, color_discrete_sequence=['#ff7f00', '#1f78b4'])
        fig.update_layout(title='Budget To vs Enquiry Status',xaxis_title='Budget To',yaxis_title='Count',legend_title='Enquiry Status',bargap=0.2,bargroupgap=0.1)
        st.plotly_chart(fig, use_container_width=True)




if selected_graph == 'Stacked bar for Success Dropped wrt Mfg Year':
    stackedbar_mfg_yr()
elif selected_graph == 'Stacked bar graph for Success Dropped wrt (top 30) Budget From':
    stackedbar_budget_from()
elif selected_graph == 'Stacked bar graph for Success Dropped wrt (top 30) Budget To':
    stackedbar_budget_to()