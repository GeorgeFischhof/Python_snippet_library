import socket
from typing import List


class MultipleWorkingPortsFound(Exception):
    pass


class WorkingPortNotFound(Exception):
    pass


def get_used_ports(host: str, ports_to_check: List[str]) -> str:
    good_ports = list()

    for port in ports_to_check:
        if is_port_used(host, port):
            good_ports.append(port)

    if len(good_ports) == 0:
        raise WorkingPortNotFound(f"requested portlist: {ports_to_check}")
    if len(good_ports) > 1:
        raise MultipleWorkingPortsFound(f"requested portlist: {ports_to_check}")

    return good_ports[0]


def is_port_used(host: str, port: (str, int), timeout: int = 2) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    try:
        sock.connect((host, int(port)))
    except TimeoutError:
        return False

    sock.close()
    return True
