from launch import LaunchDescription

from launch_ros.actions import Node


def generate_launch_description():

    return LaunchDescription([
        Node(
            package='exo_control',
            executable='csv_playback_node',
            name='csv_playback_node',
            parameters=[{'csv_path': '/mnt/d/ROS_Workspaces/exo_ros2_ws/sample_data/sample_walk.csv','publish_rate': 10.0,'loop_playback': True, 'subject_mass_kg':91.9, 'left_hip_column': 'hip_flexion_l','left_knee_column': 'knee_angle_l','left_ankle_column': 'ankle_angle_l','left_grf_column': 'left_foot_grf_si_norm','right_hip_column': 'hip_flexion_r','right_knee_column': 'knee_angle_r','right_ankle_column': 'ankle_angle_r','right_grf_column': 'right_foot_grf_si_norm','left_hip_velocity_column': 'hip_flexion_l_velocity','left_knee_velocity_column': 'knee_angle_l_velocity','left_ankle_velocity_column': 'ankle_angle_l_velocity','right_hip_velocity_column': 'hip_flexion_r_velocity','right_knee_velocity_column': 'knee_angle_r_velocity','right_ankle_velocity_column': 'ankle_angle_r_velocity',}]
        ),
        Node(
            package='exo_control',
            executable='gait_phase_node',
            name='gait_phase_node'
        ),
        Node(
            package='exo_control',
            executable='assist_node',
            name='assist_node',
            parameters=[{'hip_assistance_gain': 0.2,'ankle_assistance_gain': 0.2,'hip_assistive_torque_limit':15.0,'ankle_assistive_torque_limit':36.0}]
        ),
        Node(
            package='exo_control',
            executable='motor_command_node',
            name='motor_command_node',
            parameters=[{'hip_gear_ratio':8.0, 'ankle_gear_ratio':3.3, 'hip_motor_torque_limit':18.0, 'hip_motor_torque_limit':18.0,}]
        ),
        Node(
            package='exo_control',
            executable='power_monitor_node',
            name='power_monitor_node',
            parameters=[{'battery_voltage':24.0, 'motor_efficiency':0.6, 'battery_capacity_ah':4.5, 'depth_of_discharge':0.8}],
        ),
        Node(
            package='exo_control',
            executable='visualization_node',
            name='visualization_node',
        ),
        
    ])