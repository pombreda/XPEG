from tokens import Token, pattern
import re

class XPEGLexer(object):

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