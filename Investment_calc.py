if st.session_state.get("investment_result"):
    result = st.session_state["investment_result"]

    st.subheader("Investment Analysis Result")
    st.markdown(f"**{result['Bedrooms']} bed in {result['Location']}**")
    st.markdown(f"- Average Monthly Income After All Fees: £{result['Average Monthly Income After All Fees (£)']:.2f}")
    st.markdown(f"- Yield: {result['Yield (%)']}%")
    st.markdown(f"- Years to Return Investment: {result['Years to Return']}")

    st.subheader("Required Nightly Rate to Achieve This Income")
    with st.form("nightly_rate_form"):
        mgmt_fee = st.selectbox("Select management fee %:", [10, 15, 17, 18], key="mgmt")
        guest_clean_fee = st.number_input("Cleaning fee paid by guest (£):", min_value=0.0, step=1.0, key="guest")
        client_clean_fee = st.number_input("Cleaning fee paid by client (with VAT) (£):", min_value=0.0, step=1.0, key="client")
        linen_charge = st.number_input("Linen charge per clean (with VAT) (£):", min_value=0.0, step=1.0, key="linen")
        submit = st.form_submit_button("Calculate Required Nightly Rate")

        if submit:
            nightly_rate, error = calculate_required_nightly_rate(
                result['Average Monthly Income After All Fees (£)'],
                mgmt_fee,
                guest_clean_fee,
                client_clean_fee,
                linen_charge
            )

            if error:
                st.error(error)
            else:
                st.markdown(f"To achieve an average monthly income of £{result['Average Monthly Income After All Fees (£)']:.2f}, your average nightly rate should be: **£{nightly_rate:.2f}**")
