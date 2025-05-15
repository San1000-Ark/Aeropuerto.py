# Diccionarios globales
rute_price = {
    "Bogota - Medellin": 230000,
    "Bogota - España": 4200000
}

luggage_cost = {
    20: 50000,
    30: 70000,
    50: 110000
}

reservas = []
contador_id = 1

def calcular_costo_equipaje(peso):
    if peso > 50:
        return "No admitido", 0
    for limite in sorted(luggage_cost):
        if peso <= limite:
            return "Aceptado", luggage_cost[limite]
    return "Error", 0

def validar_equipaje_mano(lleva, peso):
    if lleva.lower() == "sí" and peso > 13:
        return "Rechazado"
    elif lleva.lower() == "sí":
        return "Aceptado"
    else:
        return "No lleva"

def registrar_reserva(nombre, destino, tipo_viaje, fecha, peso_principal, lleva_mano, peso_mano):
    global contador_id
    id_compra = f"COMP{contador_id:04d}"
    contador_id += 1

    precio_base = rute_price.get(destino, 0)
    estado_principal, costo_adicional = calcular_costo_equipaje(peso_principal)
    estado_mano = validar_equipaje_mano(lleva_mano, peso_mano)
    total = precio_base + costo_adicional

    reserva = {
        "id": id_compra,
        "nombre": nombre,
        "destino": destino,
        "tipo": tipo_viaje,
        "fecha": fecha,
        "equipaje_principal": estado_principal,
        "equipaje_mano": estado_mano,
        "total": total
    }
    reservas.append(reserva)
    return reserva

def imprimir_resumen(reserva):
    print("RESUMEN DE RESERVA")
    print(f"ID: {reserva['id']}")
    print(f"Nombre: {reserva['nombre']}")
    print(f"Destino: {reserva['destino']}")
    print(f"Fecha: {reserva['fecha']}")
    print(f"Estado equipaje principal: {reserva['equipaje_principal']}")
    print(f"Estado equipaje de mano: {reserva['equipaje_mano']}")
    print(f"Costo total: ${reserva['total']:,.0f}")

def consultar_reserva(id_busqueda):
    for r in reservas:
        if r["id"] == id_busqueda:
            return r
    return None

def reporte_admin(fecha_especifica=None):
    total = sum(r["total"] for r in reservas)
    total_fecha = sum(r["total"] for r in reservas if r["fecha"] == fecha_especifica) if fecha_especifica else None
    total_pasajeros = len(reservas)
    nacionales = sum(1 for r in reservas if r["tipo"] == "nacional")
    internacionales = sum(1 for r in reservas if r["tipo"] == "internacional")

    print("\n--- REPORTE ADMINISTRATIVO ---")
    print(f"Total recaudado: ${total:,.0f}")
    if fecha_especifica:
        print(f"Total recaudado en {fecha_especifica}: ${total_fecha:,.0f}")
    print(f"Total pasajeros: {total_pasajeros}")
    print(f"Nacionales: {nacionales}")
    print(f"Internacionales: {internacionales}")

def menu():
    while True:
        print("1. Registrar nueva reserva")
        print("2. Consultar reserva por ID")
        print("3. Reporte administrativo")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre del pasajero: ")
            print("Rutas disponibles:")
            for ruta in rute_price:
                print(f"- {ruta}")
            destino = input("Ruta exacta: ")
            tipo_viaje = input("Tipo de viaje (nacional/internacional): ").lower().strip()
            fecha = input("Fecha del viaje (YYYY-MM-DD): ")
            peso_principal = float(input("Peso del equipaje principal (kg): "))
            lleva_mano = input("¿Lleva equipaje de mano? (sí/no): ")
            peso_mano = float(input("Peso del equipaje de mano (kg): ")) if lleva_mano.lower() == "sí" else 0

            reserva = registrar_reserva(nombre, destino, tipo_viaje, fecha, peso_principal, lleva_mano, peso_mano)
            imprimir_resumen(reserva)

        elif opcion == "2":
            id_busqueda = input("Ingrese el ID de compra: ")
            reserva = consultar_reserva(id_busqueda)
            if reserva:
                imprimir_resumen(reserva)
            else:
                print("Reserva no encontrada.")

        elif opcion == "3":
            fecha = input("Ingrese una fecha específica (YYYY-MM-DD) o deje en blanco para todo: ")
            reporte_admin(fecha if fecha else None)

        elif opcion == "4":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida. Intente de nuevo.")


menu()
