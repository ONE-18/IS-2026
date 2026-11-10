from . import saludo


@saludo.route("/")
def mostrar_saludo():
    return "Hola amigos, ¿cómo estáis?"