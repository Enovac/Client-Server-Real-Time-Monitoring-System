import socket
import psutil
import time
import random

# Function to simulate GPU utilization and temperature (replace with actual GPU metrics if available)
def get_gpu_utilization():
    return random.uniform(0, 100)  # Simulating GPU utilization as a percentage

def get_temperature():
    return random.uniform(30, 90)  # Simulating temperature in degrees Celsius

# Function to gather system metrics
def gather_metrics():
    cpu_utilization = psutil.cpu_percent(interval=1)  # Measure CPU utilization
    memory = psutil.virtual_memory().percent  # Measure memory utilization
    gpu_utilization = get_gpu_utilization()  # Simulated GPU utilization
    temperature = get_temperature()  # Simulated temperature

    # Create a data dictionary
    metrics = {
        "cpu": cpu_utilization,
        "memory": memory,
        "gpu": gpu_utilization,
        "temperature": temperature
    }
    return metrics

# Create a socket object (client side)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Server details
server_address = ('localhost', 8000)  # Use the same port as the server

# Retry connection logic
max_attempts = 5
attempts = 0
connected = False

while not connected and attempts < max_attempts:
    try:
        print(f"Attempting to connect to the server (Attempt {attempts + 1}/{max_attempts})...")
        client_socket.connect(server_address)
        connected = True
        print("Connected to the server.")
    except Exception as e:
        print(f"Connection failed: {e}. Retrying...")
        attempts += 1
        time.sleep(2)  # Wait before retrying

if not connected:
    print("Failed to connect to the server after multiple attempts. Exiting.")
    exit()

# Send system metrics to the server
while True:
    metrics = gather_metrics()
    print("Sending system metrics to the server:", metrics)
    # Send metrics as a string
    client_socket.send(str(metrics).encode('utf-8'))
    
    # Receive server acknowledgment
    try:
        response = client_socket.recv(1024).decode('utf-8')
        #print(f"Received from server: {response}")
        with open("output.html", "w") as file:
            file.write(response)

    except Exception as e:
        print(f"Error receiving data from server: {e}")
    
    # Wait before sending the next update
    time.sleep(5)
    

# Close the connection
client_socket.close()
