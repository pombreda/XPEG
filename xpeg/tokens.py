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