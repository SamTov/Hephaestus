|build| |madewithpython| |license|

Hephaestus
----------
Hephaestus is a python package aimed at performing simulations of unique systems. These range from simple pendulum
1, through complex deterministic chaotic systems, and anything that is of interest as a solvable problem
in physics. 

Installation
============
.. code-block:: bash

   git clone https://github.com/SamTov/Hephaestus.git
   cd Hephaestus
   pip3 install -e .


This command will install Hephaestus locally, i.e, python will look for the package in the directory you cloned. The 
reason for this approach is that it makes modifying the code very easy, and you will not need to reinstall after every
modification.

.. badges

.. |build| image:: https://img.shields.io/badge/Build-Passing-green.svg
    :alt: Build tests passing
    :target: https://github.com/SamTov/Hephaestus/blob/readme_badges/.github/workflows/pytest.yaml

.. |license| image:: https://img.shields.io/badge/License-GPLv3.0-green.svg
    :alt: Build tests passing
    :target: https://www.gnu.org/licenses/quick-guide-gplv3.en.html

.. |madewithpython| image:: https://img.shields.io/badge/Made%20With-Python-purple.svg
    :alt: Made with python