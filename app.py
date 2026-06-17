import streamlit as st
import pandas as pd

st.set_page_config(page_title="Transaction Data Validator", layout="wide")

st.title("📊 Transaction Data Validator & Processor")

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    errors = []

    # Missing values validation
    missing_values = df.isnull().sum().sum()

    # Phone validation
    if "phone" in df.columns and "country" in df.columns:

        for index, row in df.iterrows():

            phone = str(row["phone"])
            country = str(row["country"]).lower()

            if country == "india":
                if len(phone) != 10:
                    errors.append(index)

            elif country == "singapore":
                if len(phone) != 8:
                    errors.append(index)

    st.subheader("Validation Summary")

    st.write(f"Invalid Phone Records: {len(errors)}")
    st.write(f"Missing Values Found: {missing_values}")

    cleaned_df = df.drop(errors)

    st.subheader("Cleaned Dataset")
    st.dataframe(cleaned_df.head())

    st.download_button(
        "⬇ Download Cleaned CSV",
        cleaned_df.to_csv(index=False),
        "cleaned_data.csv",
        "text/csv"
    )

    # CSV Splitter
    st.subheader("CSV Splitter")

    chunk_size = st.number_input(
        "Rows per file",
        min_value=1,
        value=100
    )

    if st.button("Split CSV"):

        total_rows = len(df)

        chunks = [
            df[i:i+chunk_size]
            for i in range(0, total_rows, chunk_size)
        ]

        st.success(
            f"{len(chunks)} files created successfully!"
        )