Chapter 2 - Testing Exceptions and using loops
----------------------------------------------

In the last chapter we covered the basics of TDD: writing tests first,
driving incremental code changes using the tests. I want to continue
with the example to show how TDD can also help us to drive code design.

### Testing error cases and raising exceptions:

Let’s start by extending our tests. Our "minimum viable calculator" can
currently add I + I, but calling it viable may be a bit of a stretch!
For starters, although it’s only currently designed to add I’s, it will
actually accept almost any input at all, and will probably return
nonsense outputs.

Let’s make it return a sensible error if it gets input it doesn’t know
how to handle. As usual, test-first, we start by specifying how we want
the code to behave, from the point of view of the caller:

    import unittest
    from rome import add

    class AdditionTest(unittest.TestCase):

        def test_adding_Is(self):
            self.assertEqual(add('I', 'I'), 'II')
            self.assertEqual(add('I', 'II'), 'III')


        def test_inputs_out_of_scope_raise_exceptions(self):
            with self.assertRaises(ValueError):
                add('I', 2)
            with self.assertRaises(ValueError):
                add('I', 'V')


    if __name__ == '__main__':
        unittest.main()

I’ve decided to add a new test method, since these tests are quite
different from the tests for addition of I’s. Like all variable names,
test names should be nice and descriptive, and in fact, they often are
almost human-readable sentences. They should summarise what we want our
code to do… I’ve seen test method names that extend to almost
100chars — after a while though, a long test method name is a code smell
that you might want to break your code up into smaller pieces.

The next thing to introduce is `assertRaises`. This is another of
unittest’s helper functions, and it works as a context manager. It
allows us to run tests which we now will raise an exceptioin, and to
make assertions about what type of exception we’ll get.

We’ve started by specifying two possible out-of-scope inputs: a
non-Roman numeral, 2, and a Roman numeral which we don’t know how to
compute yet, *V*. Let’s try running the tests:

    .E
    ======================================================================
    ERROR: test_inputs_out_of_scope_raise_exceptions (__main__.AdditionTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "book0/tests.py", line 13, in test_inputs_out_of_scope_raise_exceptions
        add('I', 2)
      File "/home/harry/Dropbox/book/book0/rome.py", line 2, in add
        return augend + addend
    TypeError: cannot concatenate 'str' and 'int' objects

    ----------------------------------------------------------------------
    Ran 2 tests in 0.000s

    FAILED (errors=1)

We now have two tests, of which one is failing. That allows us to go
ahead and write some new code. The tests are complaining about a
TypeError, so let’s get rid of it:

    def add(augend, addend):
        try:
            return augend + addend
        except TypeError:
            pass

Well, that produces a slightly different error:

    .F
    ======================================================================
    FAIL: test_inputs_out_of_scope_raise_exceptions (__main__.AdditionTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "book0/tests.py", line 13, in test_inputs_out_of_scope_raise_exceptions
        add('I', 2)
    AssertionError: ValueError not raised

    ----------------------------------------------------------------------
    Ran 2 tests in 0.000s

    FAILED (failures=1)

### How tests can save us from stupidity:

Obviously our first attempt wasn’t quite right - we want a ValueError.
Let’s go ahead and raise one of those, slightly naively:

    def add(augend, addend):
        raise ValueError
        return augend + addend

    E.
    ======================================================================
    ERROR: test_adding_Is (__main__.AdditionTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "book0/tests.py", line 7, in test_adding_Is
        self.assertEqual(add('I', 'I'), 'II')
      File "/home/harry/Dropbox/book/book0/rome.py", line 2, in add
        raise ValueError
    ValueError

    ----------------------------------------------------------------------
    Ran 2 tests in 0.001s

    FAILED (errors=1)

OK, perhaps that’s not so much naive as downright stupid. But I’m using
it to illustrate one of the great things about TDD - it can save you
from your own stupid. Now, I may well think I’m not stupid often, I may
even fancy myself as occasionally fairly smart - but I know that, for
sure, sometimes I’m stupid. It’s nice to know that the tests are there
to cover for me when that happens.

Thanks, tests! (Thests.)

    def add(augend, addend):
        if not isinstance(addend, str):
            raise ValueError
        return augend + addend

Let’s see if that will do the trick:

    .F
    ======================================================================
    FAIL: test_inputs_out_of_scope_raise_exceptions (__main__.AdditionTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "book0/tests.py", line 15, in test_inputs_out_of_scope_raise_exceptions
        add('I', 'V')
    AssertionError: ValueError not raised

    ----------------------------------------------------------------------
    Ran 2 tests in 0.001s

    FAILED (failures=1)

Another incremental change:

    def add(augend, addend):
        if not isinstance(addend, str):
            raise ValueError
        if addend == 'V':
            raise ValueError
        return augend + addend

### Looping through test cases:

These naive input validations aren’t really satisfactory though. We’re
only checking on one of the inputs, for starters. Let’s extend our tests
to cover a wider range of bad inputs, and justify some better input
validation.

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

TODO: this is pretty ugly. but no great way of checking which input
raised the exception otherwise…

There’s a couple of new things there — you’ll see that `assertRaises`
gives us a context manager, on which we can make assertions about the
exceptions that was raised. I’m also using More importantly, it shows a
common testing pattern, which is to put our tests in our loop in order
to check several similar cases. When we do this, we need a way of
figuring out which of the test values caused the error, so that’s why
I’m using `self.fail`, which is a shortcut to failing out with a given
message.

Let’s see how that does:

    .E
    ======================================================================
    ERROR: test_inputs_out_of_scope_raise_exceptions (__main__.AdditionTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "book0/tests.py", line 19, in test_inputs_out_of_scope_raise_exceptions
        add(bad_input, 'I')
      File "/home/harry/Dropbox/book/book0/rome.py", line 6, in add
        return augend + addend
    TypeError: unsupported operand type(s) for +: 'int' and 'str'

    ----------------------------------------------------------------------
    Ran 2 tests in 0.001s

    FAILED (errors=1)

That’s telling us that we need to check both the augend and the addend
for valid inputs. Here’s a minimal change:

    def add(augend, addend):
        if not isinstance(augend, str) or not isinstance(addend, str):
            raise ValueError
        if addend == 'V':
            raise ValueError
        return augend + addend

We’re now getting into a familiar TDD cycle:

-   run the tests

-   make a minimal code change, driven by the test failure message

-   repeat until the tests all pass

Let’s play it out. Testing again:

    AssertionError: Z as augend did not raise exception

(I’m just showing the last line of the test failure output now, to save
space)

Let’s fix that:

    def add(augend, addend):
        if not isinstance(augend, str) or not isinstance(addend, str):
            raise ValueError
        if addend == 'V' or augend == 'Z':
            raise ValueError
        return augend + addend

Ugly, but let’s see what the tests want:

    AssertionError: Z as augend did not raise exception

That justifies us to write some slightly cleverer input validation:

    def add(augend, addend):
        if not isinstance(augend, str) or not isinstance(addend, str):
            raise ValueError
        simple_sum = augend + addend
        if any(char != 'I' for char in simple_sum):
            raise ValueError
        return simple_sum

And that gets the tests to pass!

    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.000s

    OK

Hooray. In that chapter we covered testing for exceptions, we saw how
tests can save us from our own stupidity, and we learned about looping
through test values. In the next chapter we’ll look at refactoring and
driving design through tests.

* * * * *

Last updated 2013-01-26 20:36:42 GMT
