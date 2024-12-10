import socket

def generate_html_response(metrics):
    # Create an HTML response displaying the metrics
    html = f"""
    <html><head><title>System Metrics</title><style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
            h1 {{ color: #4CAF50; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ padding: 8px; text-align: left; border: 1px solid #ddd; }}
            th {{ background-color: #f2f2f2; }}
            .container {{ max-width: 800px; margin: auto; }}
    </style></head><body><div class="container">
            <h1>System Metrics</h1><table><tr><th>Metric</th><th>Value</th></tr><tr>
                    <td>CPU Utilization</td><td>{metrics['cpu']}%</td>
                </tr><tr>
                    <td>Memory Utilization</td><td>{metrics['memory']}%</td>
                </tr><tr>
                    <td>GPU Utilization</td><td>{metrics['gpu']}%</td>
                </tr><tr>
                    <td>Temperature</td><td>{metrics['temperature']}C</td>
                </tr></table></div></body></html>"""
    return html

def handle_client_data(client_socket):
    while True:
        data = client_socket.recv(1024)  # Receive data from the client
        if not data:
            break  # Break if no data (connection closed)
        
        # Decode the data and parse it (expected to be a dictionary)
        metrics = eval(data.decode('utf-8'))  # Convert string to dictionary (only safe for trusted sources)
        print(f"Received data from client: {metrics}")

        # Generate HTML response with the received metrics
        html_response = generate_html_response(metrics)
        
        # Send the HTTP response headers and HTML content
        print(f"Sending {html_response}")
        response = html_response
        client_socket.sendall(response.encode('utf-8'))  # Convert to bytes before sending
        #client_socket('HTTP/1.1 200 OK\n')
        #client_socket('Content-Type: text/html\n')
        #client_socket('Connection: close\n\n')
        #client_socket.sendall(response)
# Create a socket object (server side)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server to a specific address and port
server_socket.bind(('localhost', 8000))  # Bind to localhost and port 80

# Start listening for incoming connections
server_socket.listen(5)
print("Server is listening on port 8000...")

while True:
    client_socket, client_address = server_socket.accept()  # Accept new connection
    print(f"Connection established with {client_address}")
    handle_client_data(client_socket)  # Handle the incoming client data
    client_socket.close()  # Close the connection after handling
