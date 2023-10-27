#!/usr/bin/env python3

import itertools
import os
import sys
from string import Formatter

DEFAULT_DIR = './contexts'
DEFAULT_TEMPLATES_FILE = './templates'
USAGE = f'USAGE: {sys.argv[0]} <prefix> [template file] [contexts directory]'

def debug(msg, enabled=bool(os.environ.get('NVG_DEBUG', False))):
  if enabled:
    os.sys.stderr.write(f'DEBUG: {msg}\n')

def error(msg, exit_code):
  os.sys.stderr.write(f'ERROR: {msg}\n')
  sys.exit(exit_code)

def get_keys_from_templates(templates):
  keys = []
  for template in templates:
    keys.extend([f for _, f, _, _ in Formatter().parse(template) if f and f != 'prefix'])
  return(set(keys))

def get_templates(template_file):
  try:
    templates = read_data(templates_file)
  except FileNotFoundError:
    error(f'File not found {template_file}', 3)
  keys = get_keys_from_templates(templates)
  return(templates, keys)

def format_template(template, **kwargs):
  debug(template)
  debug(kwargs)
  return(template.format(**kwargs))

def read_data(source_file):
  with open(source_file) as source:
    # We only grab the first item so that comments can exist
    # in the files
    details = [x.strip().split(' ')[0] for x in source.readlines() if x.strip()]
  details.sort()
  debug(f'Found in {source_file}')
  for detail in details:
    debug(f'\t_{detail}_')
  return details

def add_keys_to_contexts(context_list, new_context, new_values):
    if not context_list:
        context_list = [{'blank': None}]
    debug(context_list)
    for context in context_list:
        if new_context in context:
            continue
        for value in new_values:
            new = context.copy()
            new[new_context] = value
            new.pop('blank', None)
            debug(f'Yielding context {new}')
            yield(new)

def generate_context_matrix(contexts, existing=[]):
    full_list = existing
    for key, values in contexts.items():
       full_list = [context for context in add_keys_to_contexts(full_list, key, values)]
    return(full_list)

def gather_contexts(context_dir, keys, prefix=''):
  contexts = {}
  for key in keys:
    if key == 'prefix':
      contexts[key] = [prefix]
      continue
    context_file = os.path.join(context_dir, key)
    try:
      contexts[key] = read_data(context_file)
    except FileNotFoundError:
      error(f'Context file {key} not found in {context_dir}', 10)
  if contexts.keys() == ['prefix']:
    error(f'Context directory {context_dir} has no context files', 11)
  return generate_context_matrix(contexts)

def process_template(template, contexts):
  for context in contexts:
    yield(format_template(template, **context))

def print_all_templates(templates, contexts):
  for template in templates:
    print(f'Template base: {template}')
    for output in process_template(template, contexts):
      print(f'\t{output}')

if __name__ == '__main__':
  try:
    prefix = sys.argv[1]
  except IndexError:
    prefix = ''
  try:
    templates_file = sys.argv[2]
  except IndexError:
    templates_file = DEFAULT_TEMPLATES_FILE
  if os.path.isdir(templates_file):
    error(f'{templates_file} is a directory', 2)
  try:
    context_dir = sys.argv[3]
  except IndexError:
    context_dir = DEFAULT_DIR

  (templates, keys) = get_templates(templates_file)
  keys = list(keys)
  keys.append('prefix')
  keys = set(keys)
  print_all_templates(templates, gather_contexts(context_dir, keys, prefix))
