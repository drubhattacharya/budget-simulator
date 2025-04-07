import streamlit as st

st.set_page_config(page_title="Interpreter Rate Adjustment Simulator", layout="centered")
st.title("📊 Vendor Rate Renegotiation Simulator")
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
projected_minutes = base_minutes * 1.20
projected_annual_cost = projected_minutes * ((vri_percent / 100 * vri_new_rate) + (phone_percent / 100 * phone_new_rate)) * 12
projected_monthly_cost = projected_annual_cost / 12

# Savings/losses
savings_annual = base_annual_cost - projected_annual_cost
savings_monthly = base_annual_cost / 12 - projected_monthly_cost

# Calculate projected savings assuming no growth (for illusion of success)
projected_savings_static = (base_minutes * ((vri_default_percent * vri_rate) + (phone_default_percent * phone_rate)) - base_minutes * ((vri_percent / 100 * vri_new_rate) + (phone_percent / 100 * phone_new_rate))) * 12
monthly_projected_savings_static = projected_savings_static / 12

# True cost impact with 20% volume growth (actual)
projected_minutes_actual = base_minutes * 1.20
projected_actual_annual_cost = projected_minutes_actual * ((vri_percent / 100 * vri_new_rate) + (phone_percent / 100 * phone_new_rate)) * 12
actual_annual_savings = base_annual_cost - projected_actual_annual_cost
actual_monthly_savings = actual_annual_savings / 12

# Formatting
static_monthly_text = f"${monthly_projected_savings_static:,.2f}" if monthly_projected_savings_static >= 0 else f"(${abs(monthly_projected_savings_static):,.2f})"
static_annual_text = f"${projected_savings_static:,.2f}" if projected_savings_static >= 0 else f"(${abs(projected_savings_static):,.2f})"
actual_monthly_text = f"${actual_monthly_savings:,.2f}" if actual_monthly_savings >= 0 else f"(${abs(actual_monthly_savings):,.2f})"
actual_annual_text = f"${actual_annual_savings:,.2f}" if actual_annual_savings >= 0 else f"(${abs(actual_annual_savings):,.2f})"

color_static = 'green' if projected_savings_static >= 0 else 'red'
color_actual = 'green' if actual_annual_savings >= 0 else 'red'

st.markdown(f"<p style='color:{color_static}; font-size:16px;'><strong>Projected (flat volume): Monthly = {static_monthly_text}, Annual = {static_annual_text}</strong></p>", unsafe_allow_html=True)
st.markdown(f"<p style='color:{color_actual}; font-size:16px;'><strong>Actual (20% growth): Monthly = {actual_monthly_text}, Annual = {actual_annual_text}</strong></p>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("**Takeaway:** While renegotiating vendor rates may appear effective in isolation, it fails to offset increasing interpreter demand. With year-over-year LEP volume growth exceeding 20%, vendor rate adjustments alone are neither effective nor sustainable.")

st.markdown("---")


monthly_savings_text = f"${savings_monthly:,.2f}" if savings_monthly >= 0 else f"(${abs(savings_monthly):,.2f})"
annual_savings_text = f"${savings_annual:,.2f}" if savings_annual >= 0 else f"(${abs(savings_annual):,.2f})"

color = 'green' if savings_annual >= 0 else 'red'
if st.button("🔍 Calculate Break-Even Rate"):
    baseline_vri_cost = base_annual_cost * (vri_percent / 100)
    baseline_phone_cost = base_annual_cost * (phone_percent / 100)
    projected_vri_minutes = base_minutes * 1.20 * (vri_percent / 100)
    projected_phone_minutes = base_minutes * 1.20 * (phone_percent / 100)
    break_even_rate_vri = baseline_vri_cost / projected_vri_minutes
    break_even_rate_phone = baseline_phone_cost / projected_phone_minutes
    st.markdown(f"<p style='font-size:16px;'><strong>How confident are you in renegotiating your VRI rate down under ${break_even_rate_vri:.2f} and your phone rate down under ${break_even_rate_phone:.2f}? It may be prudent to explore other, cost-effective solutions.</strong></p>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("This tool assumes a fixed baseline of 20,000 interpreter minutes/month with a 50/50 VRI and Phone modality split. Adjust the renegotiated per-minute rates and modality mix to explore potential savings or losses.")
