import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class MotorCommandNode(Node):
    def __init__(self):
        super().__init__('motor_command_node')
        self.declare_parameter('hip_gear_ratio', 8.0)
        self.declare_parameter('ankle_gear_ratio', 3.3)
        self.declare_parameter('hip_motor_torque_limit', 18.0)
        self.declare_parameter('ankle_motor_torque_limit', 18.0)
        self.hip_gear_ratio = self.get_parameter('hip_gear_ratio').get_parameter_value().double_value
        self.ankle_gear_ratio = self.get_parameter('ankle_gear_ratio').get_parameter_value().double_value
        self.hip_motor_torque_limit = self.get_parameter('hip_motor_torque_limit').get_parameter_value().double_value
        self.ankle_motor_torque_limit = self.get_parameter('ankle_motor_torque_limit').get_parameter_value().double_value
        self.get_logger().info(f'Hip gear ratio={self.hip_gear_ratio}, Ankle gear ratio={self.ankle_gear_ratio}')
        self.left_hip_pub = self.create_publisher(Float32,'/left/hip/motor_torque',10)
        self.right_hip_pub = self.create_publisher(Float32,'/right/hip/motor_torque',10)
        self.left_ankle_pub = self.create_publisher(Float32,'/left/ankle/motor_torque',10)
        self.right_ankle_pub = self.create_publisher(Float32,'/right/ankle/motor_torque',10)
        self.left_hip_sub = self.create_subscription(Float32,'/left/hip/assistive_torque',self.left_hip_callback,10)
        self.right_hip_sub = self.create_subscription(Float32,'/right/hip/assistive_torque',self.right_hip_callback,10)
        self.left_ankle_sub = self.create_subscription(Float32,'/left/ankle/assistive_torque',self.left_ankle_callback,10)
        self.right_ankle_sub = self.create_subscription(Float32,'/right/ankle/assistive_torque',self.right_ankle_callback,10)
        self.get_logger().info('Motor Node Started')
    def publish_motor_torque(self, assist_msg, gear_ratio, motor_limit, publisher, label):
        assistive_torque = assist_msg.data
        raw_motor_torque = assistive_torque / gear_ratio
        if raw_motor_torque > motor_limit:
            motor_torque = motor_limit
        elif raw_motor_torque < -motor_limit:
            motor_torque = -motor_limit
        else:
            motor_torque = raw_motor_torque
        motor_msg = Float32()
        motor_msg.data = motor_torque
        publisher.publish(motor_msg)
        self.get_logger().info(f'{label}: Assist={assistive_torque:.2f} Nm, 'f'RawMotor={raw_motor_torque:.2f} Nm, 'f'LimitedMotor={motor_torque:.2f} Nm')
    def left_hip_callback(self, msg):
        self.publish_motor_torque(msg,self.hip_gear_ratio,self.hip_motor_torque_limit,self.left_hip_pub,'Left Hip')
    def right_hip_callback(self, msg):
        self.publish_motor_torque(msg,self.hip_gear_ratio,self.hip_motor_torque_limit,self.right_hip_pub,'Right Hip')
    def left_ankle_callback(self, msg):
        self.publish_motor_torque(msg,self.ankle_gear_ratio,self.ankle_motor_torque_limit,self.left_ankle_pub,'Left Ankle')
    def right_ankle_callback(self, msg):
        self.publish_motor_torque(msg,self.ankle_gear_ratio,self.ankle_motor_torque_limit,self.right_ankle_pub,'Right Ankle')

def main(args=None):
    rclpy.init(args=args)
    node=MotorCommandNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()