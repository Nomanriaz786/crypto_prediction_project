from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = '-e .'

def get_requirements(file_path: str) -> List[str]:
    '''
    this function will return the list of requirements
    '''
    requirements = []

    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace('\n', "") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements

# Step 1: Define the setup configuration
setup(
    name='crypto_prediction_project',
    version='0.0.1',
    author='Muhammad_Noman_Riaz',
    author_email='muhammadnomanriaz599@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)

# Step 2: Install the package
# Run the following command in your terminal:
# pip install -e .

# Step 3: Verify the installation
# You can verify the installation by trying to import the package in a Python shell:
# python
# >>> import crypto_price_prediction