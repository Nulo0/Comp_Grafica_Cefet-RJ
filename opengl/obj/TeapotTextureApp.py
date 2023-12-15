from numpy import indices
from GLAPP import GLAPP
from OpenGL import GL
from array import array
import ctypes
import glm
import math
a = 0

class TeapotTextureApp(GLAPP):

    def setup(self):
        # Window setup
        self.title("Teapot With Texture")
        self.size(1100,1100)

        # OpenGL Initialization
        GL.glClearColor(0.2, 0.2, 0.2, 0.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_MULTISAMPLE)

        # Pipeline (shaders)
        self.pipeline = self.loadPipeline("SimpleTexture")
        GL.glUseProgram(self.pipeline)

        # Texture
        GL.glActiveTexture(GL.GL_TEXTURE0)
        self.loadTexture("./textures/uv_grid_opengl.png")
        GL.glUniform1i(GL.glGetUniformLocation(self.pipeline, "textureSlot"),0)

        self.arrayBufferId = None

    def drawTeapot(self):
        global a
        if self.arrayBufferId == None:

            vertices, uvs, normals, indices = teapotGeometry(4)

            self.arrayBufferId = GL.glGenVertexArrays(1)
            self.N = len(indices)

            GL.glBindVertexArray(self.arrayBufferId)
            GL.glEnableVertexAttribArray(0)
            GL.glEnableVertexAttribArray(1)
            
            idVertexBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idVertexBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(vertices)*vertices.itemsize, ctypes.c_void_p(vertices.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(0,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))

            idTextureBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idTextureBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(uvs)*uvs.itemsize, ctypes.c_void_p(uvs.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(1,2,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))

            idIndex = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, idIndex)
            GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, len(indices)*indices.itemsize, ctypes.c_void_p(indices.buffer_info()[0]), GL.GL_STATIC_DRAW)

        projection = glm.perspective(math.pi/4,self.width/self.height,0.1,100)
        camera = glm.lookAt(glm.vec3(0,0,20),glm.vec3(0),glm.vec3(0,1,0))
        model = glm.rotate(a,glm.vec3(0,0,1)) * glm.rotate(a,glm.vec3(0,1,0)) * glm.rotate(a,glm.vec3(1,0,0)) 
        mvp = projection * camera * model
        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.pipeline, "MVP"),1,GL.GL_FALSE,glm.value_ptr(mvp))
        GL.glBindVertexArray(self.arrayBufferId)
        GL.glDrawElements(GL.GL_TRIANGLES, self.N, GL.GL_UNSIGNED_INT, ctypes.c_void_p(0))
        a += 0.005

    def draw(self):
        # clear screen and depth buffer
        GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)
        # Draw a Triangle
        self.drawTeapot()


def teapotGeometry(size=5,segments=10,bottom=True,lid=True,body=True,fitLid=True,blinn=True):

    teapotPatches = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 3, 16, 17, 18, 7, 19, 20, 21, 11, 22, 23, 24, 15, 25, 26, 27, 18, 28, 29, 30, 21, 31, 32, 33, 24, 34, 35, 36, 27, 37, 38, 39, 30, 40, 41, 0, 33, 42, 43, 4, 36, 44, 45, 8, 39, 46, 47, 12,
        12, 13, 14, 15, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 15, 25, 26, 27, 51, 60, 61, 62, 55, 63, 64, 65, 59, 66, 67, 68, 27, 37, 38, 39, 62, 69, 70, 71, 65, 72, 73, 74, 68, 75, 76, 77, 39, 46, 47, 12, 71, 78, 79, 48, 74, 80, 81, 52, 77, 82, 83, 56, 56, 57, 58, 59, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 59, 66, 67, 68, 87, 96, 97, 98, 91, 99, 100, 101, 95, 102, 103, 104, 68, 75, 76, 77, 98, 105, 106, 107, 101, 108, 109, 110, 104, 111, 112, 113, 77, 82, 83, 56, 107, 114, 115, 84, 110, 116, 117, 88, 113, 118, 119, 92,
        120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 123, 136, 137, 120, 127, 138, 139, 124, 131, 140, 141, 128, 135, 142, 143, 132, 132, 133, 134, 135, 144, 145, 146, 147, 148, 149, 150, 151, 68, 152, 153, 154, 135, 142, 143, 132, 147, 155, 156, 144, 151, 157, 158, 148, 154, 159, 160, 68,
        161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 164, 177, 178, 161, 168, 179, 180, 165, 172, 181, 182, 169, 176, 183, 184, 173, 173, 174, 175, 176, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 176, 183, 184, 173, 188, 197, 198, 185, 192, 199, 200, 189, 196, 201, 202, 193,
        203, 203, 203, 203, 204, 205, 206, 207, 208, 208, 208, 208, 209, 210, 211, 212, 203, 203, 203, 203, 207, 213, 214, 215, 208, 208, 208, 208, 212, 216, 217, 218, 203, 203, 203, 203, 215, 219, 220, 221, 208, 208, 208, 208, 218, 222, 223, 224, 203, 203, 203, 203, 221, 225, 226, 204, 208, 208, 208, 208, 224, 227, 228, 209, 209, 210, 211, 212, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 212, 216, 217, 218, 232, 241, 242, 243, 236, 244, 245, 246, 240, 247, 248, 249, 218, 222, 223, 224, 243, 250, 251, 252, 246, 253, 254, 255, 249, 256, 257, 258, 224, 227, 228, 209, 252, 259, 260, 229, 255, 261, 262, 233, 258, 263, 264, 237,
        265, 265, 265, 265, 266, 267, 268, 269, 270, 271, 272, 273, 92, 119, 118, 113, 265, 265, 265, 265, 269, 274, 275, 276, 273, 277, 278, 279, 113, 112, 111, 104, 265, 265, 265, 265, 276, 280, 281, 282, 279, 283, 284, 285, 104, 103, 102, 95, 265, 265, 265, 265, 282, 286, 287, 266, 285, 288, 289, 270, 95, 94, 93, 92 
    ]

    teapotVertices = [ 
        1.4, 0, 2.4, 1.4, - 0.784, 2.4, 0.784, - 1.4, 2.4, 0, - 1.4, 2.4, 1.3375, 0, 2.53125, 1.3375, - 0.749, 2.53125, 0.749, - 1.3375, 2.53125, 0, - 1.3375, 2.53125, 1.4375, 0, 2.53125, 1.4375, - 0.805, 2.53125, 0.805, - 1.4375, 2.53125, 0, - 1.4375, 2.53125, 1.5, 0, 2.4, 1.5, - 0.84, 2.4, 0.84, - 1.5, 2.4, 0, - 1.5, 2.4, - 0.784, - 1.4, 2.4, - 1.4, - 0.784, 2.4, - 1.4, 0, 2.4, - 0.749, - 1.3375, 2.53125, - 1.3375, - 0.749, 2.53125, - 1.3375, 0, 2.53125, - 0.805, - 1.4375, 2.53125, - 1.4375, - 0.805, 2.53125, - 1.4375, 0, 2.53125, - 0.84, - 1.5, 2.4, - 1.5, - 0.84, 2.4, - 1.5, 0, 2.4, - 1.4, 0.784, 2.4, - 0.784, 1.4, 2.4, 0, 1.4, 2.4, - 1.3375, 0.749, 2.53125, - 0.749, 1.3375, 2.53125, 0, 1.3375, 2.53125, - 1.4375, 0.805, 2.53125, - 0.805, 1.4375, 2.53125, 0, 1.4375, 2.53125, - 1.5, 0.84, 2.4, - 0.84, 1.5, 2.4, 0, 1.5, 2.4, 0.784, 1.4, 2.4, 1.4, 0.784, 2.4, 0.749, 1.3375, 2.53125, 1.3375, 0.749, 2.53125, 0.805, 1.4375, 2.53125, 1.4375, 0.805, 2.53125, 0.84, 1.5, 2.4, 1.5, 0.84, 2.4, 1.75, 0, 1.875, 1.75, - 0.98, 1.875, 0.98, - 1.75, 1.875, 0, - 1.75, 1.875, 2, 0, 1.35, 2, - 1.12, 1.35, 1.12, - 2, 1.35, 0, - 2, 1.35, 2, 0, 0.9, 2, - 1.12, 0.9, 1.12, - 2, 0.9, 0, - 2, 0.9, - 0.98, - 1.75, 1.875, - 1.75, - 0.98, 1.875, - 1.75, 0, 1.875, - 1.12, - 2, 1.35, - 2, - 1.12, 1.35, - 2, 0, 1.35, - 1.12, - 2, 0.9, - 2, - 1.12, 0.9, - 2, 0, 0.9, - 1.75, 0.98, 1.875, - 0.98, 1.75, 1.875, 0, 1.75, 1.875, - 2, 1.12, 1.35, - 1.12, 2, 1.35, 0, 2, 1.35, - 2, 1.12, 0.9, - 1.12, 2, 0.9, 0, 2, 0.9, 0.98, 1.75, 1.875, 1.75, 0.98, 1.875, 1.12, 2, 1.35, 2, 1.12, 1.35, 1.12, 2, 0.9, 2, 1.12, 0.9, 2, 0, 0.45, 2, - 1.12, 0.45, 1.12, - 2, 0.45, 0, - 2, 0.45, 1.5, 0, 0.225, 1.5, - 0.84, 0.225, 0.84, - 1.5, 0.225, 0, - 1.5, 0.225, 1.5, 0, 0.15, 1.5, - 0.84, 0.15, 0.84, - 1.5, 0.15, 0, - 1.5, 0.15, - 1.12, - 2, 0.45, - 2, - 1.12, 0.45, - 2, 0, 0.45, - 0.84, - 1.5, 0.225, - 1.5, - 0.84, 0.225, - 1.5, 0, 0.225, - 0.84, - 1.5, 0.15, - 1.5, - 0.84, 0.15, - 1.5, 0, 0.15, - 2, 1.12, 0.45, - 1.12, 2, 0.45, 0, 2, 0.45, - 1.5, 0.84, 0.225, - 0.84, 1.5, 0.225, 0, 1.5, 0.225, - 1.5, 0.84, 0.15, - 0.84, 1.5, 0.15, 0, 1.5, 0.15, 1.12, 2, 0.45, 2, 1.12, 0.45, 0.84, 1.5, 0.225, 1.5, 0.84, 0.225, 0.84, 1.5, 0.15, 1.5, 0.84, 0.15, - 1.6, 0, 2.025, - 1.6, - 0.3, 2.025, - 1.5, - 0.3, 2.25, - 1.5, 0, 2.25, - 2.3, 0, 2.025, - 2.3, - 0.3, 2.025, - 2.5, - 0.3, 2.25, - 2.5, 0, 2.25, - 2.7, 0, 2.025, - 2.7, - 0.3, 2.025, - 3, - 0.3, 2.25, - 3, 0, 2.25, - 2.7, 0, 1.8, - 2.7, - 0.3, 1.8, - 3, - 0.3, 1.8, - 3, 0, 1.8, - 1.5, 0.3, 2.25, - 1.6, 0.3, 2.025, - 2.5, 0.3, 2.25, - 2.3, 0.3, 2.025, - 3, 0.3, 2.25, - 2.7, 0.3, 2.025, - 3, 0.3, 1.8, - 2.7, 0.3, 1.8, - 2.7, 0, 1.575, - 2.7, - 0.3, 1.575, - 3, - 0.3, 1.35, - 3, 0, 1.35, - 2.5, 0, 1.125, - 2.5, - 0.3, 1.125, - 2.65, - 0.3, 0.9375, - 2.65, 0, 0.9375, - 2, - 0.3, 0.9, - 1.9, - 0.3, 0.6, - 1.9, 0, 0.6, - 3, 0.3, 1.35, - 2.7, 0.3, 1.575, - 2.65, 0.3, 0.9375, - 2.5, 0.3, 1.125, - 1.9, 0.3, 0.6, - 2, 0.3, 0.9, 1.7, 0, 1.425, 1.7, - 0.66, 1.425, 1.7, - 0.66, 0.6, 1.7, 0, 0.6, 2.6, 0, 1.425, 2.6, - 0.66, 1.425, 3.1, - 0.66, 0.825, 3.1, 0, 0.825, 2.3, 0, 2.1, 2.3, - 0.25, 2.1, 2.4, - 0.25, 2.025, 2.4, 0, 2.025, 2.7, 0, 2.4, 2.7, - 0.25, 2.4, 3.3, - 0.25, 2.4, 3.3, 0, 2.4, 1.7, 0.66, 0.6, 1.7, 0.66, 1.425, 3.1, 0.66, 0.825, 2.6, 0.66, 1.425, 2.4, 0.25, 2.025, 2.3, 0.25, 2.1, 3.3, 0.25, 2.4, 2.7, 0.25, 2.4, 2.8, 0, 2.475, 2.8, - 0.25, 2.475, 3.525, - 0.25, 2.49375, 3.525, 0, 2.49375, 2.9, 0, 2.475, 2.9, - 0.15, 2.475, 3.45, - 0.15, 2.5125, 3.45, 0, 2.5125, 2.8, 0, 2.4, 2.8, - 0.15, 2.4, 3.2, - 0.15, 2.4, 3.2, 0, 2.4, 3.525, 0.25, 2.49375, 2.8, 0.25, 2.475, 3.45, 0.15, 2.5125, 2.9, 0.15, 2.475, 3.2, 0.15, 2.4, 2.8, 0.15, 2.4, 0, 0, 3.15, 0.8, 0, 3.15, 0.8, - 0.45, 3.15, 0.45, - 0.8, 3.15, 0, - 0.8, 3.15, 0, 0, 2.85, 0.2, 0, 2.7, 0.2, - 0.112, 2.7, 0.112, - 0.2, 2.7, 0, - 0.2, 2.7, - 0.45, - 0.8, 3.15, - 0.8, - 0.45, 3.15, - 0.8, 0, 3.15, - 0.112, - 0.2, 2.7, - 0.2, - 0.112, 2.7, - 0.2, 0, 2.7, - 0.8, 0.45, 3.15, - 0.45, 0.8, 3.15, 0, 0.8, 3.15, - 0.2, 0.112, 2.7, - 0.112, 0.2, 2.7, 0, 0.2, 2.7, 0.45, 0.8, 3.15, 0.8, 0.45, 3.15, 0.112, 0.2, 2.7, 0.2, 0.112, 2.7, 0.4, 0, 2.55, 0.4, - 0.224, 2.55, 0.224, - 0.4, 2.55, 0, - 0.4, 2.55, 1.3, 0, 2.55, 1.3, - 0.728, 2.55, 0.728, - 1.3, 2.55, 0, - 1.3, 2.55, 1.3, 0, 2.4, 1.3, - 0.728, 2.4, 0.728, - 1.3, 2.4, 0, - 1.3, 2.4, - 0.224, - 0.4, 2.55, - 0.4, - 0.224, 2.55, - 0.4, 0, 2.55, - 0.728, - 1.3, 2.55, - 1.3, - 0.728, 2.55, - 1.3, 0, 2.55, - 0.728, - 1.3, 2.4, - 1.3, - 0.728, 2.4, - 1.3, 0, 2.4, - 0.4, 0.224, 2.55, - 0.224, 0.4, 2.55, 0, 0.4, 2.55, - 1.3, 0.728, 2.55, - 0.728, 1.3, 2.55, 0, 1.3, 2.55, - 1.3, 0.728, 2.4, - 0.728, 1.3, 2.4, 0, 1.3, 2.4, 0.224, 0.4, 2.55, 0.4, 0.224, 2.55, 0.728, 1.3, 2.55, 1.3, 0.728, 2.55, 0.728, 1.3, 2.4, 1.3, 0.728, 2.4, 0, 0, 0, 1.425, 0, 0, 1.425, 0.798, 0, 0.798, 1.425, 0, 0, 1.425, 0, 1.5, 0, 0.075, 1.5, 0.84, 0.075, 0.84, 1.5, 0.075, 0, 1.5, 0.075, - 0.798, 1.425, 0, - 1.425, 0.798, 0, - 1.425, 0, 0, - 0.84, 1.5, 0.075, - 1.5, 0.84, 0.075, - 1.5, 0, 0.075, - 1.425, - 0.798, 0, - 0.798, - 1.425, 0, 0, - 1.425, 0, - 1.5, - 0.84, 0.075, - 0.84, - 1.5, 0.075, 0, - 1.5, 0.075, 0.798, - 1.425, 0, 1.425, - 0.798, 0, 0.84, - 1.5, 0.075, 1.5, - 0.84, 0.075 
    ]

    segments = max( 2, math.floor( segments ) )
    blinnScale = 1.3
    maxHeight = 3.15 * ( 1 if blinn else blinnScale )
    maxHeight2 = maxHeight / 2
    trueSize = size / maxHeight2
    numTriangles = ( 8 * segments - 4 ) * segments if bottom else 0
    numTriangles += ( 16 * segments - 4 ) * segments if lid else 0
    numTriangles += 40 * segments * segments if body else 0

    numVertices = 4 if bottom else 0
    numVertices += 8 if lid else 0
    numVertices += 20 if body else 0
    numVertices *= ( segments + 1 ) * ( segments + 1 )

    vertices = array("f")
    normals = array("f")
    uvs = array("f")
    indices = array("I")

    ms = glm.mat4( -1.0, 3.0, -3.0, 1.0, 3.0, -6.0, 3.0, 0.0, -3.0, 3.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0 )
    mst = glm.transpose(ms)
    mgm = [None]*4

    def notDegenerate(vtx1, vtx2, vtx3):
        return not( vertices[ vtx1 * 3 ] == vertices[ vtx2 * 3 ] and vertices[ vtx1 * 3 + 1 ] == vertices[ vtx2 * 3 + 1 ] and vertices[ vtx1 * 3 + 2 ] == vertices[ vtx2 * 3 + 2 ] or vertices[ vtx1 * 3 ] == vertices[ vtx3 * 3 ] and vertices[ vtx1 * 3 + 1 ] == vertices[ vtx3 * 3 + 1 ] and vertices[ vtx1 * 3 + 2 ] == vertices[ vtx3 * 3 + 2 ] or vertices[ vtx2 * 3 ] == vertices[ vtx3 * 3 ] and vertices[ vtx2 * 3 + 1 ] == vertices[ vtx3 * 3 + 1 ] and vertices[ vtx2 * 3 + 2 ] == vertices[ vtx3 * 3 + 2 ] )

    minPatches = 0 if body else 20
    maxPatches = 32 if bottom else 28
    vertPerRow = segments + 1
    surfCount = 0

    for surf in range(minPatches, maxPatches):
        if lid or surf < 20 or surf >= 28:
            for i in range(0,3):
                gmx = glm.mat4()
                for r in range(0,4):
                    for c in range(0,4):
                        gmx[c][r] = teapotVertices[ teapotPatches[ surf * 16 + r * 4 + c ] * 3 + i ]
                        if fitLid and surf >= 20 and surf < 28 and i != 2:
                            gmx[c][r] *= 1.077
                        if not blinn and i == 2:
                            gmx[c][r] *= blinnScale
                mgm[i]=mst*gmx*ms
            for sstep in range(0,segments+1):
                s = sstep/segments
                for tstep in range(0,segments+1):
                    t = tstep/segments
                    sval = tval= 1.0
                    vsp = glm.vec4()
                    vtp = glm.vec4()
                    vdsp = glm.vec4()
                    vdtp = glm.vec4()
                    for p in range(3,-1,-1):
                        vsp[p] = sval
                        vtp[p] = tval
                        sval *= s
                        tval *= t
                        if p == 3:
                            vdsp[p] = vdtp[p] = 0.0
                            dsval = dtval = 1.0
                        else:
                            vdsp[p] = dsval*(3-p)
                            vdtp[p] = dtval*(3-p)
                            dsval *= s
                            dtval *= t
                    vert = glm.vec3()
                    vsdir = glm.vec3()
                    vtdir = glm.vec3()
                    for i in range(0,3):
                        vert[i] = glm.dot(vsp*mgm[i],vtp)
                        vsdir[i] = glm.dot(vdsp*mgm[i],vtp)
                        vtdir[i] = glm.dot(vsp*mgm[i],vdtp)
                    norm = glm.normalize(glm.cross(vtdir,vsdir))
                    if vert[0] == 0 and vert[1] == 0:
                        normOut = glm.vec3(0, 1 if vert[2] > maxHeight2 else - 1, 0 )
                    else:
                        normOut = glm.vec3(norm.x,norm.z,-norm.y)
                    vertices.append(trueSize*vert[0])
                    vertices.append(trueSize*(vert[2]-maxHeight2))
                    vertices.append(-trueSize*vert[1])
                    normals.append(normOut.x)
                    normals.append(normOut.y)
                    normals.append(normOut.z)
                    uvs.append(1-t)
                    uvs.append(1-s)

            for sstep in range(0,segments):
                for tstep in range(0,segments):
                    v1 = surfCount * vertPerRow * vertPerRow + sstep * vertPerRow + tstep
                    v2 = v1 + 1
                    v3 = v2 + vertPerRow
                    v4 = v1 + vertPerRow
                    if notDegenerate(v1,v2,v3):
                        indices.append(v1)
                        indices.append(v2)
                        indices.append(v3)
                    if notDegenerate(v1,v3,v4):
                        indices.append(v1)
                        indices.append(v3)
                        indices.append(v4)
            surfCount+=1
    return vertices, uvs, normals, indices

TeapotTextureApp()
