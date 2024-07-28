import streamlit as st
import pandas as pd
import numpy as np

def calculate_tpm(data):
    # Function to calculate the TPM
    n, m = data.shape
    tpm = np.zeros((m, m))
    
    # Calculate transitions
    for i in range(m-1):
        for j in range(m-1):
            tpm[i, j] = np.sum((data.iloc[:, i] > data.iloc[:, j]) & (data.iloc[:, i+1] > data.iloc[:, j+1]))
    
    # Normalize to get probabilities
    tpm = tpm / np.sum(tpm, axis=1, keepdims=True)
    
    return pd.DataFrame(tpm, columns=data.columns, index=data.columns)

st.title("Transitional Probability Matrix Calculator")

uploaded_file = st.file_uploader("Upload your panel data CSV file", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Data Preview:")
    st.dataframe(data)

    if st.button("Calculate TPM"):
        tpm = calculate_tpm(data)
        st.write("Transitional Probability Matrix:")
        st.dataframe(tpm)
        st.download_button(
            label="Download TPM as CSV",
            data=tpm.to_csv().encode('utf-8'),
            file_name='tpm.csv',
            mime='text/csv'
        )
