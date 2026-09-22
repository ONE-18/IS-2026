from tools import *
import random


def main():
    port = input("Enter the port number for the UDP server (default 9999): ")
    if port:
        port = int(port)
    else:
        port = 9999
    s = create_udp_server(port)
    while True:
        data, addr = s.recvfrom(1024)

        if random.randint(0, 1) == 0:
            print(f"Received message: {data.decode()} from {addr}")
        else:
            print("Simulando paquete perdido")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServer shutting down.")
