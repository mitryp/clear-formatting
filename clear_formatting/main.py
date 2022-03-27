"""A module containing main formatter class :class:`ValueFormatter`. See the class documentation for more info.
"""

#  Copyright (c) 2022. Dmytro Popov

from string import Formatter
from typing import Any

from clear_formatting.formats import *


class FormatError(TypeError):
    """Raised when :class:`ValueFormatter` got instance of incorrect format type."""
    pass


class ValueFormatter:
    """A class providing formatting methods.

    Takes a list of format types (:class:`Fill`, :class:`Align`, :class:`Sign`, :class:`Alternate`, :class:`Width`,
    :class:`Groping`, :class:`Precision`, :class:`Type`) when initializing. Then uses this list to build a format
    according to Python string formatting documentation.

    Also, conversion can be specified when initializing with conversion= :class:`Conversion`.<conversion option> .

    After ValueFormatter object was initialized with needed formats, its method format(value) can be used to format the
    value as well as calling object itself with the needed values (will use the same method).

    See the methods' documentation for other abilities.
    """

    formats: tuple[FormatBase | enum.Enum]
    conversion: Conversion | None

    def __init__(self: 'ValueFormatter', *formats: FormatBase | enum.Enum, conversion: Conversion = None):
        for fmt in formats:
            if type(fmt) not in ORDERED_FORMATS:
                raise FormatError('ValueFormatter cannot accept format {}. Expected formats are {}'.format(
                    fmt.__class__.__name__, ', '.join(f.__name__ for f in ORDERED_FORMATS)
                ))
        self.formats = formats
        self.conversion = conversion

    def __call__(self: 'ValueFormatter', value: Any) -> str:
        """The same as `format` method.

        :param value: a value to be formatted
        :return: formatted value
        """

        return self.format(value)

    def format(self: 'ValueFormatter', value: Any) -> str:
        """Returns the given value formatted with the format options applied during the initializing.

        :param value: a value to be formatted
        :return: formatted value
        """

        return self.format_value(self.formats, value, conversion=self.conversion)

    def build_template(self: 'ValueFormatter') -> str:
        """Returns a format template from the format options applied during the object initializing.

        :return: formatting options template to be used with str.format() method
        """

        return self.build_format_template(self.formats, self.conversion)

    @staticmethod
    def build_format_template(formats: Collection[FormatBase | enum.Enum],
                              conversion: Conversion = None) -> str:
        """Returns a format template from the format options listed in 'formats' and, if provided, conversion option
        from 'conversion'.

        :param formats: a list of formats to be used to build a format template
        :param conversion: conversion option (optional)
        :return: formatting options template to be used with str.format() method
        """

        conversion_template = f'!{conversion.value}' if conversion else ''
        return f'{{{conversion_template}:{"".join(fmt.value for fmt in sorted_formats(formats))}}}'

    @staticmethod
    def format_value(formats: Collection[FormatBase | enum.Enum], value: Any,
                     conversion: Conversion = None) -> str:
        """Returns the given value formatted with the format options listed in 'formats' and, if provided, conversion
        option from 'conversion'.

        :param formats: a list of formats to be used to build a format template
        :param value: a value to be formatted
        :param conversion: conversion option (optional)
        :return: formatted value
        """

        options = ValueFormatter.build_format_template(formats, conversion)
        return Formatter().format(options, value)
