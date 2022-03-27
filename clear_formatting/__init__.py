"""A library providing a facade for clear formatting values into strings.

Uses custom format types Fill, Align, Sign, Alternate, Width, Groping, Precision, Type to build the standard format
templates.

Uses standard string formatting methods inside.

See the `documentation on GitHub <https://github.com/mitryp/clear-formatting>`_
and `official string formatting documentation <https://docs.python.org/3/library/string.html>`_ for more info.
"""

#  Copyright (c) 2022. Dmytro Popov

from clear_formatting.main import ValueFormatter, FormatTypeError
from clear_formatting import formats
