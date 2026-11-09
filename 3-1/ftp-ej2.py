# Ejercicio 17: MLSD, mostrando solo nombres de ficheros (sin . ni ..)
import ftplib
import getpass

lista = []
def acumular(linea):
    lista.append(linea)

clave = getpass.getpass("Clave? ")
f = ftplib.FTP("localhost")
f.login("alumno", clave)
f.cwd("carpeta")

f.retrlines("MLSD", acumular)

for linea in lista:
    if "type=cdir" in linea or "type=pdir" in linea:
        continue
    # Formato: "type=file;size=123;modify=...; nombre"
    nombre = linea.split("; ", 1)[1]
    print(nombre)
f.quit()
