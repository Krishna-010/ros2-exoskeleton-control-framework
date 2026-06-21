import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from std_msgs.msg import String
class GaitPhaseNode(Node):
    def __init__(self):
        super().__init__('gait_phase_node')
        self.get_logger().info('Gait Phase Node Started')
        self.declare_parameter('grf_threshold', 5.0)
        self.grf_threshold = self.get_parameter('grf_threshold').get_parameter_value().double_value
        self.get_logger().info(f'GRF threshold  set to {self.grf_threshold}')
        self.left_grf_subscription = self.create_subscription(Float32,'/left/foot_grf',self.left_grf_callback,10)
        self.right_grf_subscription = self.create_subscription(Float32,'/right/foot_grf',self.right_grf_callback,10)
        self.left_phase_publisher = self.create_publisher(String,'/left/gait_phase',10)
        self.right_phase_publisher = self.create_publisher(String,'/right/gait_phase',10)
    
    def compute_phase(self, grf):
        if grf >= self.grf_threshold:
            return "STANCE"
        else:
            return "SWING"
    
    def left_grf_callback(self, msg):
        grf = msg.data
        gait_phase = self.compute_phase(grf)
        phase_msg = String()
        phase_msg.data = gait_phase
        self.left_phase_publisher.publish(phase_msg)
        self.get_logger().info(f'Left GRF={grf:.2f}, Phase={gait_phase}')

    def right_grf_callback(self, msg):
        grf = msg.data
        gait_phase = self.compute_phase(grf)
        phase_msg = String()
        phase_msg.data = gait_phase
        self.right_phase_publisher.publish(phase_msg)
        self.get_logger().info(f'Right GRF={grf:.2f}, Phase={gait_phase}')
def main(args=None):
    rclpy.init(args=args)
    node=GaitPhaseNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
if __name__=='__main__':
    main()