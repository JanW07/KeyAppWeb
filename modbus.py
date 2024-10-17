from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder

# Define the Modbus TCP server details
host = '10.1.1.5'  # Replace with the IP address of your Modbus server
port = 502  # Default Modbus TCP port

# Create a Modbus TCP client
client = ModbusTcpClient(host=host, port=port)

# Connect to the server
connection = client.connect()
if connection:
    print("Connected to Modbus server")

    # Example: Read 10 holding registers starting from address 0
    result = client.read_input_registers(address=0, count=10, slave=1)
    if not result.isError():
        print(f"Register values: {result.registers}")
    else:
        print("Error reading registers")

    # Example: Write the value 100 to the holding register at address 1

    data = 502
    
    write_result = client.write_register(address=502, value=data, slave=1)
    if not write_result.isError():
        print("Successfully wrote to register")
    else:
        print("Error writing to register")


    # Close the connection
    client.close()
else:
    print("Unable to connect to Modbus server")


