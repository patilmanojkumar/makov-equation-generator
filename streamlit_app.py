import streamlit as st
import pandas as pd
import numpy as np

def calculate_transition_matrix(data):
    diffs = data.diff().dropna()
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
    sheet_name = st.text_input("Sheet Name (optional)", value="Sheet1")
    start_row = st.number_input("Start Row", min_value=1, value=1)
    end_row = st.number_input("End Row", min_value=1, value=10)
    start_col = st.number_input("Start Column (1-indexed)", min_value=1, value=1)
    end_col = st.number_input("End Column (1-indexed)", min_value=1, value=10)

    if st.button("Load Data"):
        data = pd.read_excel(uploaded_file, sheet_name=sheet_name, header=None)
        data = data.iloc[start_row-1:end_row, start_col-1:end_col]
        st.write("Data Preview:")
        st.write(data.head())

        transition_matrix = calculate_transition_matrix(data)
        st.write("Transition Probability Matrix:")
        st.write(transition_matrix)
