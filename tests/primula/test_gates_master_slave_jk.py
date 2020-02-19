import unittest
from primula import gates, Pull, Wire, Level


class Test_JKFlipFlopCircuit(unittest.TestCase):
    @staticmethod
    def construct_jk_latch():
        rnor = gates.Nor()
        snor = gates.Nor()
        kand = gates.And3()
        jand = gates.And3()

        j = Wire('J', Pull.DOWN)
        k = Wire('K', Pull.DOWN)
        clk = Wire('CLK', Pull.DOWN)
        s = Wire('S')
        r = Wire('R')
        q = Wire('Q')
        qc = Wire('Qc')

        k.connect(kand.pins.b)
        j.connect(jand.pins.b)

        clk.connect(kand.pins.a, jand.pins.c)

        s.connect(kand.pins.out, snor.pins.a)
        r.connect(jand.pins.out, rnor.pins.b)

        qc.connect(snor.pins.out, rnor.pins.a, kand.pins.c)
        q.connect(rnor.pins.out, snor.pins.b, jand.pins.a)

        return j, k, clk, s, r, q, qc

    def test_reset(self):
        j, k, clk, s, r, q, qc = self.construct_jk_latch()
        j.drive(Level.HI)
        clk.pulse()
        j.drive(Level.LO)
        self.assertEqual(s.level, Level.LO)
        self.assertEqual(r.level, Level.ERR)
        self.assertEqual(q.level, Level.LO)
        self.assertEqual(qc.level, Level.HI)

    def test_set(self):
        j, k, clk, s, r, q, qc = self.construct_jk_latch()
        k.drive(Level.HI)
        clk.pulse()
        k.drive(Level.LO)
        self.assertEqual(s.level, Level.LO)
        self.assertEqual(r.level, Level.LO)
        self.assertEqual(q.level, Level.HI)
        self.assertEqual(qc.level, Level.LO)
