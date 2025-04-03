from setuptools import setup, find_packages

setup(
    name='hkspipelines',
    version='1.0.0',
    description='HKS custom Mailman posting pipeline',
    packages=find_packages(include=["pipelines", "pipelines.*"]),
    entry_points={
        'mailman.pipeline': [
            'hks-posting-pipeline = pipelines.hks:HKSPipeline'
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
