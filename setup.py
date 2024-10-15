from setuptools import setup

def get_requirements_from_file():
    with open("./requirements.txt") as f_in:
        requirements = f_in.read().splitlines()
    return requirements

setup(
    name="package",
    version='1.0',
    description='Pythonのディレクトリ構成のテスト用',
    author='Tsuchihashi Ryo',
    author_email='tsuchihashi-ryo@jbpo.or.jp',
    url='https://github.com/koboriakira/python_package',
    package_dir={"": "proteovis"},
    install_requires=get_requirements_from_file()
)