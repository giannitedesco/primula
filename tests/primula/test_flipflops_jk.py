import unittest
from primula import flipflops, Pull, Wire, Level


class Test_JKFlipFlopCircuit(unittest.TestCase):
    @staticmethod
    def construct_jk_flip_flop():
        clk = Wire('CLK', Pull.DOWN)
        s = Wire('S', Pull.DOWN)
        r = Wire('R', Pull.DOWN)
        q = Wire('Q')
        q_ = Wire('Q_')

        flipflop = flipflops.JK()
        clk.connect(flipflop.pins.clk)
        s.connect(flipflop.pins.j)
        r.connect(flipflop.pins.k)
        q.connect(flipflop.pins.q)
        q_.connect(flipflop.pins.q_)

        return clk, s, r, q, q_

    def test_reset(self):
        clk, s, r, q, q_ = self.construct_jk_flip_flop()
        r.drive(Level.HI)
        clk.pulse()
        self.assertEqual(s.level, Level.LO)
        self.assertEqual(r.level, Level.HI)
        self.assertEqual(q.level, Level.LO)
        self.assertEqual(q_.level, Level.HI)

    def test_set(self):
        clk, s, r, q, q_ = self.construct_jk_flip_flop()
        s.drive(Level.HI)
        clk.pulse()
        self.assertEqual(s.level, Level.HI)
        self.assertEqual(r.level, Level.LO)
        self.assertEqual(q.level, Level.HI)
        self.assertEqual(q_.level, Level.LO)

    def test_set_reset(self):
        clk, s, r, q, q_ = self.construct_jk_flip_flop()
        s.drive(Level.HI)
        clk.pulse()
        s.drive(Level.LO)
        self.assertEqual(s.level, Level.LO)
        self.assertEqual(r.level, Level.LO)
        self.assertEqual(q.level, Level.HI)
        self.assertEqual(q_.level, Level.LO)

        clk, s, r, q, q_ = self.construct_jk_flip_flop()
        r.drive(Level.HI)
        clk.pulse()
        r.drive(Level.LO)
        self.assertEqual(s.level, Level.LO)
        self.assertEqual(r.level, Level.LO)
        self.assertEqual(q.level, Level.LO)
        self.assertEqual(q_.level, Level.HI)

    def test_reset_set(self):
        clk, s, r, q, q_ = self.construct_jk_flip_flop()
        r.drive(Level.HI)
        clk.pulse()
        r.drive(Level.LO)
        self.assertEqual(s.level, Level.LO)
        self.assertEqual(r.level, Level.LO)
        self.assertEqual(q.level, Level.LO)
        self.assertEqual(q_.level, Level.HI)

        clk, s, r, q, q_ = self.construct_jk_flip_flop()
        s.drive(Level.HI)
        clk.pulse()
        s.drive(Level.LO)
        self.assertEqual(s.level, Level.LO)
        self.assertEqual(r.level, Level.LO)
        self.assertEqual(q.level, Level.HI)
        self.assertEqual(q_.level, Level.LO)

    def test_toggle_r(self):
        clk, s, r, q, q_ = self.construct_jk_flip_flop()
        r.drive(Level.HI)
        clk.pulse()
        self.assertEqual(q.level, Level.LO)
        self.assertEqual(q_.level, Level.HI)

        s.drive(Level.HI)
        r.drive(Level.HI)
        clk.pulse()

        self.assertEqual(q.level, Level.HI)
        self.assertEqual(q_.level, Level.LO)

    def test_toggle_s(self):
        clk, s, r, q, q_ = self.construct_jk_flip_flop()
        s.drive(Level.HI)
        clk.pulse()

        s.drive(Level.HI)
        r.drive(Level.HI)
        clk.pulse()

        self.assertEqual(q.level, Level.LO)
        self.assertEqual(q_.level, Level.HI)
