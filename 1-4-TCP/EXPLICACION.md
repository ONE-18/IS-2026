# Sesión 1.4 · Programación de red con Python. TCP

Ingeniería de Servicios 2026-2027

Este documento explica, paso a paso, los programas de la sesión: qué problema resuelve cada uno, por qué el anterior se queda corto y cómo probarlo. Todos los scripts están en la misma carpeta y se han probado entre sí.

---

## 0. Índice de ficheros

| Apartado | Ejercicio | Servidor | Cliente |
|---|---|---|---|
| 2.1 | Ej. 1 · Bloques fijos de 5 bytes | `tcp_servidor1_simple.py` | `tcp_cliente1_simple.py` |
| 2.1.1 | Ej. 2 · `recvall()` / `sendall()` | `tcp_servidor2_recvall.py` | `tcp_cliente2_sendall.py` |
| 2.2.1 | Ej. 3 · "oche" simplista | `tcp_servidor3_oche_simplista.py` | `tcp_cliente3_oche.py`, `tcp_cliente3_oche_envia_seguido.py` |
| 2.2.3 | Ej. 4 · `recibe_mensaje()` byte a byte | `tcp_servidor4_oche_mejorado.py` | `tcp_cliente4_oche_mejorado.py` |
| 2.2.3 | Ej. 5 · `makefile()` + `readline()` | `tcp_servidor5_oche_readline.py` | `tcp_cliente5_oche_readline.py` |
| 2.3.1 | Ej. 6 · Longitud en ASCII | `tcp_servidor6_oche_len.py` | `tcp_cliente6_oche_len.py` |
| 2.3.2 | Ej. 7 · Longitud en binario (opcional) | `tcp_servidor7_opcional.py` | `tcp_cliente7_opcional.py` |

> En el enunciado el cliente del ejercicio 6 aparece como `tcp_cliente.6_oche_len.py` (con un punto). Parece una errata; aquí se llama `tcp_cliente6_oche_len.py`.

### Convenciones comunes

- **Argumentos:** los servidores reciben el puerto (`python3 servidor.py 9999`, por defecto 9999). Los clientes reciben `ip puerto` (por defecto `localhost 9999`).
- **Variable de entorno `RETARDO`:** todos los servidores aceptan `RETARDO=1` para hacer un `time.sleep(1)` justo después del `accept()`. Es el experimento que propone el PDF para que los envíos del cliente se acumulen en el buffer del socket antes de que el servidor lea. Ejemplo: `RETARDO=1 python3 tcp_servidor3_oche_simplista.py`.
- **Variable de entorno `MENSAJE`:** solo en los clientes 1 y 2. Permite cambiar `ABCDE` por `ABCD` para el experimento de los 4 bytes.
- Todos los servidores usan `SO_REUSEADDR`, para poder relanzarlos enseguida sin el error "Address already in use".

---

## 1. Idea de fondo: TCP es un flujo de bytes, no de mensajes

Con `SOCK_STREAM` el transporte va sobre TCP, que ya se encarga de reenviar, numerar y confirmar paquetes. A cambio aparece el problema del **framing**: delimitar dónde empieza y acaba cada mensaje.

Una conexión TCP es como una tubería (un *pipe*):

- Un `send()` **no** equivale a un `recv()`. Un `send("ABCDE")` puede salir en dos trozos (3+2 bytes), y varios `send()` pueden llegar fusionados en un solo `recv()`.
- TCP garantiza **orden e integridad**, pero no **fronteras entre mensajes**. UDP sí las respeta: sus datagramas son atómicos.

Por eso hay que decidir cómo delimitar mensajes. La sesión ve tres técnicas:

1. Mensajes de tamaño fijo (2.1)
2. Marca de fin de mensaje (2.2)
3. Enviar antes la longitud (2.3)

La atención concurrente a varios clientes (hilos, procesos, `select()`) queda fuera de esta sesión: los servidores atienden a un cliente cada vez.

---

## 2. Mensajes de tamaño prefijado (2.1)

### Ejercicio 1: `tcp_servidor1_simple.py` y `tcp_cliente1_simple.py`

**Servidor.** Es el ciclo clásico `socket()` → `bind()` → `listen()` → `accept()` → `recv()`:

- `s` es el socket de escucha, y `accept()` devuelve un socket de datos nuevo (`sd`). Las lecturas se hacen sobre `sd`, no sobre `s`.
- Lee bloques de 5 bytes con `sd.recv(5)` y los muestra.
- Si recibe `FINAL`, cierra `sd` y vuelve a esperar otro cliente.
- Si `recv()` devuelve vacío, el cliente cerró la conexión de forma inesperada.
- `recv()` devuelve `bytes`, así que se convierte a `str` con `.decode("ascii")`.

**Cliente.** Crea el socket, hace `connect()`, envía `ABCDE` cinco veces y luego `FINAL`. Usa un bucle sobre `send()`, porque `send()` devuelve cuántos bytes ha enviado realmente y puede ser menos de los pedidos:

```python
while mensaje != b"":
    enviados = sock.send(mensaje)
    mensaje = mensaje[enviados:]   # quedan los restantes
```

**Qué se observa.** Parece que cada `send()` es un "datagrama" de 5 bytes y cada `recv()` recibe uno. Es una ilusión: en realidad es un flujo y funciona porque la red de pruebas no tiene retardo.

### Ejercicio 2: `recvall()` y `sendall()`

**Problema.** Si `send()` puede fraccionar, `recv(5)` puede devolver 3 bytes, y entonces haría falta otro `recv()` para los 2 restantes.

**Solución.**

- **Cliente:** `sock.sendall(mensaje)` hace el bucle de `send()` internamente y de forma más eficiente (`tcp_cliente2_sendall.py`).
- **Servidor:** `recvall(sock, n)` no devuelve hasta tener `n` bytes. Pide los que faltan (no de uno en uno) y acumula los trozos en una lista, que luego une con `b"".join(...)`. Si el otro extremo cierra a mitad, devuelve lo que haya llegado.

**Limitación que revela el experimento.** `recvall()` hace al servidor *más rígido*, no más robusto frente a errores del otro extremo.

#### Experimento (4 bytes en lugar de 5)

```bash
# Terminal 1
python3 tcp_servidor1_simple.py
# Terminal 2
MENSAJE=ABCD python3 tcp_cliente1_simple.py
```

- Con `tcp_servidor1_simple.py` y **sin retardo**, lo normal es ver bloques de 4 bytes y que `FINAL` se detecte.
- Con `RETARDO=1` en el servidor, los envíos se acumulan y `recv(5)` devuelve `ABCDA`, `BCDAB`... La sincronía se rompe.
- Con `tcp_servidor2_recvall.py` el efecto es seguro: `recvall` insiste en 5 bytes y toma los que faltan del envío siguiente. Se mezclan los paquetes y `FINAL` no se detecta bien. Si no hay más envíos, el servidor se queda esperando indefinidamente.

Lo mismo ocurre si el cliente envía más de 5 bytes por `send()`.

**Conclusión.** Con longitud fija, un solo error desincroniza toda la comunicación posterior. Con UDP esto no pasa porque los datagramas son atómicos.

---

## 3. Marca de "fin de mensaje" (2.2)

La mayoría de mensajes no tienen tamaño fijo. Una solución es terminarlos con una secuencia de bytes que no aparezca dentro del mensaje. Los protocolos orientados a líneas usan `\r\n` (bytes `0D 0A`, iguales en cualquier encoding, UTF-8 incluido).

### El servicio "oche" (echo al revés)

Por cada cliente, el servidor lee mensajes continuamente y devuelve cada uno invertido: `HOLA` → `ALOH`.

Invertir un string en Python: `msg[::-1]`. Es un slice sin inicio ni fin, con paso `-1`.

### Ejercicio 3: versión simplista (`tcp_servidor3_oche_simplista.py`)

Supone que:

1. Cada mensaje es una línea ASCII terminada en `\r\n`.
2. Ninguna línea supera los 80 bytes.
3. **Cada `recv()` devuelve exactamente una línea completa.**
4. La respuesta es el mensaje invertido, también terminado en `\r\n` (por ejemplo `"HOLA\r\n"` → `"ALOH\r\n"`; el PDF escribe `"HOLA\n\n"` pero es una errata).

El bucle es: `recv(80)` → decodificar → quitar los 2 últimos caracteres (`[:-2]`) → invertir → `sendall(linea + "\r\n")`. Sale del bucle cuando `recv()` devuelve vacío, es decir, cuando el cliente cierra.

**Clientes de prueba:**

- `tcp_cliente3_oche.py` envía una línea, lee su respuesta, y repite. Funciona bien.
- `tcp_cliente3_oche_envia_seguido.py` envía tres líneas seguidas y después lee tres respuestas, mostrándolas con `repr()` para ver los `\r\n`. Tiene un timeout de 3 s para que no se cuelgue indefinidamente cuando falta una respuesta.

#### Experimento y resultado obtenido

Al ejecutar `tcp_cliente3_oche_envia_seguido.py` contra el servidor simplista aparece:

```text
Respuesta 1: 'SERT\n\rSOD\n\rONU\r\n'
Respuesta 2: TIMEOUT
Respuesta 3: TIMEOUT
```

Esto ocurre porque el servidor recibió `UNO\r\nDOS\r\nTRES\r\n` **junto** en un solo `recv()` y lo trató como una única línea. El resultado es una respuesta mal formada, con los `\r\n` de en medio invertidos a `\n\r`, y las otras dos respuestas nunca llegan.

Aviso: según la velocidad de la máquina, a veces los tres envíos llegan separados al servidor y este funciona bien, aunque las respuestas lleguen pegadas al cliente. Con `RETARDO=1` el fallo es mucho más reproducible.

### Por qué fallan también las otras suposiciones (2.2.2 y 2.2.3)

- **Suposición 3:** TCP puede concatenar varios `send()` en un `recv()`, o partir uno en varios.
- **Suposición 2:** aunque cada línea mida menos de 80, al acumularse en el buffer el servidor puede tener que leer más de 80 bytes. Con dos mensajes de 50 caracteres, `recv(80)` devolvería el primero entero, su `\r\n` y solo 28 caracteres del segundo.

Hacer `split("\r\n")` ayudaría con la primera línea, pero no resuelve que el resto de la segunda quede para el siguiente `recv()`.

**Solución típica:** una función `recibe_mensaje()` que no retorne hasta tener una línea completa, detectando el terminador. Hay dos formas de hacerla.

### Ejercicio 4: `recibe_mensaje()` byte a byte

Archivos: `tcp_servidor4_oche_mejorado.py` y `tcp_cliente4_oche_mejorado.py`.

```python
def recibe_mensaje(sock):
    buffer = []                      # lista de bytes
    while True:
        byte = sock.recv(1)
        if byte == b"":              # conexión cerrada
            return b""
        buffer.append(byte)
        if byte == b"\n" and len(buffer) >= 2 and buffer[-2] == b"\r":
            return b"".join(buffer)
```

- **Ventaja:** es muy simple y robusta. Nunca lee más de lo que hace falta.
- **Inconveniente:** es muy ineficiente si el mensaje es largo, porque hace una llamada al sistema por byte.
- **Nota de Python:** `buffer = buffer + byte` es correcto pero muy lento, porque las cadenas son inmutables y cada suma crea una copia. Lo eficiente es `append()` sobre una lista y `b"".join(buffer)` al final.

El resultado obtenido es correcto incluso con `RETARDO=1`, y las tres respuestas son `'ONU\r\n'`, `'SOD\r\n'` y `'SERT\r\n'`.

### Ejercicio 5: `makefile()` + `readline()`

Archivos: `tcp_servidor5_oche_readline.py` y `tcp_cliente5_oche_readline.py`.

Es la segunda variante de `recibe_mensaje()`, que lee bloques grandes y guarda el sobrante en un buffer propio. Para no programar ese buffer circular se usa el que ya trae Python: `makefile()` convierte el socket en un objeto fichero, y los ficheros tienen `readline()`.

```python
f = sd.makefile(encoding="utf8", newline="\r\n")
mensaje = f.readline()   # str, incluye el \r\n final; "" si el otro extremo cierra
```

- Como se especifica `encoding`, `readline()` devuelve `str` y no `bytes`.
- Con `newline="\r\n"` solo se considera fin de línea la secuencia `\r\n`.
- Es eficiente, porque lee bloques grandes del socket y los va entregando línea a línea.
- **Importante:** una vez creado `f`, **todas las lecturas** deben hacerse a través de `f`, porque `f` tiene el buffer con lo ya recibido. Si se mezclara `sd.recv()` con `f.readline()`, se perderían datos. Las **escrituras** pueden seguir haciéndose con `sd.sendall()`.

---

## 4. Enviar previamente la longitud del mensaje (2.3)

Otra opción es no usar terminadores: el emisor antepone la longitud de lo que sigue. El receptor lee la longitud y después llama a `recvall()` con ese número. Hay dos formas de codificar la longitud.

### 4.1 Longitud en ASCII (Ejercicio 6)

Archivos: `tcp_servidor6_oche_len.py` y `tcp_cliente6_oche_len.py`.

Formato de cada mensaje, en ambos sentidos:

```text
"<longitud>\n" + <mensaje>          Ejemplo:   b"4\nHOLA"
```

- La longitud en ASCII tiene tamaño variable (`23` son 2 caracteres, `123` son 3), así que hace falta un delimitador: `\n` (o `\0`).
- **Emisor:** `"%d\n" % len(datos_en_bytes)`. La longitud debe medirse en **bytes**, no en caracteres, porque con UTF-8 una `í` ocupa 2 bytes.
- **Receptor:** `f.readline()` para la cabecera, `int()` para convertirla y `f.read(longitud)` para el cuerpo.
- Los programas abren `sd.makefile("rb")` en **modo binario**: así `read(n)` trabaja con bytes y espera a tener los `n` bytes pedidos (la función hace de `recvall`).
- Como no hay terminador, el mensaje **puede contener cualquier byte**, incluidos `\r\n` o saltos de línea. Los programas lo prueban con `"línea\ncon salto"`.
- Si la cabecera no es un número, `int()` lanza `ValueError` y el servidor cierra esa conexión.

### 4.2 Longitud en binario (Ejercicio 7, opcional)

Archivos: `tcp_servidor7_opcional.py` y `tcp_cliente7_opcional.py`.

Es lo que hacen las cabeceras de UDP, TCP o IP: se envía el número directamente en binario, en un **número fijo de bytes**. Así no hace falta ningún terminador ni `readline()`: el servidor siempre lee 2 bytes y decodifica.

En C bastaría con enviar los bytes de la variable, usando `htons()`/`ntohs()` para no depender de la *endianity* de cada máquina. En Python se usa el módulo `struct`:

```python
import struct
cabecera = struct.pack(">H", len(datos))       # entero -> 2 bytes
(longitud,) = struct.unpack(">H", cabecera)    # 2 bytes -> entero (unpack devuelve una TUPLA)
```

La "clave" `">H"` significa:

- `>` es big endian (orden de red).
- `H` es unsigned short (2 bytes).

Pruebas del intérprete que propone el PDF:

| Expresión | Resultado | Explicación |
|---|---|---|
| `struct.pack(">H", 15)` | `b'\x00\x0f'` | Sí codifica el 15, con el byte alto primero. |
| `struct.pack("<H", 15)` | `b'\x0f\x00'` | Little endian: bytes en orden inverso. |
| `struct.unpack(">H", b"\x00\x10")` | `(16,)` | Tupla con el entero 16. |

Detalles:

- Con 2 bytes el mensaje puede tener como máximo 2^16 − 1 = **65535 bytes**. El código lo comprueba al enviar.
- El PDF muestra `bytes = struct.pack(">H", len(bytes(mensaje, "utf8")))`. No hay que llamar `bytes` a la variable, porque **oculta** la función `bytes()` de Python. En los scripts se llama `cabecera`.
- El servidor usa `recvall()` sobre el socket (sin `makefile`), tanto para los 2 bytes de la cabecera como para el cuerpo.

### Comparativa de técnicas

| Técnica | Ventajas | Inconvenientes |
|---|---|---|
| Tamaño fijo | Trivial | Un fallo desincroniza todo; poco flexible |
| Terminador `\r\n` | Sencilla; típica de protocolos de texto | El terminador no puede aparecer dentro del mensaje; hay que buscarlo |
| Longitud ASCII + `\n` | El mensaje puede contener cualquier byte; fácil de codificar | La cabecera tiene longitud variable y necesita su propio terminador |
| Longitud binaria | Cabecera fija, sin búsqueda de terminador | Hay que controlar endianness y límite de tamaño |

---

## 5. Despliegue con Docker (apartado 3)

### 5.1 Contenedores en la misma red

Suponiendo que la red `pruebas` ya existe de la sesión anterior (`docker network create pruebas`), desde la carpeta con los scripts:

```bash
# Servidor
docker run -d --rm --network pruebas --name servidor_oche -v $(pwd):/app \
    python:3.7 python /app/tcp_servidor5_oche_readline.py

# Cliente en la misma subred, contactando por NOMBRE
docker run --rm --network pruebas -v $(pwd):/app \
    python:3.7 python /app/tcp_cliente5_oche_readline.py servidor_oche 9999
```

- `--rm` elimina el contenedor cuando termina o se detiene con `docker stop`, como si se hubiera hecho `docker rm`. Evita que aparezcan en `docker ps -a` y bloqueen el nombre para otro contenedor.
- El DNS interno de la red resuelve `servidor_oche`, sin necesidad de conocer la IP.
- Esto es ideal para microservicios: cada servicio es un contenedor y se llaman por nombre, sin colisiones de puertos ni gestión de IPs.
- Pero la red es **privada**: desde fuera de ella no hay acceso.

### 5.2 Exponer un puerto al exterior (`-p`)

1. Detén el contenedor anterior y comprueba con `docker ps -a` que ya no aparece. Si aparece, se lanzó sin `--rm` y hay que borrarlo con `docker rm servidor_oche`.
2. Lánzalo mapeando puertos, con la forma `-p puerto_host:puerto_contenedor`:

   ```bash
   docker run -d --rm -p 9090:9999 --network pruebas \
       --name servidor_oche -v $(pwd):/app \
       python:3.7 python /app/tcp_servidor5_oche_readline.py
   ```

3. Con `docker ps` se ve en la columna PORTS el mapeo `0.0.0.0:9090->9999/tcp`. Para UDP habría que escribir `/udp` al final del mapeo, y por defecto se asume TCP.

Ahora el servicio es accesible:

- desde otros contenedores de la subred, como antes;
- desde el anfitrión: `python3 tcp_cliente5_oche_readline.py localhost 9090`;
- desde cualquier máquina que llegue a tu Ubuntu, en su puerto 9090.

### Experimentos

- **Un compañero ejecuta el cliente desde su PC.** Tiene que conectar a la IP de tu máquina y al puerto 9090. Si tu máquina virtual está en modo adaptador puente, basta su IP. Si está en modo NAT hay que redirigir un puerto de Windows al 9090 de la VM desde la configuración de red de VirtualBox.
- **Un compañero ejecuta el cliente dentro de un contenedor.** Debería funcionar si usa la IP de tu Ubuntu y el puerto 9090. Su contenedor está en otra subred, así que no ve el DNS de tu red ni puede usar el nombre `servidor_oche` ni la IP interna del contenedor: debe usar la IP del anfitrión y el puerto expuesto. Para que varias máquinas compartan una red de contenedores existe `docker swarm` con redes *overlay*, pero queda fuera del curso.

---

## 6. Resumen de ideas clave

1. TCP es un **flujo de bytes**: un `send()` no se corresponde con un `recv()`.
2. `send()` puede enviar menos de lo pedido, así que se usa `sendall()`. El equivalente en lectura, `recvall()`, hay que escribirlo.
3. `recv(n)` puede devolver menos de `n` bytes, o a la vez el final de un mensaje y el principio del siguiente.
4. Hay que definir un protocolo de **framing**: tamaño fijo, terminador o longitud previa.
5. Con terminador `\r\n` se usa `recibe_mensaje()` (byte a byte, simple pero lento) o `makefile()` + `readline()` (eficiente).
6. Con longitud previa, ASCII (con `\n`) o binaria (`struct.pack(">H", ...)`), el mensaje puede contener cualquier byte.
7. En Docker, `--rm` limpia contenedores y `-p host:contenedor` los expone fuera de la red privada.
