# naming-variation-generator

## What's this

I tend to be rather opinionated about naming.  It matters, and its hard.  One of the most useful things
I've always ended up doing is breaking down real examples for comparison purposes when talking about
the options available.

I used to do it with spreadsheets, then I started writing scripts, then I'd realized I'd written 1 too many
ad-hoc scripts to do it.

So this script is intended to facilitate that.

# Usage

```
./nvg.py [<prefix>] [<template file>] [<context dir>]
```

## Arguments
`prefix`
  * To ensure a single static prefix, provide this argument _and_ reference `{prefix}` in your template
  * Must be populated (can be any string) if passing the other arguments. If unreferenced, will be ignored.
  * Defaults to _Empty_
`template file`
  * Path to a file that contains a separate Python format string per line
  * Each referenced key should match a file name in the `context dir`
  * Defaults to `./templates`
`context_dir`
  * Path to a directory that contains a separate file for each template key (aside from `prefix`)
  * Defaults to `./contexts`

## Examples

### Most basic usage with example files in this repository

```
./nvg.py
```

### Complex usage with prefix and file structures

This creates a list of access policy groups, using multiple template options

```
./nvg.py access complex/templates/access complex/full
```

# File structures and content

* All files should be treated as 1 entry per line
* In template files, the template key references should match the names of context files
* Only the first column, separated by a single whitespace character, is processed from the files
  * This allows you to add comments and explanations to the files for your own reference
  * See the files under complex/contexts/abbrev for examples