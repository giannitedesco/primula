import unittest
from primula import gates, Pull, Wire, Level


class Test_Inverter(unittest.TestCase):
    def test_err(self):
        n = gates.Inverter()
        err = Wire('err')
        err.connect(n.pins.inp, n.pins.out)
        err.pulse()
        self.assertEqual(err.level, Level.ERR)
