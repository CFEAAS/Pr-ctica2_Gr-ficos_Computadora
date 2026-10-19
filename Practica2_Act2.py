### Practica 2 - Actividad 2

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
import math
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import urllib.request

URL_OBJ = "https://github.com/CFEAAS/Pr-ctica2_Gr-ficos_Computadora/raw/refs/heads/main/FIFA_World_Cup.obj"


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
def ShearX(angulo):
    t = math.tan(math.radians(angulo))
    H = ((1, t, t, 0),  # Inclinación en x: x' = x + t*y + t*z, los ejes y, z no cambian
         (0, 1, 0, 0),
         (0, 0, 1, 0),
         (0, 0, 0, 1))
    glMultTransposeMatrixf(H)
def ShearY(angulo):
    t = math.tan(math.radians(angulo))
    H = ((1, 0, 0, 0),  # Inclinación en y: y' = y + t*x + t*z, los ejes x, z no cambian
         (t, 1, t, 0),
         (0, 0, 1, 0),
         (0, 0, 0, 1))
    glMultTransposeMatrixf(H)
def ShearZ(angulo):
    t = math.tan(math.radians(angulo))
    H = ((1, 0, 0, 0),  # Inclinación en z: z' = z + t*x + t*y, los ejes x, y no cambian
         (0, 1, 0, 0),
         (t, t, 1, 0),
         (0, 0, 0, 1))
    glMultTransposeMatrixf(H)




def main():
    pygame.init()
    display = (512,512)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    superficie_ui = pygame.Surface(display, pygame.SRCALPHA)
    textura_ui = glGenTextures(1)
    verts, caras = cargar_obj(URL_OBJ)
    lista_modelo = crear_lista_modelo(verts, caras)
    sluderx = Slider(superficie_ui, 10, 10, 200, 20, min=-60, max=60, step=1, initial=0)
    sludery = Slider(superficie_ui, 10, 40, 200, 20, min=-60, max=60, step=1, initial=0)
    sluderz = Slider(superficie_ui, 10, 70, 200, 20, min=-60, max=60, step=1, initial=0)
    etiquetaX = TextBox(superficie_ui, 220, 10, 180, 30, fontSize=18)
    etiquetaY = TextBox(superficie_ui, 220, 40, 180, 30, fontSize=18)
    etiquetaZ = TextBox(superficie_ui, 220, 70, 180, 30, fontSize=18)
    etiquetaX.setText("Inclinación en x")
    etiquetaY.setText("Inclinación en y")
    etiquetaZ.setText("Inclinación en z")
    etiquetaX.disable()
    etiquetaY.disable()
    etiquetaZ.disable()
    glEnable(GL_DEPTH_TEST)
    outputX = TextBox(superficie_ui, 410, 10, 80, 30, fontSize=18)
    outputY = TextBox(superficie_ui, 410, 40, 80, 30, fontSize=18)
    outputZ = TextBox(superficie_ui, 410, 70, 80, 30, fontSize=18)
    outputX.disable()
    outputY.disable()
    outputZ.disable()

    gluPerspective(45, (display[0]/display[1]), 0.1, 45.0)
    glTranslatef(0.0,0.0, -5)
    glRotatef(40, 0, 1, 0)

   
    while True:
        eventos = pygame.event.get()
        for event in eventos:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        shearX = sluderx.getValue()
        shearY = sludery.getValue()
        shearZ = sluderz.getValue()
        glPushMatrix()
        ShearX(shearX)
        ShearY(shearY)
        ShearZ(shearZ)
        glCallList(lista_modelo)
        glPopMatrix()
        outputX.setText(str(shearX))
        outputY.setText(str(shearY))
        outputZ.setText(str(shearZ))
        superficie_ui.fill((0, 0, 0, 0))
        pygame_widgets.update(eventos)
        dibujar_ui(superficie_ui, textura_ui)

        pygame.display.flip()
        pygame.time.wait(10)
if __name__ == '__main__':
    main()