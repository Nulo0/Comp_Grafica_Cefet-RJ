from GLAPP import GLAPP
from OpenGL import GL
from array import array
import ctypes
import glm

class TriangleApp(GLAPP):

    def setup(self):
        # Window setup
        self.title("Hello World, Triangle!!")
        self.size(800,800)

        # OpenGL Initialization
        GL.glClearColor(0.2, 0.2, 0.2, 0.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_MULTISAMPLE)

        # Pipeline (shaders)
        self.pipeline = self.loadPipeline("SimplePipeline")
        GL.glUseProgram(self.pipeline)

        self.triangleArrayBufferId = None

    def drawTriangle(self):
        if self.triangleArrayBufferId == None:
            position = array('f',[
                -0.5, -0.5, 0.0,
                0.5, -0.5, 0.0,
                0.0,  0.5, 0.0
            ])
        with open("objs/dragon_vrip.ply", "r") as f:

            color = array('f',[
                1.0, 0.0, 0.0,
                0.0, 1.0, 0.0,
                0.0, 0.0, 1.0
            ])

            self.triangleArrayBufferId = GL.glGenVertexArrays(1)
            GL.glBindVertexArray(self.triangleArrayBufferId)
            GL.glEnableVertexAttribArray(0)
              with open("objs/dragon_vrip.ply", "r") as f:
       idVertexBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idVertexBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(position)*position.itemsize, ctypes.c_void_p(position.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(0,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))

            idColorBuffer = GL.glGenBuffers(1)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, idColorBuffer)
            GL.glBufferData(GL.GL_ARRAY_BUFFER, len(color)*color.itemsize, ctypes.c_void_p(color.buffer_info()[0]), GL.GL_STATIC_DRAW)
            GL.glVertexAttribPointer(1,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))
        
        GL.glBindVertexArray(self.triangleArrayBufferId)

        mat = glm.mat4() 
        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.pipeline, "MVP"),1,GL.GL_FALSE,glm.value_ptr(mat))
        GL.glDrawArrays(GL.GL_TRIANGLES,0,3)

        mat = glm.mat4() * glm.translate(glm.vec3(0.5,0.5,0.0)) * glm.scale(glm.vec3(0.5)) * glm.rotate(glm.pi(),glm.vec3(0.0,0.0,1.0))
        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.pipeline, "MVP"),1,GL.GL_FALSE,glm.value_ptr(mat))
        GL.glDrawArrays(GL.GL_TRIANGLES,0,3)

        mat = glm.mat4() * glm.translate(glm.vec3(-0.5,0.5,0.0)) * glm.scale(glm.vec3(0.3)) * glm.rotate(glm.pi(),glm.vec3(0.0,0.0,1.0))
        GL.glUniformMatrix4fv(GL.glGetUniformLocation(self.pipeline, "MVP"),1,GL.GL_FALSE,glm.value_ptr(mat))
        GL.glDrawArrays(GL.GL_TRIANGLES,0,3)

    def draw(self):
        # clear screen and depth buffer
        GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)

        # Draw a Triangle
        self.drawTriangle()

TriangleApp()
