# import streamlit as st
# from pymodbus.client import ModbusSerialClient
# import serial.tools.list_ports
# import serial

# def get_com_ports():
    # ports = serial.tools.list_ports.comports()
    # port_info = []
    # for port in ports:
        # try:
            # with serial.Serial(port.device) as s:
                # port_info.append((port.device, port.description, port.hwid, False))
        # except (OSError, serial.SerialException):
            # port_info.append((port.device, port.description, port.hwid, True))
    # return port_info

# def get_baud_rates():
    # return [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200]

# # Initialize session state variables
# if 'com_port' not in st.session_state:
    # st.session_state.com_port = ''
# if 'baud_rate' not in st.session_state:
    # st.session_state.baud_rate = 9600
# if 'client' not in st.session_state:
    # st.session_state.client = None
# if 'com_ports' not in st.session_state:
    # st.session_state.com_ports = get_com_ports()

# # Configuration for the COM port and Modbus client
# def update_com_ports():
    # st.session_state.com_ports = get_com_ports()

# # Function to handle port opening
# def open_port():
    # client = ModbusSerialClient(
        # method='rtu',
        # port=st.session_state.com_port,
        # baudrate=st.session_state.baud_rate,
        # parity='N',
        # stopbits=1,
        # bytesize=8,
        # timeout=1
    # )
    # connection = client.connect()
    # if connection:
        # st.session_state.client = client
        # st.session_state.success_message = f"Port {st.session_state.com_port} opened successfully at {st.session_state.baud_rate} baud."
        # st.session_state.error_message = ''
    # else:
        # st.session_state.error_message = f"Failed to open port {st.session_state.com_port}."
        # st.session_state.success_message = ''
    # update_com_ports()

# # Function to handle port closing
# def close_port():
    # if st.session_state.client is not None:
        # st.session_state.client.close()
        # st.session_state.client = None
        # st.session_state.success_message = f"Port {st.session_state.com_port} closed successfully."
        # st.session_state.warning_message = ''
    # else:
        # st.session_state.warning_message = "Port is not open."
        # st.session_state.success_message = ''
    # update_com_ports()

# # Update COM ports list
# update_com_ports()
# baud_rates = get_baud_rates()

# selected_com_port = st.selectbox(
    # "Select COM Port", [f"{port[0]} - {port[1]}" for port in st.session_state.com_ports],
    # index=[port[0] for port in st.session_state.com_ports].index(st.session_state.com_port) if st.session_state.com_port in [port[0] for port in st.session_state.com_ports] else 0
# )
# selected_baud_rate = st.selectbox(
    # "Select Baud Rate", baud_rates,
    # index=baud_rates.index(st.session_state.baud_rate) if st.session_state.baud_rate in baud_rates else 3
# )

# st.session_state.com_port = selected_com_port.split(' - ')[0]
# st.session_state.baud_rate = selected_baud_rate

# col1, col2 = st.columns(2)
# with col1:
    # if st.button("Open Port"):
        # open_port()
# with col2:
    # if st.button("Close Port"):
        # close_port()

# # Display available COM ports and their details
# st.write("##### COM Ports")

# titles = ["Device", "Description", "HWID", "Occupied"]
# output = f"{titles[0].ljust(7)} {titles[1].ljust(27)} {titles[2].ljust(36)} {titles[3].ljust(0)}\n"
# for port in st.session_state.com_ports:
    # device = port[0].ljust(7)
    # description = port[1].ljust(27)
    # hwid = port[2].ljust(36)
    # occupied = "Y" if port[3] else "N"
    # output += f"{device} {description} {hwid} {occupied.ljust(0)}\n"

# # Display output as markdown
# st.markdown(f"```\n{output}\n```")

# # Display messages
# if 'success_message' in st.session_state and st.session_state.success_message:
    # st.success(st.session_state.success_message)
# if 'error_message' in st.session_state and st.session_state.error_message:
    # st.error(st.session_state.error_message)
# if 'warning_message' in st.session_state and st.session_state.warning_message:
    # st.warning(st.session_state.warning_message)


# import streamlit as st
# from pymodbus.client import ModbusSerialClient
# import serial.tools.list_ports
# import serial

# def get_com_ports():
    # ports = serial.tools.list_ports.comports()
    # port_info = []
    # for port in ports:
        # try:
            # with serial.Serial(port.device) as s:
                # port_info.append((port.device, port.description, port.hwid, False))
        # except (OSError, serial.SerialException):
            # port_info.append((port.device, port.description, port.hwid, True))
    # return port_info

# def get_baud_rates():
    # return [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200]

# # Initialize session state variables
# if 'com_port' not in st.session_state:
    # st.session_state.com_port = ''
# if 'baud_rate' not in st.session_state:
    # st.session_state.baud_rate = 9600
# if 'client' not in st.session_state:
    # st.session_state.client = None
# if 'com_ports' not in st.session_state:
    # st.session_state.com_ports = get_com_ports()
# if 'message' not in st.session_state:
    # st.session_state.message = ''

# # Configuration for the COM port and Modbus client
# def update_com_ports():
    # st.session_state.com_ports = get_com_ports()

# # Function to handle port opening
# def open_port():
    # client = ModbusSerialClient(
        # method='rtu',
        # port=st.session_state.com_port,
        # baudrate=st.session_state.baud_rate,
        # parity='N',
        # stopbits=1,
        # bytesize=8,
        # timeout=1
    # )
    # connection = client.connect()
    # if connection:
        # st.session_state.client = client
        # st.session_state.message = f"Success: Port {st.session_state.com_port} opened successfully at {st.session_state.baud_rate} baud."
    # else:
        # st.session_state.message = f"Error: Failed to open port {st.session_state.com_port}."
    # update_com_ports()

# # Function to handle port closing
# def close_port():
    # if st.session_state.client is not None:
        # st.session_state.client.close()
        # st.session_state.client = None
        # st.session_state.message = f"Success: Port {st.session_state.com_port} closed successfully."
    # else:
        # st.session_state.message = "Warning: Port is not open."
    # update_com_ports()

# # Update COM ports list
# update_com_ports()
# baud_rates = get_baud_rates()

# selected_com_port = st.selectbox(
    # "Select COM Port", [f"{port[0]} - {port[1]}" for port in st.session_state.com_ports],
    # index=[port[0] for port in st.session_state.com_ports].index(st.session_state.com_port) if st.session_state.com_port in [port[0] for port in st.session_state.com_ports] else 0
# )
# selected_baud_rate = st.selectbox(
    # "Select Baud Rate", baud_rates,
    # index=baud_rates.index(st.session_state.baud_rate) if st.session_state.baud_rate in baud_rates else 3
# )

# st.session_state.com_port = selected_com_port.split(' - ')[0]
# st.session_state.baud_rate = selected_baud_rate

# col1, col2 = st.columns(2)
# with col1:
    # if st.button("Open Port"):
        # open_port()
# with col2:
    # if st.button("Close Port"):
        # close_port()

# # Display available COM ports and their details
# st.write("##### COM Ports")

# titles = ["Device", "Description", "HWID", "Occupied"]
# output = f"{titles[0].ljust(7)} {titles[1].ljust(27)} {titles[2].ljust(36)} {titles[3].ljust(0)}\n"
# for port in st.session_state.com_ports:
    # device = port[0].ljust(7)
    # description = port[1].ljust(27)
    # hwid = port[2].ljust(36)
    # occupied = "Y" if port[3] else "N"
    # output += f"{device} {description} {hwid} {occupied.ljust(0)}\n"

# # Display output as markdown
# st.markdown(f"```\n{output}\n```")

# # Display message in a single placeholder area
# message_placeholder = st.empty()
# if st.session_state.message.startswith("Success"):
    # message_placeholder.success(st.session_state.message)
# elif st.session_state.message.startswith("Error"):
    # message_placeholder.error(st.session_state.message)
# elif st.session_state.message.startswith("Warning"):
    # message_placeholder.warning(st.session_state.message)








import streamlit as st
from pymodbus.client import ModbusSerialClient
import serial.tools.list_ports
import serial

def get_com_ports():
    ports = serial.tools.list_ports.comports()
    port_info = []
    for port in ports:
        try:
            with serial.Serial(port.device) as s:
                port_info.append((port.device, port.description, port.hwid, False))
        except (OSError, serial.SerialException):
            port_info.append((port.device, port.description, port.hwid, True))
    return port_info

def get_baud_rates():
    return [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200]

# Initialize session state variables
if 'com_port' not in st.session_state:
    st.session_state.com_port = ''
if 'baud_rate' not in st.session_state:
    st.session_state.baud_rate = 9600
if 'client' not in st.session_state:
    st.session_state.client = None
if 'com_ports' not in st.session_state:
    st.session_state.com_ports = get_com_ports()
if 'message' not in st.session_state:
    st.session_state.message = ''

# Configuration for the COM port and Modbus client
def update_com_ports():
    st.session_state.com_ports = get_com_ports()

# Function to handle port opening
def open_port():
    client = ModbusSerialClient(
        port=st.session_state.com_port,
        baudrate=st.session_state.baud_rate,
        parity='N',
        stopbits=1,
        bytesize=8,
        timeout=1
    )
    connection = client.connect()
    if connection:
        st.session_state.client = client
        st.session_state.message = f"Success: Port {st.session_state.com_port} opened successfully at {st.session_state.baud_rate} baud."
    else:
        st.session_state.message = f"Error: Failed to open port {st.session_state.com_port}."
    update_com_ports()

# Function to handle port closing
def close_port():
    if st.session_state.client is not None:
        st.session_state.client.close()
        st.session_state.client = None
        st.session_state.message = f"Success: Port {st.session_state.com_port} closed successfully."
    else:
        st.session_state.message = "Warning: Port is not open."
    update_com_ports()

# Update COM ports list
update_com_ports()
baud_rates = get_baud_rates()

selected_com_port = st.selectbox(
    "Select COM Port", [f"{port[0]} - {port[1]}" for port in st.session_state.com_ports],
    index=[port[0] for port in st.session_state.com_ports].index(st.session_state.com_port) if st.session_state.com_port in [port[0] for port in st.session_state.com_ports] else 0
)
selected_baud_rate = st.selectbox(
    "Select Baud Rate", baud_rates,
    index=baud_rates.index(st.session_state.baud_rate) if st.session_state.baud_rate in baud_rates else 3
)

st.session_state.com_port = selected_com_port.split(' - ')[0]
st.session_state.baud_rate = selected_baud_rate

col1, col2 = st.columns(2)
with col1:
    if st.button("Open Port"):
        open_port()
with col2:
    if st.button("Close Port"):
        close_port()

# Display available COM ports and their details
st.write("##### COM Ports")

titles = ["Device", "Description", "HWID", "Occupied"]
output = f"{titles[0].ljust(7)} {titles[1].ljust(27)} {titles[2].ljust(36)} {titles[3].ljust(0)}\n"
for port in st.session_state.com_ports:
    device = port[0].ljust(7)
    description = port[1].ljust(27)
    hwid = port[2].ljust(36)
    occupied = "Y" if port[3] else "N"
    output += f"{device} {description} {hwid} {occupied.ljust(0)}\n"

# Display output as markdown
st.markdown(f"```\n{output}\n```")

# Display message in a single placeholder area
message_placeholder = st.empty()
if st.session_state.message.startswith("Success"):
    message_placeholder.success(st.session_state.message)
elif st.session_state.message.startswith("Error"):
    message_placeholder.error(st.session_state.message)
elif st.session_state.message.startswith("Warning"):
    message_placeholder.warning(st.session_state.message)












