"""Tests for the regex module.

This module contains unit tests for the regex module, which implements
a finite state machine (FSM) for regex pattern matching.
"""

import unittest
from regex import *

class TestStateClasses(unittest.TestCase):
    def test_dot_state(self):
        dot = DotState()
        self.assertTrue(dot.check_self('a'), "DotState should accept 'a'")
        self.assertTrue(dot.check_self('1'), "DotState should accept '1'")
        self.assertTrue(dot.check_self(' '), "DotState should accept space")

    def test_ascii_state(self):
        a_state = AsciiState('a')
        self.assertTrue(a_state.check_self('a'), "AsciiState('a') should accept 'a'")
        self.assertFalse(a_state.check_self('b'), "AsciiState('a') should reject 'b'")
        one_state = AsciiState('1')
        self.assertTrue(one_state.check_self('1'), "AsciiState('1') should accept '1'")
        self.assertFalse(one_state.check_self('2'), "AsciiState('1') should reject '2'")

    def test_character_class_state(self):
        az_state = CharacterClassState('a-z')
        self.assertTrue(az_state.check_self('a'), "CharacterClassState('a-z') should accept 'a'")
        self.assertTrue(az_state.check_self('z'), "CharacterClassState('a-z') should accept 'z'")
        self.assertFalse(az_state.check_self('A'), "CharacterClassState('a-z') should reject 'A'")
        self.assertFalse(az_state.check_self('0'), "CharacterClassState('a-z') should reject '0'")

        num_state = CharacterClassState('0-9')
        self.assertTrue(num_state.check_self('0'), "CharacterClassState('0-9') should accept '0'")
        self.assertTrue(num_state.check_self('5'), "CharacterClassState('0-9') should accept '5'")
        self.assertTrue(num_state.check_self('9'), "CharacterClassState('0-9') should accept '9'")
        self.assertFalse(num_state.check_self('a'), "CharacterClassState('0-9') should reject 'a'")

        negated_state = CharacterClassState('^0-9')
        self.assertTrue(negated_state.check_self('a'), "CharacterClassState('^0-9') should accept 'a'")
        self.assertTrue(negated_state.check_self('A'), "CharacterClassState('^0-9') should accept 'A'")
        self.assertFalse(negated_state.check_self('0'), "CharacterClassState('^0-9') should reject '0'")
        self.assertFalse(negated_state.check_self('5'), "CharacterClassState('^0-9') should reject '5'")

        mixed_state = CharacterClassState('a-z0-9')
        self.assertTrue(mixed_state.check_self('a'), "CharacterClassState('a-z0-9') should accept 'a'")
        self.assertTrue(mixed_state.check_self('z'), "CharacterClassState('a-z0-9') should accept 'z'")
        self.assertTrue(mixed_state.check_self('0'), "CharacterClassState('a-z0-9') should accept '0'")
        self.assertTrue(mixed_state.check_self('9'), "CharacterClassState('a-z0-9') should accept '9'")
        self.assertFalse(mixed_state.check_self('A'), "CharacterClassState('a-z0-9') should reject 'A'")
        self.assertFalse(mixed_state.check_self('-'), "CharacterClassState('a-z0-9') should reject '-'")

    def test_start_state(self):
        start = StartState()
        self.assertFalse(start.check_self('a'), "StartState should not match any character")

    def test_termination_state(self):
        term = TerminationState()
        self.assertFalse(term.check_self('a'), "TerminationState should not match any character")
        with self.assertRaises(Exception, msg="TerminationState.check_next should raise Exception"):
            term.check_next('a')

class TestRegexFSMConstruction(unittest.TestCase):
    def test_valid_regex(self):
        # Test various valid regex patterns
        RegexFSM("a")
        RegexFSM(".")
        RegexFSM("[a-z]")
        RegexFSM("[^0-9]")
        RegexFSM("a*")
        RegexFSM("a+")
        RegexFSM("a*b")
        RegexFSM("a+b")
        RegexFSM("a*4.+hi")

    def test_invalid_regex(self):
        with self.assertRaises(ValueError, msg="Lone '*' should raise ValueError"):
            RegexFSM("*")
        with self.assertRaises(ValueError, msg="Lone '+' should raise ValueError"):
            RegexFSM("+")
        with self.assertRaises(ValueError, msg="Unmatched bracket should raise ValueError"):
            RegexFSM("[a-z")

class TestRegexFSMCheckString(unittest.TestCase):
    def test_literal_characters(self):
        fsm = RegexFSM("a")
        self.assertTrue(fsm.check_string("a"), "Pattern 'a' should match 'a'")
        self.assertFalse(fsm.check_string("b"), "Pattern 'a' should not match 'b'")
        self.assertFalse(fsm.check_string("",), "Pattern 'a' should not match empty string")

        fsm = RegexFSM("abc")
        self.assertTrue(fsm.check_string("abc"), "Pattern 'abc' should match 'abc'")
        self.assertFalse(fsm.check_string("abd"), "Pattern 'abc' should not match 'abd'")
        self.assertFalse(fsm.check_string("ab"), "Pattern 'abc' should not match 'ab'")
        self.assertFalse(fsm.check_string("abcd"), "Pattern 'abc' should not match 'abcd'")

    def test_dot(self):
        fsm = RegexFSM(".")
        self.assertTrue(fsm.check_string("a"), "Pattern '.' should match 'a'")
        self.assertTrue(fsm.check_string("1"), "Pattern '.' should match '1'")
        self.assertFalse(fsm.check_string("",), "Pattern '.' should not match empty string")
        self.assertFalse(fsm.check_string("ab"), "Pattern '.' should not match 'ab'")

        fsm = RegexFSM("a.c")
        self.assertTrue(fsm.check_string("abc"), "Pattern 'a.c' should match 'abc'")
        self.assertTrue(fsm.check_string("a1c"), "Pattern 'a.c' should match 'a1c'")
        self.assertFalse(fsm.check_string("ac"), "Pattern 'a.c' should not match 'ac'")
        self.assertFalse(fsm.check_string("abcd"), "Pattern 'a.c' should not match 'abcd'")

    def test_character_class(self):
        fsm = RegexFSM("[a-z]")
        self.assertTrue(fsm.check_string("a"), "Pattern '[a-z]' should match 'a'")
        self.assertTrue(fsm.check_string("z"), "Pattern '[a-z]' should match 'z'")
        self.assertFalse(fsm.check_string("A"), "Pattern '[a-z]' should not match 'A'")
        self.assertFalse(fsm.check_string("0"), "Pattern '[a-z]' should not match '0'")
        self.assertFalse(fsm.check_string("ab"), "Pattern '[a-z]' should not match 'ab'")

        fsm = RegexFSM("[0-9]")
        self.assertTrue(fsm.check_string("0"), "Pattern '[0-9]' should match '0'")
        self.assertTrue(fsm.check_string("5"), "Pattern '[0-9]' should match '5'")
        self.assertFalse(fsm.check_string("a"), "Pattern '[0-9]' should not match 'a'")

        fsm = RegexFSM("[^0-9]")
        self.assertTrue(fsm.check_string("a"), "Pattern '[^0-9]' should match 'a'")
        self.assertTrue(fsm.check_string("A"), "Pattern '[^0-9]' should match 'A'")
        self.assertFalse(fsm.check_string("0"), "Pattern '[^0-9]' should not match '0'")

    def test_quantifiers(self):
        fsm = RegexFSM("a*")
        self.assertTrue(fsm.check_string("",), "Pattern 'a*' should match empty string")
        self.assertTrue(fsm.check_string("a"), "Pattern 'a*' should match 'a'")
        self.assertTrue(fsm.check_string("aa"), "Pattern 'a*' should match 'aa'")
        self.assertFalse(fsm.check_string("b"), "Pattern 'a*' should not match 'b'")
        self.assertFalse(fsm.check_string("ab"), "Pattern 'a*' should not match 'ab'")

        fsm = RegexFSM("a+")
        self.assertFalse(fsm.check_string("",), "Pattern 'a+' should not match empty string")
        self.assertTrue(fsm.check_string("a"), "Pattern 'a+' should match 'a'")
        self.assertTrue(fsm.check_string("aa"), "Pattern 'a+' should match 'aa'")
        self.assertFalse(fsm.check_string("b"), "Pattern 'a+' should not match 'b'")
        self.assertFalse(fsm.check_string("ab"), "Pattern 'a+' should not match 'ab'")

        fsm = RegexFSM("a*b")
        self.assertTrue(fsm.check_string("b"), "Pattern 'a*b' should match 'b'")
        self.assertTrue(fsm.check_string("ab"), "Pattern 'a*b' should match 'ab'")
        self.assertTrue(fsm.check_string("aab"), "Pattern 'a*b' should match 'aab'")
        self.assertFalse(fsm.check_string("a"), "Pattern 'a*b' should not match 'a'")
        self.assertFalse(fsm.check_string("aa"), "Pattern 'a*b' should not match 'aa'")

        fsm = RegexFSM("a+b")
        self.assertFalse(fsm.check_string("b"), "Pattern 'a+b' should not match 'b'")
        self.assertTrue(fsm.check_string("ab"), "Pattern 'a+b' should match 'ab'")
        self.assertTrue(fsm.check_string("aab"), "Pattern 'a+b' should match 'aab'")
        self.assertFalse(fsm.check_string("a"), "Pattern 'a+b' should not match 'a'")
        self.assertFalse(fsm.check_string("aa"), "Pattern 'a+b' should not match 'aa'")

    def test_complex_patterns(self):
        fsm = RegexFSM("a*4.+hi")
        self.assertTrue(fsm.check_string("aaaaaa4uhi"), "Pattern 'a*4.+hi' should match 'aaaaaa4uhi'")
        self.assertTrue(fsm.check_string("4uhi"), "Pattern 'a*4.+hi' should match '4uhi'")
        self.assertFalse(fsm.check_string("meow"), "Pattern 'a*4.+hi' should not match 'meow'")

        fsm = RegexFSM("[a-z]+[0-9]")
        self.assertTrue(fsm.check_string("abc1"), "Pattern '[a-z]+[0-9]' should match 'abc1'")
        self.assertTrue(fsm.check_string("xyz9"), "Pattern '[a-z]+[0-9]' should match 'xyz9'")
        self.assertFalse(fsm.check_string("ABC123"), "Pattern '[a-z]+[0-9]' should not match 'ABC123'")
        self.assertFalse(fsm.check_string("123"), "Pattern '[a-z]+[0-9]' should not match '123'")

        fsm = RegexFSM("[^0-9]+")
        self.assertTrue(fsm.check_string("abc"), "Pattern '[^0-9]+' should match 'abc'")
        self.assertFalse(fsm.check_string("123"), "Pattern '[^0-9]+' should not match '123'")

if __name__ == '__main__':
    unittest.main()