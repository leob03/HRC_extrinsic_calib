#!/usr/bin/env python3

#has to launch the duaro before doing that

import rospy
import tf
from IPython import embed
import tf_conversions

from geometry_msgs.msg import TransformStamped

from moveit_commander import MoveGroupCommander

#embed()

rospy.init_node('test1')

group = MoveGroupCommander("lower_arm")

eef_name = group.get_end_effector_link()

pose_rob = group.get_current_pose(eef_name)

# print(pose)
APRILTAG_2_END_OFFSET = [0, 15.5e-2, -2.7e-2]

print([pose_rob.pose.position.x,pose_rob.pose.position.y,pose_rob.pose.position.z])
print([pose_rob.pose.orientation.x,pose_rob.pose.orientation.y,pose_rob.pose.orientation.z,pose_rob.pose.orientation.w])
print(tf_conversions.transformations.translation_matrix([pose_rob.pose.position.x,pose_rob.pose.position.y,pose_rob.pose.position.z]+[0, 15.5e-2, -2.7e-2]) @ tf_conversions.transformations.quaternion_matrix([pose_rob.pose.orientation.x,pose_rob.pose.orientation.y,pose_rob.pose.orientation.z,pose_rob.pose.orientation.w]))

#launch azure_rosdriver, apriltag_ros



#create a subscriber topic that subscribe tf, coordinate of tag0 compare 



