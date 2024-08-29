from setuptools import find_packages, setup

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
    package_data={
        'my_sparql_checker': ['.env'],  # パッケージ名: ファイルのリスト
    },
    author="Hikaru Nagazumi",
    author_email="max.hikaru@fuji.waseda.jp",
    url="https://github.com/yourusername/my_sparql_checker",  # リポジトリがある場合
)