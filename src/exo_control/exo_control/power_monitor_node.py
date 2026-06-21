import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from exo_interfaces.msg import JointVelocities


class PowerMonitorNode(Node):

    def __init__(self):
        super().__init__('power_monitor_node')
        self.declare_parameter('battery_voltage', 24.0)
        self.declare_parameter('motor_efficiency', 0.60)
        self.declare_parameter('battery_capacity_ah', 4.5)
        self.declare_parameter('depth_of_discharge', 0.80)

        self.battery_voltage = self.get_parameter('battery_voltage').get_parameter_value().double_value
        self.motor_efficiency = self.get_parameter('motor_efficiency').get_parameter_value().double_value
        self.battery_capacity_ah = self.get_parameter('battery_capacity_ah').get_parameter_value().double_value
        self.depth_of_discharge = self.get_parameter('depth_of_discharge').get_parameter_value().double_value

        self.left_hip_motor_torque = None
        self.right_hip_motor_torque = None
        self.left_ankle_motor_torque = None
        self.right_ankle_motor_torque = None

        self.left_joint_velocities = None
        self.right_joint_velocities = None

        self.left_hip_torque_sub = self.create_subscription(Float32,'/left/hip/motor_torque',self.left_hip_torque_callback,10)
        self.right_hip_torque_sub = self.create_subscription(Float32,'/right/hip/motor_torque',self.right_hip_torque_callback,10)
        self.left_ankle_torque_sub = self.create_subscription(Float32,'/left/ankle/motor_torque',self.left_ankle_torque_callback,10)
        self.right_ankle_torque_sub = self.create_subscription(Float32,'/right/ankle/motor_torque',self.right_ankle_torque_callback,10)
        self.left_velocity_sub = self.create_subscription(JointVelocities,'/left/joint_velocities',self.left_velocity_callback,10)
        self.right_velocity_sub = self.create_subscription(JointVelocities,'/right/joint_velocities',self.right_velocity_callback,10)

        self.get_logger().info('Power Monitor Node Started')
        self.get_logger().info(
            f'Battery={self.battery_voltage} V, '
            f'Efficiency={self.motor_efficiency}, '
            f'Capacity={self.battery_capacity_ah} Ah, '
            f'DoD={self.depth_of_discharge}'
        )

    def left_hip_torque_callback(self, msg):
        self.left_hip_motor_torque = msg.data
        self.compute_power()

    def right_hip_torque_callback(self, msg):
        self.right_hip_motor_torque = msg.data
        self.compute_power()

    def left_ankle_torque_callback(self, msg):
        self.left_ankle_motor_torque = msg.data
        self.compute_power()

    def right_ankle_torque_callback(self, msg):
        self.right_ankle_motor_torque = msg.data
        self.compute_power()

    def left_velocity_callback(self, msg):
        self.left_joint_velocities = msg
        self.compute_power()

    def right_velocity_callback(self, msg):
        self.right_joint_velocities = msg
        self.compute_power()

    def compute_power(self):
        if self.left_hip_motor_torque is None:
            return
        if self.right_hip_motor_torque is None:
            return
        if self.left_ankle_motor_torque is None:
            return
        if self.right_ankle_motor_torque is None:
            return
        if self.left_joint_velocities is None:
            return
        if self.right_joint_velocities is None:
            return

        left_hip_power = self.left_hip_motor_torque * self.left_joint_velocities.hip
        right_hip_power = self.right_hip_motor_torque * self.right_joint_velocities.hip

        left_ankle_power = self.left_ankle_motor_torque * self.left_joint_velocities.ankle
        right_ankle_power = self.right_ankle_motor_torque * self.right_joint_velocities.ankle

        total_mechanical_power = (abs(left_hip_power)+ abs(right_hip_power)+ abs(left_ankle_power)+ abs(right_ankle_power))

        total_electrical_power = total_mechanical_power / self.motor_efficiency
        total_current = total_electrical_power / self.battery_voltage

        usable_capacity_ah = self.battery_capacity_ah * self.depth_of_discharge

        if total_current > 0:
            estimated_runtime_hours = usable_capacity_ah / total_current
        else:
            estimated_runtime_hours = 0.0

        self.get_logger().info(
            f'Power | '
            f'MechAbs={total_mechanical_power:.2f} W, '
            f'Elec={total_electrical_power:.2f} W, '
            f'Current={total_current:.2f} A, '
            f'Runtime={estimated_runtime_hours:.2f} h'
        )


def main(args=None):
    rclpy.init(args=args)
    node = PowerMonitorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()