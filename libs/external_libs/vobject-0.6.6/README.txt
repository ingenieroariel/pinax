=======
VObject
=======

VObject simplifies the process of parsing and creating iCalendar and
vCard objects.

--------------
 Installation
--------------

To install vobject, run::

  python setup.py install

vobject requires the dateutil package, which can be installed via
easy_install or downloaded from http://labix.org/python-dateutil

---------------
 Running tests
---------------

Unit tests live in doctests throughout the source code, to run all tests, use::

  python tests/tests.py

-------
 Usage
-------

Creating iCalendar objects
..........................

vobject has a basic datastructure for working with iCalendar-like
syntaxes.  Additionally, it defines specialized behaviors for many of
the commonly used iCalendar objects.

To create an object that already has a behavior defined, run:

>>> import vobject
>>> cal = vobject.newFromBehavior('vcalendar')
>>> cal.behavior
<class 'vobject.icalendar.VCalendar2_0'>

Convenience functions exist to create iCalendar and vCard objects:

>>> cal = vobject.iCalendar()
>>> cal.behavior
<class 'vobject.icalendar.VCalendar2_0'>
>>> card = vobject.vCard()
>>> card.behavior
<class 'vobject.vcard.VCard3_0'>

Once you have an object, you can use the add method to create
children:

>>> cal.add('vevent')
<VEVENT| []>
>>> cal.vevent.add('summary').value = "This is a note"
>>> cal.prettyPrint()
 VCALENDAR
    VEVENT
       SUMMARY: This is a note

Note that summary is a little different from vevent, it's a
ContentLine, not a Component.  It can't have children, and it has a
special value attribute.

ContentLines can also have parameters.  They can be accessed with
regular attribute names with _param appended:

>>> cal.vevent.summary.x_random_param = 'Random parameter'
>>> cal.prettyPrint()
 VCALENDAR
    VEVENT
       SUMMARY: This is a note
       params for  SUMMARY:
          X-RANDOM ['Random parameter']

There are a few things to note about this example

  * The underscore in x_random is converted to a dash (dashes are
    legal in iCalendar, underscores legal in Python)
  * X-RANDOM's value is a list.

If you want to access the full list of parameters, not just the first,
use <paramname>_paramlist:

>>> cal.vevent.summary.x_random_paramlist
['Random parameter']
>>> cal.vevent.summary.x_random_paramlist.append('Other param')
>>> cal.vevent.summary
<SUMMARY{'X-RANDOM': ['Random parameter', 'Other param']}This is a note>

Similar to parameters, If you want to access more than just the first
child of a Component, you can access the full list of children of a
given name by appending _list to the attribute name:

>>> cal.add('vevent').add('summary').value = "Second VEVENT"
>>> for ev in cal.vevent_list:
...     print ev.summary.value
This is a note
Second VEVENT

The interaction between the del operator and the hiding of the
underlying list is a little tricky, del cal.vevent and del
cal.vevent_list both delete all vevent children:

>>> first_ev = cal.vevent
>>> del cal.vevent
>>> cal
<VCALENDAR| []>
>>> cal.vevent = first_ev

vobject understands Python's datetime module and tzinfo classes.

>>> import datetime
>>> utc = vobject.icalendar.utc
>>> start = cal.vevent.add('dtstart')
>>> start.value = datetime.datetime(2006, 2, 16, tzinfo = utc)
>>> first_ev.prettyPrint()
     VEVENT
        DTSTART: 2006-02-16 00:00:00+00:00
        SUMMARY: This is a note
        params for  SUMMARY:
           X-RANDOM ['Random parameter', 'Other param']

Components and ContentLines have serialize methods:

>>> cal.vevent.add('uid').value = 'Sample UID'
>>> icalstream = cal.serialize()
>>> print icalstream
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//PYVOBJECT//NONSGML Version 1//EN
BEGIN:VEVENT
UID:Sample UID
DTSTART:20060216T000000Z
SUMMARY;X-RANDOM=Random parameter,Other param:This is a note
END:VEVENT
END:VCALENDAR

Observe that serializing adds missing required lines like version and
prodid.  A random UID would be generated, too, if one didn't exist.

If dtstart's tzinfo had been something other than UTC, an appropriate
vtimezone would be created for it.


Parsing iCalendar objects
.........................

To parse one top level component from an existing iCalendar stream or
string, use the readOne function:

>>> parsedCal = vobject.readOne(icalstream)
>>> parsedCal.vevent.dtstart.value
datetime.datetime(2006, 2, 16, 0, 0, tzinfo=tzutc())

Similarly, readComponents is a generator yielding one top level
component at a time from a stream or string.

>>> vobject.readComponents(icalstream).next().vevent.dtstart.value
datetime.datetime(2006, 2, 16, 0, 0, tzinfo=tzutc())

More examples can be found in source code doctests.

vCards
......

Making vCards proceeds in much the same way. Note that the 'N' and 'FN'
attributes are required.

>>> j = vobject.vCard()
>>> j.add('n')
 <N{}    >
>>> j.n.value = vobject.vcard.Name( family='Harris', given='Jeffrey' )
>>> j.add('fn')
 <FN{}>
>>> j.fn.value ='Jeffrey Harris'
>>> j.add('email')
 <EMAIL{}>
>>> j.email.value = 'jeffrey@osafoundation.org'
>>> j.email.type_param = 'INTERNET'
>>> j.prettyPrint()
 VCARD
    EMAIL: jeffrey@osafoundation.org
    params for  EMAIL:
       TYPE ['INTERNET']
    FN: Jeffrey Harris
    N:  Jeffrey  Harris

serializing will add any required computable attributes (like 'VERSION')

>>> j.serialize()
'BEGIN:VCARD\r\nVERSION:3.0\r\nEMAIL;TYPE=INTERNET:jeffrey@osafoundation.org\r\nFN:Jeffrey Harris\r\nN:Harris;Jeffrey;;;\r\nEND:VCARD\r\n'
>>> j.prettyPrint()
 VCARD
    VERSION: 3.0
    EMAIL: jeffrey@osafoundation.org
    params for  EMAIL:
       TYPE ['INTERNET']
    FN: Jeffrey Harris
    N:  Jeffrey  Harris 

Parsing vCards
..............

>>> s = """
... BEGIN:VCARD
... VERSION:3.0
... EMAIL;TYPE=INTERNET:jeffrey@osafoundation.org
... FN:Jeffrey Harris
... N:Harris;Jeffrey;;;
... END:VCARD
... """
>>> v = vobject.readOne( s )
>>> v.prettyPrint()
 VCARD
    VERSION: 3.0
    EMAIL: jeffrey@osafoundation.org
    params for  EMAIL:
       TYPE [u'INTERNET']
    FN: Jeffrey Harris
    N:  Jeffrey  Harris
>>> v.n.value.family
u'Harris'