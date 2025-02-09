from ursina import *
from ursina.shaders import lit_with_shadows_shader 
class Block(Entity):
    def __init__(self, position=(0, 0, 0), texture='', scale=1,shader=lit_with_shadows_shader):
        super().__init__(
            position=position,
            parent=scene,
            model='cube',
            origin_y=.5,
            texture=texture,
            collider='box',
            scale=scale,
            cull_face=True,
            shader=shader
        ) 