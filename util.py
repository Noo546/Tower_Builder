import maya.cmds as cmds
import random

current_block = None
animation_nodes = []

def reset_scene():
    global current_block, animation_nodes
    cmds.select(all=True)
    try:
        cmds.delete()
    except:
        pass
    current_block = None
    animation_nodes = []
    print("🔁 Scene reset complete. Ready to start a new game.")

def create_base():
    base = cmds.polyCube(name="baseBlock", w=30, h=1, d=30)[0]
    cmds.move(0, 0.5, 0, base)
    print("🧱 Base created successfully.")
    return base

def create_moving_block(count):
    global current_block, animation_nodes

    name = f"block_{count+1}"
    height = 20 + (count * 1.1)
    size = random.uniform(3.5, 6.5)
    block_height = random.uniform(4.0, 8.5)
    block_depth = random.uniform(3.5, 6.5)

    block = cmds.polyCube(name=name, w=size, h=block_height, d=block_depth)[0]

    cmds.xform(block, worldSpace=True, pivots=[0, -block_height/2, 0])

    cmds.move(-10, height, 0, block)
    current_block = block

    cmds.currentTime(1)
    cmds.setKeyframe(block, attribute="translateX")

    cmds.currentTime(60)
    cmds.move(10, height, 0, block)
    cmds.setKeyframe(block, attribute="translateX")

    cmds.currentTime(120)
    cmds.move(-10, height, 0, block)
    cmds.setKeyframe(block, attribute="translateX")

    cmds.select(block)
    cmds.setInfinity(preInfinity="oscillate", postInfinity="oscillate")

    animation_nodes = cmds.listConnections(block, type="animCurve") or []
    print(f"🎬 Created moving block: {name}")
    return block


def drop_block(count=0):
    global current_block, animation_nodes

    if not current_block:
        cmds.warning("❗ ไม่มีบล็อกที่กำลังเคลื่อนไหว")
        return False

    if animation_nodes:
        cmds.delete(animation_nodes)
        animation_nodes = []

    pos = cmds.xform(current_block, q=True, ws=True, t=True)

    if cmds.objExists("baseBlock"):
        base_top_vertex = cmds.pointPosition("baseBlock.vtx[4]", w=True)  
        ground_y = base_top_vertex[1]
    else:
        ground_y = 0.5  

    bbox = cmds.exactWorldBoundingBox(current_block)
    block_height = bbox[4] - bbox[1]  # ymax - ymin

    target_y = ground_y + (block_height / 2.0)

    start_frame = cmds.currentTime(q=True)
    end_frame = start_frame + 20

    cmds.currentTime(start_frame)
    cmds.setKeyframe(current_block, attribute="translateY")

    cmds.currentTime(end_frame)
    cmds.move(pos[0], target_y, pos[2], current_block)
    cmds.setKeyframe(current_block, attribute="translateY")

    cmds.currentTime(end_frame)
    cmds.cutKey(current_block, attribute="translateY")
    cmds.cutKey(current_block, attribute="translateX")
    cmds.move(pos[0], target_y, pos[2], current_block)

    print(f"✅ Block dropped. Pivot aligned to base top at Y={ground_y:.2f}")

    current_block = None
    new_block = create_moving_block(count + 1)
    return new_block