# Ejercicio 18: descarga de un fichero con RETR binario
import ftplib
import getpass

clave = getpass.getpass("Clave? ")
f = ftplib.FTP("localhost")
f.login("alumno", clave)
f.cwd("carpeta")          # carpeta donde está prueba.txt

f_local = open("prueba-copia.txt", "wb")
result = f.retrbinary("RETR prueba.txt", f_local.write)
f_local.close()
print(result)
f.quit()
