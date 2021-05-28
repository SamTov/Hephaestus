"""
Test the velocity verlet integration module.
"""
import unittest
from hephaestus.integrators.velocity_verlet import VelocityVerlet
from hephaestus.systems.single_pendulum import SinglePendulum


class TestVelocityVerlet(unittest.TestCase):
    """
    Class to test the euler integration module.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """
        Prepare for the Velocity verlet test.
        """
        model = SinglePendulum(time_step=1, steps=100, mass=1.0, gravity=1.0, theta_start=1.0)
        cls.integrator = VelocityVerlet(time_step=1.0, model=model)

    def test_perform_step(self):
        """
        Test the perform step method.
        """
        state = {'x0': 1.0,
                 'v0': 0.5,
                 'a0': 2.0}
        outcome = self.integrator.perform_step(state)
        self.assertEqual(outcome, {'x': 2.5, 'v': 1.200764, 'a': -0.5984721})


if __name__ == '__main__':
    unittest.main()