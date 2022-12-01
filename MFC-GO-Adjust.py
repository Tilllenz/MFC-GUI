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
w_time = st.number_input("Waiting time to adjust (s)", min_value=3, max_value=40, value=3 )
timestep= st.number_input("Timesteps between measurements", min_value=0.1, max_value=1, value=0.1)

st.write('This button will start the umf-measurement')
placeholder=st.empty()



umf = placeholder.button('Start umf-measurement')
if umf:
    placeholder.empty()

   
    max_flow_i = max_flow*128
    step_i = step*128

    V = [0]
    p = [0]
    
    for i in range(step_i, max_flow_i+step_i, step_i):
        el_flow.setpoint = i
        time.sleep(w_time)
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



st.write('Here we test, how long it takes to adjust to a new Value')
adjust = placeholder.button('Start Adjusting Sequence')
W = [0]
t = np.arange(0,int(w_time),int(timestep))
if adjust:
    placeholder.empty()
    adj= np.ones([int(w_time/timestep), int(max_flow/step)])
    m=0

    for i in range(step_i, max_flow_i+step_i, step_i):
        el_flow.setpoint = i
        k=0
        for j in range(0,w_time,timestep)
            time.sleep(timestep)
            adj[k,m] = el_flow.measure
            W.append(el_flow.measure)
            k+=1
        m+=1

    st.write(adj)
    source = pd.DataFrame({
        'x': t,
        'f(x)': W})
    bb = alt.Chart(source).mark_line().encode(
        x='x',
        y='f(x)')
    st.altair_chart(bb)


    dt = datetime.now()
    dtstr = str(dt.year) + '-' + str(dt.month) + '-' + str(dt.day) + ' ' + str(dt.hour) + '-' + str(
        dt.minute) + '-' + str(dt.second)
    name_adj = "AdjustingMFC " + dtstr

    np.savetxt(name_adj, pV, fmt='%d')
    

el_flow.setpoint = 0





