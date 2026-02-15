from setuptools import setup, find_packages

setup(
    name="legend-game",
    version="0.1.0",
    description="传奇风格游戏项目",
    author="",
    author_email="",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pygame==2.5.2"
    ],
    entry_points={
        "console_scripts": [
            "legend-game=main:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)