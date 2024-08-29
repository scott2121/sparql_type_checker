from setuptools import find_packages, setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="my_sparql_checker",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "type_check_sparql=sparql_type_check_tools.main:main",
        ],
    },
    install_requires=required, 
    author="Hikaru Nagazumi",
    author_email="max.hikaru@fuji.waseda.jp",
    url="https://github.com/scott2121/sparql_type_checker",  # リポジトリがある場合
)
