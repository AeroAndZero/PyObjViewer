from typing import final
import pygame
import numpy as np
from pygame.version import ver
import cMath
import math
import objLoader

WIDTH, HEIGHT = 600,600
FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Testing")

#Pygame Font
pygame.font.init()
myFont = pygame.font.SysFont('Arial', 12)

# Light location
lightPos = [0.0, -15.0, 5.0, 1.0]
intensity = 0.5

#Vertices      X     Y    Z    W
vertices = [ [-1.0,1.0, -1.0, 0],
             [1.0, 1.0, -1.0, 0],
             [1.0, 1.0, 1.0, 0],
             [-1.0,  1.0, 1.0, 0],
             [-1.0,-1.0, -1.0, 0],
             [1.0, -1.0, -1.0, 0],
             [1.0, -1.0, 1.0, 0],
             [-1.0, -1.0, 1.0, 0],
             [   0,   0, 0.01, 0]  ]

#Faces     v1/vt1/vn1  v2/vt2/vn2  v3/vt3/vn3
faces = [ [[0,0,0],    [0,0,0],    [0,0,0]],
          [[0,0,0],    [0,0,0],    [0,0,0]] ]
    
# Normals
normals = [[0,0,0,0]]

# A simple clamp function
def clamp(my_value,min_value,max_value):
    return max(min(my_value, max_value), min_value)

#To cartesian coordinate system
def toCartesian(verts):
    result = []
    for vert in verts:
        vert[0] += 1
        vert[1] += 1

        vert[0] *= 0.5 * WIDTH
        vert[1] *= 0.5 * HEIGHT

        result.append(vert)

    return result

#Drawing vertices
def drawVerts(verts, color, radius, convertCartesian = True, label = True):
    if convertCartesian:
        verts = toCartesian(verts)

    for i,vert in enumerate(verts):
        pygame.draw.circle(WIN, color, (vert[0], vert[1]), radius)

        if label:
            vertexNum = myFont.render(str((vert[0], vert[1],vert[2])), False, (255,255,255))
            WIN.blit(vertexNum,(vert[0],vert[1]))

def drawEdges(verts, faces, color, width, convertCartesian = False):
    
    if convertCartesian:
        verts = toCartesian(verts)

    for face in faces:
        points = ( ( verts[face[0][0]] [0], verts[face[0][0]] [1], verts[face[0][0]] [2]),
                   ( verts[face[1][0]] [0], verts[face[1][0]] [1], verts[face[1][0]] [2]),
                   ( verts[face[2][0]] [0], verts[face[2][0]] [1], verts[face[2][0]] [2])  )
       
        _,_,normalZ,_ = cMath.getNormal(points)

        if normalZ > 0:
            pygame.draw.line(WIN,color, (verts[face[0][0]] [0], verts[face[0][0]] [1]), (verts[face[1][0]] [0], verts[face[1][0]] [1]) , width)
            pygame.draw.line(WIN,color, (verts[face[1][0]] [0], verts[face[1][0]] [1]), (verts[face[2][0]] [0], verts[face[2][0]] [1]) , width)
            pygame.draw.line(WIN,color, (verts[face[2][0]] [0], verts[face[2][0]] [1]), (verts[face[0][0]] [0], verts[face[0][0]] [1]) , width)
        

def drawFaces(verts, faces, color, convertCartesian = False):

    if convertCartesian:
        verts = toCartesian(verts)

    # Format :
    # f     v1/vt1/vn1      v2/vt2/vn2      v3/vt3/vn3
    for face in faces:
        points = ( ( verts[face[0][0]] [0], verts[face[0][0]] [1], verts[face[0][0]] [2]),
                   ( verts[face[1][0]] [0], verts[face[1][0]] [1], verts[face[1][0]] [2]),
                   ( verts[face[2][0]] [0], verts[face[2][0]] [1], verts[face[2][0]] [2])  )
        
        pointsForPoly = ( ( verts[face[0][0]] [0], verts[face[0][0]] [1]),
                          ( verts[face[1][0]] [0], verts[face[1][0]] [1]),
                          ( verts[face[2][0]] [0], verts[face[2][0]] [1])  )
        

        # ----- Lighting calculations
        faceOrigin = [ (verts[face[0][0]] [0] + verts[face[1][0]] [0] + verts[face[2][0]] [0]) / 3,
                       (verts[face[0][0]] [1] + verts[face[1][0]] [1] + verts[face[2][0]] [1]) / 3,
                       (verts[face[0][0]] [2] + verts[face[1][0]] [2] + verts[face[2][0]] [2]) / 3,
                       1.0]
        

        norm_n = cMath.getNormal(points)

            # I_diff = K * I * [N . L]
            # K = between 0,1 - surface's reflectivity
            # N = the surface normal
            # L = Light direction

        if norm_n[2] > 0:

            #Calculating Lighting
            norm = cMath.normalize(norm_n)
            vecL_n = cMath.normalize(lightPos)

            diffuse = cMath.vecDot(norm,vecL_n)
            if diffuse < 0:
                diffuse *= -1

            newColor = (int(color[0] * diffuse * intensity),
                        int(color[1] * diffuse * intensity),
                        int(color[2] * diffuse * intensity))

            #Drawing Faces
            pygame.draw.polygon(WIN, newColor, pointsForPoly)

def applyOpertaions(verts, scale,angleX,angleY,angleZ,transform):
    finalVerts = []

    for vert in verts:
        currentVerts = vert

            # -- Multiplying by Transform Matrices
        currentVerts = cMath.matXvert(cMath.scaleMat(scale), currentVerts)
        currentVerts = cMath.matXvert(cMath.rotationMat('x', angleY), currentVerts)
        currentVerts = cMath.matXvert(cMath.rotationMat('y', angleX), currentVerts)
        currentVerts = cMath.matXvert(cMath.rotationMat('z', angleZ), currentVerts)
        currentVerts = cMath.matPvert(transform,currentVerts)
       
        currentVerts = cMath.applyPersProjection(45,1000,0.01, WIDTH/HEIGHT, currentVerts)

        finalVerts.append(currentVerts)

    return finalVerts

def main():
    # Some Variables
    isRunning = True
    clock = pygame.time.Clock()
    angle = 0.0
    fx, fy = WIDTH / 2, HEIGHT / 2
    mx, my = WIDTH / 2, HEIGHT / 2
    angleX = 0
    angleY = 0

    # Reading OBJ
    vertices, normals, faces = objLoader.loadOBJ('objects\\bicycle.obj')

    # ----- Main Game Loop -----
    while isRunning:
        #Locking to 60 FPS
        clock.tick(FPS)

        #Clearing the surface
        WIN.fill((0,0,0))

        # ----- Checking for events
        isClicked = False
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                isRunning = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                fx, fy = event.pos
            
            if event.type == pygame.MOUSEMOTION:
                mx, my = event.pos

        # Calculating the angle
        sensi = -0.5
        angleX = (fx - mx) * sensi * -1
        angleY = (fy - my) * sensi
        angleZ = 0

        angle += 1
        if angle >= 360:
            angle = 0

        #finalNormals = applyOpertaions(normals,2,angleX,angleY,0,[0,0.5,-15,0], isNormal=True)
        finalVerts = applyOpertaions(vertices, 2, angleX, angleY, angleZ, [0,0.5,-15,0])

        # Drawing vertices
        drawFaces(finalVerts, faces, (255,255,0), convertCartesian=True)
        #drawEdges(finalVerts, faces, (0,255,0), 1, convertCartesian=False)
        #drawVerts(finalVerts,(255,0,0), 3, convertCartesian=False, label=False)
        
        # Updating the window
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()