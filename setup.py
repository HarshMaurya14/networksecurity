
from setuptools import find_packages, setup
from typing import List

def get_requirements(file_path: str) -> List[str]:
    """
    This function will return List of requirements
    """
    requirement_list: List[str] = []
    
    try:
        with open(file_path, 'r') as file:
            # Read lines from the file
            lines = file.readlines()
            
            # Process each line
            for line in lines:
                requirement = line.strip()
                
                # Ignore empty lines and "-e ."
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)
                    
    except FileNotFoundError:
        print("requirements.txt file not found")
    
    return requirement_list


setup(
    name="network_security",
    version="0.0.1",
    author="Harsh Maurya",
    author_email="m.harsh142005@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)