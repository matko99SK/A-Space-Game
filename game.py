#Importing libraries
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import time
import sys
import random
import vlc
import os
#Initialization
app = Ursina()
window.title = "Space 3D"
window.borderless = False
window.exit_button.visible = False
window.fps_counter.enabled = True
window.fullscreen = True
window.size = (1920, 1080)
#Space Controller
class SpaceController(Entity):
    def __init__(self, **kwargs):
        self.cursor = Entity(parent=camera.ui, model='quad',
                         color=color.pink, scale=.008, rotation_z=45)
        super().__init__()
        self.speed = 5
        self.boost = 2
        self.height = 2
        self.camera_pivot = Entity(parent=self, y=self.height)
        camera.parent = self.camera_pivot
        camera.position = (0, 0, 0)
        camera.rotation = (0, 0, 0)
        camera.fov = 90
        mouse.locked = True
        self.mouse_sensitivity = Vec2(40, 40)
        for key, value in kwargs.items():
            setattr(self, key, value)
    def update(self):
 
        self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]
        self.camera_pivot.rotation_x -= mouse.velocity[1] * \
            self.mouse_sensitivity[0]
        self.camera_pivot.rotation_x = clamp(
            self.camera_pivot.rotation_x, -90, 90)
        self.direction = Vec3(
            self.camera_pivot.forward * (held_keys['w'] - held_keys['s'])
            + self.camera_pivot.right * (held_keys['d'] - held_keys['a'])
        ).normalized()
        feet_ray = raycast(self.position+Vec3(0, 0.5, 0), self.direction,
                           ignore=(self,), distance=.5, debug=False)
        head_ray = raycast(self.position+Vec3(0, self.height-.1, 0),
                           self.direction, ignore=(self,), distance=.5, debug=False)
        if not feet_ray.hit and not head_ray.hit:
            move_amount = self.direction * time.dt * self.speed
            if raycast(self.position+Vec3(-.0, 1, 0), Vec3(1, 0, 0), distance=.5, ignore=(self,)).hit:
                move_amount[0] = min(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0, 1, 0), Vec3(-1, 0, 0), distance=.5, ignore=(self,)).hit:
                move_amount[0] = max(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0, 1, 0), Vec3(0, 0, 1), distance=.5, ignore=(self,)).hit:
                move_amount[2] = min(move_amount[2], 0)
            if raycast(self.position+Vec3(-.0, 1, 0), Vec3(0, 0, -1), distance=.5, ignore=(self,)).hit:
                move_amount[2] = max(move_amount[2], 0)
            self.position += self.direction * self.speed * time.dt
 
    def on_enable(self):
        mouse.locked = True
        self.cursor.enabled = True
 
    def on_disable(self):
        mouse.locked = False
        self.cursor.enabled = False

#Camera
cam = SpaceController()

#Update
def update():
    if held_keys['x']:
        exit(code = None)

#Ship
ship = Entity(model = 'assets/ship/model/ship.obj', texture = 'assets/ship/texture/ship.jpg', color = color.gray, scale = (2,2,2), parent = cam, position = cam.position)

#Sky
Sky(texture = 'assets/sky/texture/sky.jpg', size = (1000,1000,1000))

#Planet - Ceres
ceres = Entity(model = 'sphere', texture = 'assets/planet/ceres/ceres.jpg', scale = (20,20,20), position = (100,0,0), collider = 'sphere')

#Planet - Earth
earth = Entity(model = 'sphere', texture = 'assets/planet/earth/earth.jpg', scale = (80,80,80), position = (0,0,100), collider = 'sphere')

#Planet - Mars
mars = Entity(model = 'sphere', texture = 'assets/planet/mars/mars.jpg', scale = (50,50,50), position = (100,100,0), collider = 'sphere')

#Planet - Moon
moon = Entity(model = 'sphere', texture = 'assets/planet/moon/moon.jpg', scale = (40,40,40), position = (0,100,100), collider = 'sphere')

#Audio
media_player = vlc.MediaPlayer()
aud_pos = random.randint(0,930000)
ambience = vlc.MediaPlayer('UrsinaEngine/assets/audio/music/ambience/ambience.mp3')
ambience.play()
ambience.set_time(aud_pos)
for i in range(100):
    media_player.audio_set_volume(i)
    time.sleep(0.1)

#Startup
app.run()
