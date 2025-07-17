import streamlit as st
import pandas as pd

def calculate_return_on_investment(investment, location, bedrooms, income_data):
    # Filter the row matching the given bedrooms
    row = income_data[income_data['Bedrooms'] == bedrooms].iloc[0]

    # Get monthly income based on location
    location_column = f"{location} (£)"
    monthly_income = row[location_column]
    yearly_income = monthly_income * 12
    yield_percent = (yearly_income / investment) * 100
    total_months_to_return = investment / monthly_income
    years = int(total_months_to_return // 12)
    months = int(round(total_months_to_return % 12))
    years_months_str = f"{years} years and {months} months"

    result = {
        'Bedrooms': bedrooms,
        'Location': location,
        'Average Monthly Income After All Fees (£)': monthly_income,
        'Yield (%)': round(yield_percent, 2),
        'Years to Return': years_months_str
    }
    return result

# Data setup
data = {
    'Bedrooms': ['Studio', '1', '2', '3', '4'],
    'City Centre (£)': [1445, 1500, 1703, 4200, 5131],
    'West End (£)': [1083.75, 1125.00, 1299.00, 3163.00, 3848.25],
}
df = pd.DataFrame(data)

st.title("Property Investment Return Calculator")

# User inputs
investment_input = st.number_input("Enter your investment amount in £:", min_value=0.0, value=100000.0, step=1000.0, format="%.2f")

location_input = st.selectbox("Select the location:", options=['City Centre', 'West End'])

bedrooms_input = st.selectbox("Select the number of bedrooms:", options=['Studio', '1', '2', '3', '4'])

if investment_input > 0:
    # Calculate result
    result = calculate_return_on_investment(investment_input, location_input, bedrooms_input, df)

    # Display result
    st.markdown("### Investment Analysis Result")
    st.write(f"**{result['Bedrooms']} bed in {result['Location']}**")
    st.write(f"- Average Monthly Income After All Fees: £{result['Average Monthly Income After All Fees (£)']:.2f}")
    st.write(f"- Yield: {result['Yield (%)']}%")
    st.write(f"- Years to Return Investment: {result['Years to Return']}")
else:
    st.warning("Please enter a valid investment amount.")
