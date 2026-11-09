import dns.resolver

respuesta = dns.resolver.resolve('apple.com')
for registro in respuesta:
    print(registro.address)
