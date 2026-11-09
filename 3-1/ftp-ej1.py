# Ejercicio 16: LIST con callback
import ftplib
import getpass

lista = []
def acumular(linea):
    lista.append(linea)

clave = getpass.getpass("Clave? ")
f = ftplib.FTP("localhost")      # o la IP del compañero
f.login("alumno", clave)
f.cwd("carpeta")

lista = []
resp = f.retrlines("LIST", acumular)

print("Respuesta del protocolo: ", resp)
print("Contenidos de la carpeta remota:")
for l in lista:
    print(l)
f.quit()
