#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from XPEG import GrammarParser

known_values = [
    ('<expression> = number', None)
]


class KnownValues(unittest.TestCase):

    def test_evaluate_known_values(self):
        '''
           Check if parse() function in GrammarParser return an
           expected value
        '''
        grammar_parser = GrammarParser()
        for expression, expected in known_values:
            returned = grammar_parser.parse(expression, True)
            self.assertEqual(expected, returned)
    
    def test_bootstraping_grammar(self):
        with open('XPEG.grammar') as f:
            grammar_parser = GrammarParser()
            returned = grammar_parser.parse(f.read(), True)
            self.assertEqual(None, returned)

if __name__ == '__main__':
    unittest.main()