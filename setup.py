# -*- coding: utf-8 -*-
# File  : setup.py
# Author: huwei
# Date  : 2021/3/24

from setuptools import setup,find_packages

setup(
    name='my_tools',  # 包的名字
    author='hw',  # 作者
    version='0.1.0',  # 版本号

    description="hw personal python tools",  # 描述
    packages=find_packages(),
    python_requires='>=3.7',
    # 依赖包
    install_requires=[
        'numpy',
        'requests',
    ],
    extras_require={
        "sql":["pymysql"],
        "image":["opencv-python"],
    }
)