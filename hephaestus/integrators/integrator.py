"""
Parent class for all integrators.
"""

from typing import Any
import sys

class Integrator:
    """
    Class for all integrators.
    """

    def __init__(self, time_step: float):
        """
        Constructor for the __init__ class.

        Parameters
        ----------
        time_step : float
                Time step of the integrator
        initial_conditions : dict
                Initial conditions of the system.
        """
        self.time_step = time_step

    @staticmethod
    def _run_check(variable: Any):
        """

        Parameters
        ----------
        variable : Any
                If None, system will exit.

        Returns
        -------
        Will either pass or exit the kernel.
        """
        if variable is None:
            print(f"{variable} cannot be None, please set this and re-run.")
            sys.exit(1)

    def perform_step(self, initial_conditions: dict):
        """
        Perform a step of the integrator. Implemented in the child class.

        Parameters
        ----------
        initial_conditions : dict
                Conitions associated with the integrator.
        Returns
        -------
        Any information returned by the integrator.
        """
        raise NotImplementedError
