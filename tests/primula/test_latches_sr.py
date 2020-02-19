import unittest
from primula import latches, Pull, Wire, Level


class Test_SRLatchCircuit(unittest.TestCase):
    @staticmethod
    def construct_sr_latch():
        s = Wire('S', Pull.DOWN)
        r = Wire('R', Pull.DOWN)
        q = Wire('Q')
        q_ = Wire('Q_')

        latch = latches.SR()
        s.connect(latch.pins.s)
        r.connect(latch.pins.r)
        q.connect(latch.pins.q)
        q_.connect(latch.pins.q_)

        return s, r, q, q_

    def test_reset(self):
        s, r, q, q_ = self.construct_sr_latch()
        r.pulse()
        self.assertEqual(s.level, Level.LO)
        self.assertEqual(r.level, Level.LO)
        self.assertEqual(q.level, Level.LO)
        self.assertEqual(q_.level, Level.HI)

    def test_set(self):
        s, r, q, q_ = self.construct_sr_latch()
        s.pulse()
        self.assertEqual(s.level, Level.LO)
        self.assertEqual(r.level, Level.LO)
        self.assertEqual(q.level, Level.HI)
        self.assertEqual(q_.level, Level.LO)

    def test_set_reset(self):
        s, r, q, q_ = self.construct_sr_latch()
        s.pulse()
        self.assertEqual(s.level, Level.LO)
        self.assertEqual(r.level, Level.LO)
        self.assertEqual(q.level, Level.HI)
        self.assertEqual(q_.level, Level.LO)

        s, r, q, q_ = self.construct_sr_latch()
        r.pulse()
        self.assertEqual(s.level, Level.LO)
        self.assertEqual(r.level, Level.LO)
        self.assertEqual(q.level, Level.LO)
        self.assertEqual(q_.level, Level.HI)

    def test_reset_set(self):
        s, r, q, q_ = self.construct_sr_latch()
        r.pulse()
        self.assertEqual(s.level, Level.LO)
        self.assertEqual(r.level, Level.LO)
        self.assertEqual(q.level, Level.LO)
        self.assertEqual(q_.level, Level.HI)

        s, r, q, q_ = self.construct_sr_latch()
        s.pulse()
        self.assertEqual(s.level, Level.LO)
        self.assertEqual(r.level, Level.LO)
        self.assertEqual(q.level, Level.HI)
        self.assertEqual(q_.level, Level.LO)

    def test_invalid(self):
        s, r, q, q_ = self.construct_sr_latch()
        s.drive(Level.HI)
        r.drive(Level.HI)
        self.assertEqual(s.level, Level.HI)
        self.assertEqual(r.level, Level.HI)
        self.assertEqual(q.level, Level.FLT)
        self.assertEqual(q_.level, Level.FLT)
