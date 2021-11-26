from distutils.core import setup

with open('requirements.txt') as f:
    reqs = f.read().splitlines()

setup(name='AIIntroProject',
      version='1.0',
      packages=['AI_intro_project'],
      install_requires=reqs
      )

# \AI-intro-project> pip install .
# \AI-intro-project> pip uninstall AIIntroProject
