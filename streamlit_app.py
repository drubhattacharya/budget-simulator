import streamlit as st
import pandas as pd

st.set_page_config(page_title="Language Access Budget Simulator", layout="centered")
st.title("📊 Budget Constraints Simulator")
st.caption("Note: This tool is designed for single-year planning. It helps evaluate how future volume growth impacts cost projections based on today’s interpreter usage and rate structure.")
st.subheader("Use this tool to explore cost trade-offs in language access strategies.")

# User inputs
if st.button("🔄 Reset to Default Conditions"):
    st.experimental_rerun()
st.markdown("### Interpreter Usage & Cost Settings")

st.markdown("Renegotiate your vendor rate for VRI and/or phone and determine your cost savings. Interpreter volume will increase by 20% regardless of your rate strategy due to year-over-year growth and patient/provider demand.")

# Fixed baseline volume for demo simplicity
base_minutes = 20000
st.markdown(f"**Base Interpreter Minutes per Month:** {base_minutes:,}")
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
baseline_vri_rate = 0.85
baseline_phone_rate = 0.80
# Baseline cost dynamically matches user-defined base minutes to simulate growth over the next year
baseline_vri_minutes = base_minutes * (vri_percent / 100)
baseline_phone_minutes = base_minutes * (phone_percent / 100)
baseline_monthly_cost = (baseline_vri_minutes * baseline_vri_rate) + (baseline_phone_minutes * baseline_phone_rate)


# Calculate projected losses or savings
projected_monthly_difference = (baseline_vri_minutes * baseline_vri_rate + baseline_phone_minutes * baseline_phone_rate) - (vri_minutes * vri_rate + phone_minutes * phone_rate)
projected_annual_difference = projected_monthly_difference * 12
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
    baseline_annual_cost_vri = baseline_vri_minutes * baseline_vri_rate * 12
    baseline_annual_cost_phone = baseline_phone_minutes * baseline_phone_rate * 12

    break_even_rate_vri = baseline_annual_cost_vri / (vri_minutes * 12) if vri_minutes > 0 else 0
    break_even_rate_phone = baseline_annual_cost_phone / (phone_minutes * 12) if phone_minutes > 0 else 0

    st.session_state['break_even_rate_vri'] = break_even_rate_vri
    st.session_state['break_even_rate_phone'] = break_even_rate_phone

    st.success(f"Break-Even VRI Rate ($/min): ${break_even_rate_vri:.4f}")
    st.success(f"Break-Even Phone Rate ($/min): ${break_even_rate_phone:.4f}")
    st.markdown(f"<p style='font-size:18px;'><strong>Keeping the budget as is, how confident are you in renegotiating the vendor rate down under ${break_even_rate_vri:.2f}/min for VRI and ${break_even_rate_phone:.2f}/min for phone to avoid losses? It may be prudent to explore other, cost-effective solutions.</strong></p>", unsafe_allow_html=True)

# Additional notes
st.markdown("---")
st.markdown("### 📌 Interpretation")
st.info(
    "Interpreter volume increases by 20% year-over-year regardless of rate changes. Even with lower rates, growing demand may result in overall cost increases. Sustainable planning requires considering both volume growth and technology or workflow efficiencies."
)

st.markdown("Use this tool during planning meetings to simulate what-if scenarios.")
