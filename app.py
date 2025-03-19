import streamlit as st
import pandas as pd

# Cache the data loading for performance
@st.cache_data
def load_data():
    return pd.read_csv("DP.csv")

df = load_data()

st.title("DP plus")
st.write("Select filters in the sidebar to view programs that match the criteria.")

# Start with the full DataFrame and update it as filters are applied
filtered_df = df.copy()

# Filter 1: Education Level
edu_options = ["All"] + sorted(df["education_level"].unique())
selected_edu = st.sidebar.selectbox("Education Level", options=edu_options)
if selected_edu != "All":
    filtered_df = filtered_df[filtered_df["education_level"] == selected_edu]

# Filter 2: Country (options based on the current filtered DataFrame)
country_options = ["All"] + sorted(filtered_df["country"].unique())
selected_country = st.sidebar.selectbox("Country", options=country_options)
if selected_country != "All":
    filtered_df = filtered_df[filtered_df["country"] == selected_country]

# Filter 3: University (options based on the current filtered DataFrame)
university_options = ["All"] + sorted(filtered_df["university"].unique())
selected_university = st.sidebar.selectbox("University", options=university_options)
if selected_university != "All":
    filtered_df = filtered_df[filtered_df["university"] == selected_university]

# Filter 4: Program (options based on the current filtered DataFrame)
program_options = ["All"] + sorted(filtered_df["program"].unique())
selected_program = st.sidebar.selectbox("Program", options=program_options)
if selected_program != "All":
    filtered_df = filtered_df[filtered_df["program"] == selected_program]

st.write("## Filtered Programs")
st.dataframe(filtered_df)

# Option to download the filtered DataFrame as a CSV
@st.cache_data
def convert_df_to_csv(dataframe):
    return dataframe.to_csv(index=False).encode('utf-8')

csv_data = convert_df_to_csv(filtered_df)
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv_data,
    file_name='filtered_programs.csv',
    mime='text/csv',
)
