import streamlit as st

st.set_page_config(page_title="Interpreter Rate Adjustment Simulator", layout="centered")
st.title("📊 Interpreter Rate Impact Simulator")
st.caption("This tool shows projected savings or losses based on a renegotiated per-minute rate and projected 20% increase in interpreter volume.")

# Fixed baseline
base_minutes = 20000
projected_minutes = int(base_minutes * 1.20)
base_rate = 0.825  # weighted average baseline rate
base_annual_cost = base_minutes * base_rate * 12

st.markdown(f"**Baseline Monthly Minutes:** {base_minutes:,}")
st.markdown(f"**Projected Monthly Minutes (20% increase):** {projected_minutes:,}")
st.markdown(f"**Baseline Annual Budget:** ${base_annual_cost:,.2f}")

# User input: renegotiated rate
new_rate = st.number_input("Enter your renegotiated per-minute rate ($)", min_value=0.0, value=0.75, step=0.01)
projected_annual_cost = projected_minutes * new_rate * 12
projected_monthly_cost = projected_minutes * new_rate

savings_annual = base_annual_cost - projected_annual_cost
savings_monthly = base_annual_cost / 12 - projected_monthly_cost

st.markdown("---")
st.markdown("### 💸 Projected Cost Impact")
if savings_annual < 0:
    st.markdown(f"<p style='color:red; font-size:20px;'>Annual Loss: (${abs(savings_annual):,.2f})</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:red; font-size:20px;'>Monthly Loss: (${abs(savings_monthly):,.2f})</p>", unsafe_allow_html=True)
else:
    st.markdown(f"<p style='color:green; font-size:20px;'>Annual Savings: ${savings_annual:,.2f}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:green; font-size:20px;'>Monthly Savings: ${savings_monthly:,.2f}</p>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("This tool assumes a fixed baseline of 20,000 interpreter minutes/month and a projected 20% increase in volume. Adjust the per-minute rate to see whether savings are realistic.")
