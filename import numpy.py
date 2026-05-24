import pip
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="AI Data Cleaning Assistant",
    layout="wide"
)

st.title("🧼 AI Data Cleaning Assistant")
st.markdown("Upload a CSV file and automatically clean messy data.")

# -----------------------------------
# FILE UPLOAD
# -----------------------------------

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

# -----------------------------------
# MAIN APP
# -----------------------------------

if uploaded_file is not None:

    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)

        # Copy original data
        cleaned_df = df.copy()

        # -----------------------------------
        # SIDEBAR OPTIONS
        # -----------------------------------

        st.sidebar.header("⚙️ Cleaning Options")

        # -----------------------------------
        # REMOVE DUPLICATES
        # -----------------------------------

        if st.sidebar.checkbox("Remove Duplicate Rows"):

            before = len(cleaned_df)

            cleaned_df = cleaned_df.drop_duplicates()

            after = len(cleaned_df)

            st.sidebar.success(
                f"Removed {before - after} duplicate rows"
            )

        # -----------------------------------
        # HANDLE MISSING VALUES
        # -----------------------------------

        if st.sidebar.checkbox("Handle Missing Values"):

            missing_option = st.sidebar.selectbox(
                "Choose Missing Value Strategy",
                [
                    "Drop Missing Rows",
                    "Fill Numeric with Mean",
                    "Fill Text with Unknown"
                ]
            )

            # Drop rows
            if missing_option == "Drop Missing Rows":

                cleaned_df = cleaned_df.dropna()

            # Fill numeric columns
            elif missing_option == "Fill Numeric with Mean":

                numeric_cols = cleaned_df.select_dtypes(
                    include=np.number
                ).columns

                for col in numeric_cols:
                    cleaned_df[col] = cleaned_df[col].fillna(
                        cleaned_df[col].mean()
                    )

            # Fill text columns
            elif missing_option == "Fill Text with Unknown":

                text_cols = cleaned_df.select_dtypes(
                    include="object"
                ).columns

                for col in text_cols:
                    cleaned_df[col] = cleaned_df[col].fillna("Unknown")

            st.sidebar.success("Missing values handled")

        # -----------------------------------
        # STANDARDIZE COLUMN NAMES
        # -----------------------------------

        if st.sidebar.checkbox("Standardize Column Names"):

            cleaned_df.columns = (
                cleaned_df.columns
                .str.strip()
                .str.lower()
                .str.replace(" ", "_")
            )

            st.sidebar.success("Column names standardized")

        # -----------------------------------
        # REMOVE EXTRA SPACES
        # -----------------------------------

        if st.sidebar.checkbox("Remove Extra Spaces"):

            text_cols = cleaned_df.select_dtypes(
                include="object"
            ).columns

            for col in text_cols:
                cleaned_df[col] = cleaned_df[col].astype(str).str.strip()

            st.sidebar.success("Extra spaces removed")

        # -----------------------------------
        # DATE FORMAT FIXING
        # -----------------------------------

        if st.sidebar.checkbox("Auto Detect Date Columns"):

            for col in cleaned_df.columns:

                try:
                    cleaned_df[col] = pd.to_datetime(
                        cleaned_df[col]
                    )

                except:
                    pass

            st.sidebar.success("Date detection completed")

        # -----------------------------------
        # NEGATIVE VALUE FIX
        # -----------------------------------

        if st.sidebar.checkbox("Fix Negative Numeric Values"):

            numeric_cols = cleaned_df.select_dtypes(
                include=np.number
            ).columns

            for col in numeric_cols:

                cleaned_df[col] = cleaned_df[col].clip(lower=0)

            st.sidebar.success("Negative values corrected")

        # -----------------------------------
        # DATA QUALITY REPORT
        # -----------------------------------

        st.subheader("📊 Data Quality Report")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Rows", cleaned_df.shape[0])

        with col2:
            st.metric("Columns", cleaned_df.shape[1])

        with col3:
            st.metric(
                "Missing Values",
                int(cleaned_df.isnull().sum().sum())
            )

        # -----------------------------------
        # DISPLAY DATA
        # -----------------------------------

        left, right = st.columns(2)

        with left:
            st.subheader("Original Data")
            st.dataframe(df, height=400)

        with right:
            st.subheader("Cleaned Data")
            st.dataframe(cleaned_df, height=400)

        # -----------------------------------
        # MISSING VALUES TABLE
        # -----------------------------------

        st.subheader("🔍 Missing Values Summary")

        missing_table = pd.DataFrame({
            "Column": cleaned_df.columns,
            "Missing Values": cleaned_df.isnull().sum().values
        })

        st.dataframe(missing_table)

        # -----------------------------------
        # DOWNLOAD BUTTON
        # -----------------------------------

        csv = cleaned_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download Cleaned CSV",
            data=csv,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )

    except Exception as e:

        st.error(f"Error: {e}")
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO