def loadOBJ(filepath):
    vertices = []
    normals = []
    faces = []

    with open(filepath, 'r') as f:
        for line in f.readlines():
            lineArray = line.split(' ')
            
            if lineArray[0] == 'v':
                vertices.append([ float(lineArray[1]), float(lineArray[2]), float(lineArray[3]) , 1.0])

            if lineArray[0] == 'vn':
                normals.append([ float(lineArray[1]), float(lineArray[2]), float(lineArray[3]) , 1.0])

            if lineArray[0] == 'f':
                faces.append( [[int(x) - 1 for x in lineArray[1].split('/')] , [int(x) - 1 for x in lineArray[2].split('/')], [int(x) - 1 for x in lineArray[3].split('/')] ])
         
    return vertices, normals, faces
