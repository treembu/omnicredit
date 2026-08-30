# -*- coding: utf-8 -*-
import streamlit as st

st.set_page_config(page_title="Test", layout="wide")

st.title("Testing Dollar Signs")

# Test different ways to display dollar signs
st.write("### Method 1: st.caption with f-string")
st.caption(f"${1.99:.2f} per loan")

st.write("### Method 2: st.markdown with regular text")
st.markdown("$1.99 per loan")

st.write("### Method 3: st.write with f-string")
st.write(f"${1.99:.2f} per loan")

st.write("### Method 4: st.text with f-string")
st.text(f"${1.99:.2f} per loan")

st.write("### Method 5: Plain string in caption")
st.caption("$1.99 per loan")

st.write("### Method 6: HTML escape attempt")
st.caption("&#36;1.99 per loan")
