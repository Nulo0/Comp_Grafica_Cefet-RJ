from OpenGL import GL
from array import array
import ctypes
import glfw

VERTEX_SHADER = """
#version 400

in vec3 position;

void main(void) 
{
    gl_Position = vec4(position,1.0f);
}
"""

FRAGMENT_SHADER = """
#version 400

out vec4 color;

void main(void) 
{
    color = vec4(1.0f,0.5f,0.0f,1.0f);
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

def triangulo(): 
    posicao = array('f',[
        -0.5, -0.5, 0.0, 
        0.5,  -0.5, 0.0,
        0.0, 0.5, 0.0
    ])

    VAO = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(VAO)
    GL.glEnableVertexAttribArray(0)

    VBO = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, VBO)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, len(posicao)*posicao.itemsize, ctypes.c_void_p(posicao.buffer_info()[0]), GL.GL_STATIC_DRAW)
    GL.glVertexAttribPointer(0,3,GL.GL_FLOAT,GL.GL_FALSE,0,ctypes.c_void_p(0))
    return VAO

def inicializa():
    global progId, trianguloVAO
    progId = compilaShaders()
    trianguloVAO = triangulo()

def desenha():
    GL.glClearColor(0.2, 0.3, 0.3, 1.0)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)
    GL.glUseProgram(progId)
    GL.glBindVertexArray(trianguloVAO)
    GL.glDrawArrays(GL.GL_TRIANGLES,0,3)

def main():
    if not glfw.init():
        return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
    window = glfw.create_window(800, 600, "Hello World", None, None)
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
