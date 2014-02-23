###!/usr/bin/env python
"""
unit tests for FixedPoint

This module is intended to be run as a regression test during Python
installation
"""

import sys

# Added the module path to sys.path
sys.path.extend([ '../../'])
#print sys.path

from fixedpoint import *


__copyright__  = "Copyright (C) Python Software Foundation"
__author__     = "Downright Software Collective"
__version__    = 0, 1, 0

import unittest
from fixedpoint import FixedPoint, bankersRounding, addHalfAndChop, DEFAULT_PRECISION

# declare a derived class from FixedPoint for testing
class SonOfFixedPoint(FixedPoint):
    """A subclass of FixedPoint for testing"""
    def __init__(self, value=0, precision=DEFAULT_PRECISION):
        FixedPoint.__init__(self, value, precision)
    def __repr__(self):
        return "SonOfFixedPoint" + `(str(self), self.p)`

class FixedPointTest(unittest.TestCase):
    """Unit tests for FixedPointy"""
    
    def testCreateDefault(self):
        """Simply create a default object."""
        n = FixedPoint();
        self.assertEquals(n.get_precision(), DEFAULT_PRECISION)
        self.assertEquals(long(n), 0)

        n = SonOfFixedPoint();
        self.assertEquals(n.get_precision(), DEFAULT_PRECISION)
        self.assertEquals(long(n), 0)

    def testCreateFromNone(self):
        """try to slip None in"""
        self.failUnlessRaises(TypeError, FixedPoint, None);

    def testCreateFromString(self):
        """Create a FixedPoint from a string"""

        # try an empty string
        self.failUnlessRaises(ValueError, FixedPoint, "");

        # try a fixed point zero
        n = FixedPoint("0");
        self.assertEquals(n.precision, DEFAULT_PRECISION)
        self.assertEquals(n.n, 0L)

        # try a floating point zero
        n = FixedPoint("0.0");
        self.assertEquals(n.precision, DEFAULT_PRECISION)
        self.assertEquals(n.n, 0L)

        # try a floating point number with a positive exponent
        n = FixedPoint("42.3e5");
        self.assertEquals(n.precision, DEFAULT_PRECISION)
        self.assertEquals(n.n, 423000000L)

        # try a floating point number with a negative exponent
        n = FixedPoint("42.3e-1");
        self.assertEquals(n.precision, DEFAULT_PRECISION)
        self.assertEquals(n.n, 423L)

        # try truncating the precision
        n = FixedPoint("42.123");
        self.assertEquals(n.precision, DEFAULT_PRECISION)
        self.assertEquals(n.n, 4212)

    def testCreateFromIntOrLong(self):
        """Create a FixedPoint from an int or a  long"""

        # try a negative
        n = FixedPoint(-333);
        self.assertEquals(n.precision, DEFAULT_PRECISION)
        self.assertEquals(n.n, -33300)

        # try a zero
        n = FixedPoint(0);
        self.assertEquals(n.precision, DEFAULT_PRECISION)
        self.assertEquals(n.n, 0L)

        # try a positive
        n = FixedPoint(333);
        self.assertEquals(n.precision, DEFAULT_PRECISION)
        self.assertEquals(n.n, 33300L)

    def testCreateFromFixedPoint(self):
        """Create a FixedPoint from another FixedPoint"""

        # try a negative
        n = FixedPoint(-333);
        self.assertEquals(n.precision, DEFAULT_PRECISION)
        self.assertEquals(n.n, -33300L)

        # try a negative
        x = FixedPoint(n);
        self.assertEquals(x.precision, DEFAULT_PRECISION)
        self.assertEquals(x.n, -33300L)

        x = SonOfFixedPoint(n);
        self.assertEquals(x.precision, DEFAULT_PRECISION)
        self.assertEquals(x.n, -33300L)

    def testCreateFromFloat(self):
        """Create a FixedPoint from a floating point number"""

        # try a floating point zero
        n = FixedPoint(0.0);
        self.assertEquals(n.precision, DEFAULT_PRECISION)
        self.assertEquals(n.n, 0L)

        # try a floating point number with a positive exponent
        n = FixedPoint(42.3e5);
        self.assertEquals(n.precision, DEFAULT_PRECISION)
        self.assertEquals(n.n, 423000000L)

        # try a floating point number with a negative exponent
        n = FixedPoint(42.3e-1);
        self.assertEquals(n.precision, DEFAULT_PRECISION)
        self.assertEquals(n.n, 423L)

        # try truncating the precision
        n = FixedPoint(42.123);
        self.assertEquals(n.precision, DEFAULT_PRECISION)
        self.assertEquals(n.n, 4212L)

    def testCreateFromObject(self):
        """
        Try to create a FixedPoint from something that can't be
        coerced to a number.
        """
        self.failUnlessRaises(TypeError, FixedPoint, object);
        self.failUnlessRaises(TypeError, SonOfFixedPoint, object);

    def testSetAndGetPrecision(self):
        """Change and retrieve the precision of an existin object"""
        
        # try a floating point number with a negative exponent
        n = FixedPoint(42.3e-1);
        self.assertEquals(n.get_precision(), DEFAULT_PRECISION)
        self.assertEquals(n.precision, DEFAULT_PRECISION)
        self.assertEquals(n.n, 423L)

        n = SonOfFixedPoint(42.3e-1);
        self.assertEquals(n.get_precision(), DEFAULT_PRECISION)
        self.assertEquals(n.precision, DEFAULT_PRECISION)
        self.assertEquals(n.n, 423L)

        # try something that's not a number
        self.failUnlessRaises(TypeError, n.set_precision, object);
        self.failUnlessRaises(TypeError, n.precision, object);

        # try a negative number
        self.failUnlessRaises(ValueError, n.set_precision, -3);

        # try a precision greater than we started with
        newprecision = DEFAULT_PRECISION + 1
        n.set_precision(newprecision)
        self.assertEquals(n.get_precision(), newprecision)
        self.assertEquals(n.n, 4230L)

        precision = n.precision + 1
        n.precision += 1
        self.assertEquals(n.precision, precision)

        # try a precision less than we started with
        newprecision = DEFAULT_PRECISION - 1
        n.set_precision(newprecision)
        self.assertEquals(n.get_precision(), newprecision)
        self.assertEquals(n.n, 42)

    def test__str__(self):
        """test conversion to string"""

        # try the default
        n = FixedPoint()
        self.assertEquals(str(n), "0.00")
        
        n = SonOfFixedPoint()
        self.assertEquals(str(n), "0.00")
        
        # try a floating point number with a negative exponent
        n = FixedPoint(42.3e-1);
        self.assertEquals(str(n), "4.23")
        
        n = SonOfFixedPoint(42.3e-1);
        self.assertEquals(str(n), "4.23")
        
        # try a negative floating point number
        n = FixedPoint(-4.23);
        self.assertEquals(str(n), "-4.23")

        # try an int
        n = FixedPoint(1, 0);
        self.assertEquals(str(n), "1.")
        
    def test__repr__(self):
        """test representation"""

        REPR_FORMAT = "FixedPoint('%s', %d)"

        # try the default
        n = FixedPoint()
        self.assertEquals(repr(n), REPR_FORMAT % (str(n), n.get_precision()))
        
        # try a floating point number with a negative exponent
        n = FixedPoint(42.3e-1);
        self.assertEquals(repr(n), REPR_FORMAT % (str(n), n.get_precision()))
        
        # try a negative floating point number
        n = FixedPoint(-4.23);
        self.assertEquals(repr(n), REPR_FORMAT % (str(n), n.get_precision()))

        # try an int
        n = FixedPoint(1, 0);
        self.assertEquals(repr(n), REPR_FORMAT % (str(n), n.get_precision()))
        
        SON_OF_FORMAT = "SonOfFixedPoint('%s', %d)"

        # try the default
        n = SonOfFixedPoint()
        self.assertEquals(repr(n), SON_OF_FORMAT % (str(n), n.get_precision()))
        
        # try a floating point number with a negative exponent
        n = SonOfFixedPoint(42.3e-1);
        self.assertEquals(repr(n), SON_OF_FORMAT % (str(n), n.get_precision()))
        
        # try a negative floating point number
        n = SonOfFixedPoint(-4.23);
        self.assertEquals(repr(n), SON_OF_FORMAT % (str(n), n.get_precision()))

        # try an int
        n = SonOfFixedPoint(1, 0);
        self.assertEquals(repr(n), SON_OF_FORMAT % (str(n), n.get_precision()))
        
    def test__copy__(self):
        """test shallow copy"""
        import copy
        
        # try a negative floating point number
        n = FixedPoint(-4.23);
        self.assertEquals(n, copy.copy(n))
        self.failIf(n is copy.copy(n))
        
        # try a negative floating point number
        n = SonOfFixedPoint(-4.23);
        self.assertEquals(n, copy.copy(n))
        self.failIf(n is copy.copy(n))
        
    def test__deepcopy__(self):
        """test deep copy"""
        import copy
        
        # try a negative floating point number
        n = FixedPoint(-4.23);

        self.assertEquals(n, copy.deepcopy(n))
        self.failIf(n is copy.deepcopy(n))

        # try a negative floating point number
        n = SonOfFixedPoint(-4.23);

        self.assertEquals(n, copy.deepcopy(n))
        self.failIf(n is copy.deepcopy(n))

    def test__cmp__(self):
        """test compare"""

        # test two defaults
        a = FixedPoint()
        b = FixedPoint()
        self.failIf(a < b)
        self.failUnless(a == b)
        self.failIf(a > b)
        
        # test equal precision
        a = FixedPoint(1.11)
        b = FixedPoint(1.12)
        self.failUnless(a < b)
        self.failIf(a == b)
        self.failIf(a > b)
        
        # test unequal precision
        a = FixedPoint(1.125, 3)
        b = FixedPoint(1.12)
        self.failIf(a < b)
        self.failIf(a == b)
        self.failUnless(a > b)

        # test equal precision, with subclass
        a = FixedPoint(1.11)
        b = SonOfFixedPoint(1.12)
        self.failUnless(a < b)
        self.failIf(a == b)
        self.failIf(a > b)
        
    def test__hash__(self):
        """test the hash function"""

        # test that we don't choke
        # 2002-09-19 dfort -- we could test a lot more here
        hash(FixedPoint())
        
    def test__nonzero__(self):
        """test the truth value"""

        # test the default
        self.failIf(FixedPoint())

        # test one that should be true
        self.failUnless(FixedPoint(1.0e-15, 15))
        
    def test__neg__(self):
        """test negative"""

        # test the default
        self.failIf(-FixedPoint())

        # test one that should be true
        self.failUnless(-FixedPoint(-1.0e-15, 15))
        
    def test__abs__(self):
        """test absolute value"""

        # test the default
        d = FixedPoint()
        self.assertEquals(abs(d), d)

        # test a negative
        n = FixedPoint(-1.0e-15, 15)
        self.assertEquals(abs(n), -n)
        
    def test__add__(self):
        """test addition"""

        #test with a float
        a = FixedPoint(3.33)
        b = 3.3333
        c = a + b
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.n, 666)

        # test two operands with the same precision
        a = FixedPoint(3.33)
        b = FixedPoint(6.66)
        c = a + b 
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.n, 999L)

        # test two operands with differing precision
        a = FixedPoint(3.33)
        b = FixedPoint(6.66, 3)
        c = a + b
        self.assertEquals(c.precision, 3)
        self.assertEquals(c.n, 9990L)

        a = FixedPoint(3.33)
        b = FixedPoint(6.666, 3)
        c = a + b 
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.n, 9996L)

        # test negatives
        a = FixedPoint(3.33)
        b = FixedPoint(-6.66, 3)
        c = a + b 
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.precision, 3)
        self.assertEquals(c.n, -3330L)

        a = FixedPoint(-3.33)
        b = FixedPoint(-6.666, 3)
        c = a + b
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.precision, 3)
        self.assertEquals(c.n, -9996L)

        # test subclass
        a = FixedPoint(3.33)
        b = SonOfFixedPoint(6.666, 3)
        c = a + b

        self.assert_(isinstance(c, FixedPoint))
        self.assertEquals(c.precision, 3)
        self.assertEquals(c.n, 9996L)

        a = FixedPoint(3.33)
        b = SonOfFixedPoint(6.666, 3)
        c = b + a
        self.assertEquals(type(c), type(b))
        self.assertEquals(c.precision, 3)
        self.assertEquals(c.n, 9996)

    def test__radd__(self):
        """test addition as the right argument"""

        # test with a float
        a = FixedPoint(3.33)
        b = 3.3333
        c = b + a
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.precision, DEFAULT_PRECISION)
        self.assertEquals(c.n, 666L)


        # test subclass
        a = SonOfFixedPoint(3.33)
        b = 3.3333
        c = b + a
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.precision, DEFAULT_PRECISION)
        self.assertEquals(c.n, 666L)

    def test__sub__(self):
        """test subtraction"""

        # test with a float
        a = FixedPoint(3.33)
        b = 3.3333
        c = a - b
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.precision, DEFAULT_PRECISION)
        self.assertEquals(c, 0L)

        a = SonOfFixedPoint(3.33)
        b = 3.3333
        c = a - b
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.precision, DEFAULT_PRECISION)
        self.assertEquals(c, 0L)

        # test two operands with the same precision
        a = FixedPoint(3.33)
        b = FixedPoint(6.66)
        c = b - a
        self.assertEquals(c.precision, DEFAULT_PRECISION)
        self.assertEquals(c.n, 333L)

        # test two operands with differing precision
        a = FixedPoint(3.33)
        b = FixedPoint(6.66, 3)
        c = b - a
        self.assertEquals(c.precision, 3)
        self.assertEquals(c.n, 3330L)

        a = FixedPoint(3.33)
        b = FixedPoint(6.666, 3)
        c = b - a
        self.assertEquals(c.precision, 3)
        self.assertEquals(c.n, 3336L)

        # test negatives
        a = FixedPoint(3.33)
        b = FixedPoint(-6.66, 3)
        c = b - a
        self.assertEquals(c.precision, 3)
        self.assertEquals(c.n, -9990L)

        a = FixedPoint(-3.33)
        b = FixedPoint(-6.666, 3)
        c = b - a
        self.assertEquals(c.precision, 3)
        self.assertEquals(c.n, -3336L)

        # test subclass
        a = FixedPoint(3.33)
        b = SonOfFixedPoint(6.66, 3)
        c = a - b
        self.assertEquals(c.precision, 3)
        self.assertEquals(c.n, -3330L)
        #self.assertEquals(type(c), type(b))
        self.assert_(isinstance(c, FixedPoint))

        a = FixedPoint(3.33)
        b = SonOfFixedPoint(6.66, 3)
        c = b - a
        self.assertEquals(c.precision, 3)
        self.assertEquals(c.n, 3330L)
        self.assertEquals(type(c), type(b))

    def test__rsub__(self):
        """test subtraction as the right hand argument"""

        # test with a float
        a = FixedPoint(3.33)
        b = 1.11
        c = b - a
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.precision, DEFAULT_PRECISION)
        self.assertEquals(c.n, -222)

        a = SonOfFixedPoint(3.33)
        b = 1.11
        c = b - a
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.precision, DEFAULT_PRECISION)
        self.assertEquals(c.n, -222)


    def test__mul__(self):
        """test multiplication"""
        
        #test with a float
        a = FixedPoint(2)
        b = 3.3333
        c = a * b
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.precision, DEFAULT_PRECISION)
        self.assertEquals(c.n, 666L)

        # test two operands with the same precision
        a = FixedPoint(3.33)
        b = FixedPoint(6.66)
        c = b * a
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.precision, DEFAULT_PRECISION)
        self.assertEquals(c.n, 2218L)

        # test two operands with differing precision
        a = FixedPoint(3.33)
        b = FixedPoint(6.66, 3)
        c = b * a
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.precision, 3)
        self.assertEquals(c.n, 22178L)

        # test negatives
        a = FixedPoint(3.33)
        b = FixedPoint(-6.66, 3)
        c = b * a
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.precision, 3)
        self.assertEquals(c.n, -22178L)

        a = FixedPoint(-3.33)
        b = FixedPoint(-6.666, 3)
        c = b * a
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.precision, 3)
        self.assertEquals(c.n, 22198L)

        # test subclass
        a = FixedPoint(3.33)
        b = SonOfFixedPoint(6.66, 3)
        c = a * b
        #self.assertEquals(type(c), type(b))
        self.assert_(isinstance(c, FixedPoint))
        self.assertEquals(c.precision, 3)
        self.assertEquals(c.n, 22178L)

        a = FixedPoint(3.33)
        b = SonOfFixedPoint(6.66, 3)
        c = b * a
        self.assertEquals(type(c), type(b))
        self.assertEquals(c.precision, 3)
        self.assertEquals(c.n, 22178L)

        a = FixedPoint(3.33)
        b = 3
        c = a * b
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.precision, DEFAULT_PRECISION)
        self.assertEquals(c.n, 999)
        
    def test__rmul__(self):
        """test multiplication"""
        
        a = FixedPoint(3.33)
        b = 3
        c = b * a
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.precision, DEFAULT_PRECISION)
        self.assertEquals(c.n, 999L)
        
        a = SonOfFixedPoint(3.33)
        b = 3
        c = b * a
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.precision, DEFAULT_PRECISION)
        self.assertEquals(c.n, 999L)
        

    def test__div__(self):
        """test division"""
        
        #test with a float
        a = FixedPoint(6.66)
        b = 3.3333
        c = a / b
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.precision, DEFAULT_PRECISION)
        self.assertEquals(c.n, 200L)

        a = SonOfFixedPoint(6.66)
        b = 3.3333
        c = a / b
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.precision, DEFAULT_PRECISION)
        self.assertEquals(c.n, 200L)

        # test two operands with the same precision
        a = FixedPoint(3.33)
        b = FixedPoint(6.66)
        c = b / a
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.precision, DEFAULT_PRECISION)
        self.assertEquals(c.n, 200L)

        # test two operands with differing precision
        a = FixedPoint(1)
        b = FixedPoint(3, 3)
        c = b / a
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.precision, 3)
        self.assertEquals(c.n, 3000L)

        # test negatives
        a = FixedPoint(3.33)
        b = FixedPoint(-6.66, 3)
        c = b / a
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.precision, 3)
        self.assertEquals(c.n, -2000L)

        a = FixedPoint(-3.33)
        b = FixedPoint(-6.66)
        c = b / a
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.precision, DEFAULT_PRECISION)
        self.assertEquals(c.n, 200L)

        # test subclass
        a = FixedPoint(3.33)
        b = SonOfFixedPoint(6.66, 3)
        c = a / b
        #self.assertEquals(type(c), type(b))
        self.assert_(isinstance(c, FixedPoint))
        self.assertEquals(c.precision, 3)
        self.assertEquals(c.n, 500)

        a = FixedPoint(3.33)
        b = SonOfFixedPoint(6.66, 3)
        c = b / a
        self.assertEquals(type(c), type(b))
        self.assertEquals(c.precision, 3)
        self.assertEquals(c.n, 2000L)

        a = FixedPoint(3.33)
        b = 3
        c = a / b
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.precision, DEFAULT_PRECISION)
        self.assertEquals(c.n, 111L)
        
    def test__rdiv__(self):
        """test right division"""
        
        a = FixedPoint(3)
        b = 1
        c = b / a
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.precision, DEFAULT_PRECISION)
        self.assertEquals(c.n, 33L)

        a = SonOfFixedPoint(3.33, 6)
        b = 1
        c = b / a
        self.assertEquals(type(c), type(a))
        self.assertEquals(c.precision, 6)
        self.assertEquals(c.n, 300300)

    def test__divmod__(self):
        """test integer division with modulo"""
        a = FixedPoint(3.33)
        q, m = divmod(a, 2)
        self.assertEquals(type(q), type(1L))
        self.assertEquals(type(m), type(a))
        self.assertEquals(q, 1)
        self.assertEquals(m, FixedPoint(1.33))
        
        a = SonOfFixedPoint(3.33)
        q, m = divmod(a, 2)
        self.assertEquals(type(q), type(1L))
        self.assertEquals(type(m), type(a))
        self.assertEquals(q, 1L)
        self.assertEquals(m, FixedPoint(1.33))
        
        a = FixedPoint(3.33)
        b = FixedPoint(1.11)
        q, m = divmod(a, b)
        self.assertEquals(type(q), type(1L))
        self.assertEquals(type(m), type(a))
        self.assertEquals(q, 3L)
        self.assertEquals(m, FixedPoint(0))

# 2002-10-19 dougfort -- this produces infinite recursion
##        a = FixedPoint(3.33)
##        b = SonOfFixedPoint(1.11)
##        q, m = divmod(a, b)
##        self.assertEquals(type(q), type(1L))
##        self.assertEquals(type(m), type(a))
##        self.assertEquals(q, 3L)
##        self.assertEquals(m, FixedPoint(0))
        
    def test__rdivmod__(self):
        """test right integer division with modulo"""
        a = FixedPoint(3.33)
        q, m = divmod(4, a)
        self.assertEquals(q, 1L)
        self.assertEquals(m, FixedPoint(0.67))
        
    def test__mod__(self):
        """test modulo"""
        a = FixedPoint(3.33)
        b = 2
        c = a % b
        self.assertEquals(c, FixedPoint(1.33))
        
        a = FixedPoint(3.33)
        b = FixedPoint(1.111)
        c = a % b
        self.assertEquals(c, FixedPoint(0))
        
    def test__rmod__(self):
        """test right modulo"""
        a = FixedPoint(3.33)
        b = 4
        c = b % a
        self.assertEquals(c, FixedPoint(0.67))

        a = FixedPoint(3.33)
        b = SonOfFixedPoint(6.666)
        c = b % a
        self.assertEquals(c, SonOfFixedPoint(0.01))

    def test__float__(self):
        """test casting to float"""
        self.assertEquals(float(4), float(FixedPoint(4)))
        self.assertEquals(3.1416, float(FixedPoint(3.14159, 4)))
        
    def test__long__(self):
        """test casting to long"""
        self.assertEquals(4, long(FixedPoint(4)))
        self.assertEquals(3, long(FixedPoint(3.14159, 4)))
        
    def test__int__(self):
        """test casting to int"""
        self.assertEquals(4, int(FixedPoint(4)))
        self.assertEquals(3, int(FixedPoint(3.14159, 4)))
        
    def testFrac(self):
        """test return of the fractional portion"""
        self.assertEquals(
            FixedPoint(), FixedPoint(4).frac())
        self.assertEquals(
            FixedPoint(0.1416, 4),
            FixedPoint(3.14159, 4).frac())

    def testBankersRounding(self):
        """test that bankers rounding works as expected"""
        prevrounding = FixedPoint.round
        FixedPoint.round = bankersRounding
        # we expect to round 1 up because it's odd
        self.assertEquals(
            FixedPoint(1.5,0), FixedPoint(2.0,0))
        # we expect to leave 2 alone because it's even
        self.assertEquals(
            FixedPoint(2.5,0), FixedPoint(2.0,0))
        FixedPoint.round = prevrounding

    def testAddHalfAndChop(self):
        """test that 'add half and chop' rounding works as expected"""
        prevrounding = FixedPoint.round
        FixedPoint.round = addHalfAndChop
        # we expect to round 1 up
        self.assertEquals(
            FixedPoint(1.5,0), FixedPoint(2.0,0))
        # we expect to round 2 up as well
        self.assertEquals(
            FixedPoint(2.5,0), FixedPoint(3.0,0))
        FixedPoint.round = prevrounding

    def testOriginal(self):
        """Tim's oringinal tests in __main__ of fixedpoint.py"""
        fp = FixedPoint
        o = fp("0.1")
        self.assert_(str(o) == "0.10")
        t = fp("-20e-2", 5)
        self.assert_(str(t) == "-0.20000")
        self.assert_(t < o)
        self.assert_(o > t)
        self.assert_(min(o, t) == min(t, o) == t)
        self.assert_(max(o, t) == max(t, o) == o)
        self.assert_(o != t)
        self.assert_(--t == t)
        self.assert_(abs(t) > abs(o))
        self.assert_(abs(o) < abs(t))
        self.assert_(o == o and t == t)
        self.assert_(t.copy() == t)
        self.assert_(o == -t/2 == -.5 * t)
        self.assert_(abs(t) == o + o)
        self.assert_(abs(o) == o)
        self.assert_(o/t == -0.5)
        self.assert_(-(t/o) == (-t)/o == t/-o == 2)
        self.assert_(1 + o == o + 1 == fp(" +00.000011e+5  "))
        self.assert_(1/o == 10)
        self.assert_(o + t == t + o == -o)
        self.assert_(2.0 * t == t * 2 == "2" * t == o/o * 2L * t)
        self.assert_(1 - t == -(t - 1) == fp(6L)/5)
        self.assert_(t*t == 4*o*o == o*4*o == o*o*4)
        self.assert_(fp(2) - "1" == 1)
        self.assert_(float(-1/t) == 5.0)
        for p in range(20):
            self.assert_(42 + fp("1e-20", p) - 42 == 0)
        self.assert_(1/(42 + fp("1e-20", 20) - 42) == fp("100.0E18"))
        o = fp(".9995", 4)
        self.assert_(1 - o == fp("5e-4", 10))
        o.set_precision(3)
        self.assert_(o == 1)
        o = fp(".9985", 4)
        o.set_precision(3)
        self.assert_(o == fp(".998", 10))
        self.assert_(o == o.frac())
        o.set_precision(100)
        self.assert_(o == fp(".998", 10))
        o.set_precision(2)
        self.assert_(o == 1)
        x = fp(1.99)
        self.assert_(long(x) == -long(-x) == 1L)
        self.assert_(int(x) == -int(-x) == 1)
        self.assert_(x == long(x) + x.frac())
        self.assert_(-x == long(-x) + (-x).frac())
        self.assert_(fp(7) % 4 == 7 % fp(4) == 3)
        self.assert_(fp(-7) % 4 == -7 % fp(4) == 1)
        self.assert_(fp(-7) % -4 == -7 % fp(-4) == -3)
        self.assert_(fp(7.0) % "-4.0" == 7 % fp(-4) == -1)
        self.assert_(fp("5.5") % fp("1.1") == fp("5.5e100") % fp("1.1e100") == 0)
        self.assert_(divmod(fp("1e100"), 3) == (long(fp("1e100")/3), 1))
        
        

def _make_suite():
    """
    Factory to create a test suite

    This is separated out for use by both installation regression
    testing, and in a standalone unit test.
    """
    return unittest.TestSuite((
        unittest.makeSuite(FixedPointTest, "test"),
        ))

def test_main():
    """
    Installation Regression Test

    The name test_main is required
    """
    import test_support
    test_support.run_suite(_make_suite())

if __name__ == "__main__":
    """
    Run as a stand-alone unit test.
    """
    runner = unittest.TextTestRunner()
    runner.run(_make_suite())


