import streamlit as st
import pandas as pd

# Set up the Streamlit page (optional)
st.set_page_config(page_title="DP Plus", layout="wide")

# 1. Load the data
data = pd.read_csv("DP.csv")

# 2. Convert relevant columns to numeric
numeric_columns = [
    "ranking", "academic_reputation", "employer_reputation", "faculty_student",
    "citations_per_faculty", "international_faculty", "international_students",
    "international_research_network", "employment_outcomes",
    "sustainability", "qs_overall_score"
]
for col in numeric_columns:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# 3. Sidebar Selections
st.sidebar.title("Filter Options")

# 3a. Select Education Level
edu_levels = sorted(data['education_level'].unique())
selected_edu = st.sidebar.selectbox("Select Education Level", edu_levels)

# Filter data by the selected education level
filtered_data = data[data['education_level'] == selected_edu]

# 3b. Select Country
countries = sorted(filtered_data['country'].unique())
selected_country = st.sidebar.selectbox("Select Country", countries)

# Filter further by the selected country and sort by ranking
country_data = filtered_data[filtered_data['country'] == selected_country]
country_data = country_data.sort_values(by="ranking", ascending=True)

# Display a header
st.write(f"## {selected_country} | {selected_edu}")

# 3c. Select University
unique_universities = country_data['university'].unique()
selected_uni = st.selectbox("Select University", unique_universities)

# 4. Retrieve the rows for the selected university
uni_data = country_data[country_data['university'] == selected_uni]

# Safely handle the case where there might be no data
if len(uni_data) == 0:
    st.write("No data available for this selection.")
    st.stop()

uni_stats_row = uni_data.iloc[0]  # first row for stats

# 5. Create two columns
left_col, right_col = st.columns(2)

# 5a. Left Column: Programs Offered
with left_col:
    st.subheader("Programs Offered")

    # Use HTML to render a bulleted list with larger font
    programs = uni_data['program'].unique()
    st.markdown("<ul>", unsafe_allow_html=True)
    for prog in programs:
        st.markdown(f"<li style='font-size:18px;'>{prog}</li>", unsafe_allow_html=True)
    st.markdown("</ul>", unsafe_allow_html=True)

# 5b. Right Column: University Stats (as horizontal bars)
with right_col:
    st.caption("Data from QS 2025 Ranking")

    try:
        ranking_value = int(uni_stats_row["ranking"])

        # Increase font size for the university name and ranking
        st.markdown(
            f"""
            <h2 style='font-size:28px; margin-bottom: 10px;'>
                {selected_uni} <u style='font-size:28px;'>#{ranking_value}</u>
            </h2>
            """,
            unsafe_allow_html=True
        )

        # Define the metrics to show
        stats_columns = [
            "qs_overall_score", "academic_reputation", "employer_reputation", "faculty_student",
            "citations_per_faculty", "international_faculty", "international_students",
            "international_research_network", "employment_outcomes",
            "sustainability"
        ]

        # For each metric, display a label, value, and a "progress bar" style element
        for metric in stats_columns:
            value = uni_stats_row[metric]

            metric_name = metric.replace('_', ' ').title()  # e.g. "academic_reputation" -> "Academic Reputation"
            st.write(f"**{metric_name}:** {value}")

            bar_html = f"""
            <div style="background-color: #e0e0e0; border-radius: 5px; height: 12px; width: 100%; margin-bottom: 15px;">
                <div style="background-color: #027efa; width: {value}%; height: 100%; border-radius: 5px;"></div>
            </div>
            """
            st.markdown(bar_html, unsafe_allow_html=True)

    except:
        st.write("No data available for this university.")


footer_html = f"""
    <style>
        .footer {{
            position: fixed;
            bottom: 0;
            left: 0;
            text-align: center;
            padding: 10px;
            font-size: 13px;
            color: #ffffff;
        }}
    </style>
    <div class="footer">
        <a href="https://fatulla.codage.az" target="_blank">
             <img src="https://img.icons8.com/?size=100&id=LmG49EnUQig9&format=png&color=ffffff" width="30" height="30" />
        </a>
        Fatulla Bashirov
        
    </div>
"""
st.sidebar.markdown(footer_html, unsafe_allow_html=True)