import csv

# Archivo CSV donde se almacenan todos los datos de los países
archivo = "data_paises.csv"
campos = ["nombre","poblacion","superficie","continente"] # Encabezados del archivo csv

# Lee el archivo csv, valida los datos y carga los países en una lista
def cargar_paises():
    paises = [] # Lista donde se guardarán los países válidos
    try:
        # Apertura del archivo en modo lectura
        with open(archivo, "r", newline="", encoding="utf-8") as f:
            lector = csv.DictReader(f) # Lee cada fila del archivo como un diccionario
            for fila in lector: # Recorre todas las filas del archivo
                try:
                    # Verifica que nombre y continente no estén vacíos
                    if fila["nombre"].strip() == "" or fila["continente"].strip() == "":
                        raise ValueError
                    # Convierte población y superficie a enteros
                    fila["poblacion"] = int(fila["poblacion"])
                    fila["superficie"] = int(fila["superficie"])

                    # Verifica que los valores numéricos sean positivos
                    if fila["poblacion"] < 0 or fila["superficie"] < 0:
                        raise ValueError
                    
                    paises.append(fila) # Agrega la fila a la lista de países válidos

                # Captura e informa errores de formato de los datos del archivo csv
                except (KeyError, TypeError, ValueError, AttributeError):
                    print(f"Fila ignorada por formato inválido: {fila}")
    # Si el archivo no existe, crea uno vacío
    except FileNotFoundError:
        print("No existe el archivo. Se crea uno vacío.")
        guardar_paises([])

    # Captura errores de lectura del archivo
    except OSError as error:
        print(f"Error: no se pudo leer el archivo: {error}")

    return paises

# Guarda la lista de países en el archivo csv
def guardar_paises(paises):
    try:
        # Apertura del archivo en modo escritura
        with open(archivo, "w", newline="", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=campos) # Configuración del escritor csv
            escritor.writeheader() # Escribe los encabezados
            escritor.writerows(paises) # Escribe todos los registros
        return True

    # Captura errores durante el guardado
    except OSError as error:
        print(f"Error: no se pudo guardar el archivo: {error}")
        return False

# Cargar los nombres de los países válidos
def cargar_paises_validos():
    paises_validos = []

    with open("paises_validos.csv", "r", encoding="utf-8-sig") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            paises_validos.append(fila["nombre"])

    return paises_validos       


#Validar que el país agregado exista
def validar_pais(nombre, paises_validos):

    for pais in paises_validos:
        if nombre.strip().lower() == pais.strip().lower():
            return True

    return False
###################################################################################

# Solicita un número entero mayor o igual a cero
def pedir_entero(mensaje):
    while True:
        try:
            numero = int(input(mensaje))

        # Controla que el usuario ingrese un entero válido
        except ValueError:
            print("Error: ingrese un número entero")
            continue

        # Verifica que el número no sea negativo
        if numero >= 0:
            return numero
        print("Error: el número debe ser mayor o igual a '0'")

# Solicita un texto y controla que no esté vacío
def pedir_texto(mensaje):
    texto = input(mensaje).strip()

    while texto == "":
        print("Error: no puede ingresar un texto vacío")
        texto = input(mensaje).strip()
    return texto

# Busca un país por nombre ignorando mayúsculas y minúsculas
def buscar_pais(paises,nombre):
    for pais in paises:
        # Compara los nombres normalizados
        if pais["nombre"].lower() == nombre.strip().lower():
            return pais
    return None

###################################################################################

# Agrega un nuevo país verificando que no exista previamente
def agregar_pais(paises, paises_validos):
    pais = pedir_texto("Nombre del país: ")

    # Valida que el país exista y que no esté cargado previamente
    while not validar_pais(pais, paises_validos) or buscar_pais(paises, pais) is not None:

        if not validar_pais(pais, paises_validos):
            print("Error: el nombre ingresado no corresponde a un país existente.")

        else:
            print(f"Error: {pais} ya existe")

        pais = pedir_texto("Ingrese otro país: ")

    # Solicita los datos del país a agregar
    poblacion = pedir_entero("Población: ")
    superficie = pedir_entero("Superficie: ")
    continente = pedir_texto("Continente: ").title()

    # Agrega el nuevo país a la lista
    paises.append({"nombre": pais, "poblacion": poblacion, "superficie": superficie, "continente": continente})

    # Guarda los cambios realizados en el archivo csv
    if guardar_paises(paises):
        print("Datos guardados correctamente")

# Actualiza la población y superficie de alguno de los países ya cargados en el csv
def actualizar_pais(paises):
    pais = pedir_texto("Nombre del país: ")

    # Exige un mínimo de 3 caracteres para realizar la búsqueda
    while len(pais.strip()) < 3:
        print("Error: debe ingresar al menos 3 letras")
        pais = pedir_texto("Nombre del país: ")

    # Almacena los países que coinciden con la búsqueda
    coincidencias = []

    for p in paises: # Busca coincidencias parciales en los nombres
        if pais.lower() in p["nombre"].lower():
            coincidencias.append(p)

    # Informa si no se encontraron coincidencias
    if len(coincidencias) == 0:
        print(f"Error: no se encontraron países que coincidan con '{pais}'.")
        return

    # Selecciona automáticamente el único país encontrado
    if len(coincidencias) == 1:
        pais_encontrado = coincidencias[0]
        print(f"País encontrado: {pais_encontrado['nombre']}")

    else:
        # Permite elegir entre varias coincidencias
        print("\nPaíses encontrados:")

        for i in range(len(coincidencias)):
            print(f"{i+1}. {coincidencias[i]['nombre']}")

        opcion = pedir_entero("Seleccione un país: ")

        # Valida que la opción ingresada exista
        while opcion < 1 or opcion > len(coincidencias):
            print("Error: opción inválida")
            opcion = pedir_entero("Seleccione un país: ")

        pais_encontrado = coincidencias[opcion - 1]

    # Solicita los nuevos datos del país
    pais_encontrado["poblacion"] = pedir_entero("Población: ")
    pais_encontrado["superficie"] = pedir_entero("Superficie: ")

    if guardar_paises(paises): # Guarda las modificaciones realizadas
        print(f"{pais_encontrado['nombre']} actualizado correctamente.")

# Busca un país por nombre y muestra los datos encontrados
def buscar_pais_menu(paises):
    pais = pedir_texto("Nombre del país: ")

    # Pide un mínimo de 3 caracteres para realizar la búsqueda
    while len(pais.strip()) < 3:
        print("Error: debe ingresar al menos 3 letras")
        pais = pedir_texto("Nombre del país: ")

    # Almacena los países que coinciden con la búsqueda
    coincidencias = []

    for p in paises: # Busca coincidencias parciales en los nombres
        if pais.lower() in p["nombre"].lower():
            coincidencias.append(p)

    # Informa si no se encontraron coincidencias
    if len(coincidencias) == 0:
        print(f"Error: no se encontraron países que coincidan con '{pais}'.")
        return

    # Selecciona automáticamente el único país encontrado
    if len(coincidencias) == 1:
        pais_encontrado = coincidencias[0]

    else:
        # Permite elegir entre varias coincidencias
        print("Resultado de búsqueda:")
        print("------------------------------")

        for i in range (len(coincidencias)):
            print(f"{i+1}. {coincidencias[i]['nombre']}")
        opcion = pedir_entero("Seleccione un país: ")

        # Valida que la opción ingresada exista
        while opcion < 1 or opcion > len(coincidencias):
            print("Error: opción inválida")
            opcion = pedir_entero("Seleccione un país: ")

        pais_encontrado = coincidencias[opcion - 1]

    # Muestra los datos del país encontrado
    print("------------------------------")
    print("Resultado de búsqueda:")
    print(f"""
    -País: {pais_encontrado['nombre']}
    -Continente: {pais_encontrado['continente']}
    -Población: {pais_encontrado['poblacion']:,}
    -Superficie: {pais_encontrado['superficie']:,} km²
    """)
    print("------------------------------")

# Permite filtrar países según distintos criterios
def filtrar_paises(paises):

    # Muestra las opciones de filtrado
    print("A. Continente.")
    print("B. Rango de población.")
    print("C. Rango de superficie.")

    opcion = input("Elija una opción: ").strip().upper()

    # Valida la opción ingresada
    while not opcion.isalpha() or opcion not in ("A","B","C"):
        print("Error: tiene que ser una letra: A, B o C")
        opcion = input("Elija una opción:").strip().upper()

    # Almacena los países que cumplen el criterio
    filtro = []

    match opcion: 
        case "A":
            # Lista los continentes válidos
            continentes = ["america del sur","america del norte","asia","europa","africa","oceania"]

            continente = pedir_texto("Continente: ").lower()
            continente = continente.replace("á", "a")

            # Valida que el continente exista
            while continente not in continentes:
                print("Error: el continente ingresado no es válido.")
                continente = pedir_texto("Ingrese un continente válido: ").lower()
                continente = continente.replace("á", "a")

            # Filtra los países del continente seleccionado
            for pais in paises:
                nombre_continente = pais["continente"].lower().strip().replace("á", "a")

                if nombre_continente == continente:
                    filtro.append(pais)

        case "B":
            # Solicita el rango de población
            minimo = pedir_entero("Población mínima: ")
            maximo = pedir_entero("Población máxima: ")

            # Verifica que el rango sea válido
            while minimo > maximo:
                print("Error: el mínimo no puede ser un número mayor al máximo.")
                minimo = pedir_entero("Población mínima: ")
                maximo = pedir_entero("Población máxima: ")

            # Filtra los países dentro del rango ingresado
            for pais in paises:
                if pais["poblacion"] >= minimo and pais["poblacion"] <= maximo:
                    filtro.append(pais)

        case "C":
            # Solicita un rango de superficie
            minimo = pedir_entero("Superficie mínima: ")
            maximo = pedir_entero("Superficie máxima: ")

            # Verifica que el rango sea válido
            while minimo > maximo:
                print("Error: el mínimo no puede ser un número mayor al máximo.")
                minimo = pedir_entero("Superficie mínima: ")
                maximo = pedir_entero("Superficie máxima: ")

            # Filtra los países dentro del rango de superficie
            for pais in paises:
                if pais["superficie"] >= minimo and pais["superficie"] <= maximo:
                    filtro.append(pais)

    # Verifica si se encontraron resultados
    if len(filtro) == 0:
        print("No se encontraron países con ese criterio.")
    else:
        # Muestra todos los países que cumplen el filtro
        for pais in filtro:
            print(f"""
            País: {pais['nombre']}
            Continente: {pais['continente']}
            Población: {pais['poblacion']:,}
            Superficie: {pais['superficie']:,} km²
            ------------------------------
            """)

# Ordena los países según el criterio seleccionado
def ordenar_paises(paises):

    # Muestra las opciones de ordenamiento
    print("A. Nombre.")
    print("B. Población.")
    print("C. Superficie.")

    opcion = input("Elija una opción: ").strip().upper()

    # Valida la opción ingresada
    while not opcion.isalpha() or opcion not in ("A","B","C"):
            print("Error: tiene que ser una letra: A, B o C")
            opcion = input("Elija una opción: ").strip().upper()

    match opcion:
        case "A": 
                # Ordena alfabéticamente por nombre (método burbuja)
                for i in range(len(paises)):
                    for j in range(len(paises) - 1):
                        if paises[j]["nombre"].lower() > paises[j+1]["nombre"].lower():
                            auxiliar = paises[j]
                            paises[j] = paises[j+1]
                            paises[j+1] = auxiliar

        case "B":
                # Ordena por población de menor a mayor (método burbuja)
                for i in range(len(paises)):
                    for j in range(len(paises) - 1):
                        if paises[j]["poblacion"] > paises[j+1]["poblacion"]:
                            auxiliar = paises[j]
                            paises[j] = paises[j+1]
                            paises[j+1] = auxiliar

        case "C":
            # Permite elegir sentido del ordenamiento
            orden = input("Ascendente (A) o descendente (D): ").strip().upper()

            # Valida la opción ingresada
            while orden not in ("A", "D"):
                print("Error: elija A o D.")
                orden = input("Ascendente (A) o descendente (D): ").strip().upper()

            # Ordena por superficie según el orden elegido
            for i in range(len(paises)):
                for j in range(len(paises) - 1):

                    if orden == "A": # Orden ascendente
                        if paises[j]["superficie"] > paises[j+1]["superficie"]:
                            auxiliar = paises[j]
                            paises[j] = paises[j+1]
                            paises[j+1] = auxiliar

                    else:
                        # Orden descendente
                        if paises[j]["superficie"] < paises[j+1]["superficie"]:
                            auxiliar = paises[j]
                            paises[j] = paises[j+1]
                            paises[j+1] = auxiliar

    # Muestra los países ordenados
    print("\nPaíses ordenados:")

    for pais in paises:
        print(f"""
        País: {pais['nombre']}
        Continente: {pais['continente']}
        Población: {pais['poblacion']:,}
        Superficie: {pais['superficie']:,} km²
        ------------------------------
        """)

# Calcula y muestra estadísticas de los países almacenados
def mostrar_estadisticas(paises):

    # Verifica que existan países cargados
    if len(paises) == 0:
        print("No hay países para mostrar estadísticas.")
        return

    # Inicializa variables para los cálculos
    mayor = paises[0]
    menor = paises[0]
    suma_poblacion = 0
    suma_superficie = 0
    cantidad_continentes = {} # Almacena la cantidad de países por continente

    # Recorre todos los países para calcular estadísticas
    for pais in paises:

        # Busca el país con mayor población
        if pais["poblacion"] > mayor["poblacion"]:
            mayor = pais

        # Busca el país con menor población
        if pais["poblacion"] < menor["poblacion"]:
            menor = pais

        # Acumula población y superficie
        suma_poblacion += pais["poblacion"]
        suma_superficie += pais["superficie"]

        # Obtiene el nombre normalizado del continente
        continente = pais["continente"].strip().capitalize()

        # Cuenta países por continente
        if continente in cantidad_continentes:
            cantidad_continentes[continente] += 1
        else:
            cantidad_continentes[continente] = 1

    # Calcula los promedios generales
    promedio_poblacion = suma_poblacion / len(paises)
    promedio_superficie = suma_superficie / len(paises)

    # Muestra las estadísticas obtenidas
    print("\nESTADÍSTICAS DE PAÍSES")
    print("------------------------------")

    print(f"Mayor población: {mayor['nombre']} ({mayor['poblacion']:,})")
    print(f"Menor población: {menor['nombre']} ({menor['poblacion']:,})")

    print(f"Promedio de población: {promedio_poblacion:,.2f}")
    print(f"Promedio de superficie: {promedio_superficie:,.2f} km²")

    # Muestra la cantidad de países agrupados por continente
    print("\nCantidad de países por continente:")

    for continente in cantidad_continentes:
        print(f"- {continente}: {cantidad_continentes[continente]}")

###################################################################################

# Muestra las opciones disponibles del menú
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

# Función principal del programa
def main():
    paises = cargar_paises() # Carga los países almacenados en el archivo
    paises_validos = cargar_paises_validos()   #Carga los países válidos

    while True: # Se repite el programa hasta que la opción 7 sea ingresada
        menu()
        opcion = input("Ingrese una opcion (1-7): ").strip()

        # Valida que la opción sea un número entero entre 1 y 7
        while not opcion.isdigit() or int(opcion) < 1 or int(opcion) > 7:
            print("Error: tiene que ser un digito entre 1 y 7.")
            opcion = input("Ingrese una opcion (1-7): ")

        # Ejecuta la acción seleccionada por el usuario
        match opcion:
            case"1":
                agregar_pais(paises, paises_validos)
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
                # Guarda todos los cambios antes de finalizar el programa
                guardar_paises(paises)
                break

main() # Ejecuta la función principal del programa

# Código de prueba utilizado durante el desarrollo
# if __name__ == "__main__":

# print(pedir_entero("poblacion: "))
# print(pedir_texto("nombre: "))
# paises= cargar_paises()
# print(buscar_pais(paises, "argentina"))