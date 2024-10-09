import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def bivariate_charts(df):
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
        selected_graph = st.selectbox('Select a Bivariate graph:', graph_options)

        def graph_ibb_make():
                model_enq_grouped = df.groupby(['IBB_Make', 'Enquiry Status']).size().unstack(fill_value=0)
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
                count_of_model = df['IBB_Make'].value_counts()[:30]
                for i, v in enumerate(count_of_model):
                    fig.add_annotation(x=model_enq_grouped.index[i], y=v, text=str(v), showarrow=False, yshift=10)
                # Remove grid lines
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=False, secondary_y=False)
                fig.update_yaxes(showgrid=False, secondary_y=True)
                st.plotly_chart(fig, use_container_width=True)
                








        #Model and Success rate
        def graph_ibb_model():
                model_enq_grouped = df.groupby(['IBB_Model', 'Enquiry Status']).size().unstack(fill_value=0)
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
                count_of_model = df['IBB_Model'].value_counts()[:30]
                for i, v in enumerate(count_of_model):
                    fig.add_annotation(x=model_enq_grouped.index[i], y=v, text=str(v), showarrow=False, yshift=10)
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=False, secondary_y=False)
                fig.update_yaxes(showgrid=False, secondary_y=True)
                st.plotly_chart(fig, use_container_width=True)










        #Source type and success rate bivariate
        def graph_source_type():
                model_enq_grouped = df.groupby(['Source Type', 'Enquiry Status']).size().unstack(fill_value=0)
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
                count_of_model = df['Source Type'].value_counts()[:30]
                for i, v in enumerate(count_of_model):
                    fig.add_annotation(x=model_enq_grouped.index[i], y=v, text=str(v), showarrow=False, yshift=10)
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=False, secondary_y=False)
                fig.update_yaxes(showgrid=False, secondary_y=True)
                st.plotly_chart(fig, use_container_width=True)







        #Fuel type and Success Rate bivariate
        def graph_fuel_type():
                model_enq_grouped = df.groupby(['Fuel Type', 'Enquiry Status']).size().unstack(fill_value=0)
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
                count_of_model = df['Fuel Type'].value_counts()[:30]
                for i, v in enumerate(count_of_model):
                    fig.add_annotation(x=model_enq_grouped.index[i], y=v, text=str(v), showarrow=False, yshift=10)
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=False, secondary_y=False)
                fig.update_yaxes(showgrid=False, secondary_y=True)
                st.plotly_chart(fig, use_container_width=True)







        #KM Range and Success Rate bivariate
        def graph_km_range():
                model_enq_grouped = df.groupby(['KM Range', 'Enquiry Status']).size().unstack(fill_value=0)
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
                count_of_kmrange = df['KM Range'].value_counts()[:30]
                for i, v in enumerate(count_of_kmrange):
                    fig.add_annotation(x=model_enq_grouped.index[i], y=v, text=str(v), showarrow=False, yshift=10)
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(showgrid=False, secondary_y=False)
                fig.update_yaxes(showgrid=False, secondary_y=True)
                st.plotly_chart(fig, use_container_width=True)










        #Mfg Year and Success Rate bivariate
        def graph_mfg_year():
                year_enq_grouped = df.groupby(['Manufacturing Year', 'Enquiry Status']).size().unstack(fill_value=0)
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
                    yaxis=dict(title='Count',showgrid = False),
                    yaxis2=dict(title='Success Rate(%)', overlaying='y', side='right', range=[0, 105], tickformat=".0f",showgrid = False),
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
