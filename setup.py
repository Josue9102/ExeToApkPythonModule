from setuptools import setup, find_packages

setup(
    name="ExeToApkPythonModule",  # Module name
    version="0.1.0",              # Module version
    packages=find_packages(),     # Automatically find all packages
    install_requires=[            # List of dependencies
        'buildozer',
        'pyinstaller',
        'apktool',
    ],
    entry_points={                # This allows the module to be run from the CLI
        'console_scripts': [
            'exe-to-apk = exe_to_apk.exe_to_apk:main',  # Define CLI command
        ],
    },
    include_package_data=True,
    python_requires='>=3.6',  # Python version requirement
)
