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
    continente = pedir_texto("Continente: ")

    paises.append({"nombre": pais, "poblacion": poblacion, "superficie": superficie, "continente": continente})

    if guardar_paises(paises):
        print("Datos guardados correctamente")

def actualizar_pais(paises):
    pais = pedir_texto("Nombre del país: ")
    pais_encontrado = buscar_pais(paises, pais)

    if pais_encontrado is None:
        print(f"Error: {pais} no existe en la lista")
        return

    pais_encontrado["poblacion"] = pedir_entero("Poblacion: ")
    pais_encontrado["superficie"] = pedir_entero("Superficie: ")

    print("País actualizado correctamente.")
    
def buscar_pais_menu(paises):
    pais = pedir_texto("Nombre del país: ")
    pais_encontrado = buscar_pais(paises, pais)

    if pais_encontrado is None:
        print(f"Error: {pais} no existe en la lista")
        return

    print("\nResultado de la busqueda:")
    print(f"""
    País: {pais_encontrado['nombre']}
    Continente: {pais_encontrado['continente']}
    Población: {pais_encontrado['poblacion']:,}
    Superficie: {pais_encontrado['superficie']:,} km²
    """)


def filtrar_paises(paises):
    pass

def ordenar_paises(paises):
    pass

def mostrar_estadisticas(paises):
    pass

def menu():
    print("\n===== GESTIÓN DE PAÍSES =====")
    print("1. Agregar país")
    print("2. Actualizar población y superficie")
    print("3. Buscar país por nombre")
    print("4. Filtrar países")
    print("5. Ordenar países")
    print("6. Mostrar estadísticas")
    print("7. Salir")

def main():
    paises = cargar_paises()

    while True:
        menu()
        opcion = input("Ingrese una opcion (1-7): ")
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