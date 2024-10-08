import plotly.graph_objects as go

import streamlit as st
import plotly.graph_objects as go

# Var data for the waterfall chart
def variable_reduction():
    data = [
        {"label": "Initial Variables", "value": 38},
        {"label": "Manual Data Mapping", "value": 3},
        {"label": "Dropping Var >80% blanks", "value": -12},
        {"label": "Dropping Var with only 1 unique value", "value": -5},
        {"label": "Dropping Var with S No.", "value": -1},
        {"label": "Adding Var with nBuyerOpenEnq in last 3 weeks", "value": 1},
        #{"label": "Adding Var with nBuyerCumulativeOpenEnq in last 1 month", "value": 1},
        {"label": "Adding Var with nBuyerClosedEnq in last 3 weeks", "value": 1},
        {"label": "Adding Var with nSellerEnq in last 3 weeks", "value": 1},
        {"label": "Adding Var with nPurchase in last 3 weeks", "value": 1},
        {"label": "Adding Var with nSale in last 3 weeks", "value": 1},
        {"label": "Adding Var with Temporary_Model_Name", "value": 1},
        {"label": "Adding Var with nCurrent_Unsold_Stock on the day before", "value": 1},
        {"label": "Total", "value": 1},
    ]

    # Extract the labels and values from the data list
    labels = [d["label"] for d in data]
    values = [d["value"] for d in data]

    # Create the waterfall chart
    fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=["relative"] * (len(labels) - 1) + ["total"],  # All relative except the last one (total)
        x=labels,  # Pass in the labels list
        textposition="outside",
        y=values,  # Pass in the values list
        connector={"line": {"color": "rgb(63, 63, 63)"}} 
    ))

    # Customize the chart layout
    fig.update_layout(
        title="nVariable Reduction",
        xaxis_title="Category",
        yaxis_title="Value",
        width=800,
        height=600,
        xaxis=dict(
            tickangle=-45,  # Rotate the labels by 45 degrees
            tickmode='array',
            tickvals=list(range(len(labels))),
            ticktext=labels
        )
    )

    # Show the chart in Streamlit
    st.plotly_chart(fig)