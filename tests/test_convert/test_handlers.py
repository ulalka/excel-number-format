# coding: utf-8

from __future__ import division, print_function, unicode_literals

from decimal import Decimal

import pytest

from formatcode.convert.fc import FormatCode
from formatcode.convert.handlers import (GeneralHandler, StringHandler, EmptyHandler, UnknownHandler, DigitHandler)
from formatcode.lexer.lexer import to_tokens_line


@pytest.fixture(scope='module')
def fc_1():
    tokens = to_tokens_line('0,,;\\-0" "?/10%;General;"Hello, "@\\!')
    return FormatCode(tokens=tokens)


@pytest.fixture(scope='module')
def fc_2():
    tokens = to_tokens_line('0,000.0,;0" "?/?;;@[$$]')
    return FormatCode(tokens=tokens)


@pytest.fixture(scope='module')
def fc_3():
    tokens = to_tokens_line('0,0.0;General')
    return FormatCode(tokens=tokens)


def test_general_handler(fc_1, fc_3):
    h = fc_1.else_part.handler
    assert isinstance(h, GeneralHandler)
    assert h.format(Decimal(1234)) == '1234'
    assert h.format(Decimal(-1234)) == '-1234'
    assert h.format(Decimal('1234.1234')) == '1234.1234'
    assert h.format(Decimal('-1234.1234')) == '-1234.1234'

    h = fc_3.neg_part.handler
    assert isinstance(h, GeneralHandler)
    assert h.format(Decimal(-1234)) == '1234'
    assert h.format(Decimal('-1234.1234')) == '1234.1234'
    assert h.format('test') == 'test'


def test_string_handler(fc_1, fc_2):
    h = fc_1.str_part.handler
    assert isinstance(h, StringHandler)
    assert h.format('John') == 'Hello, John!'
    assert h.format('mister') == 'Hello, mister!'

    h = fc_2.str_part.handler
    assert isinstance(h, StringHandler)
    assert h.format('John') == 'John$'
    assert h.format('mister') == 'mister$'


def test_empty_handler(fc_2):
    h = fc_2.else_part.handler
    assert isinstance(h, EmptyHandler)
    assert h.format('John') == ''
    assert h.format('mister') == ''


def test_unknown_handler(fc_3):
    h = fc_3.else_part.handler
    assert isinstance(h, UnknownHandler)
    assert h.format('John') == '###'
    assert h.format('mister') == '###'

    h = fc_3.str_part.handler
    assert isinstance(h, UnknownHandler)
    assert h.format('John') == 'John'
    assert h.format('mister') == 'mister'


def test_digit_handler():
    fc_1 = FormatCode(tokens=to_tokens_line('0,,;\\-0" "?/10%;General;"Hello, "@\\!'))

    pos_h = fc_1.pos_part.handler
    assert isinstance(pos_h, DigitHandler)
    assert pos_h.by_thousand is False
    assert pos_h.round_base == 0
    assert pos_h.fraction_divisor is None
    assert pos_h.fraction_divisor_size is None
    assert pos_h.divisor == 1000000
    assert len(pos_h.left) == 3
    assert len(pos_h.right) == 0

    neg_h = fc_1.neg_part.handler
    assert isinstance(neg_h, DigitHandler)
    assert neg_h.by_thousand is False
    assert neg_h.round_base is None
    assert neg_h.fraction_divisor == 10
    assert neg_h.fraction_divisor_size is None
    assert neg_h.divisor == 0.01
    assert len(neg_h.left) == 3
    assert len(neg_h.right) == 3

    fc_2 = FormatCode(tokens=to_tokens_line('0,000.0,;0" "?/?;;@[$$]'))
    pos_h = fc_2.pos_part.handler
    assert isinstance(pos_h, DigitHandler)
    assert pos_h.by_thousand is True
    assert pos_h.round_base == 1
    assert pos_h.fraction_divisor is None
    assert pos_h.fraction_divisor_size is None
    assert pos_h.divisor == 1000
    assert len(pos_h.left) == 5
    assert len(pos_h.right) == 2

    neg_h = fc_2.neg_part.handler
    assert isinstance(neg_h, DigitHandler)
    assert neg_h.by_thousand is False
    assert neg_h.round_base is None
    assert neg_h.fraction_divisor is None
    assert neg_h.fraction_divisor_size == 1
    assert neg_h.divisor == 1
    assert len(neg_h.left) == 2
    assert len(neg_h.right) == 3
