from pycram.designator import MotionDesignator
from pycram.bullet_world import BulletWorld
from pycram.robot_descriptions import robot_description

def ground_moving(self):




def pr2_motion_designators(desig):
    """
    This method defines the referencing of all available motion designator.
    If a possible solution is found it will be appended to the list of solutions.
    :param desig: The designator to be referenced
    :return: A list with possible solution.
    """
    solutions = []

    # Type: moving
    if desig.check_constraints([('type', 'moving'), 'target']):
        if desig.check_constraints(['orientation']):
            solutions.append(desig.make_dictionary([('cmd', 'navigate'), 'target', 'orientation']))
        solutions.append(desig.make_dictionary([('cmd', 'navigate'), 'target', ('orientation', BulletWorld.robot.get_orientation())]))

    # Type: pick-up
    if desig.check_constraints([('type', 'pick-up'), 'object']):
        if desig.check_constraints([('arm', 'right')]):
            solutions.append(desig.make_dictionary([('cmd', 'pick'), 'object', ('gripper', robot_description.get_tool_frame('right'))]))
        solutions.append(desig.make_dictionary([('cmd', 'pick'), 'object', ('gripper', robot_description.get_tool_frame('left'))]))

    # Type: place
    if desig.check_constraints([('type', 'place'), 'target']):
        if desig.check_constraints(['object']):
            if desig.check_constraints([('arm', 'right')]):
                solutions.append(desig.make_dictionary([('cmd', 'place'), 'target', 'object', ('gripper', robot_description.get_tool_frame('right'))]))
            solutions.append(desig.make_dictionary([('cmd', 'place'), 'target', 'object', ('gripper', robot_description.get_tool_frame('left'))]))

    # Type: opening
    if desig.check_constraints([('type', 'opening-prismatic'), 'joint', 'handle', 'part-of']):
        if desig.check_constraints([('arm', 'right')]):
            if desig.check_constraints(['distance']):
                solutions.append(desig.make_dictionary(
                    [('cmd', 'open-prismatic'), 'joint', 'handle', ('gripper', robot_description.get_tool_frame('right')),
                     'distance', 'part-of']))
            else:
                solutions.append(desig.make_dictionary(
                    [('cmd', 'open-prismatic'), 'joint', 'handle', ('gripper', robot_description.get_tool_frame('right')),
                     ('distance', 0.3), 'part-of']))
        else:
            if desig.check_constraints(['distance']):
                solutions.append(desig.make_dictionary(
                    [('cmd', 'open-prismatic'), 'joint', 'handle', ('gripper', robot_description.get_tool_frame('left')),
                     'distance', 'part-of']))
            else:
                solutions.append(desig.make_dictionary(
                    [('cmd', 'open-prismatic'), 'joint', 'handle', ('gripper', robot_description.get_tool_frame('left')),
                     ('distance', 0.3), 'part-of']))

    # Type: closing
    if desig.check_constraints([('type', 'closing-prismatic'), 'joint', 'handle', 'part-of']):
        if desig.check_constraints([('arm', 'right')]):
            if desig.check_constraints(['distance']):
                solutions.append(desig.make_dictionary(
                    [('cmd', 'close-prismatic'), 'joint', 'handle', ('gripper', robot_description.get_tool_frame('right')),
                     'distance', 'part-of']))
            else:
                solutions.append(desig.make_dictionary(
                    [('cmd', 'close-prismatic'), 'joint', 'handle', ('gripper', robot_description.get_tool_frame('right')),
                     ('distance', 0.3), 'part-of']))
        else:
            solutions.append(desig.make_dictionary(
                [('cmd', 'close-prismatic'), 'joint', 'handle', 'part-of', ('distance', 0.3),
                 ('gripper', robot_description.get_tool_frame('left')), 'part-of']))

    # Type: open fridge
    if desig.check_constraints([('type', 'opening-rotational'), 'joint', 'handle', 'part-of']):
        if desig.check_constraints([('arm', 'right')]):
            gripper = robot_description.get_tool_frame('right')
        else:
            gripper = robot_description.get_tool_frame('left')
        if desig.check_constraints(['distance']):
            solutions.append(desig.make_dictionary(
                [('cmd', 'open-rotational'), 'joint', 'handle', ('gripper', gripper), 'distance', 'part-of']
            ))
        else:
            solutions.append(desig.make_dictionary(
                [('cmd', 'open-rotational'), 'joint', 'handle', ('gripper', gripper), ('distance', 1), 'part-of']
            ))

    # Type: close fridge
    if desig.check_constraints([('type', 'closing-rotational'), 'joint', 'handle', 'part-of']):
        if desig.check_constraints([('arm', 'right')]):
            gripper = robot_description.get_tool_frame('right')
        else:
            gripper = robot_description.get_tool_frame('left')
        solutions.append(desig.make_dictionary(
            [('cmd', 'close-rotational'), 'joint', 'handle', ('gripper', gripper), 'part-of']
        ))

    # Type: move-tcp
    if desig.check_constraints([('type', 'move-tcp'), 'target']):
        if desig.check_constraints([('arm', 'right')]):
            solutions.append(desig.make_dictionary([('cmd', 'move-tcp'), 'target', ('gripper', robot_description.get_tool_frame('right'))]))
        solutions.append(desig.make_dictionary([('cmd', 'move-tcp'), 'target', ('gripper', robot_description.get_tool_frame('left'))]))

    # Type: park-arms
    if desig.check_constraints([('type', 'park-arms')]):
        solutions.append(desig.make_dictionary([('cmd', 'park')]))

    # Type: looking
    if desig.check_constraints([('type', 'looking')]):
        if desig.check_constraints(['target']):
            solutions.append(desig.make_dictionary([('cmd', 'looking'), 'target']))
        if desig.check_constraints(['object']):
            solutions.append(desig.make_dictionary([('cmd', 'looking'), ('target', BulletWorld.current_bullet_world.
                                                                         get_objects_by_name(desig.prop_value('object')).get_pose())]))

    # Type: opening-gripper
    if desig.check_constraints([('type', 'opening-gripper'), 'gripper']):
        solutions.append(desig.make_dictionary([('cmd', 'move-gripper'), ('motion', 'open'), 'gripper']))

    # Type: closing-gripper
    if desig.check_constraints([('type', 'closing-gripper'), 'gripper']):
        solutions.append(desig.make_dictionary([('cmd', 'move-gripper'), ('motion', 'close'), 'gripper']))

    # Type: detecting
    if desig.check_constraints([('type', 'detecting'), 'object']):
        solutions.append(desig.make_dictionary([('cmd', 'detecting'), ('cam_frame', 'wide_stereo_optical_frame'), ('front_facing_axis', [0, 0, 1]), 'object']))

    # Type: move-arm-joints
    if desig.check_constraints([('type', 'move-arm-joints')]):
        if desig.check_constraints(['left-arm', 'right-arm']):
            solutions.append(desig.make_dictionary([('cmd', 'move-joints'), ('left-poses', desig.prop_value('left-arm')), ('right-poses', desig.prop_value('right-arm'))]))
        if desig.check_constraints(['left-arm']):
            solutions.append(desig.make_dictionary([('cmd', 'move-joints'), ('left-poses', desig.prop_value('left-arm')), ('right-poses', None)]))
        if desig.check_constraints(['right-arm']):
            solutions.append(desig.make_dictionary([('cmd', 'move-joints'), ('right-poses', desig.prop_value('right-arm')), ('left-poses', None)]))

    # Type: world-state-detecting
    if desig.check_constraints([('type', 'world-state-detecting')]):
        solutions.append(desig.make_dictionary([('cmd', 'world-state-detecting'), 'object']))

    return solutions


MotionDesignator.resolvers.append(pr2_motion_designators)
