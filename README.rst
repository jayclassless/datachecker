datachecker
===========

**datachecker** is a simple library for performing common validations and sanitization of data.

A simple example:

::

    >>> import datachecker as dc
    >>> checker = dc.Checker(dc.string, dc.strip, dc.email)
    >>> checker.is_valid('hello@example.com')
    True
    >>> checker.process('hello@example.com')
    u'hello@example.com'
    >>> checker.is_valid('  hello@example.com')
    True
    >>> checker.process('  hello@example.com')
    u'hello@example.com'
    >>> checker.is_valid('bad data')
    False
    >>> checker.process('bad data')
    Traceback (most recent call last):
      ...
    datachecker.errors.FormatError: bad data is not formatted properly

A more involved example:

::

    >>> import datachecker as dc
    >>> checker = dc.Checker(dc.dict({
    ...     'foo': [dc.required, dc.string, dc.upper],
    ...     'bar': [dc.required, dc.integer(max=10)],
    ...     'baz': [dc.optional(default='green'), dc.string(coerce=True), dc.lower],
    ... }))
    >>> checker.process({
    ...     'foo': 'Happy',
    ...     'bar': 5,
    ... })
    {'baz': 'green', 'foo': u'HAPPY', 'bar': 5}
    >>> checker.process({
    ...     'foo': 'Happy',
    ...     'bar': 5,
    ...     'baz': 'PURPLE!'
    ... })
    {'baz': u'purple!', 'foo': u'HAPPY', 'bar': 5}
    >>> checker.process({
    ...     'foo': 'Turn it up',
    ...     'bar': 11,
    ... })
    Traceback (most recent call last):
      ...
    datachecker.errors.BoundsError: Value is above the limit of 10


When the data being checked passes all validations, the checker will return the processed, sanitized
data. Othewise, it will raise a CheckerError exception.


Installation
------------

Use `pip <http://www.pip-installer.org>`_. There are no excuses.

::

    pip install datachecker

If you plan on using the DNS-checking abilities of some of the built-in processors, then you'll also need
to install `dnspython <http://www.dnspython.org>`_.

::

    pip install dnspython


How it Works
------------

The main concept around **datachecker** is that it sends the incoming data through a pipeline of processors,
feeding the output of one as the input to the next. If we can get to the end of the pipeline without raising
an exception, then the resulting data is declared valid.

Processors that check the data against some rule and raises an exception when the data does not pass the rule
are known as "validators". Processors that alter the data as it passes through them are known as "sanitizers".


Checker
-------

To use **datachecker**, you first build yourself a Checker object, telling it what processors to use. You can specify any number of processors to apply to your input data.

::

    >>> checker = dc.Checker(dc.required, dc.string, dc.upper)

Then you can use your Checker object to validate and/or sanitize your data:

::

    >>> checker.process('foo')
    u'FOO'
    >>> checker.is_valid('foo')
    True

The Checker object exposes two methods:

**process(data)**

    The process method runs your input data through the processors you specified and returns the resulting value. If any of the processors finds the input data to be invalid, a CheckerError exception will be raised.

**is_valid(data)**

    The is_valid method returns a simple boolean indicating whether or not the input data passes successfuly through all the processors.


Built-In Processors
-------------------


**integer**

Ensures the input value is an integer datatype (either ``int`` or ``long``).

*Options*

* coerce: True/False; Will cause the processor to attempt to coerce the value into an integer. This allows you to accept an input of "1" and interpret it as the integer 1.
* min: Enforces a minimum value check. Defaults to ``None``, which means don't check.
* max: Enforces a maximum value check. Defaults to ``None``, which means don't check.

*Examples*

::

    >>> dc.Checker(dc.integer).is_valid(1)
    True
    >>> dc.Checker(dc.integer).is_valid('1')
    False
    >>> dc.Checker(dc.integer(coerce=True)).is_valid('1')
    True
    >>> dc.Checker(dc.integer).is_valid(1.2)
    False
    >>> dc.Checker(dc.integer(min=5)).is_valid(1)
    False
    >>> dc.Checker(dc.integer(min=5)).is_valid(6)
    True


**float**

Ensures the input value is a ``float`` datatype.

*Options*

* coerce: True/False; Will cause the processor to attempt to coerce the value into a ``float``. This allows you to accept an input of "1.23" and interpret it as the ``float`` 1.23.
* min: Enforces a minimum value check. Defaults to ``None``, which means don't check.
* max: Enforces a maximum value check. Defaults to ``None``, which means don't check.

*Examples*

::

    >>> dc.Checker(dc.float).is_valid(1)
    False
    >>> dc.Checker(dc.float).is_valid(1.23)
    True
    >>> dc.Checker(dc.float).is_valid('1.23')
    False
    >>> dc.Checker(dc.float(coerce=True)).is_valid('1.23')
    True
    >>> dc.Checker(dc.float).is_valid(1)
    False
    >>> dc.Checker(dc.float(min=5)).is_valid(1.23)
    False
    >>> dc.Checker(dc.float(min=5)).is_valid(6.23)
    True


**decimal**

Ensures the input value is a ``Decimal`` datatype.

*Options*

* coerce: True/False; Will cause the processor to attempt to coerce the value into a ``Decimal``. This allows you to accept an input of "1.23" and interpret it as Decimal('1.23').
* min: Enforces a minimum value check. Defaults to ``None``, which means don't check.
* max: Enforces a maximum value check. Defaults to ``None``, which means don't check.

*Examples*

::

    >>> dc.Checker(dc.decimal).is_valid(Decimal('1.23'))
    True
    >>> dc.Checker(dc.decimal).is_valid('1.23')
    False
    >>> dc.Checker(dc.decimal(coerce=True)).is_valid('1.23')
    True
    >>> dc.Checker(dc.decimal).is_valid(1.23)
    False
    >>> dc.Checker(dc.decimal(min=5)).is_valid(Decimal('1.23'))
    False
    >>> dc.Checker(dc.decimal(min=5)).is_valid(Decimal('6.23'))
    True


**string**

Ensures the input value is a string datatype.

*Options*

* coerce: True/False; Will cause the processor to attempt to coerce the value into a string. This allows you to accept an input of 1.23 and interpret it as the string "1.23".

*Examples*

::

    >>> dc.Checker(dc.string).is_valid('abc')
    True
    >>> dc.Checker(dc.string).is_valid(1.23)
    False
    >>> dc.Checker(dc.string(coerce=True)).is_valid(1.23)
    True
    >>> dc.Checker(dc.string).is_valid(u'abc')
    True


**boolean**

Ensures the input value is a ``bool`` datatype.

*Options*

* coerce: True/False; Will cause the processor to attempt to coerce the value into a ``bool``. Values that resembe "True"/"Yes"/"Y"/"1"/1/"On" will evaluate to True, values that resemble "False"/"No"/"N"/"0"/0/"Off" will evaluate to False.

*Examples*

::

    >>> dc.Checker(dc.boolean).is_valid(True)
    True
    >>> dc.Checker(dc.boolean).is_valid(False)
    True
    >>> dc.Checker(dc.boolean).is_valid('True')
    False
    >>> dc.Checker(dc.boolean(coerce=True)).is_valid('True')
    True
    >>> dc.Checker(dc.boolean(coerce=True)).is_valid(1)
    True
    >>> dc.Checker(dc.boolean(coerce=True)).is_valid(0)
    True
    >>> dc.Checker(dc.boolean(coerce=True)).is_valid('foo')
    False


**length**

Ensures that the input iterable has a length within the specified bounds. This processor can operate on anything that is an iterable; strings, lists, tuples, or anything that implements the iterable interface.

*Options*

* min: Enforces a minimum length check. Defaults to ``None``, which means don't check.
* min: Enforces a maximum length check. Defaults to ``None``, which means don't check.
* exact: Requires that the length be exactly the specified integer. Defaults to ``None``, which means don't check.

*Examples*

::

    >>> dc.Checker(dc.length(min=2)).is_valid([1, 2, 3])
    True
    >>> dc.Checker(dc.length(min=2)).is_valid('abc')
    True
    >>> dc.Checker(dc.length(max=2)).is_valid('abc')
    False
    >>> dc.Checker(dc.length(min=2)).is_valid(1.23)
    False
    >>> dc.Checker(dc.length(exact=3)).is_valid([1, 2, 3])
    True


**ip**

Ensures that the input value is a string representation of an IP address.

*Options*

* ipv4: True/False; Tells the processor to allow IPv4-style addresses. Defaults to True.
* ipv6: True/False; Tells the processor to allow IPv6-style addresses. Defaults to True if the system supports IPv6.

*Examples*

::

    >>> dc.Checker(dc.ip).is_valid('127.0.0.1')
    True
    >>> dc.Checker(dc.ip).is_valid('foo')
    False
    >>> dc.Checker(dc.ip).is_valid('::1')
    True
    >>> dc.Checker(dc.ip(ipv6=False)).is_valid('::1')
    False


**domain**

Ensures that the input value looks like a domain.

*Options*

* check_dns: True/False; Tells the processor to actually perform DNS checks on the domain to determine if it is actually real. Defaults to False.

*Examples*

::

    >>> dc.Checker(dc.domain).is_valid('google.com')
    True
    >>> dc.Checker(dc.domain).is_valid('googleco.m')
    False
    >>> dc.Checker(dc.domain).is_valid('foo.bar')
    True
    >>> dc.Checker(dc.domain(check_dns=True)).is_valid('foo.bar')
    False


**match**

Ensures that the input value is a string that matches the given regular expression.

There are also a set of built-in matchers for common cases: ``alpha``, ``numeric``, and ``alphanumeric``

*Options*

* options: The Python regular expression flags that should be used (e.g., re.UNICODE, re.IGNORECASE, etc). Defaults to 0 (no flags).

*Examples*

::

    >>> dc.Checker(dc.match(r'^[abc]+$')).is_valid('abcabc')
    True
    >>> dc.Checker(dc.match(r'^[abc]+$')).is_valid('foo')
    False
    >>> dc.Checker(dc.match(r'^[abc]+$')).is_valid(1)
    False
    >>> dc.Checker(dc.alpha).is_valid('abc')
    True
    >>> dc.Checker(dc.alpha).is_valid('123')
    False
    >>> dc.Checker(dc.numeric).is_valid('abc')
    False
    >>> dc.Checker(dc.numeric).is_valid('123')
    True
    >>> dc.Checker(dc.alphanumeric).is_valid('abc')
    True
    >>> dc.Checker(dc.alphanumeric).is_valid('123')
    True
    >>> dc.Checker(dc.alphanumeric).is_valid('abc123')
    True


**email**

Ensures that the input value looks like an email address.

*Options*

* check_dns: True/False; Tells the processor to actually perform DNS checks on the domain portion of the email address to determine if the domain is actually capable of receiving email. Defaults to False.

*Examples*

::

    >>> dc.Checker(dc.email).is_valid('foo@bar.com')
    True
    >>> dc.Checker(dc.email).is_valid('foo')
    False
    >>> dc.Checker(dc.email).is_valid('foo@bar@baz.com')
    False
    >>> dc.Checker(dc.email).is_valid('foo@asfdsafsasaffdsafdsafsadfdsaf.com')
    True
    >>> dc.Checker(dc.email(check_dns=True)).is_valid('foo@asfdsafsasaffdsafdsafsadfdsaf.com')
    False


**url**

Ensures that the input value looks like a URL.

*Options*

* schemes: A list that tells the processor what URL schemes to limit valid data to. Defaults to ``None``, which means don't check.

*Examples*

::

    >>> dc.Checker(dc.url).is_valid('http://www.google.com')
    True
    >>> dc.Checker(dc.url).is_valid('www.google.com')
    False
    >>> dc.Checker(dc.url).is_valid('foo')
    False
    >>> dc.Checker(dc.url(schemes=['http'])).is_valid('http://www.google.com')
    True
    >>> dc.Checker(dc.url(schemes=['https'])).is_valid('http://www.google.com')
    False


**lower**

Forces the input string to be all lowercase characters.

*Examples*

::

    >>> dc.Checker(dc.lower).process('FooBar')
    'foobar'


**upper**

Forces the input string to be all uppercase characters.

*Examples*

::

    >>> dc.Checker(dc.upper).process('FooBar')
    'FOOBAR'


**strip**

Removes whitespace (or specified characters) from one or both ends of a string.

*Options*

* left: True/False; Tells the processor to strip characters from the left end of the string. Defaults to True.
* right: True/False; Tells the processor to strip characters from the right end of the string. Defaults to True.
* chars: A string of characters that the processor will remove from either end of the string. Defaults to ``None``, which means all whitespace

*Examples*

::

    >>> dc.Checker(dc.strip).process('  foo  ')
    'foo'
    >>> dc.Checker(dc.strip(right=False)).process('  foo  ')
    'foo  '
    >>> dc.Checker(dc.strip(chars='cmowz.')).process('www.example.com')
    'example'
    >>> dc.Checker(dc.strip(left=False, chars='cmowz.')).process('www.example.com')
    'www.example'


**title**

Forces the input string to be title-cased.

*Examples*

::

    >>> dc.Checker(dc.title).process('foo bar')
    'Foo Bar'


**swapcase**

Forces the input to have its casing reversed so that lowercased characters become uppercased and vice-versa.

*Examples*

::

    >>> dc.Checker(dc.swapcase).process('FooBar')
    'fOObAR'


**capitalize**

Forces the input string to have its first character capitalized and the rest lowercase.

*Examples*

::

    >>> dc.Checker(dc.capitalize).process('FooBar')
    'Foobar'


**replace**

Performs a regular-expression based string replacement on the input.

There are also a set of built-in replacers for common cases: ``collapse_whitespace``

*Options*

* options: The Python regular expression flags that should be used (e.g., re.UNICODE, re.IGNORECASE, etc). Defaults to 0 (no flags).

*Examples*

::

    >>> dc.Checker(dc.replace(r'\sAnd\s', ' & ')).process('Baked Beans And Spam')
    'Baked Beans & Spam'
    >>> dc.Checker(dc.replace(r'\d+', '#')).process('a1b23c456d7890')
    'a#b#c#d#'


**constant**

Ensures that the input value is a specific value.

*Examples*

::

    >>> dc.Checker(dc.constant('foo')).is_valid('foo')
    True
    >>> dc.Checker(dc.constant('foo')).is_valid('bar')
    False
    >>> dc.Checker(dc.constant(123)).is_valid(123)
    True


**choice**

Ensures that the input value is one of a list of acceptible values.

*Examples*

::

    >>> dc.Checker(dc.choice('foo', 'bar')).is_valid('foo')
    True
    >>> dc.Checker(dc.choice('foo', 'bar')).is_valid('bar')
    True
    >>> dc.Checker(dc.choice('foo', 'bar')).is_valid('baz')
    False
    >>> dc.Checker(dc.choice(1, 2, 3)).is_valid(2)
    True


**required**

Ensures that a value was specified (e.g., the value is not ``None``)

*Examples*

::

    >>> dc.Checker(dc.required).is_valid('foo')
    True
    >>> dc.Checker(dc.required).is_valid(None)
    False


**optional**

If no input value was specified (e.g., the value is ``None``), then this processor will return the specified default value.

Note that if this processor returns the default value rather than the input value, then all processing will stop. No other processors specified in the chain will execute.

*Options*

* default: The value to return if an input value is not specified. Defaults to ``None``.

*Examples*

::

    >>> dc.Checker(dc.optional(default='foo')).process(None)
    'foo'
    >>> dc.Checker(dc.optional(default='foo')).process('bar')
    'bar'
    >>> dc.Checker(dc.optional(default='foo'), dc.upper).process(None)
    'foo'
    >>> dc.Checker(dc.optional(default='foo'), dc.upper).process('bar')
    'BAR'



**list**

Ensures that the input value is a ``list``.

This processor can also apply a series of processors to each element in the ``list``.

*Options*

* coerce: True/False; Tells the processor to try to coerce the input value into being a ``list``. If the value is a ``tuple`` or some other iterable object, it will be turned into a ``list`` with all the same elements. Otherwise, the value is turned into a ``list`` with one element; the original input value. Defaults to False.

*Examples*

::

    >>> dc.Checker(dc.list).is_valid([1,2,3])
    True
    >>> dc.Checker(dc.list).is_valid('foobar')
    False
    >>> dc.Checker(dc.list).is_valid(['a','b','c'])
    True
    >>> dc.Checker(dc.list(dc.integer)).is_valid(['a','b','c'])
    False
    >>> dc.Checker(dc.list(dc.integer)).is_valid([1,2,3])
    True
    >>> dc.Checker(dc.list(coerce=True)).is_valid('foobar')
    True
    >>> dc.Checker(dc.list(dc.upper, coerce=True)).process('foobar')
    ['FOOBAR']


**tuple**

Ensures that the input value is a ``tuple``.

This processor can also apply a series of processors to each element in the ``tuple``.

*Options*

* coerce: True/False; Tells the processor to try to coerce the input value into being a ``tuple``. If the value is a ``list`` or some other iterable object, it will be turned into a ``tuple`` with all the same elements. Otherwise, the value is turned into a ``tuple`` with one element; the original input value. Defaults to False.

*Examples*

::

    >>> dc.Checker(dc.tuple).is_valid((1,2,3))
    True
    >>> dc.Checker(dc.tuple).is_valid('foobar')
    False
    >>> dc.Checker(dc.tuple).is_valid(('a','b','c'))
    True
    >>> dc.Checker(dc.tuple(dc.integer)).is_valid(('a','b','c'))
    False
    >>> dc.Checker(dc.tuple(dc.integer)).is_valid((1,2,3))
    True
    >>> dc.Checker(dc.tuple(coerce=True)).is_valid('foobar')
    True
    >>> dc.Checker(dc.tuple(dc.upper, coerce=True)).process('foobar')
    ('FOOBAR',)


**dict**

Ensures that the input value is a ``dict``.

This processor can also apply a series of processors to each item in the ``dict``.

*Options*

* coerce: True/False; Tells the processor to try to coerce the input value into being a ``dict``. Defaults to False.
* ignore_extra: True/False; Tells the processor to not raise errors if keys exist beyond those that are specified. Defaults to False.
* ignore_missing: True/False; Tells the processor to not assume ``None`` for keys that are not found in the input data. Defaults to False.
* pass_extra: True/False; Tells the processor that any extra keys found in the input data beyond those that are specified should be passed along in the results. Defaults to False, which means the extras are dropped.
* capture_all_errors: True/False; Tells the processor to process every key in the input data and return an Exception that contains error messages for all keys that failed processing. Defaults to False, which means that the first error encountered in processing is immediately returned.

*Examples*

::

    >>> checker = dc.Checker(dc.dict({
    ...     'foo': [dc.required, dc.string, dc.upper],
    ...     'bar': [dc.required, dc.integer(max=10)],
    ...     'baz': [dc.optional(default='green'), dc.string(coerce=True), dc.lower],
    ... }))
    >>> checker.process({
    ...     'foo': 'Happy',
    ...     'bar': 5,
    ... })
    {'baz': 'green', 'foo': u'HAPPY', 'bar': 5}
    >>> checker.process({
    ...     'foo': 'Happy',
    ...     'bar': 5,
    ...     'baz': 'PURPLE!'
    ... })
    {'baz': u'purple!', 'foo': u'HAPPY', 'bar': 5}
    >>> checker.process({
    ...     'foo': 'Turn it up',
    ...     'bar': 11,
    ... })
    Traceback (most recent call last):
      ...
    datachecker.errors.BoundsError: Value is above the limit of 10


**iterable**

Ensures that the input data is an iterable.

*Examples*

::

    >>> dc.Checker(dc.iterable).is_valid([1,2,3])
    True
    >>> dc.Checker(dc.iterable).is_valid((1,2,3))
    True
    >>> dc.Checker(dc.iterable).is_valid('foo')
    True
    >>> dc.Checker(dc.iterable).is_valid({'foo':'bar'})
    True
    >>> dc.Checker(dc.iterable).is_valid(1)
    False


Custom Processors
-----------------

You can implement your own processors for use in **datachecker** by simply implementing a callable that accepts at least one argument to receive the input data, and then returns the (possibly modified) data. For example:

::

    >>> def reverse(data):
    ...     return data[::-1]
    ... 
    >>> dc.Checker(reverse).process('foobar')
    'raboof'

To act as a validator rather than a sanitizer, simply raise a CheckerError exception when the input data is invalid. For Example:

::

    >>> def is_foo(data):
    ...     if data != 'foo':
    ...         raise dc.CheckerError('Not foo!')
    ...     return data
    ... 
    >>> dc.Checker(is_foo).is_valid('foo')
    True
    >>> dc.Checker(is_foo).is_valid('bar')
    False

If necessary, you can also implement a function that itself returns a processor function. This is handy when you'd like to do some up-front logic or preparation that doesn't need to occur during every single invocation of your processor. To do this, you'll need to mark the generating function with a decorator. For example:

::

    >>> @dc.processor
    ... def is_twentyfive():
    ...     twentyfive = 5 * 5
    ...     def is_twentyfive_processor(data):
    ...         if data != twentyfive:
    ...             raise dc.CheckerError('Not 25!')
    ...     return is_twentyfive_processor
    ... 
    >>> dc.Checker(is_twentyfive).is_valid(25)
    True
    >>> dc.Checker(is_twentyfive).is_valid(26)
    False


License
-------

The MIT License

Copyright (c)2013 Clover Wireless

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

