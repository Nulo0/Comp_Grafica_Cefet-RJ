from abc import ABC, abstractmethod
import ctypes
import sdl2
from OpenGL import GL
from PIL import Image
import os

# TODO Desalocar os objetos criados
# TODO Implementar os modelos de ilumunação

# https://www.khronos.org/opengles/sdk/tools/Reference-Compiler/

shaderExtensions = {
    "vert" : GL.GL_VERTEX_SHADER, 
    "tesc" : GL.GL_TESS_CONTROL_SHADER, 
    "tese" : GL.GL_TESS_EVALUATION_SHADER, 
    "geom" : GL.GL_GEOMETRY_SHADER, 
    "frag" : GL.GL_FRAGMENT_SHADER, 
    "comp" : GL.GL_COMPUTE_SHADER
}

class GLAPP(ABC):
    def __init__(self):
        self.width = 800
        self.height = 800
        self.frameCount = 0
        self.mouseX = 0
        self.mouseY = 0
        self.pmouseX = 0
        self.pmouseY = 0
        self.mouseLeftPressed = False
        self.mouseRightPressed = False
        self.mouseMiddlePressed = False
        self.mousePressed = False
        sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION, 4)
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION, 0)        
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_PROFILE_MASK,sdl2.SDL_GL_CONTEXT_PROFILE_CORE)
        self.window = sdl2.SDL_CreateWindow("Gráficos".encode("utf-8"), sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED, self.width, self.height, sdl2.SDL_WINDOW_OPENGL | sdl2.SDL_WINDOW_RESIZABLE | sdl2.SDL_WINDOW_HIDDEN)
        if not self.window:
            raise Exception("Error: Could not create window")
        self.glContext = sdl2.SDL_GL_CreateContext(self.window)
        print(GL.glGetString(GL.GL_VENDOR))
        self.setup()
        sdl2.SDL_SetWindowPosition(self.window, sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED)
        sdl2.SDL_ShowWindow(self.window)
        running = True
        event = sdl2.SDL_Event()
        while running:
            while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
                if event.type == sdl2.SDL_QUIT:
                    running = False
                if event.type == sdl2.events.SDL_KEYDOWN:
                    if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                        running = False
                if event.type == sdl2.SDL_WINDOWEVENT and event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                    self.width = event.window.data1
                    self.height = event.window.data2
                    GL.glViewport(0,0,self.width,self.height)
                    self.windowResize(self.width,self.height)
            mx = ctypes.c_int(0)
            my = ctypes.c_int(0)
            status = sdl2.SDL_GetMouseState(ctypes.byref(mx),ctypes.byref(my))
            self.pmouseX = self.mouseX
            self.pmouseY = self.mouseY
            self.mouseX = mx.value
            self.mouseY = my.value
            self.mouseLeftPressed = status & sdl2.SDL_BUTTON_LMASK
            self.mouseRightPressed = status & sdl2.SDL_BUTTON_RMASK
            self.mouseMiddlePressed = status & sdl2.SDL_BUTTON_MMASK
            self.mousePressed = self.mouseLeftPressed or self.mouseRightPressed or self.mouseMiddlePressed
            # Show debug information in terminal
            print(f"\033[0G\033[0KMouse: \033[1;36m{self.mouseX}, {self.mouseY}\033[0m\tFrameCount: \033[1;31m{self.frameCount}\033[0m  ",end="",flush=True)
            self.draw()
            sdl2.SDL_GL_SwapWindow(self.window)
            self.frameCount += 1

    def title(self, newTitle):
        sdl2.SDL_SetWindowTitle(self.window, newTitle.encode("utf-8"))

    def size(self, w, h):
        sdl2.SDL_SetWindowSize(self.window, w, h)
        self.width = w
        self.height = h
        GL.glViewport(0,0,w,h)

    def compilePipeline(self, shaders):
        error = None
        progId = GL.glCreateProgram()
        for type, source in shaders.items():
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

    def loadPipeline(self, pipelineName):
        shaders = {}
        for extension, type in shaderExtensions.items():
            diretorio = os.getcwd()
            diretorio = os.path.join(diretorio, 'obj')
            diretorio = os.path.join(diretorio, 'pipeline')
            diretorio = os.path.join(diretorio, pipelineName)
            diretorio = os.path.join(diretorio, f'{pipelineName}.{extension}')

            if os.path.exists(diretorio):
                with open(diretorio,"r") as f:
                    shaders[type] = f.read()
        return self.compilePipeline(shaders) if len(shaders) > 0 else None

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    def windowResize(self,w,h):
        pass

    def loadTexture(self, filename):
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
