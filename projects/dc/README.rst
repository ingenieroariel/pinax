::

  $Id$
  $Date$
  $Author$
  $Rev$
  $URL$

.. contents::

=================
dc-special README
=================

dc-special is an internal NASA Web 2.0 social networking application built off 
the three following primary toolsets:

 * Python
 * Django
 * Pinax

----

DIRECTORY STRUCTURE
=====================

projects/
    dc_special/          The dc-special suite of applications

The photologue app requires PIL which is not included in external_libs

There is some path manipulation in manage.py to get this all to work. You'll
need to do something similar in your wsgi or mod_python configuration.

Note that if you already have an external app or external lib on the path,
you don't need to use the one we provide.

----

Get dc-special running
=======================

From the directory containing this readme type::

    $ python manage.py syncdb
    $ python manage.py runserver

----

Running Tests
================
More to come

----

Customizations
================

 * http://pinaxproject.com/docs/trunk/customization.html
 
----

Responsible Parties
====================

 * |dg| (development)
 * |cs| (engineering and development)
 * |kc| (development, css, and organization)
 * |ck| (usability)
 * |jt| and the |pt| (Pinax itself and lots of help)
 * |jm| (graphic design)
 * |wk| (css)
 * |ct| (project management)
 
----
 
.. class:: gentime


This document was generated on |date| at |time|.

.. |cs| replace:: Chris Shenton
.. |ck| replace:: Colleen Kaiser
.. |ct| replace:: Corin Turner
.. |dg| replace:: Daniel Greenfeld
.. |gw| replace:: George Williams
.. |jr| replace:: James Saint-Rossy
.. |jt| replace:: James Tauber
.. |jen| replace:: Jenny Mottar
.. |jc| replace:: Jim Consalvi
.. |kc| replace:: Katie Cunningham
.. |wk| replace:: William Keeter
.. |mem| replace:: Meredith Mengel
.. |rn| replace:: Ruth Netting
.. |pt| replace:: Pinax Team
.. |ts| replace:: Tim Smith



.. |date| date::
.. |time| date:: %H:%M

