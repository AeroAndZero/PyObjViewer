import math
import numpy as np

# Normalize Vector
def normalize(vec):
    x = vec[0]
    y = vec[1]
    z = vec[2]

    mag = math.sqrt(x*x + y*y + z*z)

    if mag != 0:
        x = x / mag
        y = y / mag
        z = z / mag

    return [x,y,z,vec[3]]

# To calculate the normal to the surface
def getNormal(points):
    aX = points[0][0] - points[1][0]
    aY = points[0][1] - points[1][1]
    aZ = points[0][2] - points[1][2]

    bX = points[0][0] - points[2][0]
    bY = points[0][1] - points[2][1]
    bZ = points[0][2] - points[2][2]

    normalX = aY * bZ - aZ * bY
    normalY = aZ * bX - aX * bZ
    normalZ = aX * bY - aY * bX

    return [normalX, normalY, normalZ, 1.0]

# Dot product
def vecDot(vec1,vec2):
    result = (vec1[0] * vec2[0]) + (vec1[1] * vec2[1]) + (vec1[2] * vec2[2])
    return result

# Multiplies vertices with matrix
def matXvert(mat, verts):
   
    tempVert = [0,0,0,0]
    tempVert[0] = verts[0] * mat[0][0] + verts[1] * mat[0][1] + verts[2] * mat[0][2] + verts[3] * mat[0][3]
    tempVert[1] = verts[0] * mat[1][0] + verts[1] * mat[1][1] + verts[2] * mat[1][2] + verts[3] * mat[1][3]
    tempVert[2] = verts[0] * mat[2][0] + verts[1] * mat[2][1] + verts[2] * mat[2][2] + verts[3] * mat[2][3]
    tempVert[3] = verts[0] * mat[3][0] + verts[1] * mat[3][1] + verts[2] * mat[3][2] + verts[3] * mat[3][3]

    return tempVert

# Adding vertices with matrix
def matPvert(displace, verts):
    result = [0,0,0,0]

    result[0] = displace[0] + verts[0]
    result[1] = displace[1] + verts[1]
    result[2] = displace[2] + verts[2]
    result[3] = displace[3] + verts[3]
        
    return result

# Returns a scale matrix
def scaleMat(scale):
    result = [[scale,0,0,0],
              [0,scale,0,0],
              [0,0,scale,0],
              [0,0,0,1]]
    return result

# Orthographic Projection Matrix
def orthoMat():
    #Orthographic projection matrix
    orthoProject = [[1,0,0,0],
                    [0,1,0,0],
                    [0,0,1,0],
                    [0,0,0,1]]

    return orthoProject

# Perspective Projection Matrix
def persMat(fov, far, near, a):
    q = far / (far - near)
    f = 1 / math.tan(fov * 0.5 * math.pi / 180)

    perspectiveProject = [[1,0,0,0],
                          [0,1,0,0],
                          [0,0,1,0],
                          [0,0,0,1]]

    perspectiveProject[0][0] = f * a 
    perspectiveProject[1][1] = f
    perspectiveProject[2][2] = q
    perspectiveProject[2][3] = 1
    perspectiveProject[3][2] = -1 * q * near
    perspectiveProject[3][3] = 0

    return perspectiveProject

# Applying Perspective Projection - Attemp 6
def applyPersProjection(fov, far, near, a, verts):
    tempVerts = [0,0,0,0]

    q = far / (far - near)
    f = 1 / math.tan(fov * 0.5 * math.pi / 180)

    tempVerts[0] = (f * verts[0]) / a
    tempVerts[1] = (f * verts[1])
    tempVerts[2] = verts[2] * q - (q * near)

    if verts[2] != 0 :
        tempVerts[0] /= verts[2]
        tempVerts[1] /= verts[2]
        #tempVerts[2] /= verts[2]

    return tempVerts

# Rotation Matrix
def rotationMat(axis, angle):
    angle = math.radians(angle)
    if(axis == 'x'):
        result = [[1, 0, 0, 0],
                  [0, math.cos(angle), -1 * math.sin(angle), 0],
                  [0, math.sin(angle), math.cos(angle), 0],
                  [0, 0, 0, 1]]

    elif(axis == 'y'):
        result = [[math.cos(angle), 0, math.sin(angle), 0],
                  [0, 1, 0, 0],
                  [-1 * math.sin(angle), 0, math.cos(angle), 1],
                  [0, 0, 0, 1]]

    elif(axis == 'z'):
        result = [[math.cos(angle),-1 * math.sin(angle),0,0],
                  [math.sin(angle),math.cos(angle),0,0],
                  [0,0,1,0],
                  [0,0,0,1]]

    else:
        result = []

    return result