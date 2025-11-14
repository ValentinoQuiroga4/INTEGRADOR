# --- Importación de Módulos ---
import csv  # Módulo para leer y escribir archivos CSV (Valores Separados por Comas)
import os   # Módulo para interactuar con el sistema operativo (usado para limpiar la pantalla)

# --- Constantes Globales ---
# Definir el nombre del archivo CSV como una constante global
# Facilita cambiar el nombre del archivo en un solo lugar.
ARCHIVO_CSV = "paises.csv"

# --- Definición de Funciones de Ayuda o Auxiliares ---

def limpiar_pantalla():
    # Limpia la pantalla de la consola para mejorar la legibilidad.
    # Limpia la consola cada vez que el menú se repite o se ejecuta una opción
    os.system('cls' if os.name == 'nt' else 'clear')

def validar_entero(mensaje):
    # Solicita un número entero al usuario y lo valida.
    # Repite la solicitud (bucle while True) hasta que se ingrese un valor válido.
    # 
    # Args:
    #     mensaje (str): El texto a mostrar al usuario para pedir el dato.
    #     
    # Returns:
    #     int: El número entero validado.
    while True:
        try:
            # Intenta convertir la entrada del usuario a un entero
            valor = int(input(mensaje))
            return valor  # Si tiene éxito, devuelve el valor
        except ValueError:
            # Si la conversión falla (ej. "abc" o "1.5"), se captura el error
            print("Error: Por favor, ingrese un número entero válido.")

# --- Definición de Funciones Principales ---

def cargar_datos(archivo):
    # Carga los datos de países desde un archivo CSV.
    # (Requisito: Lectura desde CSV)
    # 
    # Utiliza una lista de diccionarios (Estructura de Datos principal).
    # (Requisito: Listas, Diccionarios)
    # 
    # Controla errores de formato y archivo no encontrado.
    # (Requisito: Validaciones)
    #
    # Returns:
    #     list: Una lista de diccionarios, donde cada diccionario representa un país.
    #           Retorna None si el archivo no se encuentra o hay un error fatal.
    #           Retorna [] si las columnas del CSV son incorrectas.
    
    paises = []  # Inicializa la lista vacía donde se guardarán los datos
    
    # (Manejo de Archivos y Errores)
    try:
        # 'with open' asegura que el archivo se cierre automáticamente
        # 'encoding='utf-8'' es importante para manejar caracteres especiales (ej. tildes)
        with open(archivo, mode='r', encoding='utf-8') as f:
            
            # (Uso de Diccionarios)
            # csv.DictReader lee el archivo y usa la primera fila (cabecera)
            # como las 'claves' para los diccionarios de cada fila siguiente.
            lector_csv = csv.DictReader(f)
            
            # Itera sobre cada fila leída por el DictReader
            for fila in lector_csv:
                try:
                    # (Validación de Datos)
                    # Los datos leídos del CSV son siempre 'str' (texto).
                    # Debemos convertirlos al tipo de dato correcto (int).
                    fila['poblacion'] = int(fila['poblacion'])
                    fila['superficie'] = int(fila['superficie'])
                    
                    # Si las conversiones son exitosas, añade el diccionario a la lista
                    paises.append(fila)
                    
                except ValueError:
                    # (Requisito: Controlar errores de formato en el CSV)
                    # Ocurre si 'poblacion' o 'superficie' no son números (ej. "N/A")
                    print(f"Error de formato en línea: {fila} - Se omitirá esta línea.")
                except KeyError:
                    # Ocurre si el CSV no tiene las columnas esperadas.
                    print(f"Error: El CSV debe tener las columnas 'nombre', 'poblacion', 'superficie', 'continente'.")
                    return [] # Retorna lista vacía (error de estructura)
                    
    except FileNotFoundError:
        # (Requisito: Manejo básico de errores)
        # El error más común: el archivo no está en la misma carpeta.
        print(f"Error: No se encontró el archivo '{archivo}'.")
        return None # Retorna 'None' para indicar un fallo en la carga
    except Exception as e:
        # Captura cualquier otro error inesperado (ej. permisos de lectura)
        print(f"Error inesperado al leer el archivo: {e}")
        return None
        
    # Si todo fue bien, devuelve la lista completa de países
    return paises

def mostrar_paises(lista_paises):
    # Muestra una lista de países (que es una lista de diccionarios)
    # en un formato tabular bien alineado.
    # 
    # Args:
    #     lista_paises (list): La lista de diccionarios de países a mostrar.
    # (Validación)
    if not lista_paises:  # Verifica si la lista está vacía
        print("No se encontraron países que coincidan con los criterios.")
        return

    # Imprime los encabezados de la tabla
    # (Formato de 'f-strings' para alineación)
    # :<30  -> Alineado a la izquierda, 30 caracteres de ancho
    # :>15  -> Alineado a la derecha, 15 caracteres de ancho
    # :>18  -> Alineado a la derecha, 18 caracteres de ancho
    print(f"\n{'País':<30} | {'Continente':<15} | {'Población':>15} | {'Superficie (km²)':>18}")
    print("-" * 84) # Imprime una línea separadora
    
    # Itera sobre cada diccionario 'pais' en la lista
    for pais in lista_paises:
        # (Formato de 'f-strings' para números)
        # :>15, -> Alineado a la derecha, 15 de ancho, con separador de miles (,)
        print(f"{pais['nombre']:<30} | {pais['continente']:<15} | {pais['poblacion']:>15,} | {pais['superficie']:>18,}")

def buscar_pais_por_nombre(lista_paises):
    # (Requisito: Funcionalidad - Buscar un país por nombre)
    # Permite al usuario ingresar un término de búsqueda y muestra
    # los países cuyo nombre contenga ese término (parcial o exacto).
    # 
    # Args:
    #     lista_paises (list): La lista completa de países.
    limpiar_pantalla()
    print("--- Búsqueda de País por Nombre ---")
    nombre_buscado = input("Ingrese el nombre (o parte del nombre) del país a buscar: ").lower()
    
    if not nombre_buscado: # Si el usuario solo presiona Enter
        print("Búsqueda cancelada.")
        return

    # (Uso de Listas por Comprensión para Filtrado)
    # Esta es una forma "Pythonica" y eficiente de crear una nueva lista.
    # Es equivalente a:
    # encontrados = []
    # for pais in lista_paises:
    #     if nombre_buscado in pais['nombre'].lower():
    #         encontrados.append(pais)
    #
    # .lower() se usa en ambos lados para hacer la búsqueda insensible a mayúsculas.
    encontrados = [pais for pais in lista_paises if nombre_buscado in pais['nombre'].lower()]
    
    # (Validación de resultados)
    if not encontrados:
        print(f"Error: No se encontró ningún país con el nombre '{nombre_buscado}'.")
    else:
        # Reutiliza la función de mostrar para imprimir los resultados
        mostrar_paises(encontrados)

def filtrar_paises(lista_paises):
    # (Requisito: Funcionalidad - Filtrar países)
    # Muestra un submenú para aplicar diferentes filtros a la lista.
    # 
    # Args:
    #     lista_paises (list): La lista completa de países.
    limpiar_pantalla()
    print("--- Filtrar Países ---")
    print("1. Filtrar por Continente")
    print("2. Filtrar por Rango de Población")
    print("3. Filtrar por Rango de Superficie")
    opcion = input("Seleccione una opción de filtro: ")

    if opcion == '1':
        # (Requisito: Filtrar por Continente)
        # .lower() para la entrada y .capitalize() para que coincida (ej. "américa" -> "América")
        continente = input("Ingrese el nombre del continente: ").lower().capitalize()
        
        # Filtra usando una lista por comprensión
        filtrados = [pais for pais in lista_paises if pais['continente'] == continente]
        
        if not filtrados:
            print(f"No se encontraron países en el continente '{continente}' o el continente no existe.")
        else:
            mostrar_paises(filtrados)

    elif opcion == '2':
        # (Requisito: Filtrar por Rango de Población)
        print("Ingrese el rango de población:")
        # Reutiliza la función de validación
        min_pob = validar_entero("Población mínima (0 si no hay mínimo): ")
        max_pob = validar_entero(f"Población máxima (ej. 100000000): ")
        
        # Filtra usando una lista por comprensión con una condición de rango
        filtrados = [pais for pais in lista_paises if min_pob <= pais['poblacion'] <= max_pob]
        mostrar_paises(filtrados)

    elif opcion == '3':
        # (Requisito: Filtrar por Rango de Superficie)
        print("Ingrese el rango de superficie (en km²):")
        min_sup = validar_entero("Superficie mínima (0 si no hay mínimo): ")
        max_sup = validar_entero(f"Superficie máxima (ej. 500000): ")
        
        filtrados = [pais for pais in lista_paises if min_sup <= pais['superficie'] <= max_sup]
        mostrar_paises(filtrados)
        
    else:
        print("Opción inválida.")

def ordenar_paises(lista_paises):
    # (Requisito: Funcionalidad - Ordenar países)
    # Ordena la lista de países por un criterio (nombre, población, superficie)
    # y en un orden (ascendente o descendente) seleccionados por el usuario.
    # 
    # Args:
    #     lista_paises (list): La lista completa de países.
    limpiar_pantalla()
    print("--- Ordenar Países ---")
    print("Seleccione el criterio de ordenamiento:")
    print("1. Nombre")
    print("2. Población")
    print("3. Superficie")
    criterio = input("Opción: ")

    if criterio not in ['1', '2', '3']:
        print("Criterio inválido.")
        return

    print("\nSeleccione el orden:")
    print("1. Ascendente (A-Z, 0-9)")
    print("2. Descendente (Z-A, 9-0)")
    orden = input("Opción: ")

    if orden not in ['1', '2']:
        print("Orden inválido.")
        return

    # Convierte la opción de orden ('1' o '2') a un booleano (True/False)
    # 'reverse=True' significa orden descendente.
    descendente = (orden == '2')

    # (Uso de 'sorted' y 'lambda' para ordenar listas de diccionarios)
    # 'sorted()' es una función que devuelve una NUEVA lista ordenada.
    # 'key=lambda p: ...' le dice a 'sorted' CÓMO ordenar.
    # 'lambda p:' es una mini-función anónima. 'p' representa cada
    # elemento (cada diccionario de país) en la lista.
    # 'p['nombre']' le dice a 'sorted' que ordene los diccionarios
    # basándose en el valor asociado a la clave 'nombre'.
    
    if criterio == '1':
        # (Requisito: Ordenar por Nombre)
        paises_ordenados = sorted(lista_paises, key=lambda p: p['nombre'], reverse=descendente)
        print("\n--- Países ordenados por Nombre ---")
    elif criterio == '2':
        # (Requisito: Ordenar por Población)
        paises_ordenados = sorted(lista_paises, key=lambda p: p['poblacion'], reverse=descendente)
        print("\n--- Países ordenados por Población ---")
    else: # criterio == '3'
        # (Requisito: Ordenar por Superficie)
        paises_ordenados = sorted(lista_paises, key=lambda p: p['superficie'], reverse=descendente)
        print("\n--- Países ordenados por Superficie ---")

    # Muestra la nueva lista ordenada
    mostrar_paises(paises_ordenados)

def mostrar_estadisticas(lista_paises):
    # (Requisito: Funcionalidad - Mostrar estadísticas)
    # Calcula y muestra estadísticas clave sobre el conjunto de datos.
    # 
    # Args:
    #     lista_paises (list): La lista completa de países.
    if not lista_paises:
        print("No hay datos cargados para mostrar estadísticas.")
        return

    limpiar_pantalla()
    print("--- Estadísticas Globales ---")

    # 1. País con mayor y menor población
    # (Uso de 'max' y 'min' con 'lambda')
    # Al igual que 'sorted', 'max' y 'min' pueden usar una 'key'
    # para encontrar el diccionario con el valor máximo/mínimo.
    pais_mayor_pob = max(lista_paises, key=lambda p: p['poblacion'])
    pais_menor_pob = min(lista_paises, key=lambda p: p['poblacion'])
    print(f"\nPaís con Mayor Población: {pais_mayor_pob['nombre']} ({pais_mayor_pob['poblacion']:,})")
    print(f"País con Menor Población: {pais_menor_pob['nombre']} ({pais_menor_pob['poblacion']:,})")

    # 2. Promedio de población y superficie
    # (Uso de Generadores y 'sum')
    # 'sum(p['poblacion'] for p in lista_paises)' es una forma eficiente
    # de sumar todos los valores de 'poblacion' en la lista.
    total_poblacion = sum(p['poblacion'] for p in lista_paises)
    total_superficie = sum(p['superficie'] for p in lista_paises)
    cantidad_paises = len(lista_paises) # Obtiene el total de elementos
    
    # Evita la división por cero si la lista estuviera vacía (aunque ya lo chequeamos)
    if cantidad_paises > 0:
        promedio_poblacion = total_poblacion / cantidad_paises
        promedio_superficie = total_superficie / cantidad_paises
        
        # :.0f -> 0 decimales, :.2f -> 2 decimales
        print(f"\nPromedio de Población: {promedio_poblacion:,.0f}")
        print(f"Promedio de Superficie: {promedio_superficie:,.2f} km²")
        print(f"Superficie Total: {total_superficie:,.0f} km²")
        print(f"Población Total: {total_poblacion:,.0f}")

    # 3. Cantidad de países por continente
    # (Uso de Diccionarios como contadores)
    print("\nCantidad de Países por Continente:")
    conteo_continentes = {}  # Crea un diccionario vacío para contar
    
    # Itera sobre cada país
    for pais in lista_paises:
        continente = pais['continente']
        if continente in conteo_continentes:
            # Si el continente ya está en el contador, suma 1
            conteo_continentes[continente] += 1
        else:
            # Si es la primera vez que ve este continente, lo añade al contador con 1
            conteo_continentes[continente] = 1
            
    # Muestra los resultados del conteo
    # 'sorted(conteo_continentes.items())' ordena los resultados alfabéticamente
    # por el nombre del continente (la clave del diccionario).
    for continente, cantidad in sorted(conteo_continentes.items()):
        print(f"  - {continente}: {cantidad} países")

def main():
    # Función principal (main) del programa.
    # (Modularización: 'main' actúa como el controlador principal)
    # 
    # 1. Carga los datos *una sola vez* al inicio.
    # 2. Muestra el menú principal en un bucle.
    # 3. Llama a la función correspondiente según la opción del usuario.
    
    # --- Carga Inicial de Datos ---
    # Llama a la función de carga
    paises = cargar_datos(ARCHIVO_CSV)
    
    # (Validación Crítica)
    # Si 'cargar_datos' devolvió 'None' (ej. archivo no encontrado),
    # el programa no puede continuar.
    if paises is None:
        print("No se pudieron cargar los datos. El programa se cerrará.")
        return  # Termina la función 'main' y el programa

    print(f"Se cargaron {len(paises)} países correctamente.")
    input("Presione Enter para continuar...") # Pausa para que el usuario lea el mensaje

    # --- Bucle Principal del Menú ---
    while True:
        limpiar_pantalla()
        print("=====================================================")
        print("   Gestión de Datos de Países - Programación 1 UTN")
        print("=====================================================")
        print("1. Buscar país por nombre")
        print("2. Filtrar países (por continente, población, etc.)")
        print("3. Ordenar países (por nombre, población, etc.)")
        print("4. Mostrar estadísticas")
        print("5. Mostrar todos los países")
        print("6. Salir")
        print("-----------------------------------------------------")
        
        opcion = input("Seleccione una opción: ") # Pide la opción al usuario

        # (Estructura Condicional - if/elif/else)
        # Dirige el flujo del programa a la función correcta
        
        if opcion == '1':
            buscar_pais_por_nombre(paises)
        elif opcion == '2':
            filtrar_paises(paises)
        elif opcion == '3':
            ordenar_paises(paises)
        elif opcion == '4':
            mostrar_estadisticas(paises)
        elif opcion == '5':
            # Opción para ver la lista completa
            limpiar_pantalla()
            print("--- Listado Completo de Países (ordenados por nombre) ---")
            # Muestra los países ordenados por nombre por defecto para legibilidad
            paises_ordenados_nombre = sorted(paises, key=lambda p: p['nombre'])
            mostrar_paises(paises_ordenados_nombre)
        elif opcion == '6':
            # Opción para salir del bucle
            print("Gracias por usar el programa. ¡Hasta luego!")
            break  # Rompe el 'while True' y termina el programa
        else:
            # (Validación de entrada)
            print("Opción no válida. Por favor, intente de nuevo.")
        
        # (Pausa de usuario)
        # Pone una pausa al final de cada acción (excepto salir)
        # para que el usuario pueda leer el resultado antes
        # de que el bugle vuelva a limpiar la pantalla y mostrar el menú.
        input("\nPresione Enter para volver al menú principal...")

# --- Punto de Entrada del Script ---
# Esta es una convención de Python.
# El código dentro de este 'if' solo se ejecuta
# cuando el archivo se corre directamente (no cuando se importa).
if __name__ == "__main__":
    main()  # Llama a la función principal para iniciar el programa