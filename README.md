# clear-formatting

A library providing a facade for clear and easy-to-get values formatting.

I've written this lib after struggling to remember all the format symbols belonging to Python string formatting
syntax to make the formatting as easy as possible.

## Functionality

All functionality is provided by the class `ValueFormatter` with help of the formatting classes of the `formats` module.

ValueFormatter must be initialized with a list of format classes. When initialized, the
method `ValueFormatter.format(value)` can be used to format the value, as well as calling the ValueFormatter object with
the value as argument.

The class is using the default Python string formatting _(`str.format()` and curly braces)_ syntax to build a formatting
template from the given instances of the format classes.

## Formats

ValueFormatter uses custom classes to determine the needed output format for the value. The format classes are provided 
during ValueFormatter initialization. There is a list of the format classes available at the module `formats` with their
options:

0) `FormatBase` | `EnumFormatBase` - base classes for non-enum and enum format classes, respectively.
1) `Conversion` - format class that causes a type coercion (to string) before formatting. The only format class to be
   used split from others. See the [Type conversion](#type-conversion) section for details.
    * `STR` - converts the value to a string using *str()* method.
    * `REPR` - also converts the value to a string, but using *repr()* method.
    * `ASCII` - converts the value to a string with ascii() method (leaves only ASCII characters).
2) `Fill(char: str)` - determines the width fill character. The provided char will be used to replace the empty
   characters.
3) `Align` - determines the alignment options. Has its effect only with Width format class.
    * `CENTER` - forces the field to be centered within the available space.
    * `LEFT` - forces the field to be left-aligned within the available space.
    * `RIGHT` - forces the field to be right-aligned within the available space.
    * `SPLIT_WITH_SIGN` - forces the padding to be placed after the sign (if any) but before the digits.
4) `Sign` - determines the sign display options for number formatting.
    * `ALL` - indicates that a sign should be displayed for both positive and negative numbers.
    * `NEGATIVE` - indicates that a sign should be displayed only for negative numbers (this is the default option).
    * `SPACE` - indicates that a leading space should be used for positive numbers and a sign should be displayed for
      negative numbers.
5) `Alternate()` - causes the alternate form to be used for the conversion.

   The alternate form is defined differently for different types. This option is only valid for integer, float and
   complex types. For integers, when binary, octal, or hexadecimal output is used, this option adds the respective
   prefix '0b', '0o', '0x', or '0X' to the output value. For float and complex the alternate form causes the result of
   the conversion to always contain a decimal-point character, even if no digits follow it. Normally, a decimal-point
   character appears in the result of these conversions only if a digit follows it. In addition, for `GENERAL`
   and `GENERAL_UPPER` conversions, trailing zeros are not removed from the result.
7) `Width(width: int)` - determines the width (in characters) of the output string. Takes only positive integers. If the
   negative number is specified, the width is set to 0. If the floating point number is specified, casts if to integer.
8) `Groping` - determines the separator for thousands.
    * `COMMA` - signals the use of a comma as a separator for thousands. For a locale aware separator, use the
      LOCALIZED_NUMBER integer presentation type instead.
    * `UNDERSCORE` - signals the use of an underscore as a separator for thousands for floating point presentation types
      and for integer presentation type `DECIMAL`. For integer presentation types `BINARY`, `OCTAL`, `HEXADECIMAL`,
      and `HEXADECIMAL_UPPER`, underscores will be inserted every 4 digits. For other presentation types, specifying
      this option will cause an error.
9) `Precision(precision: int)` - determines the precision value for number and string formatting. For floating point
   presentation types, this value specifies the quantity of digits to be rounded to. For string type, specifying this
   value will limit the length of the string by the precision value. For integer presentation types specifying this
   value will cause an error.
10) `Type` - determines how the data should be presented.
    1) String types
        * `STRING` - string format. This is the default type for strings and may be omitted.
    2) Integer types
        * `BINARY` - binary format. Outputs the number in base 2.
        * `CHARACTER` - character. Converts the integer to the corresponding unicode character before printing.
        * `DECIMAL` - decimal Integer. Outputs the number in base 10.
        * `OCTAL` - octal format. Outputs the number in base 8.
        * `HEXADECIMAL` - hex format. Outputs the number in base 16, using lower-case letters for the digits above 9.
        * `HEXADECIMAL_UPPER` - hex format. Outputs the number in base 16, using upper-case letters for the digits above
            9. In case ALTERNATE is specified, the prefix '0x' will be upper-cased to '0X' as well
        * `LOCALIZED_NUMBER` - number. This is the same as `DECIMAL`, except that it uses the current locale setting to
          insert the appropriate number separator characters.
    3) Floating point types
        * `EXPONENT` - scientific notation. For a given precision p, formats the number in scientific notation with the
          letter ‘e’ separating the coefficient from the exponent. The coefficient has one digit before and p digits
          after the decimal point, for a total of p + 1 significant digits. With no precision given, uses a precision of
          6 digits after the decimal point for float, and shows all coefficient digits for Decimal. If no digits follow
          the decimal point, the decimal point is also removed unless the ALTERNATE option is used.
        * `EXPONENT_UPPER` - scientific notation. Same as EXPONENT except it uses an upper case ‘E’ as the separator
          character.
        * `FIXED_POINT` - fixed-point notation. For a given Precision p, formats the number as a decimal number with
          exactly p digits following the decimal point. With no precision given, uses a precision of 6 digits after the
          decimal point for float, and uses a precision large enough to show all coefficient digits for Decimal. If no
          digits follow the decimal point, the decimal point is also removed unless the ALTERNATE option is used.
        * `FIXED_POINT_UPPER` - fixed-point notation. Same as FIXED_POINT, but converts `nan` to `NAN` and `inf`
          to `INF`.
        * `GENERAL` - general format. For a given precision p >= 1, this rounds the number to p significant digits and
          then formats the result in either fixed-point format or in scientific notation, depending on its magnitude. A
          precision of 0 is treated as equivalent to a precision of 1. The precise rules are as follows: suppose that
          the result formatted with presentation type 'e' and precision p-1 would have exponent exp. Then, if m <= exp <
          p, where m is -4 for floats and -6 for Decimals, the number is formatted with presentation type 'f' and
          precision p-1-exp. Otherwise, the number is formatted with presentation type 'e' and precision p-1. In both
          cases insignificant trailing zeros are removed from the significand, and the decimal point is also removed if
          there are no remaining digits following it, unless the ALTERNATE option is used. With no precision given, uses
          a precision of 6 significant digits for float. For Decimal, the coefficient of the result is formed from the
          coefficient digits of the value; scientific notation is used for values smaller than 1e-6 in absolute value
          and values where the place value of the least significant digit is larger than 1, and fixed-point notation is
          used otherwise. Positive and negative infinity, positive and negative zero, and nans, are formatted as `inf`
          , `-inf`, `0`, `-0`
          and `nan` respectively, regardless of the precision.
        * `GENERAL_UPPER` - general format. Same as `GENERAL` except switches to `EXPONENT_UPPER` if the number gets too
          large. The representations of infinity and NaN are uppercased, too.
        * `PERCENT` - percentage. Multiplies the number by 100 and displays in `FIXED_POINT` format, followed by a
          percent sign.

## Usage
#### Installation
First, the lib must be installed with pip:
```
pip install clear-formatting
```

The lib doesn't have any dependencies, so it'll install only one package.

Import the `ValueFormatter` class and `formats` module:

```python
from clear_formatting import ValueFormatter, formats
```

#### The first formatting
To basically format any value with this library, we'll need to create a `ValueFormatter` object with a list of formats
to apply to the value. The formats themselves can be found in the [Formats](#formats) section of documentation above.

Let's create a formatter that aligns the value at the center of the string with the length of 20, that filled with the
dashes ' - ':

```python
vf = ValueFormatter(formats.Align.CENTER, formats.Width(20), formats.Fill('-'))
```

Now we can use the `vf` object to format any values we need:

```python
>>> print(vf('its a test'))  # the same as vf.format('its a test')
Out: -----its a test-----
```

_The formats can be specified in any order and combinations, but duplicating formats is not allowed due to unpredictable
behaviour._

#### Changing the view

Now let's try to convert an integer with the decimal notation to other notations.

```python
>>> dec = 31
>>> print(ValueFormatter(formats.Type.BINARY)(dec))
Out: 11111

>>> print(ValueFormatter(formats.Type.OCTAL)(dec))
Out: 37

>>> print(ValueFormatter(formats.Type.HEXADECIMAL)(dec))  # HEXADECIMAL_UPPER will return the same value in uppercase
Out: 1f  # 1F for HEXADECIMAL_UPPER
```

#### More complexity
Let me show you a little more complex example. Imagine you have to make a fixed-width column of integers, and, 
moreover, to split the sign and the digits at the opposite sides of the column:

```python
column_format = ValueFormatter(formats.Width(15), formats.Sign.ALL, formats.Align.SPLIT_WITH_SIGN)
import random
for _ in range(10):
    print(column_format(random.randint(-100, 100)))
Out:
-            40
-            82
+            80
+            18
-            13
-            57
-            11
+             3
-             4
+            70
```

#### Type conversion
Sometimes the value we need to format is not a string or a number. In that case regular formatting will cause an 
exception:

```python
>>> vf = ValueFormatter(formats.Width(20), formats.Align.CENTER, formats.Fill('-'))
>>> lst = [1, 2, 3]
>>> print(vf(lst))
Out: 
Traceback (most recent call last):
...
TypeError: unsupported format string passed to list.__format__
```
To prevent this, we can use a conversion option of the `ValueFormatter` and a `Conversion` format class:
```python
>>> vf = ValueFormatter(formats.Width(20), formats.Align.CENTER, formats.Fill('-'), conversion=formats.Conversion.STR)
>>> lst = [1,2,3]
>>> print(vf(lst))
Out: -----[1, 2, 3]------
```
In the example above, the formatter converted a list to string with `str()` function - this is what `Conversion.STR` 
stands for.

Other conversions:
* `Conversion.REPR` - uses `repr()` function instead;
* `Conversion.ASCII` - uses `ascii()` function instead.
