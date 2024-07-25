import streamlit as st
import pandas as pd
import numpy as np

def main():
    st.title("Markov Chain Analysis")

    st.sidebar.header("Upload Your Excel File")
    uploaded_file = st.sidebar.file_uploader("Choose an Excel file", type=["xlsx", "xls"])
    
    if uploaded_file:
        # Display a message to user
        st.write("**Uploaded File:**")
        st.write(uploaded_file.name)
        
        # Load the Excel file
        data = pd.ExcelFile(uploaded_file)
        sheets = data.sheet_names
        st.sidebar.write("Available sheets:")
        st.sidebar.write(sheets)
        
        # User input for data range
        st.sidebar.header("Select Data Range")
        sheet_name = st.sidebar.text_input("Sheet Name", value="Sheet1")
        start_row = st.sidebar.number_input("Start Row", min_value=1, value=2)
        end_row = st.sidebar.number_input("End Row", min_value=1, value=10)
        start_col = st.sidebar.number_input("Start Column", min_value=1, value=1)
        end_col = st.sidebar.number_input("End Column", min_value=1, value=5)

        # Button to generate equations
        if st.sidebar.button("Generate Markov Chain Equations"):
            try:
                # Load selected sheet and data range
                df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                selected_data = df.iloc[start_row-1:end_row, start_col-1:end_col]
                
                # Generate the Markov Chain equations
                equations = generate_equations(selected_data)
                
                # Display the equations
                st.subheader("Generated Markov Chain Equations")
                st.text_area("Copy the equations below:", equations, height=300)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
        
def generate_equations(df):
    """Generate Markov Chain equations based on the input data frame."""
    rows, cols = df.shape
    equations = ""
    min_u = []
    min_v = []
    s_xend = ""

    for n in range(cols):
        for i in range(rows):
            if i == 0:
                if n < cols - 1:
                    s_xend += f"1*x{chr(96+n+1)}{i+1}+"
                else:
                    s_xend += f"1*x{chr(96+n+1)}{i+1}=1;"
                if n % 10 == 0:
                    s_xend += "\n"
                
            for j in range(cols - 1):
                probability = df.iloc[i, j] / df.iloc[i, cols - 1] * 10000
                probability = round(probability + 0.5) / 10000
                equations += f"{probability}*x{chr(96+j+1)}{n+1}+"
                if j == 5:
                    equations += "\n"
            
            equations += f"m{i+1}-v{i+1}={df.iloc[i, n+1]};\n"
            min_u.append(f"m{i+1}+")
            if n == cols - 1 and i == rows - 1:
                min_v.append(f"n{i+1};")
            else:
                min_v.append(f"n{i+1}+")
                
        equations += "\n\n"

    s_text = "MODEL:\n"
    s_text += "MIN =\n"
    s_text += "".join(min_u) + "\n"
    s_text += "".join(min_v) + "\n\n"
    s_text += "!CONSTRAINTS;\n"
    s_text += equations + "\n"
    s_text += s_xend + "\n"
    s_text += "END"

    return s_text

if __name__ == "__main__":
    main()
