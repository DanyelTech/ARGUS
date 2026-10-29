from setuptools import find_packages, setup

package_name = 'argus_bringup'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='danyel@runbox.com',
    description='ARGUS bringup package',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'status_publisher = argus_bringup.status_publisher:main',
            'status_subscriber = argus_bringup.status_subscriber:main',
        ],
    },
)
