# Ejercicio 2: arrancar remotamente udp_servidor3_con_ok.py si no está en ejecución
import telnetlib
import time

HOST = "192.168.2.32"   # Cambiar por la IP del servidor
USER = "alumno"
PASSWORD = "clave"      # Mala práctica, pero se pide así en el ejercicio

tn = telnetlib.Telnet(HOST)
tn.read_until(b"login: ")
tn.write(USER.encode("ascii") + b"\n")
tn.read_until(b"Password: ")
tn.write(PASSWORD.encode("ascii") + b"\n")

tn.read_until(b"$")                  # Shell listo
tn.write(b"ps -ef\n")
respuesta = tn.read_until(b"$")      # Salida de ps -ef hasta el siguiente prompt

if b"udp_servidor3_con_ok.py" in respuesta:
    print("El servidor ya está en ejecución")
    tn.write(b"exit\n")
else:
    tn.write(b"nohup python3 udp_servidor3_con_ok.py &\n")
    time.sleep(1)
    tn.write(b"exit\n")
print(tn.read_all().decode("utf-8"))
