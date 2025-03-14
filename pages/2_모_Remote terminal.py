import streamlit as st
import subprocess

st.title('Remote Terminal')

# Define a function to execute shell commands
def execute_shell_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout + result.stderr

# Initialize session state for terminal output
if 'terminal_output' not in st.session_state:
    st.session_state.terminal_output = ""

# CSS to style the terminal window
st.markdown("""
    <style>
    .terminal {
        background-color: #0c0c0c;
        color: #cccccc;
        font-family: monospace;
        padding: 10px;
        border: 1px solid #333;
        height: 400px;
        overflow-y: auto;
        white-space: pre-wrap;
        position: relative;
        line-height: 1.2;
    }
    .prompt {
        display: block;
        margin-top: 10px;
        width: 100%;
        background: none;
        border: none;
        color: #cccccc;
        font-family: monospace;
    }
    .prompt:focus {
        outline: none;
    }
    .output {
        white-space: pre-wrap;
        line-height: 1.2;
    }
    </style>
    """, unsafe_allow_html=True)

# HTML structure for the terminal
terminal_html = f"""
    <div class="terminal">
        <div id="output" class="output">{st.session_state.terminal_output}</div>
        <input id="prompt" class="prompt" type="text" autofocus onkeydown="if(event.key === 'Enter'){{executeCommand()}}">
    </div>
    <script>
    function executeCommand() {{
        var command = document.getElementById("prompt").value;
        var outputDiv = document.getElementById("output");
        outputDiv.innerHTML += `<div>$ {{command}}</div>`;
        document.getElementById("prompt").value = '';
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/execute", true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function() {{
            if (xhr.readyState === 4 && xhr.status === 200) {{
                var response = JSON.parse(xhr.responseText);
                outputDiv.innerHTML += `<div>${{response.result}}</div>`;
                outputDiv.scrollTop = outputDiv.scrollHeight;
            }}
        }};
        xhr.send(JSON.stringify({{command: command}}));
    }}
    </script>
"""

st.markdown(terminal_html, unsafe_allow_html=True)

# Backend logic for executing commands
def execute_command():
    import json
    from flask import request

    if request.method == 'POST':
        data = json.loads(request.data)
        command = data.get("command", "")
        result = execute_shell_command(command)
        st.session_state.terminal_output += f"$ {command}\n{result}\n"
        return {"result": result}

st.experimental_set_query_params(command=None)

if st.experimental_get_query_params().get('command'):
    command = st.experimental_get_query_params().get('command')[0]
    result = execute_shell_command(command)
    st.session_state.terminal_output += f"$ {command}\n{result}\n"
    st.experimental_set_query_params(command=None)
    st.rerun()
