import time
import propar
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from datetime import datetime
import json

from smbus import SMBus
import time


def main():
    i2cbus = SMBus(1)  # Create a new I2C bus
    i2caddress = 0x28  # Address of device

    data = i2cbus.read_i2c_block_data(i2caddress, 0)
    factor = format(data[0], "b").zfill(8) + format(data[1], "b").zfill(8)
    factor = factor[2:16]

    factor = int(factor, 2)
    offset = 8192

    S = (14745 - offset) / 16000
    pressure = (factor - offset) / S
    pressure = round(pressure, 2)
    return pressure


if __name__ == "__main__":
    main()

el_flow = propar.instrument('/dev/ttyUSB0')

st.title('MFC-GUI')
st.write('Here you can determine the umf and calculate your desired V')

max_flow = st.number_input("Maximum VolumeFlow (L/min)", min_value=0, max_value=200, value=30)
min_flow = st.number_input("Minimum VolumeFlow (L/min)", min_value=0, max_value=50, value=5)
step = st.number_input("Steps between measurements (L/min)", min_value=5, max_value=20, value=5)
w_time = st.number_input("Waiting time to adjust (s)", min_value=3, max_value=40, value=3)
timestep = st.number_input("Timesteps between measurements", min_value=0.1, max_value=1.0, value=0.1)
repetitions_pressure_measurement = st.number_input("Repetition pressure measurements", min_value=1, max_value=20,
                                                   value=5)

max_flow_i = max_flow * 128
min_flow_i = min_flow * 128
step_i = step * 128
pressure = 0
measured_flow = 0
pressure1 = 0
measured_flow1 = 0

st.write('This button will start the umf-measurement')
placeholder = st.empty()

umf = placeholder.button('Start umf-measurement')
placeholder_diagram = st.empty()
if umf:
    placeholder.empty()

    V = [0]
    V1 = [0]
    p = [0]
    p1 = [0]

    for i in np.arange(min_flow_i, max_flow_i + step_i, step_i):
        with placeholder_diagram.container():
            el_flow.setpoint = i
            time.sleep(w_time)
            for repetition in np.arange(1, repetitions_pressure_measurement, 1):
                pressure = main() + pressure
                measured_flow = el_flow.measure / 128 + measured_flow
                time.sleep(timestep)
            measured_flow = round(measured_flow / repetitions_pressure_measurement, 2)
            pressure = round(pressure / repetitions_pressure_measurement, 2)
            st.write(measured_flow)
            V.append(measured_flow)
            p.append(pressure)
            source = pd.DataFrame({
                'x': V,
                'f(x)': p})
            aa = alt.Chart(source).mark_line().encode(
                x='x',
                y='f(x)')

            source1 = pd.DataFrame({
                'x': V1,
                'f(x)': p1})
            aa1 = alt.Chart(source1).mark_line().encode(
                x='x',
                y='f(x)').configure_line(color='red')
            chart = aa + aa1
            st.altair_chart(chart)

    for i in np.arange(max_flow_i + step_i, min_flow_i, -step_i):
        with placeholder_diagram.container():
            el_flow.setpoint = i
            time.sleep(w_time)
            for repetition in np.arange(1, repetitions_pressure_measurement, 1):
                pressure1 = main() + pressure1
                measured_flow1 = el_flow.measure / 128 + measured_flow1
                time.sleep(timestep)
            measured_flow1 = round(measured_flow1 / repetitions_pressure_measurement, 2)
            pressure1 = round(pressure1 / repetitions_pressure_measurement, 2)
            st.write(measured_flow1)
            V1.append(measured_flow1)
            p1.append(pressure1)

            source = pd.DataFrame({
                'x': V,
                'f(x)': p})
            aa = alt.Chart(source).mark_line().encode(
                x='x',
                y='f(x)')

            source1 = pd.DataFrame({
                'x': V1,
                'f(x)': p1})
            aa1 = alt.Chart(source1).mark_line().encode(
                x='x',
                y='f(x)').configure_line(color='red')
            chart = aa + aa1
            st.altair_chart(chart)


    pV = np.array(list(zip(V, p)))
    st.write(pV)

    dt = datetime.now()
    dtstr = str(dt.year) + '-' + str(dt.month) + '-' + str(dt.day) + ' ' + str(dt.hour) + '-' + str(
        dt.minute) + '-' + str(dt.second)
    name = "umf-messung " + dtstr

    np.savetxt(name, pV, fmt='%d')

st.write('Here we test, how long it takes to adjust to a new Value')
placeholder1 = st.empty()
adjust = placeholder1.button('Start Adjusting Sequence')
W = [0]
t = [0]
if adjust:

    placeholder1.empty()
    adj = np.ones([int(w_time / timestep), int(max_flow / step)])
    m = 0
    tc = 0

    for i in np.arange(step_i, max_flow_i + step_i, step_i):
        el_flow.setpoint = i
        k = 0
        for j in np.arange(0, w_time, timestep):
            time.sleep(timestep)
            adj[k, m] = el_flow.measure / 128
            W.append(el_flow.measure / 128)
            tc = tc + timestep
            t.append(tc)
            k += 1
        m += 1
        el_flow.setpoint = 0
        time.sleep(3)

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

    np.savetxt(name_adj, adj, fmt='%d')

el_flow.setpoint = 0
