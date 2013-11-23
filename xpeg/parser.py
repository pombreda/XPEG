#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lexer import XPEGLexer

class XPEGParser(object):

    def parse(self, rules, print_tokens=False):
        self.lexer = XPEGLexer(rules)
        if print_tokens:
            self.print_tokens()
        self.tokenizer = self.lexer.tokenizer()
        self.token = self.next_token()
        self.rules()

    def next_token(self):
        try:
            return next(self.tokenizer)
        except StopIteration:
            pass

    def token_is(self, *token_types):
        if self.token:
            return self.token.type in list(token_types)

    def match(self, token_type_expected):
        if not self.token_is(token_type_expected):
            raise ValueError('Syntax error: expected "%s" but got "%s"' % (token_type_expected, self.token.type))
        else:
            self.token = self.next_token()

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

    ########################### RULES ############################

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
        '<actions> = skip_action'
        self.match('skip_action')