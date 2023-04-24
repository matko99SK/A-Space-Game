from ursina.prefabs.first_person_controller import FirstPersonController
from ursina import *
 
 
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
 
 
if __name__ == '__main__':
    app = Ursina()
    Sky(color=color.gray)
    ground = Entity(model='plane', scale=(100, 1, 100), color=color.gray,
                    texture='white_cube', texture_scale=(100, 100), collider='box')
    e = Entity(model='cube', scale=(1, 5, 10), x=2, y=.01,
               rotation_y=45, collider='box', texture='white_cube')
    e.texture_scale = (e.scale_z, e.scale_y)
    e = Entity(model='cube', scale=(1, 5, 10), x=-2,
               y=.01, collider='box', texture='white_cube')
    e.texture_scale = (e.scale_z, e.scale_y)
    player = SpaceController(y=2, origin_y=-.5)
 
    def input(key):
        if held_keys['shift']:
            player.speed = clamp(player.speed + player.boost, 5, 20)
        else:
            player.speed = 5
    app.run()