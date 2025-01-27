import re

from setuptools import setup

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()  # type: ignore

version = ''
with open('orion/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)  # type: ignore

if not version:
    raise RuntimeError('version is not set')

if version.endswith(('a', 'b', 'rc')):
    try:
        import subprocess

        p = subprocess.Popen(['git', 'rev-list', '--count', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            version += out.decode('utf-8').strip()
        p = subprocess.Popen(['git', 'rev-parse', '--short', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if out:
            version += '+g' + out.decode('utf-8').strip()
    except Exception:  # noqa
        pass

setup(
    name="orion",
    version=version,
    description="Orion is a fast, modular web framework built on Starlette for scalable, customizable applications.",
    url="https://github.com/jnsougata/orion",
    author="Sougata Jana",
    author_email="jnsougata@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["orion"],
    python_requires=">=3.8",
    install_requires=requirements,
)