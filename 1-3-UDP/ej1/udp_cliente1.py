from tools import *


def main():
    port = input("Enter the port number for the UDP server (default 9998): ")
    if port:
        port = int(port)
    else:
        port = 9998

    s = create_udp_server(port)

    dirr = input("addr (127.0.0.1): ")
    if not dirr:
        dirr = "127.0.0.1"

    port = input("port (9999): ")
    if port:
        port = int(port)
    else:
        port = 9999

    addr = (dirr, int(port))

    while True:
        data = bytes(input(":"), "utf8")
        if data == "FIN":
            break
        else:
            s.sendto(data, addr)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServer shutting down.")
