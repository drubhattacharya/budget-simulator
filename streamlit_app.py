import streamlit as st
import pandas as pd

st.set_page_config(page_title="Language Access Budget Simulator", layout="centered")
st.title("📊 Budget Constraints Simulator")
st.subheader("Use this tool to explore cost trade-offs in language access strategies.")

# User inputs
st.markdown("### Interpreter Usage & Cost Settings")

st.markdown("Renegotiate your vendor rate for VRI and/or phone and determine your cost savings. Interpreter volume will increase by 20% regardless of your rate strategy due to year-over-year growth and patient/provider demand.")

# Base interpreter minutes per month
base_minutes = st.number_input("Base Interpreter Minutes per Month", min_value=0, value=20000, step=1000)
total_minutes = int(base_minutes * 1.20)
st.metric("Adjusted Monthly Interpreter Minutes", f"{total_minutes:,}", delta="↑ 20%")

vri_percent = st.slider("% of Minutes via VRI", 0, 100, 50)
phone_percent = 100 - vri_percent

vri_rate = st.number_input("VRI Rate ($/min)", min_value=0.0, value=0.85, step=0.01)
phone_rate = st.number_input("Phone Rate ($/min)", min_value=0.0, value=0.80, step=0.01)

# Calculations
vri_minutes = total_minutes * (vri_percent / 100)
phone_minutes = total_minutes * (phone_percent / 100)

vri_cost = vri_minutes * vri_rate
phone_cost = phone_minutes * phone_rate
total_monthly_cost = vri_cost + phone_cost
total_annual_cost = total_monthly_cost * 12

# Cost projections
# Baseline cost is based on status quo rates applied to the original base minutes (before volume growth)
baseline_vri_rate = 0.85
baseline_phone_rate = 0.80
baseline_vri_minutes = base_minutes * (vri_percent / 100)
baseline_phone_minutes = base_minutes * (phone_percent / 100)
baseline_monthly_cost = (baseline_vri_minutes * baseline_vri_rate) + (baseline_phone_minutes * baseline_phone_rate)


# Calculate projected losses or savings
baseline_annual_cost = baseline_monthly_cost * 12
projected_monthly_difference = baseline_monthly_cost - total_monthly_cost
projected_annual_difference = baseline_annual_cost - total_annual_cost
projected_monthly_difference = baseline_monthly_cost - total_monthly_cost
projected_annual_difference = baseline_annual_cost - total_annual_cost

st.markdown("---")
st.markdown("### 💸 Cost Savings")
if projected_annual_difference < 0:
    st.markdown(f"<p style='color:red; font-size:20px;'>Annual Savings: (${abs(projected_annual_difference):,.2f})</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:red; font-size:20px;'>Monthly Savings: (${abs(projected_monthly_difference):,.2f})</p>", unsafe_allow_html=True)
else:
    st.markdown(f"<p style='color:green; font-size:20px;'>Annual Savings: ${projected_annual_difference:,.2f}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:green; font-size:20px;'>Monthly Savings: ${projected_monthly_difference:,.2f}</p>", unsafe_allow_html=True)


st.markdown("### 📈 Break-Even Rate Calculator")
st.caption("The break-even rate is the single per-minute rate that would allow you to serve increased interpreter demand while keeping your total budget flat. It helps you evaluate whether renegotiating your contract is enough to offset rising volume.")

# Break-even rate based on baseline budget and increased volume
if st.button("Calculate Break-Even Rate"):
    break_even_rate = baseline_annual_cost / (total_minutes * 12)
    st.success(f"Break-Even Rate ($/min): ${break_even_rate:.4f}")

# Additional notes
st.markdown("---")
st.markdown("### 📌 Interpretation")
st.info(
    "Interpreter volume increases by 20% year-over-year regardless of rate changes. Even with lower rates, growing demand may result in overall cost increases. Sustainable planning requires considering both volume growth and technology or workflow efficiencies."
)

st.markdown("Use this tool during planning meetings to simulate what-if scenarios.")
