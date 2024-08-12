import streamlit as st
import plotly.express as px



def corr_heatmap(df):
        st.markdown("<h3 style='text-align: center;'>Correlation Heatmap</h1>", unsafe_allow_html=True)
        #Correlation Heatmap
        numeric_df = df.select_dtypes(include=['number'])
        corr_matrix = numeric_df.corr()
        fig = px.imshow(corr_matrix, text_auto=True, color_continuous_scale='Blues')
        fig.update_layout(title='Correlation Matrix',
                        xaxis_title='',
                        yaxis_title='')
        st.plotly_chart(fig, use_container_width=True)