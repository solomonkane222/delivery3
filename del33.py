import re
import time  # Import the 'time' module for adding delays
from netmiko import ConnectHandler
import getpass

# Define device parameters
device = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',
    'username': getpass.getpass('Enter Username: '),  # Use getpass for username input
    'password': getpass.getpass('Enter Password: '),  # Use getpass for password input
    'secret': 'class123!',  # class123! = secret password
}

# Connect to the device
try:
    connection = ConnectHandler(**device)
except Exception as e:
    print(f'Failed to connect to {device["ip"]}: {e}')
    exit()

# Add a delay after establishing the connection
time.sleep(2)

# Enter enable mode
connection.enable()

# Configure loopback interfaces
loopback_commands = [
    'interface Loopback0',
    'ip address 10.0.0.1 255.255.255.255',
    'interface Loopback1',
    'ip address 192.168.1.2 255.255.255.0',
]

try:
    output = connection.send_config_set(loopback_commands)
except Exception as e:
    print(f'Failed to configure loopback interfaces: {e}')

# Add a delay after configuring loopback interfaces
time.sleep(2)

# Configure the hostname to Router3
config_commands = ['hostname Router3']

try:
    output = connection.send_config_set(config_commands)
except Exception as e:
    print(f'Failed to configure hostname: {e}')

# Add a delay after configuring the hostname
time.sleep(2)

# Configure OSPF (you can modify the OSPF settings accordingly)
ospf_commands = [
    'router ospf 1',
    'network 10.0.0.1 0.0.0.0 area 0',  # Advertise the loopback into OSPF
]

try:
    output = connection.send_config_set(ospf_commands)
except Exception as e:
    print(f'Failed to configure OSPF: {e}')

# Add a delay after configuring OSPF
time.sleep(2)

# Configure EIGRP (you can modify the EIGRP settings accordingly)
eigrp_commands = [
    'router eigrp 1',
    'network 192.168.1.0 0.0.0.255',  # Advertise the loopback subnet into EIGRP
]

try:
    output = connection.send_config_set(eigrp_commands)
except Exception as e:
    print(f'Failed to configure EIGRP: {e}')

# Add a delay after configuring EIGRP
time.sleep(2)

# Configure RIP (you can modify the RIP settings accordingly)
rip_commands = [
    'router rip',
    'version 2',
    'network 10.0.0.1',  # Advertise the loopback address in RIP
    'network 192.168.1.0'  # Advertise the loopback subnet in RIP
]

try:
    output = connection.send_config_set(rip_commands)
except Exception as e:
    print(f'Failed to configure RIP: {e}')

# Add a delay after configuring RIP
time.sleep(2)

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
print('Loopback IP Addresses: 10.0.0.1/32, 192.168.1.2/24')
print('OSPF Configuration: Advertised Loopback into OSPF')
print('EIGRP Configuration: Advertised Loopback into EIGRP')
print('RIP Configuration: Advertised Loopback and Loopback Subnet into RIP')
print(f'Running Configuration saved to: {output_file_path}')
print('')
print('------------------------------------------------------')

# Disconnect from the device
connection.disconnect()
