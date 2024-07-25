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

    mcdata1 = np.zeros_like(mcdata)

    for i in range(tot_rows):
        for j in range(tot_cols - 1):
            if mcdata[i, -1] != 0:
                mcdata1[i, j] = (mcdata[i, j] / mcdata[i, -1]) * 10000
                mcdata1[i, j] = np.round(mcdata1[i, j] + 0.5) / 10000

    s_output = []
    s_xend = []
    s_minu = []
    s_minv = []
    i_rownum = 1

    for n in range(tot_cols - 1):
        for i in range(tot_rows - 1):
            row_eq = []
            for j in range(tot_cols - 1):
                row_eq.append(f"{mcdata1[i, j]:.4f}*x{chr(96 + j + 1)}{n + 1}")
                if j == 4:
                    row_eq.append("\n")

                if i == 0:
                    s_xend.append(f"1*x{chr(96 + n + 1)}{j + 1}")
                    if j == tot_cols - 2:
                        s_xend[-1] += "=1;"

            s_output.append(f"{'+'.join(row_eq)}")
            s_output.append(f"u{i_rownum}-v{i_rownum}={mcdata1[i + 1, n]:.4f};\n")

            s_minu.append(f"u{i_rownum}")
            s_minv.append(f"v{i_rownum}")
            i_rownum += 1

    s_text = "MODEL:\nMIN =\n"
    s_text += '+'.join(s_minu) + ";\n" + '+'.join(s_minv) + ";\n\n"
    s_text += "!CONSTRAINTS;\n"
    s_text += '\n'.join(s_output) + "\n"
    s_text += '\n'.join(s_xend) + "\nEND"
    
    return s_text

# Streamlit app
st.title("Markov Chain Analysis App")

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
            st.text_area("Equations", value=equations, height=300)
        except Exception as e:
            st.error(f"An error occurred: {e}")

st.sidebar.write("Upload your Excel file and specify the range to generate the Markov Chain equations.")
