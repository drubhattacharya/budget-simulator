import streamlit as st
import pandas as pd

st.set_page_config(page_title="Language Access Budget Simulator", layout="centered")
st.title("📊 Budget Constraints Simulator")
st.subheader("Use this tool to explore cost trade-offs in language access strategies.")

# User inputs
st.markdown("### Monthly Interpreter Usage Inputs")
total_minutes = st.number_input("Total Interpreter Minutes per Month", min_value=0, value=20000, step=1000)
vri_percent = st.slider("% of Minutes via VRI", 0, 100, 50)
phone_percent = 100 - vri_percent

st.markdown("### Interpreter Cost Settings")
custom_rates = st.checkbox("Use a single negotiated rate for both modalities", value=False)

if custom_rates:
    blended_rate = st.number_input("Blended Rate ($/min)", min_value=0.0, value=0.75, step=0.01)
    vri_rate = phone_rate = blended_rate
else:
    vri_rate = st.number_input("VRI Rate ($/min)", min_value=0.0, value=0.85, step=0.01)
    phone_rate = st.number_input("Phone Rate ($/min)", min_value=0.0, value=0.80, step=0.01)

# Calculations
vri_minutes = total_minutes * (vri_percent / 100)
phone_minutes = total_minutes * (phone_percent / 100)

vri_cost = vri_minutes * vri_rate
phone_cost = phone_minutes * phone_rate
total_monthly_cost = vri_cost + phone_cost
total_annual_cost = total_monthly_cost * 12

# Output results
st.markdown("---")
st.markdown("### 💰 Cost Summary")
st.metric("Monthly Cost ($)", f"{total_monthly_cost:,.2f}")
st.metric("Annual Cost ($)", f"{total_annual_cost:,.2f}")

# Additional notes
st.markdown("---")
st.markdown("### 📌 Interpretation")
st.info(
    "Even with rate improvements, growing LEP volume may still lead to rising costs year-over-year. Savings alone may not be enough — strategic reinvestment is key."
)

st.markdown("Use this tool during planning meetings to simulate what-if scenarios.")
