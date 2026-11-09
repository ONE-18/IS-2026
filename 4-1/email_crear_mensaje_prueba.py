# Sección 3.1.2 y ejercicio 9 (opcional): crear mensajes con la biblioteca email
import email.message
import email.policy
import email.utils


def email_crear_mensaje_prueba(con_adjunto=False):
    mensaje = email.message.EmailMessage()
    mensaje['To'] = 'Desti Natario <destinatario@example.com>'
    mensaje['From'] = 'Remi Tente <remitente@example.com>'
    mensaje['Subject'] = 'Mensaje de prueba'
    mensaje['Date'] = email.utils.formatdate(localtime=True)
    mensaje['Message-ID'] = email.utils.make_msgid()
    mensaje.set_content("Esto es una prueba")

    if con_adjunto:
        # wget http://www.atc.uniovi.es/estilo_atc/logoatc.gif
        with open("logoatc.gif", "rb") as f:
            gif = f.read()
        mensaje.add_attachment(gif, "image", "gif", filename="atc.gif")

    return mensaje


if __name__ == "__main__":
    mensaje = email_crear_mensaje_prueba(con_adjunto=False)
    binario = mensaje.as_bytes()
    print(binario.decode("utf-8"))

    print("=" * 60)
    mensaje = email_crear_mensaje_prueba(con_adjunto=True)
    print(mensaje.as_bytes().decode("utf-8"))
