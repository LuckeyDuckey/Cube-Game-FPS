import pygame, sys, math, os, time
from pygame.locals import *

import moderngl as mgl
from array import array

# Test boolean operator to create hall ways

## Pygame Setup Bits ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

pygame.init()
pygame.display.set_caption("3D Engine")
pygame.mouse.set_visible(False)

Resolution = (1600, 900)
Screen = pygame.display.set_mode(Resolution, flags=pygame.OPENGL | pygame.DOUBLEBUF)
Display = pygame.Surface(Resolution)

Clock = pygame.time.Clock()
LastTime = time.time()

Concrete = pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(os.getcwd(), "Textures/Concrete.jpg")),(4592 // 4, 3448 // 4)), False, True).convert_alpha()

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.set_num_channels(64)

MenuMove = pygame.mixer.Sound(os.path.join(os.getcwd(), "Sounds/MenuMove.wav"))
MenuChange = pygame.mixer.Sound(os.path.join(os.getcwd(), "Sounds/MenuChange.wav"))

## OpenGL Setup Bits ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

Context = mgl.create_context()

QuadBuffer = Context.buffer(data=array("f", [
    # Position (x, y), uv coords (x, y)
    -1.0, 1.0, 0.0, 1.0,  # Topleft
    1.0, 1.0, 1.0, 1.0,   # Topright
    -1.0, -1.0, 0.0, 0.0, # Bottomleft
    1.0, -1.0, 1.0, 0.0   # Bottomright
]))

with open(f"shaders/vertex.txt") as file:
    VertexShader = file.read()

with open(f"shaders/fragment.txt") as file:
    FragmentShader = file.read()

Program = Context.program(vertex_shader=VertexShader, fragment_shader=FragmentShader)
RenderObject = Context.vertex_array(Program, [(QuadBuffer, "2f 2f", "vert", "texcoord")])

## UI class ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

Font = pygame.font.Font("Fonts/PixelFont.ttf", 40)

class Menu:
    def __init__(self, Resolution, Font):
        self.State = "Pause" # Pause, Settings, Debug
        self.Selection = 0
        self.Lengths = {"Pause":4, "Settings":4, "Debug":3}
        self.Resolution = Resolution
        self.Font = Font
        self.SettingsValues = {"FOV":20, "Sensitivity":10, "Quality":"High", "FPS":140.0}

    def Arrow(self, Center, Direction):
        Points = [[Center[0], Center[1] + 5], [Center[0], Center[1] - 5], [Center[0] + 6 if Direction else Center[0] - 6, Center[1]]]
        return Points
        
    def Main(self, Surface):
        if self.State == "Pause":
            self.Pause(Surface)

        elif self.State == "Settings":
            self.Settings(Surface)

        elif self.State == "Debug":
            self.Debug(Surface)

    def Pause(self, Surface):
        
        Size = [800, 450]

        BaseX = self.Resolution[0] * 0.5 - Size[0] * 0.5 + 75
        BaseY = self.Resolution[1] * 0.5 - Size[1] * 0.5
        
        # Draw background
        pygame.draw.rect(Surface, (0, 0, 0), pygame.Rect(BaseX - 75, BaseY, Size[0], Size[1]))
        pygame.draw.rect(Surface, (255, 255, 255), pygame.Rect(self.Resolution[0] * 0.5 - (Size[0] * 0.5 - 4), self.Resolution[1] * 0.5 - (Size[1] * 0.5 - 4), Size[0] - 8, Size[1] - 8), width=2)

        # Draw arrow
        Lines = [BaseY + 150, BaseY + 200, BaseY + 285, BaseY + 335]
        Points = self.Arrow([BaseX - 24, Lines[self.Selection]], True)
        pygame.draw.polygon(Surface, (255, 255, 255), Points)

        # Paused Text
        Rendered = self.Font.render("- PAUSED -", True, (255,255,255))
        Surface.blit(Rendered, (800 - Rendered.get_width() * 0.5, BaseY + 75 - Rendered.get_height() * 0.5))

        # Resume Text
        Rendered = self.Font.render("Resume", True, (255,255,255))
        Surface.blit(Rendered, (BaseX, BaseY + 150 - Rendered.get_height() * 0.5))

        # Settings Text
        Rendered = self.Font.render("Settings", True, (255,255,255))
        Surface.blit(Rendered, (BaseX, BaseY + 200 - Rendered.get_height() * 0.5))

        # Debug Text
        Rendered = self.Font.render("Debug", True, (255,255,255))
        Surface.blit(Rendered, (BaseX, BaseY + 285 - Rendered.get_height() * 0.5))

        # Exit Text
        Rendered = self.Font.render("Exit", True, (255,255,255))
        Surface.blit(Rendered, (BaseX, BaseY + 335 - Rendered.get_height() * 0.5))


    def Settings(self, Surface):
        
        Size = [800, 450]

        BaseX = self.Resolution[0] * 0.5 - Size[0] * 0.5 + 75
        BaseY = self.Resolution[1] * 0.5 - Size[1] * 0.5
        
        # Draw background
        pygame.draw.rect(Surface, (0, 0, 0), pygame.Rect(BaseX - 75, BaseY, Size[0], Size[1]))
        pygame.draw.rect(Surface, (255, 255, 255), pygame.Rect(self.Resolution[0] * 0.5 - (Size[0] * 0.5 - 4), self.Resolution[1] * 0.5 - (Size[1] * 0.5 - 4), Size[0] - 8, Size[1] - 8), width=2)

        # Draw arrow
        Lines = [BaseY + 150, BaseY + 200, BaseY + 285, BaseY + 335]
        Points = self.Arrow([BaseX - 24, Lines[self.Selection]], True)
        pygame.draw.polygon(Surface, (255, 255, 255), Points)

        # Settings Text
        Rendered = self.Font.render("- SETTINGS -", True, (255,255,255))
        Surface.blit(Rendered, (800 - Rendered.get_width() * 0.5, BaseY + 75 - Rendered.get_height() * 0.5))

        # Quality Text
        Rendered = self.Font.render("Quality", True, (255,255,255))
        Surface.blit(Rendered, (BaseX, BaseY + 150 - Rendered.get_height() * 0.5))
        Rendered = self.Font.render(f"{self.SettingsValues['Quality']}", True, (255,255,255))
        Surface.blit(Rendered, (BaseX + 475 - Rendered.get_width() * 0.5, BaseY + 150 - Rendered.get_height() * 0.5))

        # Quality arrows and value
        Points = self.Arrow([BaseX + 540, Lines[0]], True)
        pygame.draw.polygon(Surface, (255, 255, 255), Points)
        Points = self.Arrow([BaseX + 400, Lines[0]], False)
        pygame.draw.polygon(Surface, (255, 255, 255), Points)

        # FPS max Text
        Rendered = self.Font.render("FPS Max", True, (255,255,255))
        Surface.blit(Rendered, (BaseX, BaseY + 200 - Rendered.get_height() * 0.5))
        Rendered = self.Font.render(f"{self.SettingsValues['FPS']}", True, (255,255,255))
        Surface.blit(Rendered, (BaseX + 475 - Rendered.get_width() * 0.5, BaseY + 200 - Rendered.get_height() * 0.5))

        # Quality arrows and value
        Points = self.Arrow([BaseX + 540, Lines[1]], True)
        pygame.draw.polygon(Surface, (255, 255, 255), Points)
        Points = self.Arrow([BaseX + 400, Lines[1]], False)
        pygame.draw.polygon(Surface, (255, 255, 255), Points)

        # Sensitivity Text
        Rendered = self.Font.render("Sensitivity", True, (255,255,255))
        Surface.blit(Rendered, (BaseX, BaseY + 285 - Rendered.get_height() * 0.5))
        Rendered = self.Font.render(f"{self.SettingsValues['Sensitivity'] / 10}", True, (255,255,255))
        Surface.blit(Rendered, (BaseX + 475 - Rendered.get_width() * 0.5, BaseY + 285 - Rendered.get_height() * 0.5))

        # Quality arrows and value
        Points = self.Arrow([BaseX + 540, Lines[2]], True)
        pygame.draw.polygon(Surface, (255, 255, 255), Points)
        Points = self.Arrow([BaseX + 400, Lines[2]], False)
        pygame.draw.polygon(Surface, (255, 255, 255), Points)

        # FOV Text
        Rendered = self.Font.render("FOV", True, (255,255,255))
        Surface.blit(Rendered, (BaseX, BaseY + 335 - Rendered.get_height() * 0.5))
        Rendered = self.Font.render(f"{self.SettingsValues['FOV'] / 10}", True, (255,255,255))
        Surface.blit(Rendered, (BaseX + 475 - Rendered.get_width() * 0.5, BaseY + 335 - Rendered.get_height() * 0.5))

        # Quality arrows and value
        Points = self.Arrow([BaseX + 540, Lines[3]], True)
        pygame.draw.polygon(Surface, (255, 255, 255), Points)
        Points = self.Arrow([BaseX + 400, Lines[3]], False)
        pygame.draw.polygon(Surface, (255, 255, 255), Points)

    def Debug(self, Surface):
                
        Size = [800, 350]

        BaseX = self.Resolution[0] * 0.5 - Size[0] * 0.5 + 75
        BaseY = self.Resolution[1] * 0.5 - Size[1] * 0.5
        
        # Draw background
        pygame.draw.rect(Surface, (0, 0, 0), pygame.Rect(BaseX - 75, BaseY, Size[0], Size[1]))
        pygame.draw.rect(Surface, (255, 255, 255), pygame.Rect(self.Resolution[0] * 0.5 - (Size[0] * 0.5 - 4), self.Resolution[1] * 0.5 - (Size[1] * 0.5 - 4), Size[0] - 8, Size[1] - 8), width=2)

        # Draw arrow
        Lines = [BaseY + 150, BaseY + 200, BaseY + 250]
        Points = self.Arrow([BaseX - 24, Lines[self.Selection]], True)
        pygame.draw.polygon(Surface, (255, 255, 255), Points)

        # Debug Text
        Rendered = self.Font.render("- DEBUG -", True, (255,255,255))
        Surface.blit(Rendered, (800 - Rendered.get_width() * 0.5, BaseY + 75 - Rendered.get_height() * 0.5))

        # Reset player Text
        Rendered = self.Font.render("Reset Player", True, (255,255,255))
        Surface.blit(Rendered, (BaseX, BaseY + 150 - Rendered.get_height() * 0.5))

        # Spawn enemy Text
        Rendered = self.Font.render("Spawn Enemy", True, (255,255,255))
        Surface.blit(Rendered, (BaseX, BaseY + 200 - Rendered.get_height() * 0.5))

        # Kill all Text
        Rendered = self.Font.render("Kill All", True, (255,255,255))
        Surface.blit(Rendered, (BaseX, BaseY + 250 - Rendered.get_height() * 0.5))

    def SelectPause(self):
        global Paused
        
        if self.Selection == 0:
            Paused = False
            
        elif self.Selection == 1:
            self.State = "Settings"
            self.Selection = 0
            
        elif self.Selection == 2:
            self.State = "Debug"
            self.Selection = 0
            
        elif self.Selection == 3:
            pygame.quit(); sys.exit()

    def SelectSettings(self):
        pass
            

    def SelectDebug(self):
        global CameraPosition, CameraRotation
        
        if self.Selection == 0:
            CameraPosition = [0, 0, 0]
            CameraRotation = [0, 0]
            
        elif self.Selection == 1:
            print("Spawn Enemy")
            
        elif self.Selection == 2:
            print("Kill All")

    def SettingsLeftRightKey(self, Side):
        global FPS, Sensitivity, FOV

        pygame.mixer.Sound.play(MenuChange)
        
        if self.Selection == 0:
            if self.SettingsValues["Quality"] == "High":
                self.SettingsValues["Quality"] = "Low"

            else:
                self.SettingsValues["Quality"] = "High"

        elif self.Selection == 1:
            if self.SettingsValues["FPS"] > 30 and not Side:
                self.SettingsValues["FPS"] -= 10

            if self.SettingsValues["FPS"] < 360 and Side:
                self.SettingsValues["FPS"] += 10

        elif self.Selection == 2:
            if self.SettingsValues["Sensitivity"] > 1 and not Side:
                self.SettingsValues["Sensitivity"] -= 1

            if self.SettingsValues["Sensitivity"] < 30 and Side:
                self.SettingsValues["Sensitivity"] += 1

        elif self.Selection == 3:
            if self.SettingsValues["FOV"] > 10 and not Side:
                self.SettingsValues["FOV"] -= 1

            if self.SettingsValues["FOV"] < 30 and Side:
                self.SettingsValues["FOV"] += 1

        FOV = self.SettingsValues["FOV"] / 10
        Sensitivity = self.SettingsValues["Sensitivity"] / 10
        FPS = self.SettingsValues["FPS"]

    def KeyPress(self, Key):
        global Paused

        if not Paused and Key == pygame.K_ESCAPE:
            Paused = True
            pygame.mixer.Sound.play(MenuMove)

        elif Paused:
            if Key == pygame.K_ESCAPE:
                if self.State in ["Settings", "Debug"]:
                    self.State = "Pause"
                    self.Selection = 0

                elif self.State == "Pause":
                    Paused = False

                pygame.mixer.Sound.play(MenuMove)

            if Key == pygame.K_RETURN:
                
                if self.State == "Pause":
                    self.SelectPause()

                elif self.State == "Settings":
                    self.SelectSettings()

                elif self.State == "Debug":
                    self.SelectDebug()

                pygame.mixer.Sound.play(MenuMove)

            if Key == pygame.K_w:
                self.Selection -= 1

                if self.Selection < 0:
                    self.Selection = self.Lengths[self.State] - 1

                pygame.mixer.Sound.play(MenuMove)

            if Key == pygame.K_s:
                self.Selection += 1

                if self.Selection >= self.Lengths[self.State]:
                    self.Selection = 0

                pygame.mixer.Sound.play(MenuMove)

            if Key == pygame.K_a:
                if self.State == "Settings":
                    self.SettingsLeftRightKey(False)

            if Key == pygame.K_d:
                if self.State == "Settings":
                    self.SettingsLeftRightKey(True)

UI = Menu(Resolution, Font)
Paused = False

## Functions and variables ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

def surfaceToTexture(Surface):
    Texure = Context.texture(Surface.get_size(), 4) # Innit texture
    Texure.filter = (mgl.NEAREST, mgl.NEAREST) # Set properties
    Texure.swizzle = "BGRA" # Set format
    Texure.write(Surface.get_view("1")) # Render surf to texture

    return Texure # Return OpenGL texture

def freeCam(Position, RotationX, RotationY, Speed):
    # Calculate the displacement in the xyz planes
    DisX = -Speed * math.cos(RotationY) * math.sin(RotationX)
    DisY = -Speed * math.sin(RotationY)
    DisZ = Speed * math.cos(RotationY) * math.cos(RotationX)

    # Return updated position vector
    return (Position[0] + DisX, Position[1] + DisY, Position[2] + DisZ)

CameraPosition = [0, 0, 0]
CameraRotation = [0, 0]

FreeCamSpeed = 1
Time = 1

FOV = 2
Sensitivity = 1
FPS = 140

## Main game loop ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

while True:

    # Set fps
    Clock.tick(FPS)

    # Update delta time
    DeltaTime = time.time() - LastTime
    LastTime = time.time()

    Time += DeltaTime # Update game time
        
    ## Mouse handling ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

    # Get mouse pos
    mx, my = pygame.mouse.get_pos()

    if pygame.mouse.get_focused(): # Check if window is user target
        
        pygame.event.set_grab(True) # Confining the mouse to the window
        
        MouseMovement = pygame.mouse.get_rel() # Get relative mouse movement each frame

        if not Paused:
            CameraRotation[0] -= MouseMovement[0] / (540 / Sensitivity) # Rotate camera x direction
            CameraRotation[1] += MouseMovement[1] / (540 / Sensitivity) # Rotate camera y direction

    else:
        pygame.event.set_grab(False) # Let mouse leave window

    ## Keyboard handling ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

    Keys = pygame.key.get_pressed() # Get keys pressed

    if not Paused:
        # Forward and backward
        if Keys[K_w]: CameraPosition = freeCam(CameraPosition, CameraRotation[0], CameraRotation[1], FreeCamSpeed * DeltaTime)
        if Keys[K_s]: CameraPosition = freeCam(CameraPosition, CameraRotation[0], CameraRotation[1], -FreeCamSpeed * DeltaTime)

        # Left and right
        if Keys[K_a]: CameraPosition = freeCam(CameraPosition, CameraRotation[0] - 1.571, 0, -FreeCamSpeed * DeltaTime)
        if Keys[K_d]: CameraPosition = freeCam(CameraPosition, CameraRotation[0] - 1.571, 0, FreeCamSpeed * DeltaTime)

        # Up no down
        if Keys[K_SPACE]: CameraPosition = freeCam(CameraPosition, 0, 1.571, -FreeCamSpeed * DeltaTime)

    ## Pygame screen rendering ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

    Display.fill((255, 0, 0))

    if Paused:
        UI.Main(Display)

    ## OpenGL section ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

    # Pass in pygame display texture
    DisplayTexure = surfaceToTexture(pygame.transform.flip(Display, False, True))
    DisplayTexure.use(0)
    Program["tex"] = 0

    # Pass in concrete texture
    ConcreteTexure = surfaceToTexture(Concrete)
    ConcreteTexure.use(1)
    Program["Concrete"] = 1

    Program["Time"] = Time
    Program["Resolution"] = Resolution
    Program["Rotation"] = CameraRotation
    Program["Position"] = CameraPosition

    RenderObject.render(mode=mgl.TRIANGLE_STRIP) # Call render function

    # Update pygame window
    pygame.display.flip()
    pygame.display.set_caption(str(Clock.get_fps()))

    # Release textures to avoid memory leaks
    DisplayTexure.release()
    ConcreteTexure.release()

    ## General inputs handling ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

    for event in pygame.event.get():
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            UI.KeyPress(event.key)
            
            if event.key == pygame.K_LSHIFT:
                FreeCamSpeed = 6

        if event.type == pygame.KEYUP:
            
            if event.key == pygame.K_LSHIFT:
                FreeCamSpeed = 1
        
        if event.type == MOUSEBUTTONDOWN:
            
            if event.button == 1:
                pass
