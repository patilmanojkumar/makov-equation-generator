import streamlit as st
import pandas as pd
import numpy as np
import io

# Function to read data from an uploaded file
def read_data(file, sheet_name, start_row, end_row, start_col, end_col):
    df = pd.read_excel(file, sheet_name=sheet_name, header=None)
    data = df.iloc[start_row-1:end_row, start_col-1:end_col].values
    return data

# Function to calculate Markov Chain probabilities and generate equations
def calculate_markov_chain(data):
    tot_rows, tot_cols = data.shape
    mcdata = data.copy()

    # Normalize the data to get Markov Chain probabilities
    for i in range(tot_rows):
        row_sum = mcdata[i, :-1].sum()
        if row_sum != 0:
            mcdata[i, :-1] /= row_sum

    equations = []
    for row in range(tot_rows):
        for col in range(tot_cols - 1):
            equation = []
            for var in range(tot_cols - 1):
                coeff = f"{mcdata[row, var]:.4f}"
                equation.append(f"{coeff}*x{chr(97 + var)}{row + 1}")
            u_var = f"u{row + 1}"
            v_var = f"v{row + 1}"
            const_term = f"{data[row, -1]:.4f}"
            equation = " + ".join(equation)
            equations.append(f"{equation} + {u_var} - {v_var} = {const_term};")
    
    # Constraint for sum of probabilities being 1
    for col in range(tot_cols - 1):
        x_vars = [f"x{chr(97 + col)}{row + 1}" for row in range(tot_rows)]
        equations.append(" + ".join(x_vars) + " = 1;")
    
    return equations

# Streamlit app
st.title("Markov Chain Equations Generator")

st.sidebar.header("Upload Your Excel File")
uploaded_file = st.sidebar.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file:
    st.sidebar.header("Specify Data Range")
    sheet_name = st.sidebar.text_input("Sheet Name", value="Sheet1")
    start_row = st.sidebar.number_input("Start Row", min_value=1, value=2)
    end_row = st.sidebar.number_input("End Row", min_value=start_row, value=start_row+10)
    start_col = st.sidebar.number_input("Start Column (1-indexed)", min_value=1, value=2)
    end_col = st.sidebar.number_input("End Column (1-indexed)", min_value=start_col, value=start_col+3)

    if st.sidebar.button("Generate Markov Chain Equations"):
        try:
            data = read_data(uploaded_file, sheet_name, start_row, end_row, start_col, end_col)
            equations = calculate_markov_chain(data)
            st.subheader("Generated Markov Chain Equations")
            st.text_area("Equations", value="\n".join(equations), height=300)
        except Exception as e:
            st.error(f"An error occurred: {e}")

st.sidebar.write("Upload your Excel file and specify the range to generate the Markov Chain equations.")
