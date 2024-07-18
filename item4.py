import netmiko
import requests
from netmiko import ConnectHandler

# Definir las credenciales de conexión
router = {
    'device_type': 'cisco_ios',
    'host': '192.168.56.101',  # Dirección IP del CSR1000v
    'username': 'cisco',       # Nombre de usuario
    'password': 'cisco123!',   # Contraseña
    'secret': 'cisco123!',     # Enable secret
}

# Conexión al router
net_connect = ConnectHandler(**router)
print('Conexión exitosa')

# Entrar al modo enable
net_connect.enable()

# Verificación de la conexión
output = net_connect.send_command('show ip interface brief')
print(output)

# Cambiar el hostname
commands = [
    'hostname ARAVENA-OLMOS',
    'end',
    'write memory'
]
output = net_connect.send_config_set(commands)
print(output)

# Crear la interfaz loopback 11
commands = [
    'interface loopback 11',
    'ip address 11.11.11.11 255.255.255.255',
    'end',
    'write memory'
]
output = net_connect.send_config_set(commands)
print(output)


# Cerrar la conexión
net_connect.disconnect()

print("Conexion finalizada")
