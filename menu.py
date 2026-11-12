import csv

archivo = "data_paises.csv"
campos = ["nombre","poblacion","superficie","continente"]

def cargar_paises():
    paises = []
    try:
        with open(archivo, "r", newline="", encoding="utf-8") as f:
            lector = csv.DictReader(f)
            for fila in lector:
                try:
                    if fila["nombre"].strip() == "" or fila["continente"].strip() == "":
                        raise ValueError
                    fila["poblacion"] = int(fila["poblacion"])
                    fila["superficie"] = int(fila["superficie"])

                    if fila["poblacion"] < 0 or fila["superficie"] < 0:
                        raise ValueError
                    
                    paises.append(fila)

                except (KeyError, TypeError, ValueError, AttributeError):
                    print(f"Fila ignorada por formato inválido: {fila}")

    except FileNotFoundError:
        print("No existe el archivo. Se crea uno vacío.")
        guardar_paises([])

    except OSError as error:
        print(f"Error: no se pudo leer el archivo: {error}")
    return paises


def guardar_paises(paises):
    try:
        with open(archivo, "w", newline="", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(paises)
        return True
    except OSError as error:
        print(f"Error: no se pudo guardar el archivo: {error}")
        return False
    
###################################################################################

def pedir_entero(mensaje):
    while True:
        try:
            numero = int(input(mensaje))
        except ValueError:
            print("Error: ingrese un número entero")
            continue

        if numero >= 0:
            return numero
        print("Error: el número debe ser mayor o igual a '0'")

def pedir_texto(mensaje):
    texto = input(mensaje).strip()

    while texto == "":
        print("Error: no puede ingresar un texto vacío")
        texto = input(mensaje).strip()
    return texto

def buscar_pais(paises,nombre):
    for pais in paises:
        if pais["nombre"].lower() == nombre.strip().lower():
            return pais
    return None

###################################################################################

def agregar_pais(paises):
    pais = pedir_texto("Nombre del país: ")

    while buscar_pais(paises,pais) is not None:
        print(f"Error: {pais} ya existe")
        pais = pedir_texto("Nombre del país: ")

    poblacion = pedir_entero("Población: ")
    superficie = pedir_entero("Superficie: ")
    continente = pedir_texto("Continente: ").title()

    paises.append({"nombre": pais, "poblacion": poblacion, "superficie": superficie, "continente": continente})

    if guardar_paises(paises):
        print("Datos guardados correctamente")

def actualizar_pais(paises):
    pais = pedir_texto("Nombre del país: ")

    while len(pais.strip()) < 3:
        print("Error: debe ingresar al menos 3 letras")
        pais = pedir_texto("Nombre del país: ")

    coincidencias = []

    for p in paises:
        if pais.lower() in p["nombre"].lower():
            coincidencias.append(p)

    if len(coincidencias) == 0:
        print(f"Error: no se encontraron países con '{pais}'.")
        return

    if len(coincidencias) == 1:
        pais_encontrado = coincidencias[0]
        print(f"País encontrado: {pais_encontrado['nombre']}")

    else:
        print("\nPaíses encontrados:")

        for i in range(len(coincidencias)):
            print(f"{i+1}. {coincidencias[i]['nombre']}")

        opcion = pedir_entero("Seleccione un país: ")

        while opcion < 1 or opcion > len(coincidencias):
            print("Error: opción inválida")
            opcion = pedir_entero("Seleccione un país: ")

        pais_encontrado = coincidencias[opcion - 1]

    pais_encontrado["poblacion"] = pedir_entero("Población: ")
    pais_encontrado["superficie"] = pedir_entero("Superficie: ")

    if guardar_paises(paises):
        print(f"{pais_encontrado['nombre']} actualizado correctamente.")

def buscar_pais_menu(paises):
    pais = pedir_texto("Nombre del país: ")

    while len(pais.strip()) < 3:
        print("Error: debe ingresar al menos 3 letras")
        pais = pedir_texto("Nombre del país: ")

    coincidencias = []

    for p in paises:
        if pais.lower() in p["nombre"].lower():
            coincidencias.append(p)

    if len(coincidencias) == 0:
        print(f"Error: no se encontraron países con '{pais}'.")
        return

    if len(coincidencias) == 1:
        pais_encontrado = coincidencias[0]

    else:
        print("Resultado de búsqueda:")
        print("------------------------------")

        for i in range (len(coincidencias)):
            print(f"{i+1}. {coincidencias[i]['nombre']}")
        opcion = pedir_entero("Seleccione un país: ")

        while opcion < 1 or opcion > len(coincidencias):
            print("Error: opción inválida")
            opcion = pedir_entero("Seleccione un país: ")

        pais_encontrado = coincidencias[opcion - 1]

    print("------------------------------")
    print("Resultado de búsqueda:")
    print(f"""
    -País: {pais_encontrado['nombre']}
    -Continente: {pais_encontrado['continente']}
    -Población: {pais_encontrado['poblacion']:,}
    -Superficie: {pais_encontrado['superficie']:,} km²
    """)
    print("------------------------------")

def filtrar_paises(paises):

    print("A. Continente.")
    print("B. Rango de población.")
    print("C. Rango de superficie.")

    opcion = input("Elija una opción: ").strip().upper()

    while not opcion.isalpha() or opcion not in ("A","B","C"):
        print("Error: tiene que ser una letra: A, B o C")
        opcion = input("Elija una opción:").strip().upper()

    filtro = []

    match opcion: 
        case "A":
            
            continentes = ["america", "asia", "europa", "africa", "oceania"]

            continente = pedir_texto("Continente: ").lower()
            continente = continente.replace("á", "a")

            while continente not in continentes:
                print("Error: el continente ingresado no es válido.")
                continente = pedir_texto("Ingrese un continente válido: ").lower()
                continente = continente.replace("á", "a")

            for pais in paises:
                nombre_continente = pais["continente"].lower().strip().replace("á", "a")

                if nombre_continente == continente:
                    filtro.append(pais)

        case "B":
            minimo = pedir_entero("Población mínima: ")
            maximo = pedir_entero("Población máxima: ")

            while minimo > maximo:
                print("Error: el mínimo no puede ser un número mayor al máximo.")
                minimo = pedir_entero("Población mínima: ")
                maximo = pedir_entero("Población máxima: ")

            for pais in paises:
                if pais["poblacion"] >= minimo and pais["poblacion"] <= maximo:
                    filtro.append(pais)

        case "C":
            minimo = pedir_entero("Superficie mínima: ")
            maximo = pedir_entero("Superficie máxima: ")

            while minimo > maximo:
                print("Error: el mínimo no puede ser un número mayor al máximo.")
                minimo = pedir_entero("Superficie mínima: ")
                maximo = pedir_entero("Superficie máxima: ")

            for pais in paises:
                if pais["superficie"] >= minimo and pais["superficie"] <= maximo:
                    filtro.append(pais)

    if len(filtro) == 0:
        print("No se encontraron países con ese criterio.")
    else:
        for pais in filtro:
            print(f"""
            País: {pais['nombre']}
            Continente: {pais['continente']}
            Población: {pais['poblacion']:,}
            Superficie: {pais['superficie']:,} km²
            ------------------------------
            """)

def ordenar_paises(paises):

    print("A. Nombre.")
    print("B. Población.")
    print("C. Superficie.")

    opcion = input("Elija una opción: ").strip().upper()
    
    while not opcion.isalpha() or opcion not in ("A","B","C"):
            print("Error: tiene que ser una letra: A, B o C")
            opcion = input("Elija una opción: ").strip().upper()

    match opcion:
        case "A": 
                for i in range(len(paises)):
                    for j in range(len(paises) - 1):
                        if paises[j]["nombre"].lower() > paises[j+1]["nombre"].lower():
                            auxiliar = paises[j]
                            paises[j] = paises[j+1]
                            paises[j+1] = auxiliar

        case "B":
                for i in range(len(paises)):
                    for j in range(len(paises) - 1):
                        if paises[j]["poblacion"] > paises[j+1]["poblacion"]:
                            auxiliar = paises[j]
                            paises[j] = paises[j+1]
                            paises[j+1] = auxiliar

        case "C":
            orden = input("Ascendente (A) o descendente (D): ").strip().upper()

            while orden not in ("A", "D"):
                print("Error: elija A o D.")
                orden = input("Ascendente (A) o descendente (D): ").strip().upper()

            for i in range(len(paises)):
                for j in range(len(paises) - 1):

                    if orden == "A":
                        if paises[j]["superficie"] > paises[j+1]["superficie"]:
                            auxiliar = paises[j]
                            paises[j] = paises[j+1]
                            paises[j+1] = auxiliar

                    else:
                        if paises[j]["superficie"] < paises[j+1]["superficie"]:
                            auxiliar = paises[j]
                            paises[j] = paises[j+1]
                            paises[j+1] = auxiliar

    print("\nPaíses ordenados:")

    for pais in paises:
        print(f"""
        País: {pais['nombre']}
        Continente: {pais['continente']}
        Población: {pais['poblacion']:,}
        Superficie: {pais['superficie']:,} km²
        ------------------------------
        """)
    
def mostrar_estadisticas(paises):

    if len(paises) == 0:
        print("No hay países para mostrar estadísticas.")
        return

    mayor = paises[0]
    menor = paises[0]
    suma_poblacion = 0
    suma_superficie = 0
    cantidad_continentes = {}

    for pais in paises:

        if pais["poblacion"] > mayor["poblacion"]:
            mayor = pais

        if pais["poblacion"] < menor["poblacion"]:
            menor = pais

        suma_poblacion += pais["poblacion"]
        suma_superficie += pais["superficie"]

        continente = pais["continente"].strip().capitalize()

        if continente in cantidad_continentes:
            cantidad_continentes[continente] += 1
        else:
            cantidad_continentes[continente] = 1

    promedio_poblacion = suma_poblacion / len(paises)
    promedio_superficie = suma_superficie / len(paises)

    print("\nESTADÍSTICAS DE PAÍSES")
    print("------------------------------")

    print(f"Mayor población: {mayor['nombre']} ({mayor['poblacion']:,})")
    print(f"Menor población: {menor['nombre']} ({menor['poblacion']:,})")

    print(f"Promedio de población: {promedio_poblacion:,.2f}")
    print(f"Promedio de superficie: {promedio_superficie:,.2f} km²")

    print("\nCantidad de países por continente:")

    for continente in cantidad_continentes:
        print(f"- {continente}: {cantidad_continentes[continente]}")

###################################################################################

def menu():
    print("\n===== GESTIÓN DE PAÍSES =====")
    print("1. Agregar país")
    print("2. Actualizar población y superficie")
    print("3. Buscar país por nombre")
    print("4. Filtrar países")
    print("5. Ordenar países")
    print("6. Mostrar estadísticas")
    print("7. Salir")
    print("")

def main():
    paises = cargar_paises()

    while True:
        menu()
        opcion = input("Ingrese una opcion (1-7): ").strip()
        while not opcion.isdigit() or int(opcion) < 1 or int(opcion) > 7:
            print("Error: tiene que ser un digito entre 1 y 7.")
            opcion = input("Ingrese una opcion (1-7): ")

        match opcion:
            case"1":
                agregar_pais(paises)
            case "2":
                actualizar_pais(paises)
            case "3":
                buscar_pais_menu(paises)
            case "4":
                filtrar_paises(paises)
            case "5":
                ordenar_paises(paises)
            case "6":
                mostrar_estadisticas(paises)
            case "7":
                print("¡Hasta luego!")
                guardar_paises(paises)
                break

main()


# if __name__ == "__main__":

# print(pedir_entero("poblacion: "))
# print(pedir_texto("nombre: "))
# paises= cargar_paises()
# print(buscar_pais(paises, "argentina"))
