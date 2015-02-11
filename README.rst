====================
Supervisor SOA
====================

Adds a graph-based set abstraction to Supervisor_. Instead of issuing
commands to a process, or group, you can issue commands to a logical
set, which can be described as a DAG_.

Description
===========

Groups in Supervisor_ are exclusive sets. As a developer on an SOA
project comprised of many heterogeneous microservices_, the venn diagram of a
processes to a particular application feature varies
significantly. Adding mock services makes it more complicated to
manage a working set. This plugin adds a powerful expressiveness to
simplify the lives of mere mortals.

The plugin patches the default `status`, `start`, `restart`, and `stop`, to allow
you to operate on these high-level, non-exclusive sets transparently.


Installation
============

::

  pip install supervisor-soadev


Example
=======



In a `supervisord.conf`

::

  [ctlplugin:soadev]
  supervisor.ctl_factory = supervisorsoadev.controllerplugin:make_soadev_controllerplugin
  sets = cool warm rgb canvas
  graph:
    cool -> blue, green, purple, canvas
    warm -> red, yellow, orange, canvas
    rgb -> red, green, blue, canvas
    canvas -> infra:studio, infra:artist

  [program:blue]
  ...


Now, you can issue commands like:

::

  supervisor> status canvas blue
  infra:studio                        STOPPED   Not started
  infra:artist                        STOPPED   Not started
  blue                        STOPPED   Not started
  ...
  supervisor> start rgb purple
  ...
  supervisor> restart blue canvas
  ...

Don't worry about overlap; the full list will be resolved and
deduplicated before execution.

Configuration
=============

::

  [ctlplugin:soadev]
  supervisor.ctl_factory = supervisorsoadev.controllerplugin:make_soadev_controllerplugin
  sets = <set name> [, <set name>]*
  graph:
    <set or program> -> <set or program> [, <set or program>]*
    ...

`sets` is a comma delimited string of any string symbol.

`graph` is a newline delimited DAG_, containing any combination of
set names or program names. Programs in groups must be denoted as `<group>:<name>`.

Changelog
=========

 * 0.1.0

   * Released.


.. _Supervisor: http://supervisord.org/
.. _DAG: http://en.wikipedia.org/wiki/Directed_acyclic_graph
.. _microservices: http://martinfowler.com/articles/microservices.html
