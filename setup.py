from setuptools import setup, find_packages

setup(
    name='ExeToApkPythonModule',  # Name of the module
    version='0.1',
    packages=find_packages(),  # Automatically find all sub-packages
    install_requires=[          # Dependencies for the module
        'buildozer',
        'pyinstaller',
        'apktool',
    ],
    entry_points={              # Make the module executable via python -m
        'console_scripts': [
            'exe-to-apk=exe_to_apk.exe_to_apk:main',  # Define the entry point
        ],
    },
    include_package_data=True,  # Ensure MANIFEST.in is used
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
