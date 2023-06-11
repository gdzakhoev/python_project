import time
import streamlit as st
import pandas as pd

st.write("Дзаха текстовые секции на тебе =)")

# st.title("App Title")

st.header("Our main table")
statesData = pd.read_csv('EXPstateData.csv')
st.dataframe(statesData)

st.header("Correlation")
st.image('corr.png')

st.header("Heatmap")
st.image('geodata.png')
