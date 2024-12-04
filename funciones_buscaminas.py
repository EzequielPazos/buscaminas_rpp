import pygame

def generar_buscaminas(cant_filas:int, cant_columnas:int, cant_minas:int)->list[list]:
    """Genera un buscaminas de cierto tamaño y con determinada cantidad de minas

    Args:
        cant_filas (int): cantidad de filas del buscaminas
        cant_columnas (int): cantidad de columnas del buscaminas
        cant_minas (int): cantidad de minas

    Returns:
        list[list]: buscaminas generado
    """
    from random import randint
    
    lista = []
    for fila in range(cant_filas):
        fila = []
        for columna in range(cant_columnas):
            fila.append(0)  # 0 -> no hay minas
        lista.append(fila)
    
    for mina in range(cant_minas):
        fila = randint(0, cant_filas-1)
        columna = randint(0, cant_columnas-1)
        while lista[fila][columna] == -1:   # si ya hay una mina ahi recalcular coordenadas
            fila = randint(0, cant_filas-1)
            columna = randint(0, cant_columnas-1)
        lista[fila][columna] = -1   # -1 -> MINA    
        
    return lista

def numerar_casillas(buscaminas:list[list]):
    """Numera las casillas adyacentes a las minas segun la cantidad de estas cercana

    Args:
        buscaminas (list[list]): buscaminas numerado
    """
    #recorrer la matriz
    for fila in range(len(buscaminas)):
        for columna in range(len(buscaminas[fila])):
            
            flag_arriba = True
            flag_abajo = True
            flag_derecha = True
            flag_izquierda = True
            
            #verifico la casilla
            if buscaminas[fila][columna] == -1:  # si es una mina
                #verifico arriba
                if fila == 0: #si es la primera fila no tiene arriba
                    flag_arriba = False
                #verifico abajo
                if fila == len(buscaminas)-1: # si es la ultima fila no tiene abajo
                    flag_abajo = False
                #verifico derecha
                if columna == len(buscaminas[fila])-1:   # si es la ultima columna no tiene derecha
                    flag_derecha = False
                #verifico izquierda
                if columna == 0:    # si es la primera columna no tiene izquierda
                    flag_izquierda = False
                
                #calculo valores en orden 123  M = MINA
                #                         4M6
                #                         789
                
                #le sumo un +1 a todas las casillas de su alrededor que no sean minas
                
                #ESCRIBIR CONSTANTES? EJ: ARRIBA = FILA-1 PARA MAYOR CLARIDAD?
                
                if flag_arriba and flag_izquierda:
                    if buscaminas[fila-1][columna-1] != -1:
                        buscaminas[fila-1][columna-1] += 1
                if flag_arriba:
                    if buscaminas[fila-1][columna] != -1:
                        buscaminas[fila-1][columna] += 1
                if flag_arriba and flag_derecha:
                    if buscaminas[fila-1][columna+1] != -1:
                        buscaminas[fila-1][columna+1] += 1
                if flag_izquierda:
                    if buscaminas[fila][columna-1] != -1:
                        buscaminas[fila][columna-1] += 1
                if flag_derecha:
                    if buscaminas[fila][columna+1] != -1:
                        buscaminas[fila][columna+1] += 1
                if flag_abajo and flag_izquierda:
                    if buscaminas[fila+1][columna-1] != -1:
                        buscaminas[fila+1][columna-1] += 1
                if flag_abajo:
                    if buscaminas[fila+1][columna] != -1:
                        buscaminas[fila+1][columna] += 1
                if flag_abajo and flag_derecha:
                    if buscaminas[fila+1][columna+1] != -1:
                        buscaminas[fila+1][columna+1] += 1

def escribir_archivo_csv(ruta:str, dato:str):
    """Guarda datos ya formateados para csv en un archivo del mismo tipo

    Args:
        ruta (str): ruta de guardado del archivo
        dato (str): dato a guardar en el archivo
    """
    with open(ruta, "w") as archivo:
        archivo.write(dato)

def crear_casillas(matriz:list[list], coordenadas_tablero:tuple, display, dimensiones_cuadro:tuple, color_1:tuple, color_2:tuple)->None:
    """Crea un tablero de casillas adaptable utilizando dos colores para intercalarse

    Args:
        matriz (list[list]): buscaminas
        coordenadas_tablero (tuple): coordenadas de origen del tablero
        display (surface): superficie donde se refleja el tablero
        dimensiones_cuadro (tuple): dimensiones de cada cuadro (tamaño)
        color_1 (tuple): color 1 para las casillas
        color_2 (tuple): color 2 para las casillas
    """
    i = 0
    for fila in range(len(matriz)):
        if fila != 0:   # modifico coordenadas para dibujar
            coordenadas_tablero = list(coordenadas_tablero)
            coordenadas_tablero[0] += dimensiones_cuadro[0]
            coordenadas_tablero[1] = 100
            coordenadas_tablero = tuple(coordenadas_tablero)
            i += 1
        for columna in range(len(matriz[fila])):
            if i % 2 == 0:
                pygame.draw.rect(display, color_1, (coordenadas_tablero, dimensiones_cuadro))
            else:
                pygame.draw.rect(display, color_2, (coordenadas_tablero, dimensiones_cuadro))
            
            coordenadas_tablero = list(coordenadas_tablero)
            coordenadas_tablero[1] += dimensiones_cuadro[1]
            coordenadas_tablero = tuple(coordenadas_tablero)
            i += 1
            
def encontrar_casilla(posicion_click:tuple, ancho_cuadro:int, alto_cuadro:int)->list:
    """Encuentra la casilla del tablero en la que se esta haciendo click

    Args:
        posicion_click (tuple): _description_
        ancho_cuadro (int): _description_
        alto_cuadro (int): _description_

    Returns:
        list: casilla encontrada [x, y]
    """
    fila = (posicion_click[0] - 25 ) // ancho_cuadro
    columna = (posicion_click[1] - 100) // alto_cuadro
    
    return [fila, columna]

def checkear_casilla(buscaminas:list[list], casilla_clickeada:list, coordenadas_tablero:tuple, dimensiones_cuadro:tuple, display, fuente, imagen_tablero_mina, imagen_tablero_explosion, color_1:tuple, color_2:tuple, color_3:tuple)->int:
    """checkea la casilla y dependiendo de su contenido dentro de la matriz la revela

    Args:
        buscaminas (list[list]): matriz del buscaminas
        casilla_clickeada (list): casilla que se ha clickeado y que se desea revelar
        coordenadas_tablero (tuple): coordenadas de origen del tablero
        dimensiones_cuadro (tuple): dimensiones de cada cuadro del tablero
        display(surface): superficie donde se ven reflejados los cambios
        fuente(font): fuente para renderizar las cadenas
        imagen_tablero_mina (surface): imagen de una mina
        imagen_tablero_explosion (surface): imagen de una explosion
        color_1 (tuple): color de la casilla revelada
        color_2 (tuple): color de la casilla revelada si es una mina
        color_3 (tuple): color de la fuente -> aplica a los string renderizados

    Returns:
        int: codigo: -1 -> es una mina
                      0 -> es una casilla vacia
            numero(1-8) -> tiene "numero" cantidad de minas adyacentes a la casilla clickeada
    """
    coordenadas_tablero = list(coordenadas_tablero)
    coordenadas_tablero[0] = casilla_clickeada[0] * dimensiones_cuadro[0] + 25
    coordenadas_tablero[1] = casilla_clickeada[1] * dimensiones_cuadro[1] + 100
    coordenadas_tablero = tuple(coordenadas_tablero)

    if buscaminas[casilla_clickeada[0]][casilla_clickeada[1]] == -1:
        pygame.draw.rect(display, color_1, (coordenadas_tablero, dimensiones_cuadro))
        display.blit(imagen_tablero_mina, (coordenadas_tablero[0] + 35, coordenadas_tablero[1] + 15))
        display.blit(imagen_tablero_explosion, (coordenadas_tablero[0] + 20, coordenadas_tablero[1] + 5))
        codigo = -1
    elif buscaminas[casilla_clickeada[0]][casilla_clickeada[1]] == 0:    # cuadro vacio
        pygame.draw.rect(display, color_2, (coordenadas_tablero, dimensiones_cuadro))
        codigo = 0
    else:   # casilla numerada
        pygame.draw.rect(display, color_2, (coordenadas_tablero, dimensiones_cuadro))
        numero = fuente.render(f"{buscaminas[casilla_clickeada[0]][casilla_clickeada[1]]}", True, color_3)
        display.blit(numero, (coordenadas_tablero[0] + 40, coordenadas_tablero[1] + 5))
        codigo = numero
    
    return codigo

def flagear_casilla(casilla_clickeada:list, coordenadas_tablero:tuple, dimensiones_cuadro:tuple, display, imagen_tablero_flag):
    """Pone una bandera en una casilla clickeada

    Args:
        casilla_clickeada (list): casilla en la que se quiere poner una bandera
        coordenadas_tablero (tuple): coordenadas de origen del tablero (Esquina izquierda y arriba)
        dimensiones_cuadro (tuple): dimensiones de cada cuadro del tablero
        display (surface): superficie donde se ven reflejados los cambios en pantalla
        imagen_tablero_flag (surface): imagen de la bandera
    """
    coordenadas_tablero = list(coordenadas_tablero)
    coordenadas_tablero[0] = casilla_clickeada[0] * dimensiones_cuadro[0] + 25
    coordenadas_tablero[1] = casilla_clickeada[1] * dimensiones_cuadro[1] + 100
    coordenadas_tablero = tuple(coordenadas_tablero)
    
    display.blit(imagen_tablero_flag, (coordenadas_tablero[0] + 35, coordenadas_tablero[1] + 15))

def formatear_puntaje_csv(puntuaciones_csv:str, usuario:str, puntaje:str)->str:
    """Da un formato al usuario y al puntaje para sumarlo a un string con los datos del archivo de puntuaciones

    Args:
        puntuaciones_csv (str): datos de las puntuaciones
        usuario (str): usuario que acaba de jugar
        puntaje (str): puntaje del usuario que acaba de jugar

    Returns:
        str: texto formateado para guardar en el archivo de puntuaciones
    """
    texto = puntuaciones_csv + f"\n{usuario}, {puntaje}"
    return texto

def leer_archivo_csv(ruta:str)->str:
    """Lee los datos de un archivo csv y los devuelve como dato str

    Args:
        ruta (str): ruta del archivo a leer

    Returns:
        str: datos leidos del archivo
    """
    with open(f"{ruta}", "r") as archivo:
        datos_archivo = archivo.read()

    return datos_archivo

# def buscar_mayor_csv(datos:list, lista_mayores:list)->int:
#     """Busca el mayor dentro de los datos de puntuacion siempre que no este ya dentro de la lista de los mayores

#     Args:
#         datos (list): lista con los datos de las puntuaciones
#         lista_mayores (list): lista con los puntajes mayores ordenados de mayor a menor

#     Returns:
#         int: indice del mayor,
#             -1 si todos los elementos de la lista de datos estan en la lista de mayores
#     """
#     retorno = -1

#     if len(datos) > 2:
#         mayor = 0
#         mayor_indice = 0
#         for i in range(3, len(datos), 2):   # comienza en el segundo puntaje, y salta de puntaje en puntaje
#             if i in lista_mayores:
#                 continue
#             else:
#                 puntaje = int(datos[i])
#                 if puntaje >= mayor:
#                     mayor = puntaje
#                     mayor_indice = i
#         if mayor_indice != 0:
#             retorno =  mayor_indice

#     return retorno

def buscar_mayores_lista(lista:list[int], cantidad_mayores:int)->list:
    """Busca una X cantidad de mayores en una lista de enteros

    Args:
        lista (list[int]): Lista de enteros a trabajar
        cantidad_mayores (int): cantidad de x numeros mayores

    Returns:
        list: lista con los indices de los numeros mayores
    """
    lista_indices = []
    if len(lista) > 0:
        for _ in range(cantidad_mayores):
            mayor = -1
            mayor_indice = -1
            for j in range(len(lista)):
                if j in lista_indices:
                    continue
                else:
                    if lista[j] >= mayor:
                        mayor = lista[j]
                        mayor_indice = j
            if mayor_indice != -1:
                lista_indices.append(mayor_indice)
    
    return lista_indices

def crear_listas_paralelas(lista_datos:list[str])->list[list]:
    """Crea dos listas paralelas a partir de una lista de varios elementos

    Args:
        lista_datos (list[str]): lista de datos

    Returns:
        list[list]: lista con las dos listas paralelas dentro donde cada dato coincide con su indice respectivo
    """
    lista_usuarios_puntajes = []
    lista_usuarios = []
    lista_puntajes = []
    
    for i in range(2, len(lista_datos)):
        if i % 2 == 0:
            lista_usuarios.append(lista_datos[i])
        else:
            lista_puntajes.append(int(lista_datos[i]))
    lista_usuarios_puntajes.append(lista_usuarios)
    lista_usuarios_puntajes.append(lista_puntajes)
    return lista_usuarios_puntajes
    
# def descubrir_vacias_adyacentes(buscaminas, casilla, coordenadas_tablero, dimensiones_cuadro, display, fuente, imagen_tablero_mina, imagen_tablero_explosion, COLOR_ROJO, COLOR_BLANCO, COLOR_NEGRO, lista_libres, lista_casillas):
#     flag_arriba = True
#     flag_abajo = True
#     flag_izq = True
#     flag_der = True
    
#     if casilla[0] == 0: # no tiene arriba
#         flag_arriba = False
#     elif casilla[0] == len(buscaminas)-1: # no tiene abajo
#         flag_abajo = False
#     elif casilla[1] == 0: # no tiene izquierda
#         flag_izq = False
#     elif casilla[1] == len(buscaminas[0])-1: # no tiene derecha
#         flag_der = False

#     if flag_arriba:
#         casilla_arriba = [casilla[0 - 1], casilla[1]]
#         if checkear_casilla(buscaminas, casilla_arriba, coordenadas_tablero, dimensiones_cuadro, display, fuente, imagen_tablero_mina, imagen_tablero_explosion, COLOR_ROJO, COLOR_BLANCO, COLOR_NEGRO) != -1:
#             lista_libres.append(casilla_arriba)
#             lista_casillas.append(casilla_arriba)
#     if flag_izq:
#         casilla_izq = [casilla[0], casilla[1 - 1]]
#         if checkear_casilla(buscaminas, casilla_arriba, coordenadas_tablero, dimensiones_cuadro, display, fuente, imagen_tablero_mina, imagen_tablero_explosion, COLOR_ROJO, COLOR_BLANCO, COLOR_NEGRO) != -1:
#             lista_libres.append(casilla_izq)
#             lista_casillas.append(casilla_izq)
#     if flag_der:
#         casilla_der = [casilla[0], casilla[1 + 1]]
#         if checkear_casilla(buscaminas, casilla_arriba, coordenadas_tablero, dimensiones_cuadro, display, fuente, imagen_tablero_mina, imagen_tablero_explosion, COLOR_ROJO, COLOR_BLANCO, COLOR_NEGRO) != -1:
#             lista_libres.append(casilla_der)
#             lista_casillas.append(casilla_der)
#     if flag_abajo:
#         casilla_abajo = [casilla[0 + 1], casilla[1]]
#         if checkear_casilla(buscaminas, casilla_arriba, coordenadas_tablero, dimensiones_cuadro, display, fuente, imagen_tablero_mina, imagen_tablero_explosion, COLOR_ROJO, COLOR_BLANCO, COLOR_NEGRO) != -1:
#             lista_libres.append(casilla_abajo)
#             lista_casillas.append(casilla_abajo)