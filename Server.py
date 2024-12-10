import socket
import threading
from flask import Flask, render_template_string, request

# Flask App for Server
app = Flask(__name__)

# Global variables for storing client data
client_data = {
    "Client A": {"CPU": 0, "Memory": 0, "GPU": 0, "Temperature": 0},
    "Client B": {"CPU": 0, "Memory": 0, "GPU": 0, "Temperature": 0}
}
thresholds = {
    "Client A": {"CPU": 100, "Memory": 100, "GPU": 100, "Temperature": 100},
    "Client B": {"CPU": 100, "Memory": 100, "GPU": 100, "Temperature": 100}
}

# Server HTML Template
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Resource Monitor</title>
    <meta http-equiv="refresh" content="5"> <!-- Refresh the page every 5 seconds -->
</head>
<body>
    <h1>Resource Monitor</h1>
    <table border="1">
        <tr>
            <th>Client</th>
            <th>CPU Utilization</th>
            <th>Memory Utilization</th>
            <th>GPU Utilization</th>
            <th>Temperature</th>
        </tr>
        {% for client, data in client_data.items() %}
        <tr>
            <td>{{ client }}</td>
            <td style="color: {{ 'red' if data.get('CPU', 0) > thresholds.get(client, {}).get('CPU', 100) else 'black' }};">{{ data.get('CPU', 0) }}%</td>
            <td style="color: {{ 'red' if data.get('Memory', 0) > thresholds.get(client, {}).get('Memory', 100) else 'black' }};">{{ data.get('Memory', 0) }}%</td>
            <td style="color: {{ 'red' if data.get('GPU', 0) > thresholds.get(client, {}).get('GPU', 100) else 'black' }};">{{ data.get('GPU', 0) }}%</td>
            <td style="color: {{ 'red' if data.get('Temperature', 0) > thresholds.get(client, {}).get('Temperature', 100) else 'black' }};">{{ data.get('Temperature', 0) }}°C</td>
        </tr>
        {% endfor %}
    </table>
    <h2>Set Thresholds</h2>
    <form method="POST">
        <label for="client">Client:</label>
        <select name="client">
            <option value="Client A">Client A</option>
            <option value="Client B">Client B</option>
        </select><br>
        <label for="cpu">CPU Threshold (%):</label>
        <input type="number" name="cpu"><br>
        <label for="memory">Memory Threshold (%):</label>
        <input type="number" name="memory"><br>
        <label for="gpu">GPU Threshold (%):</label>
        <input type="number" name="gpu"><br>
        <label for="temperature">Temperature Threshold (°C):</label>
        <input type="number" name="temperature"><br>
        <button type="submit">Set Threshold</button>
    </form>
</body>
</html>
"""


@app.route('/', methods=['GET', 'POST'])
def monitor():
    global thresholds
    if request.method == 'POST':
        client = request.form['client']
        thresholds[client] = {
            "CPU": int(request.form.get('cpu', 100)),
            "Memory": int(request.form.get('memory', 100)),
            "GPU": int(request.form.get('gpu', 100)),
            "Temperature": int(request.form.get('temperature', 100))
        }
    return render_template_string(html_template, client_data=client_data, thresholds=thresholds)

def server_thread(client_name, conn):
    while True:
        try:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            client_data[client_name] = eval(data)  # Convert string back to dictionary
        except:
            break
    conn.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8080))
    server_socket.listen(2)
    print("Server listening...")

    while True:
        conn, addr = server_socket.accept()
        client_name = "Client A" if addr[0].endswith(".1") else "Client B"
        threading.Thread(target=server_thread, args=(client_name, conn)).start()

if __name__ == '__main__':
    threading.Thread(target=start_server).start()
    app.run(host='0.0.0.0', port=5000)
