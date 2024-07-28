import streamlit as st
import pandas as pd
import numpy as np

def calculate_transition_matrix(data, columns):
    diffs = data[columns].diff().dropna()
    states = diffs.applymap(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
    transition_matrix = np.zeros((3, 3))

    for i in range(len(states) - 1):
        row = states.iloc[i].values
        next_row = states.iloc[i + 1].values
        for j in range(len(row)):
            transition_matrix[row[j] + 1, next_row[j] + 1] += 1

    transition_matrix /= transition_matrix.sum(axis=1)[:, None]
    return transition_matrix

st.title("Transition Probability Matrix Calculator")

uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])
if uploaded_file is not None:
    data = pd.read_excel(uploaded_file)
    st.write("Data Preview:")
    st.write(data.head())

    selected_columns = st.multiselect("Select Columns for Analysis", data.columns)
    if selected_columns:
        transition_matrix = calculate_transition_matrix(data, selected_columns)
        st.write("Transition Probability Matrix:")
        st.write(transition_matrix)
