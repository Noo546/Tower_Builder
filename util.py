import maya.cmds as cmds
import random
import time

def reset_scene():
    cmds.select(all=True)
    cmds.delete()

def create_base():
    base = cmds.polyCube(name="baseBlock", w=30, h=1, d=30)[0]
    cmds.move(0, 0.5, 0, base)
    return base
    
def drop_new_block(count):
    name = f"block_{count+1}"
    pos_y = 15
    pos_x = random.uniform(-3, 3)
    size = random.uniform(3.5, 4.5)

    block = cmds.polyCube(name=name, w=size, h=1, d=4)[0]
    cmds.move(pos_x, pos_y, 0, block)

    for y in range(15, 1, -1):
        cmds.move(pos_x, y, 0, block)
        time.sleep(0.02)

    if abs(pos_x) > 2:
        return False
    else:
        return True
