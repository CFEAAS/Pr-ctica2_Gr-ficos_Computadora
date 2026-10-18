### Practica 2 - Actividad 1

import pygame
from pygame.locals import *
import math
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import urllib.request

URL_OBJ = "https://raw.githubusercontent.com/USUARIO/REPO/main/modelo.obj"



def cargar_obj(url):
    texto = urllib.request.urlopen(url).read().decode("utf-8")
    verts = []
    caras = []
    for linea in texto.splitlines():
        partes = linea.split()
        if not partes:
            continue
        if partes[0] == "v":
            verts.append([float(p) for p in partes[1:4]])
        elif partes[0] == "f":
            idx = []
            for p in partes[1:]:
                i = int(p.split("/")[0])
                idx.append(i - 1 if i > 0 else len(verts) + i)
            for k in range(1, len(idx) - 1):
                caras.append((idx[0], idx[k], idx[k + 1]))
    minimos = [min(v[e] for v in verts) for e in range(3)]
    maximos = [max(v[e] for v in verts) for e in range(3)]
    centro = [(minimos[e] + maximos[e]) / 2 for e in range(3)]
    escala = 2 / max(maximos[e] - minimos[e] for e in range(3))
    verts = [[(v[e] - centro[e]) * escala for e in range(3)] for v in verts]
    return verts, caras


def crear_lista_modelo(verts, caras):
    lista = glGenLists(1)
    glNewList(lista, GL_COMPILE)
    glBegin(GL_TRIANGLES)
    for cara in caras:
        for i in cara:
            glColor3f((verts[i][0] + 1) / 2, (verts[i][1] + 1) / 2, (verts[i][2] + 1) / 2)
            glVertex3fv(verts[i])
    glEnd()
    glEndList()
    return lista


def dibujar_ui(superficie, textura):
    ancho, alto = superficie.get_size()
    datos = pygame.image.tostring(superficie, "RGBA", True)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, ancho, 0, alto, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glBindTexture(GL_TEXTURE_2D, textura)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ancho, alto, 0, GL_RGBA, GL_UNSIGNED_BYTE, datos)

    glColor4f(1, 1, 1, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(0, 0)
    glTexCoord2f(1, 0); glVertex2f(ancho, 0)
    glTexCoord2f(1, 1); glVertex2f(ancho, alto)
    glTexCoord2f(0, 1); glVertex2f(0, alto)
    glEnd()

    glDisable(GL_BLEND)
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
def Rotacion(anguloX, anguloY, anguloZ):
    Rx=(1,0,0,0,0,math.cos(math.radians(anguloX)),-math.sin(math.radians(anguloX)),0,0,math.sin(math.radians(anguloX)),math.cos(math.radians(anguloX)),0,0,0,0,1)
    Ry=(math.cos(math.radians(anguloY)),0,math.sin(math.radians(anguloY)),0,0,1,0,0,-math.sin(math.radians(anguloY)),0,math.cos(math.radians(anguloY)),0,0,0,0,1)
    Rz=(math.cos(math.radians(anguloZ)),-math.sin(math.radians(anguloZ)),0,0,math.sin(math.radians(anguloZ)),math.cos(math.radians(anguloZ)),0,0,0,0,1,0,0,0,0,1)
    glMultTransposeMatrixf(Rx)
    glMultTransposeMatrixf(Ry)
    glMultTransposeMatrixf(Rz)


def Trasladar(dx, dy, dz):
    glTranslatef(dx, dy, dz)
def Escalar(sx, sy, sz):
    E = (
    sx, 0.0, 0.0, 0.0,
    0.0, sy, 0.0, 0.0,
    0.0, 0.0, sz, 0.0,
    0.0, 0.0, 0.0, 1.0  # El último elemento suele ser 1.0 para coordenadas homogéneas
)
    glMultTransposeMatrixf(E)
def inicializar_pygame():
    pygame.init()
    display = (512, 512)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glEnable(GL_DEPTH_TEST)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    superficie_ui = pygame.Surface(display, pygame.SRCALPHA)
    textura_ui = glGenTextures(1)
    return superficie_ui, textura_ui

def crear_boton(superficie, x, y, texto, accion):
    return Button(
        superficie,  # Superficie
        x, y,  # Posición X, Y
        150, 50,   # Ancho, Alto
        text=texto,
        fontSize=20,
        margin=20,
        inactiveColour=(40, 120, 240),
        pressedColour=(0, 200, 100),
        radius=10,
        onClick=accion
    )


def crear_slider(superficie, x, y):
    return Slider(
        superficie,  # Superficie
        x, y,  # Posición X, Y
        80, 20,   # Ancho, Alto
        min=-5,
        max=5,
        step=1,
        handleColour=(40, 120, 240),
        colour=(200, 200, 200)
    )
def crear_textbox(superficie, x, y, texto):
    textbox = TextBox(
        superficie,  # Superficie
        x, y,        # Posición X, Y
        70, 25,     # Ancho, Alto (se aumenta el alto a 25)
        fontSize=14, # Tamaño de letra más adecuado para el alto
        colour=(255, 255, 255),
        textColour=(0, 0, 0),  # Color del texto en negro
        borderColour=(40, 120, 240),
        borderThickness=2,
        radius=10
    )
    textbox.setText(texto)
    textbox.disable()
    return textbox
    
def CambiarMenu(menus, nombre):
    for botones in menus.values():
        for boton in botones:
            boton.hide()
    for boton in menus[nombre]:
        boton.show()

def crear_menus(superficie):
    menus = {}
    atras = crear_boton(superficie, 400, 20, 'Atrás', lambda: CambiarMenu(menus, 'principal'))
    menus['principal'] = [
        crear_boton(superficie, 10, 10, 'Transformar en X', lambda: CambiarMenu(menus, 'x')),
        crear_boton(superficie, 180, 10, 'Transformar en Y', lambda: CambiarMenu(menus, 'y')),
        crear_boton(superficie, 360, 10, 'Transformar en Z', lambda: CambiarMenu(menus, 'z'))
    ]
    menus['x'] = [atras, crear_slider(superficie, 10, 50),crear_textbox(superficie, 10, 25,"Escalar"), crear_slider(superficie, 150, 50),crear_textbox(superficie, 150, 25,"Trasladar"),crear_slider(superficie, 290, 50),crear_textbox(superficie, 290, 25,"Rotar")]
    menus['y'] = [atras, crear_slider(superficie, 10, 50), crear_textbox(superficie, 10, 25,"Escalar"), crear_slider(superficie, 150, 50),crear_textbox(superficie, 150, 25,"Trasladar"),crear_slider(superficie, 290, 50),crear_textbox(superficie, 290, 25,"Rotar")]
    menus['z'] = [atras, crear_slider(superficie, 10, 50), crear_textbox(superficie, 10, 25,"Escalar"), crear_slider(superficie, 150, 50),crear_textbox(superficie, 150, 25,"Trasladar"),crear_slider(superficie, 290, 50),crear_textbox(superficie, 290, 25,"Rotar")]
    CambiarMenu(menus, 'principal')
    return menus

def main():
    superficie_ui, textura_ui = inicializar_pygame()
    menus = crear_menus(superficie_ui)
    verts, caras = cargar_obj(URL_OBJ)
    lista_modelo = crear_lista_modelo(verts, caras)

    while True:
        eventos = pygame.event.get()
        for event in eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        ### Activar la función del cubo
        sx = 1 + menus['x'][1].getValue() / 10
        sy = 1 + menus['y'][1].getValue() / 10
        sz = 1 + menus['z'][1].getValue() / 10
        dx = menus['x'][3].getValue() / 10
        dy = menus['y'][3].getValue() / 10
        dz = menus['z'][3].getValue() / 10
        rx = menus['x'][5].getValue() * 5
        ry = menus['y'][5].getValue() * 5
        rz = menus['z'][5].getValue() * 5
        glPushMatrix()
        Escalar(sx, sy, sz)
        Trasladar(dx, dy, dz)
        Rotacion(rx, ry, rz)
        glCallList(lista_modelo)
        glPopMatrix()

        superficie_ui.fill((0, 0, 0, 0))
        pygame_widgets.update(eventos)
        dibujar_ui(superficie_ui, textura_ui)

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == '__main__':
    main()