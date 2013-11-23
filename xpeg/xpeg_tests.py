#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from parser import XPEGParser

known_values = [
    ('<expression> = number', None)
]


class KnownValues(unittest.TestCase):

    def test_evaluate_known_values(self):
        '''
           Check if parse() function in XPEGParser return an
           expected value
        '''
        grammar_parser = XPEGParser()
        for expression, expected in known_values:
            returned = grammar_parser.parse(expression, True)
            self.assertEqual(expected, returned)
    
    def test_bootstraping_grammar(self):
        with open('xpeg.grammar') as f:
            grammar_parser = XPEGParser()
            returned = grammar_parser.parse(f.read(), True)
            self.assertEqual(None, returned)

if __name__ == '__main__':
    unittest.main()