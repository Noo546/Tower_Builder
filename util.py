import maya.cmds as cmds
import random

current_block = None
animation_nodes = []
placed_blocks = []

def reset_scene():
    global current_block, animation_nodes, placed_blocks
    cmds.select(all=True)
    try:
        cmds.delete()
    except:
        pass
    current_block = None
    animation_nodes = []
    placed_blocks = []
    print("🔁 Scene reset complete.")

def create_base():
    base = cmds.polyCube(name="baseBlock", w=30, h=1, d=30)[0]
    cmds.move(0, 0.5, 0, base)
    print("🧱 Base created.")
    return base


def create_moving_block(count, mode="NORMAL"):
    global current_block, animation_nodes

    name = f"block_{count+1}"
    height = 15 + (count * 6)
    size = random.uniform(1.5, 4.5)
    block_height = random.uniform(3.5, 5.5)
    block_depth = random.uniform(3.5, 6.5)

    block = cmds.polyCube(name=name, w=size, h=block_height, d=block_depth)[0]
    cmds.xform(block, worldSpace=True, pivots=[0, -block_height / 2, 0])
    cmds.move(-10, height, 0, block)
    current_block = block

    shader_name = f"shader_{name}"
    shader = cmds.shadingNode("lambert", asShader=True, name=shader_name)
    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f"{shader_name}SG")
    cmds.connectAttr(shader + ".outColor", sg + ".surfaceShader", force=True)

    random_color = (random.random(), random.random(), random.random())
    cmds.setAttr(shader + ".color", *random_color, type="double3")
    cmds.sets(block, edit=True, forceElement=sg)

    print(f"🎨 Block {name} color: {random_color}")

    if mode == "EASY":
        frame_speed = 180
    elif mode == "HARD":
        frame_speed = 40
    else:
        frame_speed = 90

    cmds.playbackOptions(minTime=1, maxTime=frame_speed)

    cmds.currentTime(1)
    cmds.setKeyframe(block, attribute="translateX")

    cmds.currentTime(frame_speed / 2)
    cmds.move(10, height, 0, block)
    cmds.setKeyframe(block, attribute="translateX")

    cmds.currentTime(frame_speed)
    cmds.move(-10, height, 0, block)
    cmds.setKeyframe(block, attribute="translateX")

    cmds.select(block)
    cmds.setInfinity(preInfinity="cycle", postInfinity="cycle")
    cmds.keyTangent(block, attribute="translateX", inTangentType="auto", outTangentType="auto")

    animation_nodes = cmds.listConnections(block, type="animCurve") or []
    print(f"🎬 Created moving block: {name} ({mode}) - Frames: {frame_speed}")
    return block


def check_collision(block):
    if not placed_blocks:
        return False

    bbox_new = cmds.exactWorldBoundingBox(block)
    min_x_new, min_y_new, min_z_new, max_x_new, max_y_new, max_z_new = bbox_new

    for prev in placed_blocks:
        if not cmds.objExists(prev) or prev == "baseBlock":
            continue

        bbox_prev = cmds.exactWorldBoundingBox(prev)
        min_x_prev, min_y_prev, min_z_prev, max_x_prev, max_y_prev, max_z_prev = bbox_prev

        overlap_x = (min_x_new <= max_x_prev) and (max_x_new >= min_x_prev)
        overlap_y = (min_y_new <= max_y_prev) and (max_y_new >= min_y_prev)
        overlap_z = (min_z_new <= max_z_prev) and (max_z_new >= min_z_prev)

        if overlap_x and overlap_y and overlap_z:
            print(f"💥 Collision detected between {block} and {prev}")
            return True

    return False


def drop_block(count=0, mode="NORMAL"):

    global current_block, animation_nodes, placed_blocks

    if not current_block:
        cmds.warning("❗ ไม่มีบล็อกที่กำลังเคลื่อนไหว")
        return False, "no_block"

    if animation_nodes:
        cmds.delete(animation_nodes)
        animation_nodes = []

    pos = cmds.xform(current_block, q=True, ws=True, t=True)

    if cmds.objExists("baseBlock"):
        ground_y = cmds.pointPosition("baseBlock.vtx[4]", w=True)[1]
    else:
        ground_y = 0.5

    bbox = cmds.exactWorldBoundingBox(current_block)
    block_height = bbox[4] - bbox[1]
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

    if check_collision(current_block):
        print("💥 Tower collapsed! Game over.")
        current_block = None
        return False, "collision"

    print(f"✅ Block {count+1} dropped safely.")
    placed_blocks.append(current_block)
    current_block = None

    new_block = create_moving_block(count + 1, mode)
    return True, new_block
