# import streamlit as st
# import pandas as pd
# import sqlite3
# import json

# # Function to create Modbus tables
# def create_modbus_tables():
    # conn = sqlite3.connect('modbus_data.db')
    # cursor = conn.cursor()

    # cursor.execute('''
    # CREATE TABLE IF NOT EXISTS Modbus_Address_Data (
        # Address INTEGER PRIMARY KEY,
        # Data TEXT,
        # Definition TEXT,
        # Data_Type TEXT
    # )
    # ''')

    # cursor.execute('''
    # CREATE TABLE IF NOT EXISTS Modbus_Sequential_Data (
        # ID INTEGER PRIMARY KEY AUTOINCREMENT,
        # Address_0 TEXT,
        # Address_1 TEXT,
        # Address_2 TEXT,
        # Address_3 TEXT,
        # Address_4 TEXT,
        # Address_5 TEXT,
        # Address_6 TEXT,
        # Address_7 TEXT,
        # Address_8 TEXT,
        # Address_9 TEXT
    # )
    # ''')

    # conn.commit()
    # conn.close()

# # Function to apply custom style to DataFrame
# def apply_custom_style(df):
    # styled_df = df.style.set_properties(**{str(i): 'width: 100px' for i in range(10)})
    # return styled_df

# # Function to load Modbus address descriptions from JSON
# def load_modbus_descriptions():
    # with open('modbus_addr_def.json', 'r', encoding='utf-8') as f:
        # descriptions_list = json.load(f)
    # descriptions_dict = {}
    # for item in descriptions_list:
        # address = item.get("Modbus Address")
        # if address is not None:
            # descriptions_dict[address] = item
    # return descriptions_dict

# # Function to get definition from data
# def get_definition(value, unit, states):
    # if unit == "0.1dBm":
        # return f"{value * 0.1} dBm"
    # elif unit == "0-2" and states:
        # return states.get(str(value), "Unknown")
    # elif unit == "次":
        # return f"{value}次"
    # else:
        # return str(value)

# # Initialize session state variables
# if 'start_address' not in st.session_state:
    # st.session_state.start_address = 0
# if 'end_address' not in st.session_state:
    # st.session_state.end_address = 0
# if 'device_id' not in st.session_state:
    # st.session_state.device_id = 0
# if 'df_address_data' not in st.session_state:
    # st.session_state.df_address_data = None
# if 'df_sequential_data' not in st.session_state:
    # st.session_state.df_sequential_data = None
# if 'modbus_descriptions' not in st.session_state:
    # st.session_state.modbus_descriptions = load_modbus_descriptions()

# start_address = st.sidebar.number_input("Enter starting address", min_value=0, max_value=65535, step=1, value=st.session_state.start_address)
# end_address = st.sidebar.number_input("Enter ending address", min_value=0, max_value=65535, step=1, value=st.session_state.end_address)
# device_id = st.sidebar.number_input("Enter Device ID", min_value=0, max_value=255, step=1, value=st.session_state.device_id)

# st.session_state.start_address = start_address
# st.session_state.end_address = end_address
# st.session_state.device_id = device_id

# if st.sidebar.button("Start Reading"):
    # if start_address > end_address:
        # st.sidebar.error("Starting address should be less than or equal to ending address.")
    # else:
        # if st.session_state.client is not None and st.session_state.client.is_socket_open():
            # address_data = []
            # for addr in range(start_address, end_address + 1):
                # rr = st.session_state.client.read_holding_registers(addr, 1, slave=device_id)
                # if rr.isError():
                    # address_data.append((addr, "Error", "", "N/A", "N/A"))
                # else:
                    # hex_value = f"{rr.registers[0]:04X}"
                    # hex_value_formatted = f"{hex_value[:2]} {hex_value[2:]}"
                    # description = st.session_state.modbus_descriptions.get(addr, {}).get("Description", "N/A")
                    # data_type = st.session_state.modbus_descriptions.get(addr, {}).get("Data Type", "N/A")
                    # unit = st.session_state.modbus_descriptions.get(addr, {}).get("Unit", "")
                    # states = st.session_state.modbus_descriptions.get(addr, {}).get("States", {})

                    # if data_type == "INT16":
                        # data_value = str(int(hex_value, 16))
                    # elif data_type == "UINT16":
                        # data_value = str(int(hex_value, 16) if int(hex_value, 16) < 2**15 else int(hex_value, 16) - 2**16)
                    # else:
                        # data_value = "N/A"

                    # definition = get_definition(data_value, unit, states)
                    # address_data.append((addr, description, hex_value_formatted, data_value, definition))

            # df_address_data = pd.DataFrame(address_data, columns=['Modbus Address', 'Description', 'Raw Data', 'Data', 'Definition'])
            # df_address_data_styled = apply_custom_style(df_address_data)

            # sequential_data = []
            # for i in range((start_address // 10) * 10, end_address + 1, 10):
                # row = [f"{i}"]
                # for j in range(10):
                    # addr = i + j
                    # if addr < start_address or addr > end_address:
                        # row.append("     ")
                    # else:
                        # rr = st.session_state.client.read_holding_registers(addr, 1, slave=device_id)
                        # if rr.isError():
                            # row.append("Error")
                        # else:
                            # hex_value = f"{rr.registers[0]:04X}"
                            # hex_value_formatted = f"{hex_value[:2]} {hex_value[2:]}"
                            # row.append(hex_value_formatted)
                # sequential_data.append(row)

            # df_sequential_data = pd.DataFrame(sequential_data, columns=['Modbus Address', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
            # df_sequential_data.set_index('Modbus Address', inplace=True)

            # df_sequential_data_styled = apply_custom_style(df_sequential_data)

            # st.session_state.df_address_data = df_address_data_styled
            # st.session_state.df_sequential_data = df_sequential_data_styled

        # else:
            # st.error("Port is not open. Please open the port first.")

# if st.session_state.df_sequential_data is not None:
    # st.write("Modbus Sequential Data")
    # st.dataframe(st.session_state.df_sequential_data)

# if st.session_state.df_address_data is not None:
    # st.write("Modbus Address Data")
    # st.dataframe(st.session_state.df_address_data)

# create_modbus_tables()


# import streamlit as st
# import pandas as pd
# import sqlite3
# import json
# import logging

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)

# # Function to create Modbus tables
# def create_modbus_tables():
    # conn = sqlite3.connect('modbus_data.db')
    # cursor = conn.cursor()

    # cursor.execute('''
    # CREATE TABLE IF NOT EXISTS Modbus_Address_Data (
        # Address INTEGER PRIMARY KEY,
        # Data TEXT,
        # Definition TEXT,
        # Data_Type TEXT
    # )
    # ''')

    # cursor.execute('''
    # CREATE TABLE IF NOT EXISTS Modbus_Sequential_Data (
        # ID INTEGER PRIMARY KEY AUTOINCREMENT,
        # Address_0 TEXT,
        # Address_1 TEXT,
        # Address_2 TEXT,
        # Address_3 TEXT,
        # Address_4 TEXT,
        # Address_5 TEXT,
        # Address_6 TEXT,
        # Address_7 TEXT,
        # Address_8 TEXT,
        # Address_9 TEXT
    # )
    # ''')

    # conn.commit()
    # conn.close()

# # Function to apply custom style to DataFrame
# def apply_custom_style(df):
    # styled_df = df.style.set_properties(**{str(i): 'width: 100px' for i in range(10)})
    # return styled_df

# # Function to load Modbus address descriptions from JSON
# def load_modbus_descriptions():
    # with open('modbus_addr_def.json', 'r', encoding='utf-8') as f:
        # descriptions_list = json.load(f)
    # descriptions_dict = {}
    # for item in descriptions_list:
        # address = item.get("Modbus Address")
        # if address is not None:
            # descriptions_dict[address] = item
    # return descriptions_dict

# def get_definition(value, unit, states):
    # unit = unit.strip("*")  # Remove leading asterisk
    # try:
        # value = float(value)
    # except ValueError:
        # return "N/A"

    # if unit == "0.1dBm":
        # value = value / 10  # Correctly divide the value by 10
        # value_str = f"{value:.1f} dBm"  # Format the value with one decimal place
        # return value_str
    # elif unit == "0-2" and states:
        # return states.get(str(int(value)), "Unknown")
    # elif unit == "0-7" and states:
        # return states.get(str(int(value)), "Unknown")
    # elif unit == "次":
        # return f"{int(value)} 次"
    # elif unit == "dBuV":
        # return f"{int(value)} dBuV"
    # else:
        # return str(value)

# # Initialize session state variables
# if 'start_address' not in st.session_state:
    # st.session_state.start_address = 0
# if 'end_address' not in st.session_state:
    # st.session_state.end_address = 0
# if 'device_id' not in st.session_state:
    # st.session_state.device_id = 0
# if 'df_address_data' not in st.session_state:
    # st.session_state.df_address_data = None
# if 'df_sequential_data' not in st.session_state:
    # st.session_state.df_sequential_data = None
# if 'modbus_descriptions' not in st.session_state:
    # st.session_state.modbus_descriptions = load_modbus_descriptions()

# start_address = st.sidebar.number_input("Enter starting address", min_value=0, max_value=65535, step=1, value=st.session_state.start_address)
# end_address = st.sidebar.number_input("Enter ending address", min_value=0, max_value=65535, step=1, value=st.session_state.end_address)
# device_id = st.sidebar.number_input("Enter Device ID", min_value=0, max_value=255, step=1, value=st.session_state.device_id)

# st.session_state.start_address = start_address
# st.session_state.end_address = end_address
# st.session_state.device_id = device_id

# if st.sidebar.button("Start Reading"):
    # if start_address > end_address:
        # st.sidebar.error("Starting address should be less than or equal to ending address.")
    # else:
        # if st.session_state.client is not None and st.session_state.client.is_socket_open():
            # address_data = []
            # for addr in range(start_address, end_address + 1):
                # rr = st.session_state.client.read_holding_registers(addr, 1, slave=device_id)
                # if rr.isError():
                    # address_data.append((addr, "Error", "", "N/A", "N/A"))
                # else:
                    # hex_value = f"{rr.registers[0]:04X}"
                    # hex_value_formatted = f"{hex_value[:2]} {hex_value[2:]}"
                    # description = st.session_state.modbus_descriptions.get(addr, {}).get("Description", "N/A")
                    # data_type = st.session_state.modbus_descriptions.get(addr, {}).get("Data Type", "N/A")
                    # unit = st.session_state.modbus_descriptions.get(addr, {}).get("Unit", "")
                    # states = st.session_state.modbus_descriptions.get(addr, {}).get("States", {})

                    # if data_type == "INT16":
                        # data_value = str(int(hex_value, 16))
                    # elif data_type == "UINT16":
                        # data_value = str(int(hex_value, 16) if int(hex_value, 16) < 2**15 else int(hex_value, 16) - 2**16)
                    # else:
                        # data_value = "N/A"

                    # definition = get_definition(data_value, unit, states)
                    # address_data.append((addr, description, hex_value_formatted, data_value, definition))

            # df_address_data = pd.DataFrame(address_data, columns=['Modbus Address', 'Description', 'Raw Data', 'Data', 'Definition'])
            # df_address_data_styled = apply_custom_style(df_address_data)

            # sequential_data = []
            # for i in range((start_address // 10) * 10, end_address + 1, 10):
                # row = [f"{i}"]
                # for j in range(10):
                    # addr = i + j
                    # if addr < start_address or addr > end_address:
                        # row.append("     ")
                    # else:
                        # rr = st.session_state.client.read_holding_registers(addr, 1, slave=device_id)
                        # if rr.isError():
                            # row.append("Error")
                        # else:
                            # hex_value = f"{rr.registers[0]:04X}"
                            # hex_value_formatted = f"{hex_value[:2]} {hex_value[2:]}"
                            # row.append(hex_value_formatted)
                # sequential_data.append(row)

            # df_sequential_data = pd.DataFrame(sequential_data, columns=['Modbus Address', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
            # df_sequential_data.set_index('Modbus Address', inplace=True)

            # df_sequential_data_styled = apply_custom_style(df_sequential_data)

            # st.session_state.df_address_data = df_address_data_styled
            # st.session_state.df_sequential_data = df_sequential_data_styled

        # else:
            # st.error("Port is not open. Please open the port first.")

# if st.session_state.df_sequential_data is not None:
    # st.write("Modbus Sequential Data")
    # st.dataframe(st.session_state.df_sequential_data)

# if st.session_state.df_address_data is not None:
    # st.write("Modbus Address Data")
    # st.dataframe(st.session_state.df_address_data)

# create_modbus_tables()








import streamlit as st
import pandas as pd
import sqlite3
import json
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Function to create Modbus tables
def create_modbus_tables():
    conn = sqlite3.connect('modbus_data.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Modbus_Address_Data (
        Address INTEGER PRIMARY KEY,
        Data TEXT,
        Definition TEXT,
        Data_Type TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Modbus_Sequential_Data (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Address_0 TEXT,
        Address_1 TEXT,
        Address_2 TEXT,
        Address_3 TEXT,
        Address_4 TEXT,
        Address_5 TEXT,
        Address_6 TEXT,
        Address_7 TEXT,
        Address_8 TEXT,
        Address_9 TEXT
    )
    ''')

    conn.commit()
    conn.close()

# Function to apply custom style to DataFrame
def apply_custom_style(df):
    styled_df = df.style.set_properties(**{str(i): 'width: 100px' for i in range(10)})
    return styled_df

# Function to load Modbus address descriptions from JSON
def load_modbus_descriptions():
    with open('modbus_addr_def.json', 'r', encoding='utf-8') as f:
        descriptions_list = json.load(f)
    descriptions_dict = {}
    for item in descriptions_list:
        address = item.get("Modbus Address")
        if address is not None:
            descriptions_dict[address] = item
    return descriptions_dict

def get_definition(value, unit, states):
    unit = unit.strip("*")  # Remove leading asterisk
    try:
        value = float(value)
    except ValueError:
        return "N/A"

    if unit == "0.1dBm":
        value = value / 10  # Correctly divide the value by 10
        value_str = f"{value:.1f} dBm"  # Format the value with one decimal place
        return value_str
    elif unit == "0-2" and states:
        return states.get(str(int(value)), "Unknown")
    elif unit == "0-7" and states:
        return states.get(str(int(value)), "Unknown")
    elif unit == "次":
        return f"{int(value)} 次"
    elif unit == "dBuV":
        return f"{int(value)} dBuV"
    else:
        return str(value)

# Initialize session state variables
if 'start_address' not in st.session_state:
    st.session_state.start_address = 0
if 'end_address' not in st.session_state:
    st.session_state.end_address = 0
if 'device_id' not in st.session_state:
    st.session_state.device_id = 0
if 'df_address_data' not in st.session_state:
    st.session_state.df_address_data = None
if 'df_sequential_data' not in st.session_state:
    st.session_state.df_sequential_data = None
if 'modbus_descriptions' not in st.session_state:
    st.session_state.modbus_descriptions = load_modbus_descriptions()

start_address = st.sidebar.number_input("Enter starting address", min_value=0, max_value=65535, step=1, value=st.session_state.start_address)
end_address = st.sidebar.number_input("Enter ending address", min_value=0, max_value=65535, step=1, value=st.session_state.end_address)
device_id = st.sidebar.number_input("Enter Device ID", min_value=0, max_value=255, step=1, value=st.session_state.device_id)

st.session_state.start_address = start_address
st.session_state.end_address = end_address
st.session_state.device_id = device_id

if st.sidebar.button("Start Reading"):
    if start_address > end_address:
        st.sidebar.error("Starting address should be less than or equal to ending address.")
    else:
        if st.session_state.client is not None and st.session_state.client.is_socket_open():
            address_data = []
            for addr in range(start_address, end_address + 1):
                rr = st.session_state.client.read_holding_registers(addr, count=1, slave=device_id)
                if rr.isError():
                    address_data.append((addr, "Error", "", "N/A", "N/A"))
                else:
                    hex_value = f"{rr.registers[0]:04X}"
                    hex_value_formatted = f"{hex_value[:2]} {hex_value[2:]}"
                    description = st.session_state.modbus_descriptions.get(addr, {}).get("Description", "N/A")
                    data_type = st.session_state.modbus_descriptions.get(addr, {}).get("Data Type", "N/A")
                    unit = st.session_state.modbus_descriptions.get(addr, {}).get("Unit", "")
                    states = st.session_state.modbus_descriptions.get(addr, {}).get("States", {})

                    if data_type == "INT16":
                        data_value = str(int(hex_value, 16))
                    elif data_type == "UINT16":
                        data_value = str(int(hex_value, 16) if int(hex_value, 16) < 2**15 else int(hex_value, 16) - 2**16)
                    else:
                        data_value = "N/A"

                    definition = get_definition(data_value, unit, states)
                    address_data.append((addr, description, hex_value_formatted, data_value, definition))

            df_address_data = pd.DataFrame(address_data, columns=['Modbus Address', 'Description', 'Raw Data', 'Data', 'Definition'])
            df_address_data_styled = apply_custom_style(df_address_data)

            sequential_data = []
            for i in range((start_address // 10) * 10, end_address + 1, 10):
                row = [f"{i}"]
                for j in range(10):
                    addr = i + j
                    if addr < start_address or addr > end_address:
                        row.append("     ")
                    else:
                        rr = st.session_state.client.read_holding_registers(addr, count=1, slave=device_id)
                        if rr.isError():
                            row.append("Error")
                        else:
                            hex_value = f"{rr.registers[0]:04X}"
                            hex_value_formatted = f"{hex_value[:2]} {hex_value[2:]}"
                            row.append(hex_value_formatted)
                sequential_data.append(row)

            df_sequential_data = pd.DataFrame(sequential_data, columns=['Modbus Address', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
            df_sequential_data.set_index('Modbus Address', inplace=True)

            df_sequential_data_styled = apply_custom_style(df_sequential_data)

            st.session_state.df_address_data = df_address_data_styled
            st.session_state.df_sequential_data = df_sequential_data_styled

        else:
            st.error("Port is not open. Please open the port first.")

if st.session_state.df_sequential_data is not None:
    st.write("Modbus Sequential Data")
    st.dataframe(st.session_state.df_sequential_data)

if st.session_state.df_address_data is not None:
    st.write("Modbus Address Data")
    st.dataframe(st.session_state.df_address_data)

create_modbus_tables()
