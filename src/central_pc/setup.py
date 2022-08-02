from setuptools import setup

package_name = 'central_pc'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sycamore',
    maintainer_email='sycamore@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'start = central_pc.centralPC:main',
            'test = central_pc.test:main',
            'deadzones_id = central_pc.DeadzoneActionClient:main',
            'identification = central_pc.IdentificationActionClient:main',
            'control = central_pc.ControlActionClient:main',
            'gamepad = central_pc.GamepadActionServer:main',
        ],
    },
)
