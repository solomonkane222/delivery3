import re
from netmiko import ConnectHandler
import getpass

# Define device parameters
device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',
    'username': getpass.getpass('Enter Username (e.g., prne): '),  # Use getpass for username input
    'password': getpass.getpass('Enter Password (e.g., cisco123!): '),  # Use getpass for password input
    'secret': 'class123!',  # class123! = secret password
}

# Connect to the device
try:
    connection = ConnectHandler(**device)
except Exception as e:
    print(f'Failed to connect to {device["ip"]}: {e}')
    exit()

# Enter enable mode
connection.enable()

# Configure loopback interfaces
loopback_commands = [
    'interface Loopback0',
    'ip address 10.0.0.1 255.255.255.255',
    'interface Loopback1',
    'ip address 10.0.0.2 255.255.255.255',
]
output = connection.send_config_set(loopback_commands)

# Configure the hostname to Router3
config_commands = ['hostname Router3']
output = connection.send_config_set(config_commands)

# Configure EIGRP (you can modify the EIGRP settings accordingly)
eigrp_commands = [
    'router eigrp 1',
    'network 10.0.0.1 0.0.0.0',
    'network 10.0.0.2 0.0.0.0',
]
output = connection.send_config_set(eigrp_commands)

# Configure RIP (you can modify the RIP settings accordingly)
rip_commands = [
    'router rip',
    'version 2',
    'network 10.0.0.0',
]
output = connection.send_config_set(rip_commands)

# Saving the file locally as 'running_config.txt'
output_file_path = 'running_config.txt'
running_config = connection.send_command('show running-config')
with open(output_file_path, 'w') as output_file:
    output_file.write(running_config)

# Display a success message - for a successful connection.
print('------------------------------------------------------')
print('')
print(f'Successfully connected to IP address: {device["ip"]}')
print(f'Username: {device["username"]}')
print('Password: ********')  # Masking the password for security
print('Hostname: Router3')
print('Loopback IP Addresses: 10.0.0.1/32, 10.0.0.2/32')
print('EIGRP Configuration: Advertised Loopbacks into EIGRP')
print('RIP Configuration: Advertised Loopbacks into RIP')
print(f'Running Configuration saved to: {output_file_path}')
print('')
print('------------------------------------------------------')

# Disconnect from the device
connection.disconnect()
