import csv
import rclpy
from rclpy.node import Node
from exo_interfaces.msg import JointAngles
from exo_interfaces.msg import JointMoments
from exo_interfaces.msg import JointVelocities
from std_msgs.msg import Float32

class CsvPlaybackNode(Node):

    def __init__(self):
        super().__init__('csv_playback_node')
        self.declare_parameter('csv_path', '')
        self.declare_parameter('publish_rate', 10.0)
        self.declare_parameter('loop_playback', True)
        self.declare_parameter('subject_mass_kg', 91.9)
        self.declare_parameter('left_hip_column', 'hip_flexion_l')
        self.declare_parameter('left_knee_column', 'knee_angle_l')
        self.declare_parameter('left_ankle_column', 'ankle_angle_l')
        self.declare_parameter('left_grf_column', 'left_foot_grf_si_norm')
        self.declare_parameter('right_hip_column', 'hip_flexion_r')
        self.declare_parameter('right_knee_column', 'knee_angle_r')
        self.declare_parameter('right_ankle_column', 'ankle_angle_r')
        self.declare_parameter('right_grf_column', 'right_foot_grf_si_norm')
        self.declare_parameter('left_hip_moment_column', 'hip_flexion_l_moment')
        self.declare_parameter('left_knee_moment_column', 'knee_angle_l_moment')
        self.declare_parameter('left_ankle_moment_column', 'ankle_angle_l_moment')
        self.declare_parameter('right_hip_moment_column', 'hip_flexion_r_moment')
        self.declare_parameter('right_knee_moment_column', 'knee_angle_r_moment')
        self.declare_parameter('right_ankle_moment_column', 'ankle_angle_r_moment')
        self.declare_parameter('left_hip_velocity_column', 'hip_flexion_l_velocity')
        self.declare_parameter('left_knee_velocity_column', 'knee_angle_l_velocity')
        self.declare_parameter('left_ankle_velocity_column', 'ankle_angle_l_velocity')
        self.declare_parameter('right_hip_velocity_column', 'hip_flexion_r_velocity')
        self.declare_parameter('right_knee_velocity_column', 'knee_angle_r_velocity')
        self.declare_parameter('right_ankle_velocity_column', 'ankle_angle_r_velocity')
        self.csv_path = self.get_parameter('csv_path').get_parameter_value().string_value
        self.subject_mass_kg = self.get_parameter('subject_mass_kg').get_parameter_value().double_value
        self.publish_rate = self.get_parameter('publish_rate').get_parameter_value().double_value
        self.loop_playback = self.get_parameter('loop_playback').get_parameter_value().bool_value
        self.left_hip_column = self.get_parameter('left_hip_column').get_parameter_value().string_value
        self.left_knee_column = self.get_parameter('left_knee_column').get_parameter_value().string_value
        self.left_ankle_column = self.get_parameter('left_ankle_column').get_parameter_value().string_value
        self.left_grf_column = self.get_parameter('left_grf_column').get_parameter_value().string_value
        self.right_hip_column = self.get_parameter('right_hip_column').get_parameter_value().string_value
        self.right_knee_column = self.get_parameter('right_knee_column').get_parameter_value().string_value
        self.right_ankle_column = self.get_parameter('right_ankle_column').get_parameter_value().string_value
        self.right_grf_column = self.get_parameter('right_grf_column').get_parameter_value().string_value
        self.left_hip_moment_column = self.get_parameter('left_hip_moment_column').get_parameter_value().string_value
        self.left_knee_moment_column = self.get_parameter('left_knee_moment_column').get_parameter_value().string_value
        self.left_ankle_moment_column = self.get_parameter('left_ankle_moment_column').get_parameter_value().string_value
        self.right_hip_moment_column = self.get_parameter('right_hip_moment_column').get_parameter_value().string_value
        self.right_knee_moment_column = self.get_parameter('right_knee_moment_column').get_parameter_value().string_value
        self.right_ankle_moment_column = self.get_parameter('right_ankle_moment_column').get_parameter_value().string_value
        self.left_hip_velocity_column = self.get_parameter('left_hip_velocity_column').get_parameter_value().string_value
        self.left_knee_velocity_column = self.get_parameter('left_knee_velocity_column').get_parameter_value().string_value
        self.left_ankle_velocity_column = self.get_parameter('left_ankle_velocity_column').get_parameter_value().string_value
        self.right_hip_velocity_column = self.get_parameter('right_hip_velocity_column').get_parameter_value().string_value
        self.right_knee_velocity_column = self.get_parameter('right_knee_velocity_column').get_parameter_value().string_value
        self.right_ankle_velocity_column = self.get_parameter('right_ankle_velocity_column').get_parameter_value().string_value
        self.rows = []
        self.current_index = 0
        self.left_joint_publisher = self.create_publisher(JointAngles,'/left/joint_angles',10)
        self.right_joint_publisher = self.create_publisher(JointAngles,'/right/joint_angles',10)
        self.left_moment_publisher = self.create_publisher(JointMoments,'/left/joint_moments',10)
        self.right_moment_publisher = self.create_publisher(JointMoments,'/right/joint_moments',10)
        self.left_grf_publisher = self.create_publisher(Float32,'/left/foot_grf',10)
        self.right_grf_publisher = self.create_publisher(Float32,'/right/foot_grf',10)
        self.left_velocity_publisher = self.create_publisher(JointVelocities,'/left/joint_velocities',10)
        self.right_velocity_publisher = self.create_publisher(JointVelocities,'/right/joint_velocities',10)
        self.get_logger().info('CSV playback node started')
        self.get_logger().info(f'CSV path: {self.csv_path}')
        self.get_logger().info(f'Publish rate: {self.publish_rate}')
        self.get_logger().info(f'Loop playback: {self.loop_playback}')
        self.load_csv()
        timer_period = 1.0 / self.publish_rate
        self.timer = self.create_timer(timer_period,self.publish_next_row)

    def load_csv(self):
        if self.csv_path=='':
            self.get_logger().error('No CSV Path provided')
            return
        with open(self.csv_path,'r') as file:
            reader=csv.DictReader(file)
            for row in reader:
                self.rows.append(row)
        self.get_logger().info(f'Loaded {len(self.rows)} rows from CSV')

    def publish_next_row(self):
        if len(self.rows) == 0:
            return
        if self.current_index >= len(self.rows):
            if self.loop_playback:
                self.current_index = 0
            else:
                self.get_logger().info('Reached end of CSV playback.')
                return
        row = self.rows[self.current_index]
        left_msg = JointAngles()
        left_msg.hip = float(row[self.left_hip_column])
        left_msg.knee = float(row[self.left_knee_column])
        left_msg.ankle = float(row[self.left_ankle_column])
        right_msg = JointAngles()
        right_msg.hip = float(row[self.right_hip_column])
        right_msg.knee = float(row[self.right_knee_column])
        right_msg.ankle = float(row[self.right_ankle_column])
        left_moment_msg = JointMoments()
        left_moment_msg.hip = float(row[self.left_hip_moment_column])* self.subject_mass_kg
        left_moment_msg.knee = float(row[self.left_knee_moment_column])* self.subject_mass_kg
        left_moment_msg.ankle = float(row[self.left_ankle_moment_column])* self.subject_mass_kg
        right_moment_msg = JointMoments()
        right_moment_msg.hip = float(row[self.right_hip_moment_column])* self.subject_mass_kg
        right_moment_msg.knee = float(row[self.right_knee_moment_column])* self.subject_mass_kg
        right_moment_msg.ankle = float(row[self.right_ankle_moment_column])* self.subject_mass_kg
        left_velocity_msg = JointVelocities()
        left_velocity_msg.hip = float(row[self.left_hip_velocity_column])
        left_velocity_msg.knee = float(row[self.left_knee_velocity_column])
        left_velocity_msg.ankle = float(row[self.left_ankle_velocity_column])
        right_velocity_msg = JointVelocities()
        right_velocity_msg.hip = float(row[self.right_hip_velocity_column])
        right_velocity_msg.knee = float(row[self.right_knee_velocity_column])
        right_velocity_msg.ankle = float(row[self.right_ankle_velocity_column])
        left_grf_msg = Float32()
        left_grf_msg.data = float(row[self.left_grf_column])
        right_grf_msg = Float32()
        right_grf_msg.data = float(row[self.right_grf_column])
        self.left_joint_publisher.publish(left_msg)
        self.right_joint_publisher.publish(right_msg)
        self.left_grf_publisher.publish(left_grf_msg)
        self.right_grf_publisher.publish(right_grf_msg)
        self.left_moment_publisher.publish(left_moment_msg)
        self.right_moment_publisher.publish(right_moment_msg)
        self.left_velocity_publisher.publish(left_velocity_msg)
        self.right_velocity_publisher.publish(right_velocity_msg)
        self.get_logger().info(f'Row {self.current_index}: 'f'L_Hip={left_msg.hip:.2f}, L_Ankle={left_msg.ankle:.2f}, L_GRF={left_grf_msg.data:.2f} | 'f'R_Hip={right_msg.hip:.2f}, R_Ankle={right_msg.ankle:.2f}, R_GRF={right_grf_msg.data:.2f}')
        self.current_index += 1

def main(args=None):
    rclpy.init(args=args)
    node = CsvPlaybackNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()