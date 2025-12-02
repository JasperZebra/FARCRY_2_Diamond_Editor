from cx_Freeze import setup, Executable
import sys

# Build options
build_options = {
    'include_files': [
        # Include the assets folder with the icon
        ('assets', 'assets'),
    ],
    'packages': [
        # Standard libraries
        'os', 'sys', 'tkinter', 'struct', 'shutil',
        
        # Tkinter related
        'tkinter.filedialog', 'tkinter.messagebox',
    ],
    'excludes': [
        # Packages to exclude to reduce size
        'test', 'unittest', 'matplotlib', 'scipy', 'pandas', 'numpy',
        'PIL', 'sqlite3', 'email', 'html', 'http', 'urllib', 'xml'
    ],
    'include_msvcr': True,  # Include Microsoft Visual C Runtime
}

# Set up the executable
executables = [
    Executable(
        'fc2_diamond_editor.py',  # Your main script
        base='Win32GUI' if sys.platform == 'win32' else None,  # GUI application (no console)
        target_name='FC2_Diamond_Editor.exe',  # Name of the final executable
        icon='assets/fc2_icon.ico',  # Your custom icon
    )
]

# Setup
setup(
    name='Far Cry 2 Diamond Editor',
    version='1.0',
    description='Far Cry 2 Diamond Editor - Edit your diamonds instantly',
    author='Advanced Modding Tools',
    options={'build_exe': build_options},
    executables=executables
)

# To build: python setup.py build