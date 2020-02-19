import unittest
from primula import gates, Pull, Wire, Level


class Test_Wire(unittest.TestCase):
    def test_empty_drive(self):
        w = Wire()
        w.drive(Level.HI)
        self.assertEqual(w.level, Level.HI)

    def test_drive_gate_in(self):
        w = Wire()
        g = gates.And()
        w.connect(g.pins.a)
        w.drive(Level.HI)
        self.assertEqual(w.level, Level.HI)

    def test_drive_gate_out(self):
        w = Wire()
        g = gates.And()
        w.connect(g.pins.out)
        w.drive(Level.HI)
        self.assertEqual(w.level, Level.HI)

    def test_drive_gate_in(self):
        a = Wire('a', Pull.DOWN)
        b = Wire('b', Pull.DOWN)
        g = gates.And()

        a.connect(g.pins.a)
        b.connect(g.pins.b)

        self.assertEqual(g.pins.out.level, Level.LO)

        a.drive(Level.HI)
        self.assertEqual(g.pins.out.level, Level.LO)

        b.drive(Level.HI)
        self.assertEqual(g.pins.out.level, Level.HI)
