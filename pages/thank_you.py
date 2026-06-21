import streamlit as st

st.set_page_config(page_title="Thank You", page_icon="✅")
st.title("🎉 Thank you for your order!")
st.write("You will receive a confirmation email shortly.")
st.write("We'll process your order and get back to you.")
st.link_button("Return to Home", "/")
