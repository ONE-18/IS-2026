import dns.resolver

respuesta = dns.resolver.resolve("gmail.com", "MX")

# Ordenado por preferencia (menor número = mayor prioridad)
for mx in sorted(respuesta, key=lambda r: r.preference):
    nombre = mx.exchange.to_text()
    ips = dns.resolver.resolve(nombre, "A")
    print(mx.preference, nombre, ips[0].address)
