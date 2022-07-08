"""A module containing format classes for :class:`clear_formatting.ValueFormatter` class.
"""

#  Copyright (c) 2022. Dmytro Popov

from __future__ import annotations

import abc
import enum
from typing import Collection, Union


class FormatBase(abc.ABC):
    """An abstract base class for non-enum format types for `ValueFormatter` class."""
    value: str

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value})'


class EnumFormatBase(enum.Enum):
    """A base class for enum format types for `ValueFormatter` class."""

    def __repr__(self):
        return f'{self.__class__.__name__}.{self.name}'


class Conversion(EnumFormatBase):
    """Causes a type coercion before formatting.

    Is used with :class:`ValueFormatter` (..., conversion=Conversion.STR).

    Normally, the job of formatting a value is done by the __format__() method of the value itself. However, in some
    cases it is desirable to force a type to be formatted as a string, overriding its own definition of formatting.
    By converting the value to a string before calling __format__(), the normal formatting logic is bypassed.

    For example, you would need conversion when trying to format a collection with some additional options. Normally,
    lists cannot be formatted with these formats, but with conversion=Conversion.STR or REPR it will be possible.

    Available conversions:

    * **STR** - calls str() on the value before formatting
    * **REPR** - calls repr() on the value before formatting
    * **ASCII** - calls ascii() on the value before formatting
    """

    STR = 's'
    REPR = 'r'
    ASCII = 'a'


class Fill(FormatBase):
    """Determines **fill character** for alignment.

    Will use only first symbol of the given string. If no string is given, counts equal to space char.

    *Curly braces '{' and '}' are not valid Fill values and will raise ValueErrors during formatting.*
    """

    def __init__(self, char: str):
        self.value = char[0] if char else ''


class Align(EnumFormatBase):
    """Determines align options for number and string formatting. Available option descriptions:

    * **CENTER** - Forces the field to be **centered** within the available space.

    * **LEFT** - Forces the field to be **left-aligned** within the available space.

    * **RIGHT** - Forces the field to be **right-aligned** within the available space.

    * **SPLIT_WITH_SIGN** - Forces the *padding to be placed after the sign (if any) but before the digits*.
      This is used for printing fields in the form ‘+000000120’. This alignment option is only valid for numeric types.
      It becomes the default for numbers when ‘0’ immediately precedes the field width.
    """

    CENTER = '^'
    LEFT = '<'
    RIGHT = '>'
    SPLIT_WITH_SIGN = '='


class Sign(EnumFormatBase):
    """Determines sign options for number formatting. Available option descriptions:

    * **ALL** - Indicates that a sign should be used for **both positive and negative numbers**.

    * **NEGATIVE** - Indicates that a sign should be used **only for negative numbers**.

    * **SPACE** - Indicates that a **leading space** should be used on positive numbers, and a **minus** sign on
      negative numbers.
    """

    ALL = '+'
    NEGATIVE = '-'
    SPACE = ' '


class Alternate(FormatBase):
    """Causes the **“alternate form”** to be used for the conversion.

    The alternate form is defined differently for
    different types. This option is only valid for integer, float and complex types. For integers, when binary, octal,
    or hexadecimal output is used, this option adds the respective prefix '0b', '0o', '0x', or '0X' to the output value.
    For float and complex the alternate form causes the result of the conversion to always contain a decimal-point
    character, even if no digits follow it. Normally, a decimal-point character appears in the result of these
    conversions only if a digit follows it. In addition, for GENERAL and GENERAL_UPPER conversions, trailing zeros are
    not removed from the result.
    """

    value = '#'


class Width(FormatBase):
    """Determines the **width** of the output string.

    Width is a decimal integer defining the minimum total field width, including any prefixes, separators, and other
    formatting characters. If not specified, then the field width will be determined by the content.

    Takes only positive integers. If negative values are given, it counts as 0.

    If correct Fill values are given, empty chars will be replaced with Fill values. In other cases, fills the empty
    chars with spaces.

    If the width is less than the needed for displaying the representation, Width values will be ignored. To limit
    the width purposely (even for strings), use the Precision format type.
    """

    def __init__(self, width: int = 0):
        self.value = str(max(int(width), 0))


class Groping(EnumFormatBase):
    """Determines separator for thousands. Available options:

    * **COMMA** - signals the use of a comma as a separator for thousands. For a locale aware separator, use the
      LOCALIZED_NUMBER integer presentation type instead.

    * **UNDERSCORE** - signals the use of an underscore as a separator for thousands for floating point presentation
      types and for integer presentation type DECIMAL. For integer presentation types BINARY, OCTAL, HEXADECIMAL,
      and HEXADECIMAL_UPPER, underscores will be inserted every 4 digits. For other presentation types, specifying this
      option is an error.
    """

    COMMA = ','
    UNDERSCORE = '_'


class Precision(FormatBase):
    """Determines the precision value for number and string formatting.

    The precision is a decimal integer indicating how many digits should be displayed after the decimal point
    for presentation types FIXED_POINT and FIXED_POINT_UPPER, or before and after the decimal point for presentation
    types GENERAL or GENERAL_UPPER.

    For **string** presentation types the field indicates the maximum field size - in other words, how many characters
    will be used from the field content. The precision is not allowed for integer presentation types.
    """

    def __init__(self, precision: int):
        self.value = f'.{precision}'


class Type(EnumFormatBase):
    """Determines how the data should be presented.

    *String types:*

    * **STRING** - String format. This is the default type for strings and may be omitted.

    *Integer types:*

    * **BINARY** - Binary format. Outputs the number in base 2.
    * **CHARACTER** - Character. Converts the integer to the corresponding unicode character before printing.
    * **DECIMAL** - Decimal Integer. Outputs the number in base 10.
    * **OCTAL** - Octal format. Outputs the number in base 8.
    * **HEXADECIMAL** - Hex format. Outputs the number in base 16, using lower-case letters for the digits above 9.
    * **HEXADECIMAL_UPPER** - Hex format. Outputs the number in base 16, using upper-case letters for the digits above
      9. In case ALTERNATE is specified, the prefix '0x' will be upper-cased to '0X' as well
    * **LOCALIZED_NUMBER** - Number. This is the same as DECIMAL, except that it uses the current locale setting to
      insert the appropriate number separator characters.

    *Floating point types:*

    * **EXPONENT** - Scientific notation. For a given precision p, formats the number in scientific notation with the
      letter ‘e’ separating the coefficient from the exponent. The coefficient has one digit before and p digits after
      the decimal point, for a total of p + 1 significant digits. With no precision given, uses a precision of 6 digits
      after the decimal point for float, and shows all coefficient digits for Decimal. If no digits follow the decimal
      point, the decimal point is also removed unless the ALTERNATE option is used.
    * **EXPONENT_UPPER** - Scientific notation. Same as EXPONENT except it uses an upper case ‘E’ as the separator
      character.
    * **FIXED_POINT** - Fixed-point notation. For a given Precision p, formats the number as a decimal number with
      exactly p digits following the decimal point. With no precision given, uses a precision of 6 digits after the
      decimal point for float, and uses a precision large enough to show all coefficient digits for Decimal. If no
      digits follow the decimal point, the decimal point is also removed unless the ALTERNATE option is used.
    * **FIXED_POINT_UPPER** - Fixed-point notation. Same as FIXED_POINT, but converts `nan` to `NAN` and `inf` to `INF`.
    * **GENERAL** - General format. For a given precision p >= 1, this rounds the number to p significant digits and
      then formats the result in either fixed-point format or in scientific notation, depending on its magnitude.
      A precision of 0 is treated as equivalent to a precision of 1. The precise rules are as follows: suppose that the
      result formatted with presentation type 'e' and precision p-1 would have exponent exp. Then, if m <= exp < p,
      where m is -4 for floats and -6 for Decimals, the number is formatted with presentation type 'f' and precision
      p-1-exp. Otherwise, the number is formatted with presentation type 'e' and precision p-1. In both cases
      insignificant trailing zeros are removed from the significand, and the decimal point is also removed if there are
      no remaining digits following it, unless the ALTERNATE option is used. With no precision given, uses a precision
      of 6 significant digits for float. For Decimal, the coefficient of the result is formed from the coefficient
      digits of the value; scientific notation is used for values smaller than 1e-6 in absolute value and values where
      the place value of the least significant digit is larger than 1, and fixed-point notation is used otherwise.
      Positive and negative infinity, positive and negative zero, and nans, are formatted as `inf`, `-inf`, `0`, `-0`
      and `nan` respectively, regardless of the precision.
    * **GENERAL_UPPER** - General format. Same as GENERAL except switches to EXPONENT_UPPER if the number gets too
      large. The representations of infinity and NaN are uppercased, too.
    * **PERCENT** - Percentage. Multiplies the number by 100 and displays in FIXED_POINT format, followed by a percent
      sign.
    """

    # STRING TYPES
    STRING = 's'

    # NUMBER TYPES

    # INTEGER TYPES
    BINARY = 'b'
    CHARACTER = 'c'
    DECIMAL = 'd'
    OCTAL = 'o'
    HEXADECIMAL = 'x'
    HEXADECIMAL_UPPER = 'X'
    LOCALIZED_NUMBER = 'n'

    # FLOATING POINT TYPES
    EXPONENT = 'e'
    EXPONENT_UPPER = 'E'
    FIXED_POINT = 'f'
    FIXED_POINT_UPPER = 'F'
    GENERAL = 'g'
    GENERAL_UPPER = 'G'
    PERCENT = '%'


ORDERED_FORMATS = (Fill, Align, Sign, Alternate, Width, Groping, Precision, Type)


def sorted_formats(formats: Collection[Union[FormatBase, EnumFormatBase]]) -> list:
    """Returns format types list sorted by the order specified in the string `formatting documentation
    <https://docs.python.org/3/library/string.html>`_.

    Takes the instances of types :class:`Fill`, :class:`Align`, :class:`Sign`, :class:`Alternate`, :class:`Width`,
    :class:`Groping`, :class:`Precision`, :class:`Type` in the formats list.

    If 'formats' contains a Fill format type, but Align format is not specified, chooses :class:`Align.RIGHT` format as
    align option.

    :param formats: a list of format types
    :return: sorted list of format types
    """

    format_types = list(map(lambda x: type(x), formats))
    if Fill in format_types and Align not in format_types:
        formats = list(formats)
        formats.append(Align.RIGHT)

    return sorted(formats, key=lambda x: ORDERED_FORMATS.index(x.__class__))
