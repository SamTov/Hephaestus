"""
Test the single pendulum module.
"""
import unittest
from hephaestus.systems.single_pendulum import SinglePendulum
from hephaestus.integrators.euler import Euler
import numpy as np


class TestSimplePendulum(unittest.TestCase):
    """
    Class to test the euler integration module.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """
        Prepare for the Pendulum class test test.
        """
        cls.pendulum = SinglePendulum(time_step=1,
                                      steps=100,
                                      mass=1.0,
                                      gravity=1.0,
                                      v0=0.5,
                                      theta_start=1.0)

    def test_compute_forces(self):
        """
        Test the compute forced method.
        """
        reference_f = -0.29552022
        forces = self.pendulum.compute_forces(0.3)
        self.assertEqual(forces, reference_f)

    def test_compute_pe(self):
        """
        Test the compute_pe method.
        """
        reference_pe = 0.04466349
        pe = self.pendulum._compute_pe(0.3)
        self.assertEqual(pe, reference_pe)

    def test_instantiate_system(self):
        """
        Test the instantiate system method.
        """
        self.assertEqual(self.pendulum.theta[0], np.deg2rad(1.0))
        self.assertEqual(self.pendulum.velocity[0], np.deg2rad(0.5))
        self.assertEqual(self.pendulum.force[0],
                         self.pendulum.compute_forces(np.deg2rad(1.0)))
        self.assertEqual(self.pendulum.pe[0],
                         self.pendulum._compute_pe(np.deg2rad(1.0)))
        self.assertEqual(self.pendulum.ke[0],
                         self.pendulum._compute_ke(np.deg2rad(0.5)))
        self.assertIsInstance(self.pendulum.integrator, Euler)

    def test_set_conditions(self):
        """
        Test the set conditions method.
        """
        reference = {'x0': np.deg2rad(1.0), 'v0': np.deg2rad(0.5), 'a0': self.pendulum.compute_forces(np.deg2rad(1.0))}
        state = self.pendulum._set_conditions(step=1)
        self.assertEqual(state, reference)

    def test_compute_velocity(self):
        """
        Test the compute velocity method.
        """
        self.assertEqual(self.pendulum._compute_velocity(3, 5), 2)

    def test_run_simulation(self):
        """
        Test the run simulation method.
        """
        self.pendulum.run_simulation()


if __name__ == '__main__':
    unittest.main()
