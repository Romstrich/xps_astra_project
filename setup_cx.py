from cx_Freeze import setup, Executable

executables = [Executable('CLI_module.py')]

setup(name='xps_astra',
      version='0.4.a',
      description='CLI_module',
      executables=executables)