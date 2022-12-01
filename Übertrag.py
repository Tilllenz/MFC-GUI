with col3:
    st.write('This button will start the umf-measurement')
    placeholder2 = st.empty()
    umf = placeholder2.button('Start dynamic graph')
    diagram = st.empty()

    if umf:
        x_values = []
        y_values = []
        for x_value in range(10):
            with diagram.container():
                x_values.append(x_value)
                y_values.append(random.random())
                source_2 = pd.DataFrame({'x': x_values, 'f(x)': y_values})
                ab = alt.Chart(source_2).mark_line().encode(x='x', y='f(x)',).configure_line(color='red')
                st.altair_chart(ab)
                time.sleep(0.5)