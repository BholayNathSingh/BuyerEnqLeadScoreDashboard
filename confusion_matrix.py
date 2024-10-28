# confusion_matrix.py

import streamlit as st
import pandas as pd

def display_confusion_matrix(data, model_type, value_type):
    """Display the confusion matrix based on selected data and model type."""
    TP = data.loc['TP', model_type]
    TN = data.loc['TN', model_type]
    FP = data.loc['FP', model_type]
    FN = data.loc['FN', model_type]

    if value_type == 'Number':
        value_display = f"""
        <table class="matrix-table">
            <tr>
                <th colspan="2" rowspan="2" class="blank-space"></th>
                <th colspan="2" class="header-cell">Predicted Class</th>
                <th rowspan="2" class="blank-space"></th>
            </tr>
            <tr>
                <th class="header-cell">Success</th>
                <th class="header-cell">Drop</th>
            </tr>
            <tr>
                <th rowspan="2" class="header-cell">Actual Class</th>
                <th class="header-cell">Success</th>
                <td class="metric-formula">True Positive (TP)<br>{int(TP)}</td>
                <td class="metric-formula">False Negative (FN)<br>{int(FN)} <br> <span class="error-text">Type II Error</span></td>
                <td class="metric-formula">TP+FN<br> = {int(TP + FN)}</td>
            </tr>
            <tr>
                <th class="header-cell">Drop</th>
                <td class="metric-formula">False Positive (FP)<br>{int(FP)}<br><span class="error-text">Type I Error</span></td>
                <td class="metric-formula">True Negative (TN)<br>{int(TN)}</td>
                <td class="metric-formula">FP+TN = {int(TN + FP)}</td>
            </tr>
            <tr>
                <th class="blank-space"></th>
                <th class="blank-space"></th>
                <td class="metric-formula">TP+FP = {int(TP + FP)}</td>
                <td class="metric-formula">FN+TN = {int(TN + FN)}</td>
                <td class="metric-formula">Total = {int((TP + FP) + (TN + FN))}</td>
            </tr>
        </table>
        """
    elif value_type == 'Percentage':
        value_display = f"""
        <table class="matrix-table">
            <tr>
                <th colspan="2" rowspan="2" class="blank-space"></th>
                <th colspan="2" class="header-cell">Predicted Class</th>
                <th rowspan="2" class="blank-space"></th>
            </tr>
            <tr>
                <th class="header-cell">Success</th>
                <th class="header-cell">Drop</th>
            </tr>
            <tr>
                <th rowspan="2" class="header-cell">Actual Class</th>
                <th class="header-cell">Success</th>
                <td class="metric-formula">TPR/Sensitivity=<br>{(TP / (TP + FN) * 100):.2f}%</td>
                <td class="metric-formula">FNR=<br>{(FN / (TP + FN) * 100):.2f}%<span class="error-text"><br>Type II Error</span></td>
                <td class="metric-formula">(TPR + FNR) = {(((TP / (TP + FN)) * 100) + ((FN / (TP + FN)) * 100)):.2f}%</td>
            </tr>
            <tr>
                <th class="header-cell">Drop</th>
                <td class="metric-formula">FPR=<br>{(FP / (TN + FP) * 100):.2f}%<br><span class="error-text">Type I Error</span></td>
                <td class="metric-formula">TNR/Specificity=<br>{(TN / (TN + FP) * 100):.2f}%</td>
                <td class="metric-formula">(FPR + TNR) = {(((TN / (TN + FP)) * 100) + ((FP / (TN + FP)) * 100)):.2f}%</td>
            </tr>
            <tr>
                <th class="blank-space"></th>
                <th class="blank-space"></th>
                <td class="metric-formula">(TPR + FPR) =<br>{(((TP / (TP + FN)) * 100) + ((FP / (TN + FP)) * 100)):.2f}%</td>
                <td class="metric-formula">(FNR + TNR) =<br>{(((TN / (TN + FP)) * 100) + ((FN / (TP + FN)) * 100)):.2f}%</td>
                <td class="metric-formula">Accuracy=<br>(TP + TN)/(TP + FP + FN + TN)=<br>{(TP + TN) / (TP + FP + FN + TN) * 100:.2f}%</td>
            </tr>
        </table>
        """

    st.markdown(value_display, unsafe_allow_html=True)

def test_matrix(data,model_type,value_type):
    st.write("( "+model_type+" )"+" Test Confusion Matrix")    
    display_confusion_matrix(data, model_type, value_type)

def train_matrix(data,model_type,value_type):
    st.write("( "+model_type+" )"+" Train Confusion Matrix")
    display_confusion_matrix(data, model_type, value_type)