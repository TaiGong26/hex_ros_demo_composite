import os
from glob import glob

from setuptools import find_packages
from setuptools import setup

package_name = 'hex_ros_demo_composite'


def get_files(tar: str, src: str):
    all_paths = glob(f'{src}/*')

    data_files = []
    for path in all_paths:
        if os.path.isfile(path):
            data_files.append((tar, [path]))
        elif os.path.isdir(path):
            sub_files = get_files(f'{tar}/{os.path.basename(path)}', path)
            data_files.extend(sub_files)

    return data_files


setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        *get_files('share/' + package_name, 'launch/ros2'),
        *get_files('share/' + package_name + '/config/ros2',
                   'config/ros2'),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='taigong26',
    maintainer_email='thetaigon@qq.com',
    description='Whole-body impedance control launch compositions',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [],
    },
)
