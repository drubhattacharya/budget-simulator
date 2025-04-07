import streamlit as st

st.set_page_config(page_title="Interpreter Rate Adjustment Simulator", layout="centered")
st.title("📊 Interpreter Rate Impact Simulator")
st.caption("This tool shows projected savings or losses based on renegotiated per-minute rates and adjustments to modality distribution, assuming a consistent monthly interpreter volume.")

# Fixed baseline
base_minutes = 20000
vri_rate = 0.85
phone_rate = 0.80
vri_default_percent = 0.5
phone_default_percent = 0.5

# Baseline budget (fixed rates and fixed 50/50 modality split)
base_annual_cost = base_minutes * ((vri_default_percent * vri_rate) + (phone_default_percent * phone_rate)) * 12

st.markdown(f"**Baseline Monthly Minutes:** {base_minutes:,}")
st.markdown(f"**Baseline Annual Budget:** ${base_annual_cost:,.2f}")

# Display current rates
st.markdown("**Current VRI Rate:** $0.85/min")
st.markdown("**Current Phone Rate:** $0.80/min")

# User-adjustable inputs
vri_new_rate = st.number_input("Enter your renegotiated VRI rate ($/min)", min_value=0.0, value=0.85, step=0.01)
phone_new_rate = st.number_input("Enter your renegotiated Phone rate ($/min)", min_value=0.0, value=0.80, step=0.01)
vri_percent = st.slider("% of Minutes via VRI", 0, 100, 50)
phone_percent = 100 - vri_percent

# Projected annual cost using updated inputs
projected_annual_cost = base_minutes * ((vri_percent / 100 * vri_new_rate) + (phone_percent / 100 * phone_new_rate)) * 12
projected_monthly_cost = projected_annual_cost / 12

# Savings/losses
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
st.markdown("This tool assumes a fixed baseline of 20,000 interpreter minutes/month with a 50/50 VRI and Phone modality split. Adjust the renegotiated per-minute rates and modality mix to explore potential savings or losses.")
