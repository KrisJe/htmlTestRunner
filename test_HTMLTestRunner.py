# -*- coding: utf-8 -*-

#from io import StringIO
import io
import sys
import unittest

import HTMLTestRunner

# ----------------------------------------------------------------------

def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)

def safe_str(obj):
    """ return the byte string representation of obj """
    try:
        return str(obj)
    except UnicodeEncodeError:
        # obj is unicode
        return unicode(obj).encode('unicode_escape')

# ----------------------------------------------------------------------
# Sample tests to drive the HTMLTestRunner

class SampleTest0(unittest.TestCase):
    """ A class that passes.

    This simple class has only one test case that passes.
    """
    def __init__(self, methodName):
        unittest.TestCase.__init__(self, methodName)

    def test_pass_no_output(self):
        """        test description
        """
        pass
    
    @unittest.skip("This test has been skipped!")
    def test_skipped_with_reason(self):
        """        test description
        """
        pass    

class SampleTest1(unittest.TestCase):
    """ A class that fails.

    This simple class has only one test case that fails.
    """
    def test_fail(self):
        """
        test description (描述)
        """
        self.fail()

class SampleOutputTestBase(unittest.TestCase):
    """ Base TestCase. Generates 4 test cases x different content type. """
    def test_1(self):
        print(self.MESSAGE)
    def test_2(self):
        print (self.MESSAGE , file=sys.stderr)
    def test_3(self):
        self.fail(self.MESSAGE)
    def test_4(self):
        raise RuntimeError(self.MESSAGE)

class SampleTestBasic(SampleOutputTestBase):
    MESSAGE = 'basic test'

class SampleTestHTML(SampleOutputTestBase):
    MESSAGE = 'the message is 5 symbols: <>&"\'\nplus the HTML entity string: [&copy;] on a second line'

class SampleTestLatin1(SampleOutputTestBase):
    MESSAGE = u'the message is áéíóú'.encode('latin-1')

class SampleTestUnicode(SampleOutputTestBase):
    u""" Unicode (統一碼) test """
    MESSAGE = u'the message is \u8563'
    # 2006-04-25 Note: Exception would show up as
    # AssertionError: <unprintable instance object>
    #
    # This seems to be limitation of traceback.format_exception()
    # Same result in standard unittest.
    def test_pass(self):
        u""" A test with Unicode (統一碼) docstring """
        pass


