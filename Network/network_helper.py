
import re
import socket
import subprocess
import binascii

import puresnmp
from puresnmp.x690.types import Integer


def get_my_host_name():
    return socket.gethostname()


def get_my_ip_address():
    return socket.gethostbyname(socket.gethostname())


def get_my_ip_addresses():
    return socket.gethostbyname_ex(socket.gethostname())[2]


def get_mac_from_ip(ip_address):
    output = subprocess.Popen(['arp', '-a', '%s' % ip_address], stdout=subprocess.PIPE)
    output = str(output.communicate()[0])
    mac = re.search('([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', output).group()
    if len(mac) != 17:
        mac = 'NO_MAC_FOUND'
    else:
        mac = mac.replace('-', '')
        mac = mac.replace(':', '')
    return mac


def wake_printer(ip_address, printer_tcp_port=9100):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip_address, printer_tcp_port))
    client_socket.close()


def wake_hp_printer_by_snmp(ip_address):
    result = puresnmp.set(ip_address, 'public', "1.3.6.1.4.1.11.2.3.9.4.2.1.1.1.2.0", Integer(1))
    if result == 1:
        return True
    else:
        return False


def set_sleep_hp_printer_by_snmp(ip_address):
    result = puresnmp.set(ip_address, 'public', "1.3.6.1.4.1.11.2.3.9.4.2.1.1.1.2.0", Integer(2))
    if result == 2:
        return True
    else:
        return False


def is_hp_printer_sleep_by_snmp(ip_address):
    result = puresnmp.get(ip_address, 'public', "1.3.6.1.4.1.11.2.3.9.4.2.1.1.1.2.0")
    if result == 1:
        return False
    elif result == 2:
        return True
    else:
        return None


def get_mac_from_snmp(device_ip, device_type):
    if device_type[:2].lower() == 'hp':
        return str(binascii.b2a_hex(puresnmp.get(device_ip, 'public', '1.3.6.1.2.1.2.2.1.6.2')), 'utf-8').upper()
    else:
        return str(binascii.b2a_hex(puresnmp.get(device_ip, 'public', '1.3.6.1.2.1.2.2.1.6.1')), 'utf-8').upper()


def get_device_name_from_snmp(device_ip):
    return str(puresnmp.get(device_ip, 'public', '1.3.6.1.2.1.25.3.2.1.3.1'), 'utf-8').replace(' ', '_')
