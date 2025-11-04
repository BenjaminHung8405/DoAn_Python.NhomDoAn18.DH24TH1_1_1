#!/usr/bin/env python3
"""
Build script for creating cross-platform executables using PyInstaller
"""

import os
import sys
import subprocess
import platform

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print("✓ PyInstaller is installed")
        return True
    except ImportError:
        print("PyInstaller not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("✗ Failed to install PyInstaller")
            return False

def build_executable():
    """Build executable for current platform"""
    print(f"\nBuilding executable for {platform.system()}...")

    # Base PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--windowed",  # No console window (for GUI apps)
        "--name", "Amplify",
        "--icon", os.path.join("images", "app_64.png"),
        "--add-data", f"images{os.pathsep}images",  # Include images folder
        "--add-data", f"ActivityIndicator{os.pathsep}ActivityIndicator",  # Include ActivityIndicator folder
        "main.py"
    ]

    # Platform-specific adjustments
    if platform.system() == "Windows":
        # Windows specific settings
        pass
    elif platform.system() == "Darwin":  # macOS
        cmd.extend([
            "--osx-bundle-identifier", "com.amplify.musicplayer"
        ])
    elif platform.system() == "Linux":
        # Linux specific settings
        pass

    try:
        subprocess.check_call(cmd)
        print("✓ Executable built successfully")
        print(f"✓ Find the executable in the 'dist' folder")
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        return False

    return True

def main():
    """Main build function"""
    print("Amplify Music Player - Cross-Platform Build Script")
    print("=" * 50)

    if not check_pyinstaller():
        sys.exit(1)

    if not build_executable():
        sys.exit(1)

    print("\nBuild completed!")
    print("Note: For true cross-platform distribution, build on each target platform.")

if __name__ == "__main__":
    main()