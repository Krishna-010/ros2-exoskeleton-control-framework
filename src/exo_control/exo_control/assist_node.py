import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String
from exo_interfaces.msg import JointMoments

class AssistNode(Node):
    def __init__(self):
        super().__init__('assist_node')
        self.last_ankle_angle=None
        self.last_gait_phase=None
        self.declare_parameter('hip_assistance_gain', 0.2)
        self.declare_parameter('ankle_assistance_gain', 0.2)
        self.declare_parameter('hip_assistive_torque_limit', 15.0)
        self.declare_parameter('ankle_assistive_torque_limit', 36.0)
        self.hip_assistance_gain = self.get_parameter('hip_assistance_gain').get_parameter_value().double_value
        self.ankle_assistance_gain = self.get_parameter('ankle_assistance_gain').get_parameter_value().double_value
        self.hip_assistive_torque_limit = self.get_parameter('hip_assistive_torque_limit').get_parameter_value().double_value
        self.ankle_assistive_torque_limit = self.get_parameter('ankle_assistive_torque_limit').get_parameter_value().double_value
        self.get_logger().info('Assist Node Started')
        self.left_hip_pub = self.create_publisher(Float32,'/left/hip/assistive_torque',10)
        self.right_hip_pub = self.create_publisher(Float32,'/right/hip/assistive_torque',10)
        self.left_ankle_pub = self.create_publisher(Float32,'/left/ankle/assistive_torque',10)
        self.right_ankle_pub = self.create_publisher(Float32,'/right/ankle/assistive_torque',10)
        self.left_moment_sub = self.create_subscription(JointMoments,'/left/joint_moments',self.left_moment_callback,10)
        self.right_moment_sub = self.create_subscription(JointMoments,'/right/joint_moments',self.right_moment_callback,10)
        self.left_phase_sub = self.create_subscription(String,'/left/gait_phase',self.left_phase_callback,10)
        self.right_phase_sub = self.create_subscription(String,'/right/gait_phase',self.right_phase_callback,10)
        self.left_moments = None
        self.right_moments = None
        self.left_gait_phase = None
        self.right_gait_phase = None
    def saturate_torque(self, torque, limit):
        if torque > limit:
            return limit
        elif torque < -limit:
            return -limit
        else:
            return torque
    def left_moment_callback(self, msg):
        self.left_moments = msg
        self.compute_left_assistance()
    def right_moment_callback(self, msg):
        self.right_moments = msg
        self.compute_right_assistance()
    def left_phase_callback(self, msg):
        self.left_gait_phase = msg.data
        self.compute_left_assistance()
    def right_phase_callback(self, msg):
        self.right_gait_phase = msg.data
        self.compute_right_assistance() 
    def compute_left_assistance(self):
        if self.left_moments is None:
            return
        if self.left_gait_phase is None:
            return
        raw_hip_torque = self.hip_assistance_gain * self.left_moments.hip
        hip_torque = self.saturate_torque(raw_hip_torque,self.hip_assistive_torque_limit)
        if self.left_gait_phase == "STANCE":
            raw_ankle_torque = self.ankle_assistance_gain * self.left_moments.ankle
            ankle_torque = self.saturate_torque(raw_ankle_torque,self.ankle_assistive_torque_limit)
        else:
            ankle_torque = 0.0
        hip_msg = Float32()
        hip_msg.data = hip_torque
        ankle_msg = Float32()
        ankle_msg.data = ankle_torque
        self.left_hip_pub.publish(hip_msg)
        self.left_ankle_pub.publish(ankle_msg)
        self.get_logger().info(f'LEFT | Phase={self.left_gait_phase}, 'f'HipAssist={hip_torque:.2f}, AnkleAssist={ankle_torque:.2f}')
    def compute_right_assistance(self):
        if self.right_moments is None:
            return
        if self.right_gait_phase is None:
            return
        raw_hip_torque = self.hip_assistance_gain * self.right_moments.hip
        hip_torque = self.saturate_torque(raw_hip_torque,self.hip_assistive_torque_limit)
        if self.left_gait_phase == "STANCE":
            raw_ankle_torque = self.ankle_assistance_gain * self.right_moments.ankle
            ankle_torque = self.saturate_torque(raw_ankle_torque,self.ankle_assistive_torque_limit)
        else:
            ankle_torque = 0.0
        hip_msg = Float32()
        hip_msg.data = hip_torque
        ankle_msg = Float32()
        ankle_msg.data = ankle_torque
        self.right_hip_pub.publish(hip_msg)
        self.right_ankle_pub.publish(ankle_msg)
        self.get_logger().info(f'RIGHT | Phase={self.right_gait_phase}, 'f'HipAssist={hip_torque:.2f}, AnkleAssist={ankle_torque:.2f}')

def main(args=None):
    rclpy.init(args=args)
    node=AssistNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()