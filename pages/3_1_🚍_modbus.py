import streamlit as st
from pymodbus.client import ModbusSerialClient as ModbusClient
import serial.tools.list_ports

def get_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

st.title("Modbus Communication")

com_port = st.selectbox("Select COM Port", get_ports())
baud_rate = st.selectbox("Select Baud Rate", ["9600", "19200", "38400", "57600", "115200"])
device_id = st.number_input("Device ID", min_value=1, max_value=255, value=1)
address = st.number_input("Address", min_value=0, value=0)
value = st.text_input("Value")

if st.button("Send Data"):
    try:
        client = ModbusClient(method='rtu', port=com_port, baudrate=int(baud_rate), timeout=1)
        client.connect()
        client.write_register(address, int(value), unit=device_id)
        client.close()
        st.success("Data sent successfully!")
    except Exception as e:
        st.error(f"Error: {e}")

if st.button("Read Data"):
    try:
        client = ModbusClient(method='rtu', port=com_port, baudrate=int(baud_rate), timeout=1)
        client.connect()
        response = client.read_holding_registers(address, 1, unit=device_id)
        client.close()

        if response.isError():
            st.error("Error reading data")
        else:
            st.success(f"Read value: {response.registers[0]}")
    except Exception as e:
        st.error(f"Error: {e}")
