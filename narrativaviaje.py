import openrouteservice

api_key = '5b3ce3597851110001cf62487731f568190f489d88dcb24f724c66f9'

# Opciones de medios de transporte con sus perfiles correspondientes
opciones_medios_transporte = [
    {'nombre': 'Coche', 'perfil': 'driving-car'},
    {'nombre': 'Caminando', 'perfil': 'foot-walking'},
    {'nombre': 'Bicicleta', 'perfil': 'cycling-regular'},
    {'nombre': 'Transporte público', 'perfil': 'driving-car'}
]

def calcular_distancia(ciudad_origen, ciudad_destino):
    client = openrouteservice.Client(key=api_key)
    coords_origen = client.pelias_search(text=ciudad_origen)['features'][0]['geometry']['coordinates']
    coords_destino = client.pelias_search(text=ciudad_destino)['features'][0]['geometry']['coordinates']
    result = client.directions(coordinates=[coords_origen, coords_destino], profile='driving-car', format='geojson', language='es')
    distancia = result['features'][0]['properties']['segments'][0]['distance']
    distancia_km = distancia / 1000  # Convertir a kilómetros
    distancia_millas = distancia_km * 0.621371  # Convertir a millas
    return distancia_km, distancia_millas

def obtener_duracion_y_narrativa(ciudad_origen, ciudad_destino, perfil_transporte):
    client = openrouteservice.Client(key=api_key)
    coords_origen = client.pelias_search(text=ciudad_origen)['features'][0]['geometry']['coordinates']
    coords_destino = client.pelias_search(text=ciudad_destino)['features'][0]['geometry']['coordinates']
    result = client.directions(coordinates=[coords_origen, coords_destino], profile=perfil_transporte, format='geojson', language='es')
    
    # Obtener la duración del viaje en segundos
    duracion_segundos = result['features'][0]['properties']['segments'][0]['duration']
    
    # Convertir la duración a minutos
    duracion_minutos = duracion_segundos / 60
    
    # Calcular horas y minutos si la duración es mayor a 60 minutos
    horas = int(duracion_minutos // 60)
    minutos = int(duracion_minutos % 60)
    
    # Obtener la narrativa del viaje en español
    narrativa = []
    for step in result['features'][0]['properties']['segments'][0]['steps']:
        instruccion = step['instruction']
        narrativa.append(instruccion)

    return horas, minutos, narrativa

def mostrar_menu(opciones):
    print("Elige el tipo de medio de transporte:")

    for i, opcion in enumerate(opciones, start=1):
        print(f"{i}. {opcion['nombre']}")

    while True:
        try:
            seleccion = int(input("Ingresa el número correspondiente al medio de transporte: "))
            if 1 <= seleccion <= len(opciones):
                return opciones[seleccion - 1]['perfil']
            else:
                print("Opción inválida. Ingresa un número válido.")
        except ValueError:
            print("Debes ingresar un número.")

def main():
    print("Bienvenido al calculador de viaje.")
    while True:
        ciudad_origen = input("Por favor, ingresa la ciudad de origen (en español): ")
        ciudad_destino = input("Ahora ingresa la ciudad de destino (en español): ")

        try:
            distancia_km, distancia_millas = calcular_distancia(ciudad_origen, ciudad_destino)

            print(f"\nLa distancia entre {ciudad_origen} y {ciudad_destino} es:")
            print(f"- {distancia_km:.2f} kilómetros")
            print(f"- {distancia_millas:.2f} millas")

            perfil_transporte = mostrar_menu(opciones_medios_transporte)
            horas, minutos, narrativa = obtener_duracion_y_narrativa(ciudad_origen, ciudad_destino, perfil_transporte)

            if horas > 0:
                print(f"\nLa duración del viaje es aproximadamente: {horas} horas y {minutos} minutos")
            else:
                print(f"\nLa duración del viaje es aproximadamente: {minutos} minutos")

            print("\nNarrativa del viaje:")
            for i, instruccion in enumerate(narrativa, start=1):
                print(f"{i}. {instruccion}")

        except Exception as e:
            print(f"Error: {e}")

        opcion = input("\n¿Quieres calcular otra ruta? (Presiona 's' para salir, cualquier otra tecla para continuar): ")
        if opcion.lower() == 's':
            print("¡Hasta luego!")
            break

if __name__ == "__main__":
    main()
