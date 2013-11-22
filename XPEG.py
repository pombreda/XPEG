#!/usr/bin/python3
# -*- coding: utf-8 -*-


import collections
import re

token_patterns = [
    ('assignment',          r'='),
    ('open_paren',          r'\('),    
    ('close_paren',         r'\)'),            
    ('pipe',                r'\|'),                
    ('rule_identifier',     r'<[a-z_][a-z0-9_]*>'),
    ('rule_reference',      r'[a-z_][a-z0-9_]*'),    
    ('skip_action',         r'\[skip\]'),    
    ('regex',               r'~u?r?\".*?[^\\]\"[ilmsux]*'),
    ('literal',             r'u?r?\".*?[^\\]\"'),
    ('lookahead_assertion', r'[&!]'),
    ('quantifier',          r'[?*+]|{[0-9]+(\s*,\s*([0-9]+)?)?}'), #add other quantifier, like ??, *?, +?
    ('comment',             r'#[^\r\n]*'),
    ('newline',             r'\n'),
    ('whitespaces',         r'[ \t]')
]

pattern = '|'.join('(?P<%s>%s)' % pair for pair in token_patterns)

Token = collections.namedtuple('Token', 'type value line column')


class GrammarLexer(object):

    def __init__(self, rules):
        self.rules = rules

    def tokenizer(self):
        line = 1
        column = line_start = 0
        next_token = re.compile(pattern, re.IGNORECASE).match
        token = next_token(self.rules)
        while token:
            token_type = token.lastgroup
            if token_type == 'newline':
                line_start = column
                line += 1
            elif not token_type in ['whitespaces', 'comment']:
                token_value = token.group(token_type)
                yield Token(token_type, token_value, line, token.start()-line_start)
            column = token.end()
            token = next_token(self.rules, column)
        if column != len(self.rules):
            raise RuntimeError('Syntax error: Unexpected character %r on line %d' % (self.rules[column], line))


class GrammarParser(object):

    def __init__(self):
        pass

    def next_token(self):
        try:
            return next(self.tokenizer)
        except StopIteration:
            pass

    def print_tokens(self):
        line_format = "| %20s | %80s | %6s | %6s |"
        separator = '=' * 125
        print('Tokenizing...')
        print(separator)
        print(line_format % ('TYPE', 'VALUE', 'LINE', 'COLUMN'))
        print(separator)
        self.tokenizer = self.lexer.tokenizer()
        for token in self.tokenizer:
            print(line_format % token)
        print(separator)

    def parse(self, rules, print_tokens=False):
        self.lexer = GrammarLexer(rules)
        if print_tokens:
            self.print_tokens()
        self.tokenizer = self.lexer.tokenizer()
        self.token = self.next_token()
        self.rules()

    def token_is(self, *token_types):
        if self.token:
            return self.token.type in list(token_types)

    def match(self, token_type_expected):
        if not self.token_is(token_type_expected):
            raise ValueError('Syntax error: expected "%s" but got "%s"' % (token_type_expected, self.token.type))
        else:
            self.token = self.next_token()

    # RULES

    def rules(self):
        '<rules> = rule+'
        self.rule()
        while self.token_is('rule_identifier'):
            self.rule()

    def rule(self):
        '<rule> = rule_identifier assignment expression actions?'
        self.match('rule_identifier')
        self.match('assignment')
        self.expression()
        if self.token_is('skip_action'):
            self.actions()

    def expression(self):
        '<expression> = sequence ("|" sequence)*'
        self.sequence()
        while self.token_is('pipe'):
            self.match('pipe')
            self.sequence()

    def sequence(self):
        '<sequence> = prefix*'
        while self.token_is('lookahead_assertion', 'rule_reference', 'open_paren', 'literal', 'regex'):
            self.prefix()

    def prefix(self):
        '<prefix> = lookahead_assertion? suffix'
        if self.token_is('lookahead_assertion'):
            self.match('lookahead_assertion')
        self.suffix()

    def suffix(self):
        '<suffix> = primary quantifier?'
        self.primary()
        if self.token_is('quantifier'):
            self.match('quantifier')

    def primary(self):
        """
        <primary> = rule_reference 
                  | parenthesized_expression
                  | literal
                  | regex
        """
        if self.token_is('rule_reference'):
            self.match('rule_reference')
        elif self.token_is('open_paren'):
            self.parenthesized_expression()
        elif self.token_is('literal'):
            self.match('literal')
        else:
            self.match('regex')

    def parenthesized_expression(self):
        '<parenthesized_expression> = "(" expression ")"'
        self.match('open_paren')
        self.expression()
        self.match('close_paren')

    def actions(self):
        self.match('skip_action')