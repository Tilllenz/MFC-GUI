import streamlit as st
import numpy as np
import pandas as pd
import time
import altair as alt
import random
from datetime import datetime

n = 20
pV = np.random.randint(0, 100, 20)
x = np.arange(0, 100, 5)
source = pd.DataFrame({
    'x': x,
    'f(x)': pV
})
aa = alt.Chart(source).mark_line().encode(
    x='x',
    y='f(x)',
    color='red'
)

# st.write(pV,x)

st.set_page_config(
    page_title="MFC-Controller",
    layout="wide",
)
st.title('MFC-GUI')
st.write('Here you can determine the umf and calculate your desired V')

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.write('This button will start the umf-measurement')
    placeholder = st.empty()
    umf = placeholder.button('Start umf-measurement')
    if umf:
        placeholder.empty()
        st.write('UMF Measurement is running...')

        st.write('Diagram will be created...')

        st.write('This takes approx. 5 minutes')
        xx = np.array(list(zip(x, pV)))
        st.altair_chart(aa)
        st.write(xx)

with col2:
    ratio = st.number_input("Enter u/umf-ratio to determine V", min_value=0.0, max_value=5.0)
    x = ratio
    st.write('The calculated V is ', x, ' * V at umf')

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

with col4:
    a = st.number_input("Enter a", min_value=0.0, max_value=5.0)
    b = st.number_input("Enter b", min_value=0.0, max_value=5.0)
    c = st.number_input("Enter c", min_value=0.0, max_value=5.0)

    dt = datetime.now()
    dtstr = str(dt.year) + '-' + str(dt.month) + '-' + str(dt.day) + ' ' + str(dt.hour) + '-' + str(
        dt.minute) + '-' + str(dt.second)

    name = st.text_input('Name of data')
    name2 = name + ' ' + dtstr
    st.write('This button will save your input in a data')

    save = st.button('Save Data')
    if save:
        data = open(name2, 'w')
        data.write('A= ' + str(a) + ' B= ' + str(b) + ' C= ' + str(c))
        data.close()
