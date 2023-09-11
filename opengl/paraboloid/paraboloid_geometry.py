import array
import math

ValorM = 0
ValorN = 50


def mapP5(valor, a, b, c, d):
    return (valor-a)/(b-a)*(d-c)+c


def paraboloid(m=ValorM, n=ValorN):

    vertex = array.array('f')

    for i in range(m):
        x = mapP5(i, 0, m, 0, 2)
        # mapP5(i,0,m,-math.pi/2,math.pi/2)
        for j in range(n):
            phi = j*2*math.pi/n

            Qx = x * math.cos(phi)
            Qy = x * x
            Qz = x * math.sin(phi)

            vertex.append(Qx)
            vertex.append(Qy)
            vertex.append(Qz)
    return vertex
