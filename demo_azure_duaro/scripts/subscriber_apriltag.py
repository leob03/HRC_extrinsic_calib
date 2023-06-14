#!/usr/bin/env python3

import rospy

from geometry_msgs.msg import TransformStamped


# class basic_subscriber:

# 	def __init__(self):
# 		# initialize the subscriber node now.
# 		# here we deal with messages of type Twist()
# 		self.image_sub = rospy.Subscriber("/tf",
# 										TransformStamped, self.callback)
# 		print("Initializing the instance!")

# 	def callback(self, TransformStamped):
		
# 		# now simply display what
# 		# you've received from the topic
# 		rospy.loginfo(rospy.get_caller_id() + "The apriltagtf position is %s",
# 					TransformStamped)
# 		print('Callback executed!')

def callback(data):
		
		# now simply display what
		# you've received from the topic
		print('Callback executed!')
		rospy.loginfo(rospy.get_caller_id() + "The apriltagtf position is %s", TransformStamped)

def main():
	# create a subscriber instance
	# sub = basic_subscriber()
	
	# follow it up with a no-brainer sequence check
	print('Currently in the main function...')
	
	# initializing the subscriber node
	rospy.init_node('apriltag_listener', anonymous=True)
	sub = rospy.Subscriber("/tf", TransformStamped, callback)
	print(sub)
	rospy.spin()

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass