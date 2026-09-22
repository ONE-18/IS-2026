from tools import *


def main():
    timeout_value = 0.1
    port = input("Enter the port number for the UDP server (default 9998): ")
    if port:
        port = int(port)
    else:
        port = 9998

    s = create_udp_server(port)
    s.settimeout(timeout_value)

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
    reintentar = False

    while True:
        if reintentar:
            if timeout_value >= 2:
                print("Puede que el servidor esté caído. Inténtelo más tarde.")
                break
            s.sendto(data, addr)
        else:
            data = bytes(input(f"{cont}:"), "utf8")
            if data == "FIN":
                break
            else:
                s.sendto(data, addr)

        try:
            datagrama, origen = s.recvfrom(1024)  # Tamaño máximo a recibir
            datagrama = datagrama.decode("utf8")
            if datagrama == "OK":
                print("Recibida confirmación")
                cont += 1
                reintentar = False
                timeout_value = 0.1  # Reset timeout value on successful confirmation
            else:
                print("Recibido datagrama no esperado")
        except socket.timeout:
            print("Reintentando...")
            reintentar = True
            timeout_value *= 2  # Double the timeout value on unexpected datagram
            s.settimeout(timeout_value)  # Update the socket timeout
        except:  # Otras posibles excepciones dejamos que las maneje el usuario
            raise


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServer shutting down.")
