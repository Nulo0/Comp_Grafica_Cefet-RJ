"""
Grupo: Daniel Pedro, Gabriel Alves, Vinícius Alves
"""

import ctypes
import math
from array import array

import glfw
import glm
from PIL import Image

from OpenGL import GL

VERTEX_SHADER = """
#version 400

layout (location=0) in vec3 attr_posicao;
layout (location=1) in vec2 textura;

uniform mat4 mvp;
out vec2 fsTextura;

void main(void) 
{
    fsTextura = textura;
    gl_Position = mvp * vec4(attr_posicao,1.0f);
}
"""

FRAGMENT_SHADER = """
#version 400

uniform sampler2D textureSlot;
in vec2 fsTextura;
out vec4 color;

void main(void) 
{
    color = texture(textureSlot,fsTextura);
}
"""
def compilaShaders():
    error = None
    progId = GL.glCreateProgram()
    for type, source in [ (GL.GL_VERTEX_SHADER, VERTEX_SHADER), (GL.GL_FRAGMENT_SHADER, FRAGMENT_SHADER) ]:
        shaderId = GL.glCreateShader(type)
        GL.glShaderSource(shaderId,[source])
        GL.glCompileShader(shaderId)
        status = GL.glGetShaderiv(shaderId,GL.GL_COMPILE_STATUS)
        if not status:
            error = GL.glGetShaderInfoLog(shaderId)
            GL.glDeleteShader(shaderId)
            break
        else:
            GL.glAttachShader(progId,shaderId)
    if error == None:
        GL.glLinkProgram(progId)
        status = GL.glGetProgramiv(progId,GL.GL_LINK_STATUS)
        if not status:
            error = GL.glGetProgramInfoLog(progId)
        else:
            return progId
    for shaderId in GL.glGetAttachedShaders(progId):
        GL.glDetachShader(progId, shaderId)
        GL.glDeleteShader(shaderId)
    GL.glDeleteProgram(progId)
    raise Exception(error)

def cubo():

    A = (1.0, -1.0,  1.0)
    B = (1.0, 1.0,  1.0)
    C = (-1.0,  1.0,  1.0)
    D = (-1.0,  -1.0,  1.0)
    E = (1.0, -1.0, -1.0)
    F = (1.0, 1.0, -1.0)
    G = (-1.0,  1.0, -1.0)
    H = (-1.0,  -1.0, -1.0)

    posicao = array('f',[
        *A,*B,*D,*D,*B,*C, # 1
        *E,*F,*A,*A,*F,*B, # 2
        *H,*G,*E,*E,*G,*F, # 3
        *D,*C,*H,*H,*C,*G, # 4
        *B,*F,*C,*C,*F,*G, # 5
        *A,*E,*D,*D,*E,*H # 6
    ])

    f1 = (1/3, 1/2, 1/3, 1.0, 0.0, 1/2, 0.0, 1/2, 1/3, 1.0, 0.0, 1.0)
    f2 = (2/3, 1/2, 2/3, 1.0, 1/3, 1/2, 1/3, 1/2, 2/3, 1.0, 1/3, 1.0)
    f3 = (1.0, 1/2, 1.0, 1.0, 2/3, 1/2, 2/3, 1/2, 1.0, 1.0, 2/3, 1.0)
    f4 = (1/3, 0.0, 1/3, 1/2, 0.0, 0.0, 0.0, 0.0, 1/3, 1/2, 0.0, 1/2)
    f5 = (2/3, 0.0, 2/3, 1/2, 1/3, 0.0, 1/3, 0.0, 2/3, 1/2, 1/3, 1/2)
    f6 = (1.0, 0.0, 1.0, 1/2, 2/3, 0.0, 2/3, 0.0, 1.0, 1/2, 2/3, 1/2)

    texture = array('f',[
        *f1,
        *f2,
        *f3,
        *f4,
        *f5,
        *f6
    ])


    VAO = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(VAO)
    GL.glEnableVertexAttribArray(0) # Atributo da posicao
    GL.glEnableVertexAttribArray(1) # Atributo da cor

    VBO_posicao = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, VBO_posicao)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, len(posicao)*posicao.itemsize, ctypes.c_void_p(posicao.buffer_info()[0]), GL.GL_STATIC_DRAW)
    GL.glVertexAttribPointer(0,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))

    VBO_textura = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, VBO_textura)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, len(texture)*texture.itemsize, ctypes.c_void_p(texture.buffer_info()[0]), GL.GL_STATIC_DRAW)
    GL.glVertexAttribPointer(1,2,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))

    return VAO

def loadTexture(filename):
    im = Image.open(filename)
    w, h = im.size
    if(im.mode == "RGBA"):
        modo = GL.GL_RGBA
        data = im.tobytes("raw", "RGBA", 0, -1)
    else:
        modo = GL.GL_RGB
        data = im.tobytes("raw", "RGB", 0, -1)
    textureId = GL.glGenTextures(1)
    GL.glBindTexture(GL.GL_TEXTURE_2D, textureId)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, modo, w, h, 0, modo,GL. GL_UNSIGNED_BYTE, data)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
    return textureId

def inicializa():
    global progId, cuboVAO
    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glEnable(GL.GL_MULTISAMPLE)
    progId = compilaShaders()
    cuboVAO = cubo()
    GL.glUseProgram(progId)
    GL.glActiveTexture(GL.GL_TEXTURE0)
    loadTexture("./textures/dado.png")
    GL.glUniform1i(GL.glGetUniformLocation(progId, "textureSlot"),0)


a = 0
def desenha():
    global a
    GL.glClearColor(0.0, 0.0, 0.0, 1.0)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)

    projection = glm.perspective(math.pi/4,800/600,0.1,100)
    camera = glm.lookAt(glm.vec3(0,2,8),glm.vec3(0,0,0),glm.vec3(0,1,0))
    model = glm.rotate(a,glm.vec3(0,1,0))*glm.rotate(a,glm.vec3(1,0,0))
    mvp = projection * camera * model

    GL.glBindVertexArray(cuboVAO)
    GL.glUseProgram(progId)
    GL.glUniformMatrix4fv(GL.glGetUniformLocation(progId, "mvp"),1,GL.GL_FALSE,glm.value_ptr(mvp))
    GL.glDrawArrays(GL.GL_TRIANGLES,0,36)

    a += 0.0001


def main():
    if not glfw.init():
        return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
    glfw.window_hint(glfw.SAMPLES, 4)
    window = glfw.create_window(800, 600, "Cubo", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    inicializa()
    while not glfw.window_should_close(window):
        desenha()
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
