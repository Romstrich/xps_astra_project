from cx_Freeze import setup, Executable

executables = [Executable('GUI_module.py')]

setup(name='xps_astra',
      version='0.5dev',
      description='GUI_module',
      executables=executables)