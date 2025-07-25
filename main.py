import pygame
from auth.login_register import crear_bd, registrar_usuario, validar_usuario
import sqlite3

pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Inicio de Sesión - UNOverse")
fuente = pygame.font.SysFont("Arial", 28)
fuente_chica = pygame.font.SysFont("Arial", 20)

usuario = ''
contrasena = ''
modo = 'login'  # o 'registro'
estado = 'autenticacion'  # o 'sala'
mensaje = ''
campo_activo = 'usuario'

def dibujar_texto(texto, x, y, fuente, color=(255, 255, 255)):
    render = fuente.render(texto, True, color)
    pantalla.blit(render, (x, y))

def dibujar_caja(texto, x, y, ancho, activo):
    color_fondo = (50, 50, 50)
    color_borde = (100, 200, 250) if activo else (100, 100, 100)
    pygame.draw.rect(pantalla, color_fondo, (x, y, ancho, 40))
    pygame.draw.rect(pantalla, color_borde, (x, y, ancho, 40), 2)
    dibujar_texto(texto, x + 10, y + 5, fuente)

def interfaz_autenticacion():
    pantalla.fill((40, 0, 0))  # Fondo rojo oscuro

    # Sombra y fondo de formulario
    pygame.draw.rect(pantalla, (80, 0, 0), (140, 120, 520, 280), border_radius=20)
    pygame.draw.rect(pantalla, (200, 0, 0), (150, 130, 500, 260), border_radius=15)

    # Título
    dibujar_texto("UNOverse", 320, 50, fuente, (255, 80, 80))
    subtitulo = "Iniciar sesión" if modo == 'login' else "Registrarse"
    dibujar_texto(subtitulo, 320, 90, fuente_chica, (255, 180, 180))

    # Campos
    dibujar_texto("Usuario:", 180, 170, fuente_chica, (255, 200, 200))
    dibujar_caja(usuario + ("|" if campo_activo == 'usuario' else ""), 300, 165, 350, campo_activo == 'usuario')

    dibujar_texto("Contraseña:", 180, 230, fuente_chica, (255, 200, 200))
    contrasena_mostrada = "*" * len(contrasena)
    dibujar_caja(contrasena_mostrada + ("|" if campo_activo == 'contrasena' else ""), 300, 225, 350, campo_activo == 'contrasena')

    # Botones de acción
    dibujar_texto("[Enter] Aceptar", 300, 300, fuente_chica, (255, 120, 120))
    dibujar_texto("[Tab] Cambiar campo", 470, 300, fuente_chica, (255, 120, 120))
    dibujar_texto("[R] Registro  |  [L] Login", 340, 340, fuente_chica, (255, 180, 180))

    # Mensaje de error o confirmación
    if mensaje:
        color = (255, 0, 0) if "incorrectas" in mensaje or "uso" in mensaje else (0, 255, 0)
        dibujar_texto(mensaje, 300, 380, fuente_chica, color)

def interfaz_sala(nombre):
    pantalla.fill((15, 15, 60))
    dibujar_texto(f"Bienvenido {nombre}", 280, 200, fuente)
    dibujar_texto("Sala de espera - esperando a más jugadores...", 180, 260, fuente_chica)
    dibujar_texto("Esto será dinámico más adelante", 260, 300, fuente_chica)

def borrar_usuario(nombre):
    conn = sqlite3.connect("db/users.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE usuario=?", (nombre,))
    conn.commit()
    conn.close()

crear_bd()
reloj = pygame.time.Clock()
corriendo = True

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == pygame.KEYDOWN:
            if estado == 'autenticacion':
                if evento.key == pygame.K_TAB:
                    campo_activo = 'contrasena' if campo_activo == 'usuario' else 'usuario'
                elif evento.key == pygame.K_RETURN:
                    if modo == 'login':
                        if validar_usuario(usuario, contrasena):
                            estado = 'sala'
                        else:
                            mensaje = "Credenciales incorrectas"
                    else:
                        if registrar_usuario(usuario, contrasena):
                            mensaje = "Usuario registrado correctamente"
                        else:
                            mensaje = "Ese nombre ya está en uso"
                elif evento.key == pygame.K_r:
                    modo = 'registro'
                    mensaje = ''
                elif evento.key == pygame.K_l:
                    modo = 'login'
                    mensaje = ''
                elif evento.key == pygame.K_BACKSPACE:
                    if campo_activo == 'usuario':
                        usuario = usuario[:-1]
                    else:
                        contrasena = contrasena[:-1]
                else:
                    char = evento.unicode
                    if char.isprintable():
                        if campo_activo == 'usuario':
                            usuario += char
                        else:
                            contrasena += char

    if estado == 'autenticacion':
        interfaz_autenticacion()
    elif estado == 'sala':
        interfaz_sala(usuario)

    pygame.display.flip()
    reloj.tick(30)

pygame.quit()
