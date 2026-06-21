import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point


class VisualizationNode(Node):

    def __init__(self):
        super().__init__('visualization_node')
        self.left_hip_torque = 0.0
        self.marker_pub = self.create_publisher(Marker,'/visualization_marker',10)
        self.left_hip_sub = self.create_subscription(Float32,'/left/hip/assistive_torque',self.left_hip_callback,10)
        self.timer = self.create_timer(0.1,self.publish_marker)

        self.get_logger().info('Visualization Node Started')

    def left_hip_callback(self, msg):
        self.left_hip_torque = msg.data

    def publish_marker(self):
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "hip_torque"
        marker.id = 0
        marker.type = Marker.ARROW
        marker.action = Marker.ADD
        start = Point()
        start.x = 0.0
        start.y = 0.0
        start.z = 0.0
        end = Point()
        end.x = self.left_hip_torque * 0.05
        end.y = 0.0
        end.z = 0.0
        marker.points = [start, end]
        marker.scale.x = 0.03
        marker.scale.y = 0.06
        marker.scale.z = 0.08
        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0
        marker.color.a = 1.0
        self.marker_pub.publish(marker)


def main(args=None):
    rclpy.init(args=args)
    node = VisualizationNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()