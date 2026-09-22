import socket


def create_udp_server(port):
    if not port:
        print("Port needed")
        return
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", port))
    return s
