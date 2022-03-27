# clear-formatting
A library providing a facade for clear values formatting.

### Functionality
All functionality is provided by the class `ValueFormatter` with help of the formatting classes of the `formats` module.

ValueFormatter must be initialized with a list of format classes. When initialized, the method `ValueFormatter.format(value)`
can be used to format the value, as well as calling the ValueFormatter object.

The class is using the default Python string formatting _(`str.format()` and curly braces)_ syntax to build a formatting template from the given instances of the format classes.

### Formats
ValueFormatter uses custom classes to determine the needed format for the value. The format classes are provided during ValueFormatter initialization. There is a list
of the format classes available at the module `formats`:
0) `FormatBase` - an abstract base class for not-enum format classes.

### Motives
I've written that lib after struggling with remembering all the format symbols belonging to Python string formatting syntax to make the formatting as easy as possible.
