from setuptools import setup

setup(
    name='rockrover',
    version='0.1',
    description='Bogie Runt Rover with Raspberry Pi - on the rocks!',
    author='Fischbacher Markus',
    author_email='fischbacher.markus@gmail.com',
    url='https://fischbacher.rocks',
    packages=['rockrover'],
    install_requires=['evdev','adafruit-circuitpython-motorkit'],
    zip_safe=False
)
