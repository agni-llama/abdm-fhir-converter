from setuptools import find_packages, setup

setup(
    name='fhir_converter',
    packages=find_packages(include=['fhir_converter']),
    version='0.0.4',
    description='Dashmed fhir converter',
    install_requires=["fhir.resources"],
    author='Vibhor',
)