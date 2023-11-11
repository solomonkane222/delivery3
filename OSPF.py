import re
from netmiko import ConnectHandler
import getpass 

# Define device parameters
device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',
    'username': getpass.getpass('Enter Username (e.g., prne): '),  # Use getpass for username input
    'password': getpass.getpass('Enter Password (e.g., cisco123!): '),  # Use getpass for password input
    'secret': 'class123!', #class123! = secret passwrd
}

# Connect to the device
try:
    connection = ConnectHandler(**device)
except Exception as e:
    print(f'Failed to connect to {device["ip"]}: {e}')
    exit()

# Enter enable mode
connection.enable()

# Configuring the hostname to Router3
config_commands = ['hostname Router3']

# Configuring the loopback interface
config_commands += [
    'interface loopback0',
    'ip address 1.1.1.1 255.255.255.255',
    'exit'
]

# Configuring OSPF routing protocol
config_commands += [
    'router ospf 1',
    'router-id 1.1.1.1',  # Specify the router ID
    'network 0.0.0.0 255.255.255.255 area 0',
    'exit'
]

output = connection.send_config_set(config_commands)

# Saving the file locally as 'running_config.txt 
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
print(f'Running Configuration saved to: {output_file_path}')
print('')
print('------------------------------------------------------')

# Disconnect from the device
connection.disconnect()
