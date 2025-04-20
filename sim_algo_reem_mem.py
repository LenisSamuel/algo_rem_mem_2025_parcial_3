marcos_libres = [0x0,0x1,0x2]
reqs = [ 0x00, 0x12, 0x64, 0x65, 0x8D, 0x8F, 0x19, 0x18, 0xF1, 0x0B, 0xDF, 0x0A ]
segmentos =[ ('.text', 0x00, 0x1A),
             ('.data', 0x40, 0x28),
             ('.heap', 0x80, 0x1F),
             ('.stack', 0xC0, 0x22),
           ]

def procesar(segmentos, reqs, marcos_libres):
    tam = 0x10
    paginas = {}
    historial = {}
    tiempo = 0
    resultado = []

    for dir_logica in reqs:
        tiempo += 1
        segmento_ok = any(base <= dir_logica < base + size for _, base, size in segmentos)

        if not segmento_ok:
            resultado.append((dir_logica, 0x1FF, "Segmention Fault"))
            continue

        pag = dir_logica // tam
        off = dir_logica % tam

        if pag in paginas:
            marco = paginas[pag]
            historial[pag] = tiempo
            fisica = marco * tam + off
            resultado.append((dir_logica, fisica, "Marco ya estaba asignado"))
        else:
            if marcos_libres:
                nuevo = marcos_libres.pop(0)
                paginas[pag] = nuevo
                historial[pag] = tiempo
                fisica = nuevo * tam + off
                resultado.append((dir_logica, fisica, "Marco libre asignado"))
            else:
                menos_usada = min(historial, key=historial.get)
                marco_reemplazo = paginas[menos_usada]
                del paginas[menos_usada]
                del historial[menos_usada]
                paginas[pag] = marco_reemplazo
                historial[pag] = tiempo
                fisica = marco_reemplazo * tam + off
                resultado.append((dir_logica, fisica, "Marco asignado"))

    return resultado


def print_results(results):
    for result in results:
        print(f"Req: {result[0]:#0{4}x} Direccion Fisica: {result[1]:#0{4}x} Acción: {result[2]}")

if __name__== '__main__':
    results = procesar(segmentos, reqs, marcos_libres)
    print_results(results)
