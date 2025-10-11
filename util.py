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
    
def dropBlock(count):
    name = f"block_{count+1}"
    model_path = "C:/Users/NAC/Documents/maya/2026/scripts/TowerBuilder/Model/Tower.obj"
    cmds.file(model_path, i=True)
    block = cmds.ls(sl=True)[0]  # ตัวโมเดลที่ import ล่าสุด
    block = cmds.rename(block, name)
    cmds.move(0, y_height, 0, block)
    return block