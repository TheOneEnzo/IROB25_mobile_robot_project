from setuptools import setup, find_packages
import os
from glob import glob

package_name = 'irob_assignment_5'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),  # This will automatically find all packages
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
# Include srv files for generation
        (os.path.join('share', package_name, 'srv'), glob('srv/*.srv')),

        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')),
    ],
    # Add this line:
    python_requires='>=3.5',
    extras_require={
        'rosidl_default_runtime': ['rosidl_default_runtime'],
    },
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Parag Khanna',
    maintainer_email='paragk@kth.se',
    description='Intro to robotics-KTH assignment 5',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'explorer = irob_assignment_5.explorer:main',
            'goal_server = irob_assignment_5.goal_server:main',
            'activation_server = irob_assignment_5.activation_server:main',
            'at_goal_server = irob_assignment_5.at_goal_server:main',
        ],
    },
)
