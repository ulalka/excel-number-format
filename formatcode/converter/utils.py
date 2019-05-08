# coding: utf8

from __future__ import division, print_function, unicode_literals
from formatcode.lexer.tokens import BlockDelimiter, ConditionToken
from formatcode.converter.errors import ConditionError, PartsCountError


def split_tokens_by_parts(tokens):
    counter = 1

    part = []
    for token in tokens:
        if isinstance(token, BlockDelimiter):
            if counter == 4:
                # There can be only 4 parts
                raise PartsCountError(tokens)
            yield part
            counter += 1
            part = []
        else:
            if isinstance(token, ConditionToken) and counter > 2:
                # Only 1 or 2 block can have the condition
                raise ConditionError(tokens)

            part.append(token)
    yield part