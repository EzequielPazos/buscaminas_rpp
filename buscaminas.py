"""
ALUMNO: PAZOS ACEBAL EZEQUIEL

CREDITS:

MUSIC:
Song: Dosi & Aisake - Cruising [NCS Release]
Music provided by NoCopyrightSounds
Free Download/Stream: http://ncs.io/Cruising
Watch: http://ncs.lnk.to/CruisingAT/youtube

"""

import pygame, funciones_buscaminas

pygame.init()
pygame.mixer.init()


# DISPLAY
PANTALLA_ANCHO = 800
PANTALLA_ALTO = 600
RESOLUCION_PANTALLA = (PANTALLA_ANCHO, PANTALLA_ALTO)

display = pygame.display.set_mode(RESOLUCION_PANTALLA) # Ventana maximizable

pygame.display.set_caption("Buscaminas")

# IMAGENES
imagen_mina = pygame.image.load("NUEVO PLAN/Proyecto Pygame copy/assets/images/mine.png") # Cargando una imagen de una mina
pygame.display.set_icon(imagen_mina) # Creo el icono de la ventana principal
#imagen_mina_pixel = pygame.Surface.convert(imagen_mina) # Paso la imagen a formato pixel ya que es el mejor formato para aplicar blit a una imagen
imagen_mina = pygame.transform.scale(imagen_mina, (300, 300))
imagen_bg = pygame.image.load("NUEVO PLAN/Proyecto Pygame copy/assets/images/buscaminas_bg.jpg")
imagen_bg = pygame.transform.scale(imagen_bg, (PANTALLA_ANCHO, PANTALLA_ALTO))
imagen_tablero_mina = pygame.transform.scale(imagen_mina, (30, 30))
imagen_explosion = pygame.image.load("NUEVO PLAN/Proyecto Pygame copy/assets/images/explosion.png")
imagen_tablero_explosion = pygame.transform.scale(imagen_explosion, (50, 50))
imagen_flag = pygame.image.load("NUEVO PLAN/Proyecto Pygame copy/assets/images/flag.png")
imagen_tablero_flag = pygame.transform.scale(imagen_flag, (30, 30))

# SFX

# cancion en loop a definir

pygame.mixer.music.load("NUEVO PLAN/Proyecto Pygame copy/assets/sfx/musica_bg.mp3")
pygame.mixer.music.set_volume(0.1)  # 0.5 == 50%

# COLORES

COLOR_AZUL_CLARO = (127, 157, 235)
COLOR_NEGRO = (0, 0, 0)
COLOR_BLANCO = (255, 255, 255)
COLOR_AMARILLO = (255, 255, 0)
COLOR_MAGENTA = (255, 0, 255)
COLOR_ROJO = (255, 0, 0)
COLOR_MARRON = (135, 116, 89)
COLOR_VERDE = (0, 255, 0)

# TEXTOS

fuente = pygame.font.SysFont("Arial", 40, bold=True)
texto_nivel = fuente.render("NIVEL", True, COLOR_NEGRO)
texto_jugar = fuente.render("JUGAR", True, COLOR_NEGRO)
texto_puntajes = fuente.render("PUNTAJES", True, COLOR_NEGRO)
texto_salir = fuente.render("SALIR", True, COLOR_NEGRO)
texto_titulo = fuente.render("BUSCAMINAS", True, COLOR_NEGRO)
texto_reiniciar = fuente.render("REINICIAR", True, COLOR_NEGRO)
texto_atras = fuente.render("ATRAS", True, COLOR_NEGRO)
texto_usuario = ""
pedir_nombre = fuente.render("Ingrese su nombre: ", True, COLOR_NEGRO)
texto_top_usuarios = fuente.render(f"TOP JUGADORES", True, COLOR_NEGRO)
texto_ganar = fuente.render("GANASTE! :)", True, COLOR_NEGRO)
texto_perder = fuente.render("PERDISTE :(", True, COLOR_NEGRO)

# BOTONES
ANCHO_BOTON = 200
ALTURA_BOTON = 100
coordenadas_tablero = (25, 100)

clock = pygame.time.Clock()
corriendo = True
pantalla = "Inicio"
puntaje = "0000"
dificultad = "Facil"
buscaminas_generado = False
lista_casillas = []
lista_casillas_flag = []
ingresado = False
    # LEER EL CSV CON DATOS Y GUARDARLOS EN UNA VARIABLE
try: 
    archivo = open("NUEVO PLAN/Proyecto Pygame copy/puntuaciones.csv", "r")
    puntuaciones_csv = archivo.read()
    archivo.close()
except FileNotFoundError:
    # SI NO EXISTE QUE PUNTUACIONES SEA ESTO
    archivo = open("NUEVO PLAN/Proyecto Pygame copy/puntuaciones.csv", "w")
    puntuaciones_csv = "usuario, puntaje"
    archivo.write(puntuaciones_csv)
    archivo.close()
    
pygame.mixer.music.play(-1)    # LOOP MUSICA

while corriendo == True:
    
    #CHECKEO PANTALLA
        
    if pantalla == "Inicio":    # DENTRO DE LA PANTALLA INICIO
        
        #CHECKEO EVENTOS
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                posicion_click = pygame.mouse.get_pos()
                if posicion_click[0] >= 50 and posicion_click[0] <= (ANCHO_BOTON + 50):
                    if posicion_click[1] >= 25 and posicion_click[1] <=  125:
                        pantalla = "Niveles"
                    if posicion_click[1] >= 175 and posicion_click[1] <=  275:
                        pantalla = "Jugar"
                    if posicion_click[1] >= 325 and posicion_click[1] <=  425:
                        pantalla = "Puntajes"
                    if posicion_click[1] >= 475 and posicion_click[1] <=  575:
                        corriendo = False
                    # CAMBIAR A COLLIDEPOINT DE LOS BOTONES CLASS RECT
        # BG
        
        display.blit(imagen_bg, (0, 0))
        
        # TITULO
        
        display.blit(imagen_mina, (375, 25))    # Muestro imagen en superficie
        display.blit(texto_titulo, (415, 325))
        
        # BOTONES -------
        
        # NIVEL
        pygame.draw.rect(display, (COLOR_BLANCO), (50, 25, ANCHO_BOTON, ALTURA_BOTON), 0, 3)
        display.blit(texto_nivel, (60, (ALTURA_BOTON/2)))
        
        # JUGAR
        pygame.draw.rect(display, (COLOR_BLANCO), (50, 175, ANCHO_BOTON, ALTURA_BOTON), 0, 3)
        display.blit(texto_jugar, (60, 175 + (ALTURA_BOTON/2) - 25))
        
        # PUNTAJES
        pygame.draw.rect(display, (COLOR_BLANCO), (50, 325, ANCHO_BOTON, ALTURA_BOTON), 0, 3)
        display.blit(texto_puntajes, (60, 325 + (ALTURA_BOTON/2) - 25))
        
        # SALIR
        pygame.draw.rect(display, (COLOR_BLANCO), (50, 475, ANCHO_BOTON, ALTURA_BOTON), 0, 3)
        display.blit(texto_salir, (60, 475 + (ALTURA_BOTON/2) - 25))
        
        # ------------
        
    elif pantalla == "Niveles":
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                botones = pygame.mouse.get_pressed(3)
                posicion_click = pygame.mouse.get_pos()
                if botones[0]: #click izquierdo
                    if boton_atras.collidepoint(posicion_click):
                        pantalla = "Inicio"
        # BG
              
        display.blit(imagen_bg, (0, 0))

        # BOTONES

        # ATRAS

        boton_atras = pygame.draw.rect(display, COLOR_BLANCO, (575, 25, 200, 50))
        display.blit(texto_atras, (620, 25))
        
    elif pantalla == "Jugar":
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                botones = pygame.mouse.get_pressed(3)
                posicion_click = pygame.mouse.get_pos()
                if botones[0]: #click izquierdo
                    if boton_reinicio.collidepoint(posicion_click):
                        puntaje = "0000"
                        buscaminas_generado = False    # Asi se vuelve a generar uno
                        lista_casillas.clear()    # Limpio la lista de casillas que desmarque
                    if boton_atras.collidepoint(posicion_click):
                        pantalla = "Inicio"
                    if posicion_click[0] >= 25 and posicion_click[0] <= 25 + (ancho_cuadro * cantidad_columnas) and posicion_click[1] >= 100 and posicion_click[1] <= 100 + (alto_cuadro * cantidad_filas):
                        # DENTRO DEL TABLERO
                        casilla_clickeada = funciones_buscaminas.encontrar_casilla(posicion_click, ancho_cuadro, alto_cuadro)
                        if casilla_clickeada not in lista_casillas and casilla_clickeada not in lista_casillas_flag:
                            lista_casillas.append(casilla_clickeada)

                if botones[2]: #click derecho
                    if posicion_click[0] >= 25 and posicion_click[0] <= 25 + (ancho_cuadro * cantidad_columnas) and posicion_click[1] >= 100 and posicion_click[1] <= 100 + (alto_cuadro * cantidad_filas):
                        casilla_clickeada = funciones_buscaminas.encontrar_casilla(posicion_click, ancho_cuadro, alto_cuadro)
                        if casilla_clickeada not in lista_casillas_flag:
                            lista_casillas_flag.append(casilla_clickeada)
                        else:
                            lista_casillas_flag.remove(casilla_clickeada)
        # BG     
        display.blit(imagen_bg, (0, 0))
        
        # BOTONES ----
        
        # REINICIAR
        
        boton_reinicio = pygame.draw.rect(display, COLOR_BLANCO, (25, 25, 200, 50))
        display.blit(texto_reiniciar, (40, 25))
        
        #funcion de reinicio
        
        # ATRAS
        
        boton_atras = pygame.draw.rect(display, COLOR_BLANCO, (575, 25, 200, 50))
        display.blit(texto_atras, (620, 25))
        
        # ----
        
        # PUNTAJE
        
        fondo_puntaje = pygame.draw.rect(display, COLOR_AZUL_CLARO, (300, 25, 200, 50))
        texto_puntaje = fuente.render(f"{puntaje}", True, COLOR_NEGRO)
        display.blit(texto_puntaje, (365, 25))
        
        # TABLERO
        
        #checkear dificultad
        match dificultad:
            case "Facil":
                cantidad_filas = 8
                cantidad_columnas = 8
                cantidad_minas = 10
            case "Medio":
                cantidad_filas = 16
                cantidad_columnas = 16
                cantidad_minas = 40
            case "Dificil":
                cantidad_filas = 16
                cantidad_columnas = 30
                cantidad_minas = 100
                
        # TAMAÑO DEPENDE DE LA PANTALLA
        
        ancho_cuadro = (PANTALLA_ANCHO - 50) // cantidad_columnas
        alto_cuadro = (PANTALLA_ALTO - 125) // cantidad_filas
        
        dimensiones_cuadro = (ancho_cuadro, alto_cuadro)
        
        if buscaminas_generado == False:
            buscaminas = funciones_buscaminas.generar_buscaminas(cantidad_filas, cantidad_columnas, cantidad_minas)
            funciones_buscaminas.numerar_casillas(buscaminas)
            buscaminas_generado = True

        funciones_buscaminas.crear_casillas(buscaminas, coordenadas_tablero, display, dimensiones_cuadro, COLOR_AZUL_CLARO, COLOR_NEGRO)
        
        lista_libres = []
        
        if len(lista_casillas) > 0:
            for casilla in lista_casillas:       
                if funciones_buscaminas.checkear_casilla(buscaminas, casilla, coordenadas_tablero, dimensiones_cuadro, display, fuente, imagen_tablero_mina, imagen_tablero_explosion, COLOR_ROJO, COLOR_BLANCO, COLOR_NEGRO) == -1:
                    #muerto
                    #pygame.time.wait(1000) ->delay para ver la explosion
                    pantalla = "Terminar"
                elif funciones_buscaminas.checkear_casilla(buscaminas, casilla, coordenadas_tablero, dimensiones_cuadro, display, fuente, imagen_tablero_mina, imagen_tablero_explosion, COLOR_ROJO, COLOR_BLANCO, COLOR_NEGRO) == 0:
                    #vacio
                    #puntaje = (str(int(puntaje) + 1)).zfill(4)
                    #descubrir_vacias_adyacentes(buscaminas, casilla, coordenadas_tablero, dimensiones_cuadro)
                    lista_libres.append(casilla)
                    puntaje = str(len(lista_libres)).zfill(4)
                else:
                    #numero
                    #puntaje = (str(int(puntaje) + 1)).zfill(4)
                    lista_libres.append(casilla)
                    puntaje = str(len(lista_libres)).zfill(4)
        
        if len(lista_casillas_flag) > 0:
            for casilla_flag in lista_casillas_flag:
                if casilla_flag not in lista_casillas:
                    funciones_buscaminas.flagear_casilla(casilla_flag, coordenadas_tablero, dimensiones_cuadro, display, imagen_tablero_flag)
        
        if puntaje == "0054":   # Puntaje maximo de casillas vacias -> GANAR // CHECKEAR MISMA CANTIDAD DE MINAS QUE DE CASILLAS SIN DAR VUELTA?
            pantalla = "Terminar"

    elif pantalla == "Puntajes":
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                botones = pygame.mouse.get_pressed(3)
                posicion_click = pygame.mouse.get_pos()
                if botones[0]: #click izquierdo
                    if boton_atras.collidepoint(posicion_click):
                        pantalla = "Inicio"

        # BG
        display.blit(imagen_bg, (0, 0))

        # FONDO TEXTOS

        superficie_rect = pygame.Surface(pygame.Rect(25, 100, 750, 475).size, pygame.SRCALPHA)
        pygame.draw.rect(superficie_rect, (255, 255, 255, 127), superficie_rect.get_rect())
        display.blit(superficie_rect, (25, 100, 750, 475))
        #fondo_puntuaciones = pygame.draw.rect(display, COLOR_BLANCO, (25, 100, 750, 475))

        display.blit(texto_top_usuarios, (250, 125))

        # BOTON ATRAS

        boton_atras = pygame.draw.rect(display, COLOR_BLANCO, (575, 25, 200, 50))
        display.blit(texto_atras, (620, 25))

        # MOSTRAR LOS MAYORES 3 PUNTAJES

        datos_archivo = funciones_buscaminas.leer_archivo_csv("NUEVO PLAN/Proyecto Pygame copy/puntuaciones.csv")

        datos_archivo = datos_archivo.replace(",", "").split()

        #lista_mayores = []

        # while len(lista_mayores) < 3 and funciones_buscaminas.buscar_mayor_csv(datos_archivo, lista_mayores) != -1:
        #     lista_mayores.append(funciones_buscaminas.buscar_mayor_csv(datos_archivo, lista_mayores))

        lista_usuarios_puntajes = funciones_buscaminas.crear_listas_paralelas(datos_archivo)
        lista_indices_mayores = funciones_buscaminas.buscar_mayores_lista(lista_usuarios_puntajes[1], 3)

        x = 250
        y = 200
        if len(lista_indices_mayores) > 0:
            for indice in lista_indices_mayores:
                #BLITEAR TEXTOS
                texto_usuario_puntuacion = fuente.render(f"{lista_usuarios_puntajes[0][indice].ljust(20)}", True, COLOR_NEGRO)
                display.blit(texto_usuario_puntuacion, (x, y))
                texto_puntuacion = fuente.render(f"{str(lista_usuarios_puntajes[1][indice]).zfill(4).rjust(5)}", True, COLOR_NEGRO)
                display.blit(texto_puntuacion, (450, y))
                y += 100
        else:
            #BLITEAR TEXTO
            x = 175
            texto_puntuacion = fuente.render("AUN NO HAY PUNTUACIONES", True, COLOR_NEGRO)
            display.blit(texto_puntuacion, (x, y))

    elif pantalla == "Terminar":
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    ingresado = True
                    buscaminas_generado = False
                    lista_casillas.clear()
                    lista_casillas_flag.clear()
                    pantalla = "Inicio"           
                elif evento.key == pygame.K_BACKSPACE:
                    texto_usuario = texto_usuario[0:-1]
                else:
                    texto_usuario += evento.unicode

        if puntaje == "0054": #maximo de casillas libres en la tabla de 8x8 -> hacer variable a la dificultad
            display.fill(COLOR_VERDE)
            display.blit(texto_ganar, (310, 125))
        else:
            display.fill(COLOR_ROJO)
            display.blit(texto_perder, (310, 125))
            
        rectangulo_nombre = pygame.draw.rect(display, COLOR_BLANCO, (250, 250, 310, 50))
        display.blit(pedir_nombre, (250, 200))
        superficie_texto = fuente.render(texto_usuario, True, COLOR_NEGRO)
        display.blit(superficie_texto, (250, 250))
        
        datos_csv = funciones_buscaminas.formatear_puntaje_csv(puntuaciones_csv, texto_usuario, puntaje)

        if ingresado:
            funciones_buscaminas.escribir_archivo_csv("NUEVO PLAN/Proyecto Pygame copy/puntuaciones.csv", datos_csv)
            ingresado = False
            puntaje = "0000"
            texto_usuario = ""
            puntuaciones_csv = datos_csv # guardo los datos en la variable -> multiples intentos en una misma sesion

    pygame.display.flip() # Actualizo display
    
    clock.tick(60) # 60 FPS limite
    
pygame.quit()