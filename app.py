import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="AI Data Cleaning Assistant",
    layout="wide"
)

st.title("🧼 AI Data Cleaning Assistant")
st.markdown("Upload a CSV or Excel file and automatically clean messy data.")

# -----------------------------------
# FILE UPLOAD
# -----------------------------------

uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

# -----------------------------------
# MAIN APP
# -----------------------------------

if uploaded_file is not None:

    try:

        # -----------------------------------
        # READ FILE
        # -----------------------------------

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        else:
            df = pd.read_excel(uploaded_file)

        # Create copy
        cleaned_df = df.copy()

        # -----------------------------------
        # SIDEBAR
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

            # Drop missing rows
            if missing_option == "Drop Missing Rows":

                cleaned_df = cleaned_df.dropna()

            # Fill numeric with mean
            elif missing_option == "Fill Numeric with Mean":

                numeric_cols = cleaned_df.select_dtypes(
                    include=np.number
                ).columns

                for col in numeric_cols:

                    cleaned_df[col] = cleaned_df[col].fillna(
                        cleaned_df[col].mean()
                    )

            # Fill text with Unknown
            elif missing_option == "Fill Text with Unknown":

                text_cols = cleaned_df.select_dtypes(
                    include="object"
                ).columns

                for col in text_cols:

                    cleaned_df[col] = cleaned_df[col].fillna(
                        "Unknown"
                    )

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

            st.sidebar.success(
                "Column names standardized"
            )

        # -----------------------------------
        # REMOVE EXTRA SPACES
        # -----------------------------------

        if st.sidebar.checkbox("Remove Extra Spaces"):

            text_cols = cleaned_df.select_dtypes(
                include="object"
            ).columns

            for col in text_cols:

                cleaned_df[col] = (
                    cleaned_df[col]
                    .astype(str)
                    .str.strip()
                )

            st.sidebar.success(
                "Extra spaces removed"
            )

        # -----------------------------------
        # NAME STANDARDIZATION
        # -----------------------------------

        if st.sidebar.checkbox("Standardize Names"):

            text_cols = cleaned_df.select_dtypes(
                include="object"
            ).columns

            for col in text_cols:

                cleaned_df[col] = (
                    cleaned_df[col]
                    .astype(str)
                    .str.title()
                )

            st.sidebar.success(
                "Names standardized"
            )

        # -----------------------------------
        # DATE DETECTION
        # -----------------------------------

        if st.sidebar.checkbox("Auto Detect Date Columns"):

            for col in cleaned_df.columns:

                try:

                    cleaned_df[col] = pd.to_datetime(
                        cleaned_df[col]
                    )

                except:

                    pass

            st.sidebar.success(
                "Date detection completed"
            )

        # -----------------------------------
        # FIX NEGATIVE VALUES
        # -----------------------------------

        if st.sidebar.checkbox("Fix Negative Numeric Values"):

            numeric_cols = cleaned_df.select_dtypes(
                include=np.number
            ).columns

            for col in numeric_cols:

                cleaned_df[col] = cleaned_df[col].clip(
                    lower=0
                )

            st.sidebar.success(
                "Negative values corrected"
            )

        # -----------------------------------
        # DATA QUALITY REPORT
        # -----------------------------------

        st.subheader("📊 Data Quality Report")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Rows",
                cleaned_df.shape[0]
            )

        with col2:
            st.metric(
                "Columns",
                cleaned_df.shape[1]
            )

        with col3:
            st.metric(
                "Missing Values",
                int(cleaned_df.isnull().sum().sum())
            )

        with col4:
            st.metric(
                "Duplicate Rows",
                int(cleaned_df.duplicated().sum())
            )

        # -----------------------------------
        # DISPLAY DATA
        # -----------------------------------

        left, right = st.columns(2)

        with left:

            st.subheader("📄 Original Data")

            st.dataframe(
                df,
                height=400
            )

        with right:

            st.subheader("✅ Cleaned Data")

            st.dataframe(
                cleaned_df,
                height=400
            )

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
        # DATA TYPES
        # -----------------------------------

        st.subheader("📌 Column Data Types")

        dtype_table = pd.DataFrame({

            "Column": cleaned_df.columns,

            "Data Type": cleaned_df.dtypes.astype(str)

        })


        st.dataframe(dtype_table)

        # -----------------------------------
        # DOWNLOAD BUTTON
        # -----------------------------------

        csv = cleaned_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Download Cleaned CSV",
            data=csv,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )

    except Exception as e:

        st.error(f"❌ Error: {e}")

else:

    st.info("Please upload a CSV or Excel file to begin.")

