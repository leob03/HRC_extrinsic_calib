#!/usr/bin/python3

import rospy
import tf
import tf_conversions
import numpy as np
from IPython import embed
from moveit_commander import MoveGroupCommander

# Apriltag offset from robot end effector
APRILTAG_2_END_OFFSET_x = -15.5e-2
APRILTAG_2_END_OFFSET_y = 0
APRILTAG_2_END_OFFSET_z = -1.7e-2
rospy.init_node('duaro_apriltag_calibration')

#coordinate of the end effector in the ref of the robot
group = MoveGroupCommander("lower_arm")
# group1 = MoveGroupCommander("upper_arm")

eef_name = group.get_end_effector_link()
# j1 = group1.get

pose_rob = group.get_current_pose(eef_name)
pose_rob_pos = [pose_rob.pose.position.x + APRILTAG_2_END_OFFSET_x, pose_rob.pose.position.y + APRILTAG_2_END_OFFSET_y, pose_rob.pose.position.z + APRILTAG_2_END_OFFSET_z]
pose_rob_orientation = [pose_rob.pose.orientation.x,pose_rob.pose.orientation.y,pose_rob.pose.orientation.z,pose_rob.pose.orientation.w]

fiducial = "tag_0"
camera = "camera_base"
# robot = "base"
robot = "base_link"

broadcaster = tf.TransformBroadcaster()
listener = tf.TransformListener()
rate = rospy.Rate(10)

# Define transform from robot to fiducial

#robot to fiducial
# r_T_f = tf_conversions.transformations.translation_matrix(FIDUCIAL_TO_BASE)  # WRT base
r_T_f = tf_conversions.transformations.translation_matrix(pose_rob_pos) @ tf_conversions.transformations.quaternion_matrix(pose_rob_orientation)


i = 1
# Get first transform
while not rospy.is_shutdown():
    try:
        print('trying')
        # Get transform from fiducial to camera
        pos0, quat0 = listener.lookupTransform(
            target_frame=fiducial,
            source_frame=camera,
            time=rospy.Time.now() - rospy.Duration(2.0)
            )
        break
    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        print('excepting')
        rate.sleep()
        continue


rospy.loginfo('Handeye calibration found:')
rospy.loginfo(pos0)

while not rospy.is_shutdown():
    # try:
    #     # Get transform from fiducial to camera
    #     pos, quat = listener.lookupTransform(
    #         # target_frame=camera,
    #         # source_frame=fiducial,
    #         target_frame=fiducial,
    #         source_frame=camera,
    #         time=rospy.Time.now() - rospy.Duration(2.0)
    #     )
    #     pos0 = pos
    #     quat0 = quat
    # except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
    #     pos = pos0
    #     quat = quat0

    pos = pos0
    quat = quat0

    #fiducial to camera
    f_T_c = tf_conversions.transformations.translation_matrix(pos) @ tf_conversions.transformations.quaternion_matrix(quat)
    
    # Compute transform from robot to camera
    r_T_c = r_T_f @ f_T_c
    pos = tf_conversions.transformations.translation_from_matrix(r_T_c)
    quat = tf_conversions.transformations.quaternion_from_matrix(r_T_c)

    broadcaster.sendTransform(
        translation=pos,
        rotation=quat,
        time=rospy.Time.now(),
        child=camera,
        parent=robot
    )

    rate.sleep()
