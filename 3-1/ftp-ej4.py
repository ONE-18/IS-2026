# Ejercicio 19: descargar todos los ficheros de una carpeta (omitiendo subcarpetas)
import ftplib
import getpass

clave = getpass.getpass("Clave? ")
f = ftplib.FTP("localhost")
f.login("alumno", clave)
f.cwd("carpeta")

lista = []
f.retrlines("MLSD", lista.append)

for linea in lista:
    if "type=file" not in linea:       # omite cdir, pdir y dir
        continue
    nombre = linea.split("; ", 1)[1]
    with open(nombre, "wb") as f_local:
        f.retrbinary("RETR " + nombre, f_local.write)
    print("Descargado:", nombre)
f.quit()
