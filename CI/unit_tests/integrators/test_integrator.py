"""
Test the integrator module.
"""
import unittest
from hephaestus.integrators.integrator import Integrator
import pytest


class TestIntegrator(unittest.TestCase):
    """
    Class to test the integrator module.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """
        Prepare the test class.
        """
        cls.integrator = Integrator(time_step=1, model=None)

    def test_run_check(self):
        """
        Test the _run_check method.
        """
        a = None
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            self.integrator._run_check(a)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1


if __name__ == '__main__':
    unittest.main()
