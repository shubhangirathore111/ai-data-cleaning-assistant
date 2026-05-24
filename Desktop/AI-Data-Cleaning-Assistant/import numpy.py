




import streamlit as st
import pandas as pd

st.title("AI Data Cleaning Assistant")

uploaded_file = st.file_uploader("Upload CSV File")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.write("Original Data")
    st.dataframe(df)

    import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Data Cleaning Assistant", layout="wide")
st.title("🧼 AI Data Cleaning Assistant")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file:
    # Load data
    df = pd.read_csv(uploaded_file)
    
    # We create a copy to keep track of changes
    cleaned_df = df.copy()

    # Layout: Split screen into Sidebar (Controls) and Main Panel (Data preview)
    st.sidebar.header("Data Cleaning Options")

    # --- 1. HANDLE DUPLICATES ---
    if st.sidebar.checkbox("Remove Duplicate Rows"):
        initial_count = len(cleaned_df)
        cleaned_df = cleaned_df.drop_duplicates()
        removed_dupes = initial_count - len(cleaned_df)
        st.sidebar.success(f"Removed {removed_dupes} duplicate rows!")

    # --- 2. HANDLE MISSING VALUES ---
    if st.sidebar.checkbox("Handle Missing Values"):
        missing_action = st.sidebar.selectbox(
            "Choose strategy for missing data:",
            ["Drop rows with any missing values", "Fill missing numeric values with Mean", "Fill with 'Unknown' (Text)"]
        )
        
        if missing_action == "Drop rows with any missing values":
            cleaned_df = cleaned_df.dropna()
        elif missing_action == "Fill missing numeric values with Mean":
            numeric_cols = cleaned_df.select_dtypes(include=['number']).columns
            cleaned_df[numeric_cols] = cleaned_df[numeric_cols].fillna(cleaned_df[numeric_cols].mean())
        elif missing_action == "Fill with 'Unknown' (Text)":
            cleaned_df = cleaned_df.fillna("Unknown")
            
        st.sidebar.success("Missing values handled!")

    # --- MAIN PANEL SHOWCASE ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Data")
        st.caption(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
        st.dataframe(df, height=400)

    with col2:
        st.subheader("Cleaned Data Preview")
        st.caption(f"Shape: {cleaned_df.shape[0]} rows, {cleaned_df.shape[1]} columns")
        st.dataframe(cleaned_df, height=400)

    # --- DOWNLOAD BUTTON ---
    st.markdown("---")
    st.subheader("Export Your Clean Data")
    
    # Convert cleaned dataframe to CSV bytes
    csv_bytes = cleaned_df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 Download Cleaned CSV",
        data=csv_bytes,
        file_name="cleaned_data.csv",
        mime="text/csv"

        streamlit run app.py

    )
st.subheader("Missing Values")

missing = df.isnull().sum()

st.write(missing)
duplicates = df[df.duplicated()]

st.subheader("Duplicate Rows")

st.dataframe(duplicates)

try:
    df['Date'] = pd.to_datetime(df['Date'])
except:
    st.write("Date format issue detected")

    outliers = df[df['Salary'] < 0]

st.subheader("Outliers")

st.dataframe(outliers)

if st.button("Clean Data"):

    df = df.drop_duplicates()

    df['City'] = df['City'].fillna("Unknown")

    df['Salary'] = df['Salary'].clip(lower=0)

    st.success("Data Cleaned")

    st.dataframe(df)

    csv = df.to_csv(index=False)

st.download_button(
    label="Download Cleaned CSV",
    data=csv,
    file_name='cleaned_data.csv',
    mime='text/csv'
)
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY"
)

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "user", "content": "Hello"}
    ]
)

print(response.choices[0].message.content)

from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY"
)

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "user", "content": "Hello"}
    ]
)

print(response.choices[0].message.content)



st.metric()
st.columns()
st.sidebar()


git --version



README.md

# AI Data Cleaning Assistant

An AI-powered application that detects duplicates, null values, format issues, and outliers in datasets.

## Features
- Duplicate detection
- Missing value handling
- Outlier detection
- AI cleaning suggestions
- CSV download

## Tech Stack
- Python
- Pandas
- Streamlit
- OpenAI API
venv/
__pycache__/
.env
*.pyc




h
echo "# ai-data-cleaning-assistant" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/shubhangirathore111/ai-data-cleaning-assistant.git
git push -u origin main

git branch
git push -u origin main


git add .

git push -u origin main

git remote add origin ...