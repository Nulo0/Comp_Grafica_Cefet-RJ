import ctypes
import math
from array import array

import glfw
import glm
import paraboloid_geometry
from OpenGL import GL

VERTEX_SHADER = """
#version 400

layout(location=0) in vec3 attr_posicao;
uniform mat4 mvp;

void main(void)
{
    gl_Position = mvp * vec4(attr_posicao,1.0f);
}

"""
FRAGMENT_SHADER = """
#version 400

out vec4 color;

void main(void)
{
    color = vec4(1.0f);
}
"""


def compilaShaders():

    error = None
    progId = GL.glCreateProgram()

    for type, source in [(GL.GL_VERTEX_SHADER, VERTEX_SHADER), (GL.GL_FRAGMENT_SHADER, FRAGMENT_SHADER)]:
        shaderId = GL.glCreateShader(type)

        GL.glShaderSource(shaderId, [source])
        GL.glCompileShader(shaderId)

        status = GL.glGetShaderiv(shaderId, GL.GL_COMPILE_STATUS)

        if not status:
            error = GL.glGetShaderInfoLog(shaderId)
            GL.glDeleteShader(shaderId)
            break
        else:
            GL.glAttachShader(progId, shaderId)

    if error == None:
        GL.glLinkProgram(progId)

        status = GL.glGetProgramiv(progId, GL.GL_LINK_STATUS)
        if not status:
            error = GL.glGetProgramInfoLog(progId)
        else:
            return progId

    for shaderId in GL.glGetAttachedShaders(progId):
        GL.glDetachShader(progId, shaderId)
        GL.glDeleteShader(shaderId)
    GL.glDeleteProgram(progId)

    raise Exception(error)


def paraboloid():
    posicao = paraboloid_geometry.paraboloid(20, 20)

    VAO = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(VAO)
    GL.glEnableVertexAttribArray(0)  # Atributo da posicao
    VBO_posicao = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, VBO_posicao)

    GL.glBufferData(GL.GL_ARRAY_BUFFER, len(posicao)*posicao.itemsize,
                    ctypes.c_void_p(posicao.buffer_info()[0]), GL.GL_STATIC_DRAW)
    GL.glVertexAttribPointer(
        0, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, ctypes.c_void_p(0))

    return VAO


def inicializa():
    global progId, paraboloidVAO

    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glEnable(GL.GL_MULTISAMPLE)

    progId = compilaShaders()
    paraboloidVAO = paraboloid()


a = 0


def desenha():
    global a
    GL.glClearColor(0.0, 0.0, 0.0, 1.0)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

    projection = glm.perspective(math.pi/4, 800/600, 0.1, 100)
    camera = glm.lookAt(glm.vec3(0, 2, 8), glm.vec3(
        0, 0, 0), glm.vec3(0, 1, 0))
    model = glm.rotate(a, glm.vec3(0, 1, 0))
    mvp = projection * camera * model

    GL.glBindVertexArray(paraboloidVAO)
    GL.glUseProgram(progId)
    GL.glUniformMatrix4fv(GL.glGetUniformLocation(
        progId, "mvp"), 1, GL.GL_FALSE, glm.value_ptr(mvp))
    GL.glDrawArrays(GL.GL_POINTS, 0, 400)

    a += 0.00005


def main():

    if not glfw.init():
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
    glfw.window_hint(glfw.SAMPLES, 4)

    window = glfw.create_window(800, 600, "Paraboloid", None, None)

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
