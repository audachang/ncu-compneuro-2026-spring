import streamlit as st
import time

st.balloons()
st.progress(10)
with st.spinner('Wait for it...'):
    time.sleep(10)
st.success("You did it!")
st.error("Error occurred")
st.warning("This is a warning")
st.info("It's easy to build a Streamlit app")
st.exception(RuntimeError("RuntimeError exception"))
