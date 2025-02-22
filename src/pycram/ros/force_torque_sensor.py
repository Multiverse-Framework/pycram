import atexit
import time
import threading

import rospy
import pybullet as pb

from geometry_msgs.msg import WrenchStamped
from std_msgs.msg import Header
from..bullet_world import BulletWorld


class ForceTorqueSensor:
    """
    Simulated force-torque sensor for a joint with a given name.
    Reads simulated forces and torques at that joint from bullet_world and publishes geometry_msgs/Wrench messages
    to the given topic.
    """
    def __init__(self, joint_name, fts_topic="/pycram/fts", interval=0.1):
        """
        The given joint_name has to be part of :py:attr:`~pycram.bullet_world.BulletWorld.robot` otherwise a
        RuntimeError will be raised.

        :param joint_name: Name of the joint for which force-torque should be simulated
        :param fts_topic: Name of the ROS topic to which should be published
        :param interval: Interval at which the messages should be published, in seconds
        """
        self.world = BulletWorld.current_bullet_world
        self.fts_joint_idx = None
        if joint_name in self.world.robot.joints.keys():
            self.fts_joint_idx = self.world.robot.joints[joint_name]
        else:
            raise RuntimeError(f"Could not register ForceTorqueSensor: Joint {joint_name} does not exist in robot object")
        pb.enableJointForceTorqueSensor(self.world.robot.id, self.fts_joint_idx, enableSensor=1)

        self.fts_pub = rospy.Publisher(fts_topic, WrenchStamped, queue_size=10)
        self.interval = interval
        self.kill_event = threading.Event()

        self.thread = threading.Thread(target=self._publish)
        self.thread.start()

        atexit.register(self._stop_publishing)

    def _publish(self) -> None:
        """
        Continuously publishes the force-torque values for the simulated joint. Values are published as long as the
        kill_event is not set.
        """
        seq = 0
        while not self.kill_event.is_set():
            current_joint_state = pb.getJointState(self.world.robot.id, self.fts_joint_idx)
            joint_ft = current_joint_state[2]
            h = Header()
            h.seq = seq
            h.stamp = rospy.Time.now()

            wrench_msg = WrenchStamped()
            wrench_msg.header = h
            wrench_msg.wrench.force.x = joint_ft[0]
            wrench_msg.wrench.force.y = joint_ft[1]
            wrench_msg.wrench.force.z = joint_ft[2]

            wrench_msg.wrench.torque.x = joint_ft[3]
            wrench_msg.wrench.torque.y = joint_ft[4]
            wrench_msg.wrench.torque.z = joint_ft[5]

            self.fts_pub.publish(wrench_msg)
            seq += 1
            time.sleep(self.interval)

    def stop_publishing(self) -> None:
        """
        Sets the kill_event and therefore terminates the Thread publishing the force-torque values as well as join the
        threads.
        """
        self.kill_event.set()
        self.thread.join()
