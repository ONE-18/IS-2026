# Ejercicio 8: AutoAddPolicy (acepta ciegamente cualquier clave de servidor)
import getpass
import paramiko
import time

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())   # antes de connect()
clave = getpass.getpass("Clave de alumno: ")
client.connect('localhost', username='alumno', password=clave)
print("Conectado!!")

stdin, stdout, stderr = client.exec_command('ls')
for line in stdout:
    print(line.rstrip())
time.sleep(1)
client.close()
