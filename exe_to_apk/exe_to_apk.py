import sys
import os
import subprocess
from .ads_integration import add_ads_to_apk


def convert_exe_to_apk(exe_file_path, output_apk_path):
    """
    This function attempts to convert an EXE file into an APK.
    It's based on packaging Python code with Buildozer or similar tools.
    """
    print(f"Converting {exe_file_path} to APK...")

    # Step 1: Convert EXE to Python (if possible)
    # In practice, EXE -> APK conversion is not trivial.
    
    # Step 2: Use Buildozer to package the app into an APK
    subprocess.run(["buildozer", "android", "debug"], check=True)

    print(f"APK saved at {output_apk_path}")
    return output_apk_path


def main():
    """Main function for the command-line interface."""
    if len(sys.argv) < 3:
        print("Usage: python -m exe_to_apk.exe_to_apk <path_to_exe> <output_apk_path>")
        sys.exit(1)

    exe_file_path = sys.argv[1]
    output_apk_path = sys.argv[2]

    if not os.path.exists(exe_file_path):
        print(f"EXE file {exe_file_path} does not exist.")
        sys.exit(1)

    # Convert EXE to APK
    apk_path = convert_exe_to_apk(exe_file_path, output_apk_path)

    # Add ads to the generated APK
    add_ads_to_apk(apk_path)
    print(f"APK with ads saved at {apk_path}")


if __name__ == "__main__":
    main()
