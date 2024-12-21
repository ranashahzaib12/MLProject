from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = "-e ."

def get_requirements(file_path: str) -> List[str]:
    """
    This function reads a requirements file and returns a list of dependencies,
    excluding '-e .' if present.
    """
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.strip() for req in requirements]  # Remove newline characters

        # Remove '-e .' if present in the requirements
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    return requirements

setup(
    name='mlProject',
    version='0.0.1',
    author='Shahzaib',
    author_email='ranashahzaib2025@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')  # Corrected the function call and file name
)
