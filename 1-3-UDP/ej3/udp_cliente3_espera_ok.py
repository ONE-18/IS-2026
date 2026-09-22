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
    cont = 0
    s.settimeout(0.1)

    while True:
        data = bytes(input(f"{cont}:"), "utf8")
        if data == "FIN":
            break
        else:
            s.sendto(data, addr)
            cont += 1

        try:
            datagrama, origen = s.recvfrom(1024)  # Tamaño máximo a recibir
            datagrama = datagrama.decode("utf8")
            if datagrama == "OK":
                print("Recibida confirmación")
            else:
                print("Recibido datagrama no esperado")
        except socket.timeout:
            print("ERROR. El datagrama de confirmación no llega")
        except:  # Otras posibles excepciones dejamos que las maneje el usuario
            raise


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServer shutting down.")
