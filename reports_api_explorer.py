import streamlit as st
import pandas as pd
import numpy as np

title = "My First Data Explorer"
st.set_page_config(page_title=title)
st.title(title)
st.text("A basic data data explorer by Martyn (aged 9)")

# Let's get data
report = st.file_uploader("Upload a file", type="csv",
                          accept_multiple_files=False)

if not report:
    st.stop()

if report is not None:
    report.seek(0)
    df = pd.read_csv(report)
    # st.balloons()

    analysis_column, dataframe_column = st.beta_columns(2)

    with analysis_column:
        st.header("Analysis")
        st.write("Number of rows: ", len(df.index))
        st.write("Number of columns: ", len(df.columns))

        empty_cols = [col for col in df.columns if df[col].isnull().all()]
        has_empty_columns = "Yes" if len(empty_cols) > 0 else "No"
        st.write("Are there empty columns? ", has_empty_columns)

        if st.button("Remove empty columns"):
            df.drop(empty_cols, axis=1, inplace=True)

    with dataframe_column:
        st.header("Dataframe")
        df

# Traffic Analysis
st.header("Traffic Analysis")

traffic_column, direction_column = st.beta_columns(2)

with traffic_column:
    st.subheader("Traffic By Hour")
    df["date_received"] = pd.to_datetime(df["date_received"])

    values_by_hour = np.histogram(df["date_received"].dt.hour,
                                  bins=24, range=(0, 24))[0]

    values_by_minutes = np.histogram(df["date_received"].dt.minute,
                                     bins=1440, range=(0, 60))[0]

    option = st.selectbox("Pick a resolution", ("Hourly", "Minutes"))

    if option == "Hourly":
        values = values_by_hour
    else:
        values = values_by_minutes
    st.line_chart(values)

with direction_column:
    st.subheader("Direction of Traffic")
    if st.checkbox("Show traffic direction"):
        directions = df["direction"].value_counts()
        st.bar_chart(directions)

# Network Analysis
st.header("Network Analysis")
networks = df["network_name"].unique()
network_usage = df["network_name"].value_counts()


network_selections = st.multiselect("Select specific networks", networks)

if network_selections:
    network_usage = network_usage.loc[network_usage.index.isin(
        network_selections)]

st.bar_chart(network_usage)
