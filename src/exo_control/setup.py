from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'exo_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
        glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='bossoflords',
    maintainer_email='bossoflords@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'imu_sim_node=exo_control.imu_sim_node:main',
            'gait_phase_node=exo_control.gait_phase_node:main',
            'assist_node=exo_control.assist_node:main',
            'motor_command_node=exo_control.motor_command_node:main',
            'csv_playback_node = exo_control.csv_playback_node:main',
            'power_monitor_node = exo_control.power_monitor_node:main',
            'visualization_node = exo_control.visualization_node:main',
        ],
    },
)
