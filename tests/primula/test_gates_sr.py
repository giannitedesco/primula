import unittest
from primula import gates, Pull, Wire, Level


class Test_SRLatchCircuit(unittest.TestCase):
    @staticmethod
    def construct_sr_latch():
        nor1 = gates.Nor()
        nor2 = gates.Nor()

        s = Wire('S', Pull.DOWN)
        s.connect(nor2.pins.b)

        r = Wire('R', Pull.DOWN)
        r.connect(nor1.pins.a)

        q = Wire('Q')
        q.connect(nor1.pins.out, nor2.pins.a)

        qc = Wire('Qc')
        qc.connect(nor2.pins.out, nor1.pins.b)

        return s, r, q, qc

    def test_reset(self):
        s, r, q, qc = self.construct_sr_latch()
        r.pulse()
        self.assertEqual(s.level, Level.LO)
        self.assertEqual(r.level, Level.LO)
        self.assertEqual(q.level, Level.LO)
        self.assertEqual(qc.level, Level.HI)

    def test_set(self):
        s, r, q, qc = self.construct_sr_latch()
        s.pulse()
        self.assertEqual(s.level, Level.LO)
        self.assertEqual(r.level, Level.LO)
        self.assertEqual(q.level, Level.HI)
        self.assertEqual(qc.level, Level.LO)

    def test_set_reset(self):
        s, r, q, qc = self.construct_sr_latch()
        s.pulse()
        self.assertEqual(s.level, Level.LO)
        self.assertEqual(r.level, Level.LO)
        self.assertEqual(q.level, Level.HI)
        self.assertEqual(qc.level, Level.LO)

        s, r, q, qc = self.construct_sr_latch()
        r.pulse()
        self.assertEqual(s.level, Level.LO)
        self.assertEqual(r.level, Level.LO)
        self.assertEqual(q.level, Level.LO)
        self.assertEqual(qc.level, Level.HI)

    def test_reset_set(self):
        s, r, q, qc = self.construct_sr_latch()
        r.pulse()
        self.assertEqual(s.level, Level.LO)
        self.assertEqual(r.level, Level.LO)
        self.assertEqual(q.level, Level.LO)
        self.assertEqual(qc.level, Level.HI)

        s, r, q, qc = self.construct_sr_latch()
        s.pulse()
        self.assertEqual(s.level, Level.LO)
        self.assertEqual(r.level, Level.LO)
        self.assertEqual(q.level, Level.HI)
        self.assertEqual(qc.level, Level.LO)

    def test_invalid(self):
        s, r, q, qc = self.construct_sr_latch()
        s.drive(Level.HI)
        r.drive(Level.HI)
        self.assertEqual(s.level, Level.HI)
        self.assertEqual(r.level, Level.HI)
        self.assertEqual(q.level, Level.LO)
        self.assertEqual(qc.level, Level.LO)
