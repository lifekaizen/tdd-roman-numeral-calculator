Chapter 3 - Using TDD to drive desgin
-------------------------------------

In the last chapter we tested our input validation and exceptions. Now
let’s extend our tests to try and get our calculator to do more useful
stuff. We’ll start by extending it to handle one more numeral, and then
see if we can’t generalise to a full suite.

    import unittest
    from rome import add

    class AdditionTest(unittest.TestCase):

        def test_adding_Is(self):
            self.assertEqual(add('I', 'I'), 'II')
            self.assertEqual(add('I', 'II'), 'III')


        def test_inputs_out_of_scope_raise_exceptions(self):
            for bad_input in (2, None, 'Z', 'V', 'X', 'L', 'C', 'D', 'M'):
                with self.assertRaises(ValueError) as m:
                    add('I', bad_input)
                    if not hasattr(m, 'exception'):
                        self.fail('%s as augend did not raise exception' % bad_input)

                with self.assertRaises(ValueError) as m:
                    add(bad_input, 'I')
                    if not hasattr(m, 'exception'):
                        self.fail('%s as addend did not raise exception' % bad_input)

        def test_IV_and_V(self):
            self.assertEqual(add('II', 'II'), 'IV')
            self.assertEqual(add('III', 'II'), 'V')
            self.assertEqual(add('IV', 'I'), 'V')
            self.assertEqual(add('V', 'I'), 'VI')
            self.assertEqual(add('I', 'V'), 'VI')


    if __name__ == '__main__':
        unittest.main()

Let’s try running that:

    F..
    ======================================================================
    FAIL: test_IV_and_V (__main__.AdditionTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "book0/tests.py", line 24, in test_IV_and_V
        self.assertEqual(add('II', 'II'), 'IV')
    AssertionError: 'IIII' != 'IV'

    ----------------------------------------------------------------------
    Ran 3 tests in 0.000s

    FAILED (failures=1)

Right - we’re not outputing *IV* correctly. Let’s fix that:

    def add(augend, addend):
        if not isinstance(augend, str) or not isinstance(addend, str):
            raise ValueError
        simple_sum = augend + addend
        if any(char != 'I' for char in simple_sum):
            raise ValueError

        canonicalised_sum = simple_sum.replace('IIII', 'IV')
        return canonicalised_sum

How about that?

    F..
    ======================================================================
    FAIL: test_IV_and_V (__main__.AdditionTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "book0/tests.py", line 25, in test_IV_and_V
        self.assertEqual(add('III', 'II'), 'V')
    AssertionError: 'IVI' != 'V'

    ----------------------------------------------------------------------
    Ran 3 tests in 0.002s

    FAILED (failures=1)

Ah. IV might work, but V is broken. Let’s fix it:

    def add(augend, addend):
        if not isinstance(augend, str) or not isinstance(addend, str):
            raise ValueError
        simple_sum = augend + addend
        if any(char != 'I' for char in simple_sum):
            raise ValueError

        canonicalised_sum = simple_sum.replace('IIIII', 'V').replace('IIII', 'IV')
        return canonicalised_sum

    E..
    ======================================================================
    ERROR: test_IV_and_V (__main__.AdditionTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "book0/tests.py", line 26, in test_IV_and_V
        self.assertEqual(add('IV', 'I'), 'V')
      File "/home/harry/Dropbox/book/book0/rome.py", line 6, in add
        raise ValueError
    ValueError

    ----------------------------------------------------------------------
    Ran 3 tests in 0.001s

    FAILED (errors=1)

Oops, looks like using a *V* as an input raises a value error. Let’s
remove that case from our exception testing:

    def test_inputs_out_of_scope_raise_exceptions(self):
        for bad_input in (2, None, 'Z', 'X', 'L', 'C', 'D', 'M'):
            with self.assertRaises(ValueError) as m:
                add('I', bad_input)
                [...]

And try some new code:

    ROMAN_NUMERALS = ('I', 'V')
    def add(augend, addend):
        if not isinstance(augend, str) or not isinstance(addend, str):
            raise ValueError
        simple_sum = augend + addend

        if any(char not in ROMAN_NUMERALS for char in simple_sum):
            raise ValueError

        canonicalised_sum = simple_sum.replace('IIIII', 'V').replace('IIII', 'IV')
        return canonicalised_sum

How about that?

    F..
    ======================================================================
    FAIL: test_IV_and_V (__main__.AdditionTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "book0/tests.py", line 26, in test_IV_and_V
        self.assertEqual(add('IV', 'I'), 'V')
    AssertionError: 'IVI' != 'V'

    ----------------------------------------------------------------------
    Ran 3 tests in 0.002s

    FAILED (failures=1)

Looks like our naive addition code can’t handle *IV* as an input. Just
as we canonicalise at the end of our add function, we probably need to
simplify our numerals, stripping out any *IV* forms and replacing them
with more computable 'IIII’s:

    ROMAN_NUMERALS = ('I', 'V')
    def add(augend, addend):
        if not isinstance(augend, str) or not isinstance(addend, str):
            raise ValueError

        simple_augend = augend.replace('IV', 'IIII')
        simple_addend = addend.replace('IV', 'IIII')

        simple_sum = simple_augend + simple_addend

        if any(char not in ROMAN_NUMERALS for char in simple_sum):
            raise ValueError

        canonicalised_sum = simple_sum.replace('IIIII', 'V').replace('IIII', 'IV')
        return canonicalised_sum

How about that?

    F..
    ======================================================================
    FAIL: test_IV_and_V (__main__.AdditionTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "book0/tests.py", line 28, in test_IV_and_V
        self.assertEqual(add('I', 'V'), 'VI')
    AssertionError: 'IV' != 'VI'

    ----------------------------------------------------------------------
    Ran 3 tests in 0.002s

    FAILED (failures=1)

Ah, looks like our canonicalised sum isn’t clever enough to tell the
difference between *IV* and *VI*. Order matters!

Here’s another excellent example of TDD. I think I need to figure out
how to take the `simple_sum`, and order its digits so that the largest
roman numerals come out first. I’m pretty comfortable with Python, so I
have some sense that I can use the duck-typing of string as lists, and
maybe Python’s built-in `sorted` and `reversed` functions… but if you
asked me exactly how they work, without looking at the docs or an
interepreter, I have to say I’m not 100% sure of how I’d do it… How does
`sorted` apply to strings anyway? Thankfully, the magic of TDD means I
don’t need to look at the docs, or open up an interpreter to try out
some examples. I can simply try a few different options, directly in my
code, and rely on the tests to tell me what I get right or wrong. Here’s
how I went about it this time:

    ROMAN_NUMERALS = ('I', 'V')
    def add(augend, addend):
        if not isinstance(augend, str) or not isinstance(addend, str):
            raise ValueError

        simple_augend = augend.replace('IV', 'IIII')
        simple_addend = addend.replace('IV', 'IIII')

        simple_sum = simple_augend + simple_addend

        if any(char not in ROMAN_NUMERALS for char in simple_sum):
            raise ValueError

        ordered_sum = sorted(simple_sum)

        canonicalised_sum = ordered_sum.replace('IIIII', 'V').replace('IIII', 'IV')
        return canonicalised_sum

That gave me two test failures:

    AttributeError: 'list' object has no attribute 'replace'
    AttributeError: 'list' object has no attribute 'replace'

Ah, looks like `sorted` has produced a list instead of a string. Didn’t
know it would do that. No matter:

        ordered_sum = ''.join(sorted(simple_sum))

Any better?

    AssertionError: 'IV' != 'VI'

Nope. We need to reverse the direction of the sort. 

        ordered_sum = ''.join(sorted(simple_sum,reverse=True))

That gets the tests to pass

    ...
    ----------------------------------------------------------------------
    Ran 3 tests in 0.001s

    OK

So it looks like there are 5 parts to our roman numeral adder:

-   validating inputs

-   simplifying inputs by replacing 'IV’s with 'IIII’s

-   adding them together by simply concatenating the two numerals

-   sorting the result so that the higher numerals are at the beginning

-   finally, canonicalising the result by transforming any 'IIII’s back
    into 'IV’s and any 'IIIII’s into 'V’s.

The next stage is to get the calculator to do *X*. We might be tempted,
at this point, to start refactoring - building out some helper functions
for one or many of the 5 steps above. But there are a couple of useful
sayings in TDD, which are pertinent at this point:

-   “YAGNI”

-   “3 strikes, then refactor”

“YAGNI” stands for “You ain’t gonna need it”. Programming is all about
the joy of building stuff, and we enjoy noticing patterns, thinking of
ways to generalise things, jumping in and adding another layer of
indirection. But it’s all too easy to get carried away with this, and
classes like `ActionTemplateManagerFactoryFactory` are not far away. TDD
aims for simple code, and that simple sometimes means not generalising
too soon. YAGNI and the 3 strikes rule are there to stop us from
generalising too soon.

So, before we dive in and make a `canonicalize` function or a
`simplify_numeral` function, let’s make sure we know what we want by
seeing if we can get `X` to work, getting a second strike in, and we’ll
be ready to refactor at the next numeral.

    def test_IX_and_X(self):
        self.assertEqual(add('V', 'V'), 'X')
        self.assertEqual(add('V', 'IV'), 'IX')
        self.assertEqual(add('VIII', 'I'), 'IX')
        self.assertEqual(add('IX', 'I'), 'X')
        self.assertEqual(add('X', 'I'), 'XI')
        self.assertEqual(add('I', 'X'), 'XI')
        self.assertEqual(add('X', 'V'), 'XV')
        self.assertEqual(add('V', 'X'), 'XV')
        self.assertEqual(add('X', 'X'), 'XX')

Let’s run those:

    .F..
    ======================================================================
    FAIL: test_IX_and_X (__main__.AdditionTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "book0/tests.py", line 32, in test_IX_and_X
        self.assertEqual(add('V', 'V'), 'X')
    AssertionError: 'VV' != 'X'

    ----------------------------------------------------------------------
    Ran 4 tests in 0.002s

    FAILED (failures=1)

Looks like we need to convert *VV* to *X* before returning:

    canonicalised_sum = ordered_sum.replace('IIIII', 'V').replace('IIII', 'IV').replace('VV', 'X')

How about that?

        self.assertEqual(add('V', 'IV'), 'IX')
    AssertionError: 'VIV' != 'IX'

OK, we need to recognise *IX* just like we recognise *IV*:

    canonicalised_sum = ordered_sum.replace('IIIII', 'V').replace('IIII', 'IV').replace('VV', 'X').replace('VIV', 'IX')

How’s that?

    .E..
    ======================================================================
    ERROR: test_IX_and_X (__main__.AdditionTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "book0/tests.py", line 35, in test_IX_and_X
        self.assertEqual(add('IX', 'I'), 'X')
      File "/home/harry/Dropbox/book/book0/rome.py", line 12, in add
        raise ValueError
    ValueError

    ----------------------------------------------------------------------
    Ran 4 tests in 0.001s

    FAILED (errors=1)

Oops, looks like we need to add *X* to our valid inputs:

    ROMAN_NUMERALS = ('I', 'V', 'X')

What about now?

    .F.F
    ======================================================================
    FAIL: test_IX_and_X (__main__.AdditionTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "book0/tests.py", line 35, in test_IX_and_X
        self.assertEqual(add('IX', 'I'), 'X')
    AssertionError: 'XII' != 'X'

    ======================================================================
    FAIL: test_inputs_out_of_scope_raise_exceptions (__main__.AdditionTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "book0/tests.py", line 16, in test_inputs_out_of_scope_raise_exceptions
        self.fail('%s as augend did not raise exception' % bad_input)
    AssertionError: X as augend did not raise exception

    ----------------------------------------------------------------------
    Ran 4 tests in 0.001s

    FAILED (failures=2)

Urg, two fails. One just reminds us that we need to change our scope
tests if we change our scope!

    def test_inputs_out_of_scope_raise_exceptions(self):
        for bad_input in (2, None, 'Z', 'L', 'C', 'D', 'M'):

Now what?

    .F..
    ======================================================================
    FAIL: test_IX_and_X (__main__.AdditionTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "book0/tests.py", line 35, in test_IX_and_X
        self.assertEqual(add('IX', 'I'), 'X')
    AssertionError: 'XII' != 'X'

    ----------------------------------------------------------------------
    Ran 4 tests in 0.006s

    FAILED (failures=1)

* * * * *

Last updated 2013-01-26 20:36:42 GMT
