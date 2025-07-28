import streamlit as st
import pandas as pd

# --- Functions ---
def calculate_return_on_investment(investment, location, bedrooms, income_data):
    row = income_data[income_data['Bedrooms'] == bedrooms].iloc[0]
    location_column = f"{location} (£)"
    monthly_income = row[location_column]
    yearly_income = monthly_income * 12
    yield_percent = (yearly_income / investment) * 100
    total_months_to_return = investment / monthly_income
    years = int(total_months_to_return // 12)
    months = int(round(total_months_to_return % 12))
    years_months_str = f"{years} years and {months} months"
    return {
        'Bedrooms': bedrooms,
        'Location': location,
        'Average Monthly Income After All Fees (£)': monthly_income,
        'Yield (%)': round(yield_percent, 2),
        'Years to Return': years_months_str
    }

def calculate_required_nightly_rate(take_home, mgmt_fee, guest_clean_fee, client_clean_fee, linen_charge):
    fee_multipliers = {
        10: 100 / 69,
        15: 100 / 64,
        17: 100 / 60,
        18: 100 / 59
    }
    if mgmt_fee not in fee_multipliers:
        return None, "Invalid management fee. Please choose from 10, 15, 17, or 18."

    extra_cleaning_cost = (client_clean_fee + linen_charge) - guest_clean_fee
    adjusted_take_home = take_home + extra_cleaning_cost * 7 if extra_cleaning_cost > 0 else take_home
    average_nightly_rate = adjusted_take_home * fee_multipliers[mgmt_fee] / 21
    return average_nightly_rate, None

# --- Data ---
data = {
    'Bedrooms': ['Studio', '1', '2', '3', '4'],
    'City Centre (£)': [1445, 1500, 1703, 4200, 5131],
    'West End (£)': [1083.75, 1125.00, 1299.00, 3163.00, 3848.25],
}
df = pd.DataFrame(data)

# --- App Layout ---
st.set_page_config(page_title="Property Investment Calculator", layout="centered")
st.title("🏠 Property Investment Calculator")

# --- Section 1: Investment Return Calculator ---
st.header("📈 Investment Return")
investment_input = st.number_input("Enter your investment amount in £:", min_value=0.0, step=1000.0)
location_input = st.selectbox("Select the location:", ['City Centre', 'West End'])
bedrooms_input = st.selectbox("Select the number of bedrooms:", ['Studio', '1', '2', '3', '4'])

if st.button("🔍 Calculate Investment Return"):
    st.session_state["investment_result"] = calculate_return_on_investment(
        investment_input, location_input, bedrooms_input, df
    )

if st.session_state.get("investment_result"):
    result = st.session_state["investment_result"]
    st.subheader("📊 Investment Analysis Result")
    st.markdown(f"**{result['Bedrooms']} bed in {result['Location']}**")
    st.markdown(f"- **Average Monthly Income After All Fees**: £{result['Average Monthly Income After All Fees (£)']:.2f}")
    st.markdown(f"- **Yield**: {result['Yield (%)']}%")
    st.markdown(f"- **Years to Return Investment**: {result['Years to Return']}")

# --- Section 2: Nightly Rate Calculator ---
st.header("💷 Required Nightly Rate Calculator")
st.markdown("Enter your **desired monthly take-home pay**, and we'll calculate the nightly rate you need to charge.")

with st.form("nightly_rate_form"):
    take_home_input = st.number_input(
        "Enter your **desired monthly take-home pay** (£):",
        min_value=0.0,
        step=50.0,
        help="This is the net rent you want to pocket each month after all fees."
    )
    mgmt_fee = st.selectbox("Select management fee %:", [10, 15, 17, 18])
    guest_clean_fee = st.number_input("Cleaning fee paid by guest (£):", min_value=0.0, step=1.0)
    client_clean_fee = st.number_input("Cleaning fee paid by owner (with VAT) (£):", min_value=0.0, step=1.0)
    linen_charge = st.number_input("Linen charge per clean (with VAT) (£):", min_value=0.0, step=1.0)
    submit = st.form_submit_button("Calculate Required Nightly Rate")

if submit:
    nightly_rate, error = calculate_required_nightly_rate(
        take_home_input, mgmt_fee, guest_clean_fee, client_clean_fee, linen_charge
    )
    if error:
        st.error(error)
    else:
        st.success(
            f"✅ To pocket £{take_home_input:.2f} per month, "
            f"you need an **average nightly rate of £{nightly_rate:.2f}**."
        )
