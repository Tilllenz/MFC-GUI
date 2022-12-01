import time
import propar
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from datetime import datetime
import json

el_flow = propar.instrument('/dev/ttyUSB0')

st.title('MFC-GUI')
st.write('Here you can determine the umf and calculate your desired V')

max_flow = st.number_input("Maximum VolumeFlow (L/min)", min_value=0, max_value=100, value=0)
step = st.number_input("Steps between measurements (L/min)", min_value=5, max_value=20, value=5)

st.write('This button will start the umf-measurement')
placeholder=st.empty()



umf = placeholder.button('Start umf-measurement')
if umf:
    placeholder.empty()

   
    max_flow_i = max_flow*128
    step_i = step*128

    V = [0]
    p = [0]
    a = 0
    s = 10
    
    for i in range(0, max_flow_i, step_i):
        el_flow.setpoint = i
        time.sleep(s)
        st.write(el_flow.measure)
        V.append(el_flow.measure/128)
        p.append(el_flow.measure/4/128)


    source = pd.DataFrame({
        'x': V,
        'f(x)': p})
    aa = alt.Chart(source).mark_line().encode(
        x='x',
        y='f(x)')
    pV = np.array(list(zip(V, p)))
    st.altair_chart(aa)
    st.write(pV)

    dt = datetime.now()
    dtstr = str(dt.year) + '-' + str(dt.month) + '-' + str(dt.day) + ' ' + str(dt.hour) + '-' + str(
            dt.minute) + '-' + str(dt.second)
    name = "umf-messung " + dtstr
    
    
    np.savetxt(name,pV, fmt='%d')
    
    
    
    #data = open(name, 'w')
    #data.write("Maximum VolumeFlow (L/min): ")
    #data.write(str(max_flow))
    #data.write("Steps between measurements (L/min): ")
    #data.write(str(step))
    #data.write("Waiting time between steps (s): ")
    #data.write(str(s))
    #data.write(pV)
    #data.close()

el_flow.setpoint = 0





