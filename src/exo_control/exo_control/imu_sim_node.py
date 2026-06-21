import rclpy
from rclpy.node import Node
from exo_interfaces.msg import JointAngles
import math

class ImuSimNode(Node):

    def __init__(self):
        super().__init__('imu_sim_node')
        self.get_logger().info('IMU Node started')
        self.publisher=self.create_publisher(JointAngles, '/joint_angles', 10)
        self.counter=0
        self.timer=self.create_timer(1.0, self.timer_callback)
    
    def timer_callback(self):
        self.counter+=1
        hip_angle= 15.0*math.sin(self.counter*0.1)
        knee_angle=40.0*math.sin(self.counter*0.1 + 0.5)
        ankle_angle=10*math.sin(self.counter*0.1 - 0.3)
        msg=JointAngles()
        msg.hip=hip_angle
        msg.knee=knee_angle
        msg.ankle=ankle_angle
        self.publisher.publish(msg)
        self.get_logger().info(f'Published: {JointAngles}')

def main(args=None):
    rclpy.init(args=args)
    node=ImuSimNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
if __name__=='__main__':
    main()