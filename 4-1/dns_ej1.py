import dns.resolver

# En dnspython >= 2.0 se recomienda resolve(); query() es la versión antigua (deprecated)
respuesta = dns.resolver.resolve('en.wikipedia.org')
print(respuesta[0].address)

# Respuesta completa del servidor, en texto legible
print(respuesta.response)

# Representación binaria usada por el protocolo (curiosidad)
print(respuesta.response.to_wire())
