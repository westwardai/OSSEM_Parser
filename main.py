#!/usr/bin/env python3

import argparse, os, sys
from functools import reduce
import mistune
from mistune import Markdown

__version__ = '0.0.1'
__author__ = 'Zack Payton <zack.payton@westward.ai>'

VERBOSE = True

class DictRenderer(mistune.Renderer):
  def __init__(self, renderer=None, inline=None, block=None, **kwargs):
    super().__init__(**kwargs)
    self.object_data = {}
  def lower_under_joined(self, text):
    return '_'.join(list(map(lambda w: w.lower(), text.split(' ')))) # this will convert something like 'Blase Blah' to 'blase_blah'
  #def placeholder(self):
  #  return {}
    #raise NotImplementedError("placeholder has not been implemented")
  def get_python_dict(self):
    return self.object_data
  def block_code(self, code, lang=None):
    if VERBOSE:
      print("block_code: {} lang: {}".format(code, lang))
    #raise NotImplementedError("block_code has not been implemented")
    return code
  def block_quote(self, text):
    if VERBOSE:
      print("block_quote: {}".format(text))
    #raise NotImplementedError("block_quote has not been implemented")
    return text
  def block_html(self, html):
    raise NotImplementedError("block_html has not been implemented")
  def hrule(self):
    if VERBOSE:
      print("hrule")
    #raise NotImplementedError("hrule has not been implemented")
    return ''
  def list(self, body, ordered=True):
    if VERBOSE:
      print("body: {} ordered: {}".format(body, ordered))
    #raise NotImplementedError("list has not been implemented")
    return body
  def list_item(self, text):
    if VERBOSE:
      print("list_item: {}".format(text))
    #raise NotImplementedError("list_item has not been implemented")
    return text
  def paragraph(self, text):
    if VERBOSE:
      print("paragraph: {}".format(text))
    #raise NotImplementedError("paragraph has not been implemented")
    return text
  def table(self, header, body):
    if VERBOSE:
      print("table header: {} table body: {}".format(header, body))
    #raise NotImplementedError("table has not been implemented")
    return body
  def double_emphasis(self, text):
    if VERBOSE:
      print("double_emphasis: {}".format(text))
    #raise NotImplementedError("double_emphasis has not been implemented")
    return text
  def emphasis(self, text):
    raise NotImplementedError("emphasis has not been implemented")
  def codespan(self, text):
    raise NotImplementedError("codespan has not been implemented")
  def linebreak(self):
    raise NotImplementedError("linebreak has not been implemented")
  def strikethrough(self, text):
    raise NotImplementedError("strikethrough has not been implemented")
  def escape(self, text):
    if VERBOSE:
      print("escape: {}".format(text))
    #raise NotImplementedError("escape has not been implemented")
    return text
  def autolink(self, link, is_email=False):
    if VERBOSE:
      print("link: {} is_email: {}".format(link, is_email))
    #raise NotImplementedError("autolink has not been implemented")
    return link
  def link(self, link, title, text):
    if VERBOSE:
      print("link: {} title: {} text: {}".format(link, title, text))
    #raise NotImplementedError("link has not been implemented")
    return link
  def image(self, src, title, text):
    if VERBOSE:
      print("image src: {} title: {} text: {}".format(src, title, text))
    #raise NotImplementedError("image has not been implemented")
    return src
  def inline_html(self, html):
    if VERBOSE:
      print("inline_html: {}".format(html)) 
    #raise NotImplementedError("inline_html has not been implemented")
    return html
  def newline(self):
    raise NotImplementedError("newline has not been implemented")
  def footnote_ref(self, key, index):
    raise NotImplementedError("footnote_ref has not been implemented")
  def footnote_item(self, key, text):
    raise NotImplementedError("footnote_item has not been implemented")
  def footnotes(self, text):
    raise NotImplementedError("footnotes has not been implemented")
  def header(self, text, level, raw=None):
    raise NotImplementedError("header has not been implemented")
  def table_row(self, content):
    raise NotImplementedError("table_row has not been implemented")
  def table_cell(self, content, **flags):
    raise NotImplementedError("table_cell has not been implemented")
  def header(self, text, level, raw=None):
    raise NotImplementedError("header has not been implemented")
  def table_row(self, content):
    raise NotImplementedError("table_row has not been implemented")
  def table_cell(self, content, **flags):
    raise NotImplementedError("table_cell has not been implemented")
  def text(self, text):
    raise NotImplementedError("text has not been implemented")



class CIMDictRenderer(DictRenderer):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.description_next = False
    self.fields_key = None
    self.table_headers_done = None
    self.table_headers = []
    self.current_table_entry = {}
    self.current_table_entry_index = 0
  def header(self, text, level, raw=None):
    if VERBOSE:
      print("header: {} level: {}".format(text, level))
    if level == 1 and 'name' not in self.object_data:
      self.object_data['name'] = text
      self.description_next = True
    if level == 2 and text not in self.object_data:
      text = self.lower_under_joined(text)
      self.fields_key = self.lower_under_joined(text)
      self.object_data[self.fields_key] = {}
    return text
  def table_row(self, content):
    if VERBOSE:
      print("table_row: {}".format(content))
    self.table_headers_done = True #table_row gets called by mistune at the end of the row
    self.entry_length = len(self.table_headers)
    #raise NotImplementedError("table_row has not been implemented")
    return content
  def table_cell(self, content, **flags):
    if VERBOSE:
      print("table_cell: {}".format(content))
    if not self.table_headers_done:
      self.table_headers.append(self.lower_under_joined(content))
    else:
      self.current_table_entry[self.table_headers[self.current_table_entry_index]] = content
      if VERBOSE:
        print("current_table_entry: {} current_table_entry_index: {}".format(self.current_table_entry, self.current_table_entry_index))
      self.current_table_entry_index += 1
      if self.current_table_entry_index >= self.entry_length:
        standard_name = self.current_table_entry['standard_name']
        if self.current_table_entry['type'] == 'integer':
          self.current_table_entry['sample_value'] = int(self.current_table_entry['sample_value'])
        del self.current_table_entry['standard_name']
        self.object_data[self.fields_key][standard_name] = self.current_table_entry
        self.current_table_entry = {}
        self.current_table_entry_index = 0
    return content
  def text(self, text):
    if self.description_next == True:
      self.object_data['description'] = text
      self.description_next = False
    if VERBOSE:
      print("text: {}".format(text))
    return text
    #raise NotImplementedError("text has not been implemented")

class DataDictionaryDictRenderer(DictRenderer):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
  def text(self, text):
    if VERBOSE:
      print("text: {}".format(text))
    return text
  def header(self, text, level, raw=None):
    if VERBOSE:
      print("header: {} level: {}".format(text, level))
    return text
  def table_cell(self, content, **flags):
    if VERBOSE:
      print("table_cell: {}")
    return content
  def table_row(self, content):
    if VERBOSE:
      print("table_row: {}".format(content))
    return content

class OSSEMParser(object):
  def read_file(self, filename):
    ''' parse a markdown file '''
    try:
      with open(filename) as file:
        file_content = file.read()
        return file_content
    except FileNotFoundError as e:
        print("File not found: {0}".format(filename))

  def parse_cim_md(self, markdown):
    dict_renderer = CIMDictRenderer()
    md = Markdown(escape=True, renderer=dict_renderer)
    md.parse(markdown)
    d = md.renderer.get_python_dict()
    return d
  def parse_dd_md(self, markdown):
    dict_renderer = DataDictionaryDictRenderer()
    md = Markdown(escape=True, renderer=dict_renderer)
    md.parse(markdown)
    d = md.renderer.get_python_dict()
    return d

  def parse_ossem(self, ossem_dir):
    d = {} # data stucture to maintain representation of OSSEM
    start = ossem_dir.rfind(os.sep) + 1
    for root, subdirs, files in os.walk(ossem_dir):
      subdirs[:] = [d for d in subdirs if not d.startswith('.')] # skip hidden directories
      files[:] = [f for f in files if not f.startswith('.') and not f.endswith('png')]
      folders = root[start:].split(os.sep)  # http://code.activestate.com/recipes/577879-create-a-nested-dictionary-from-oswalk/
      subdir = dict.fromkeys(files)         # this code is discusting and needs to be refactored
      parent = reduce(dict.get, folders[:-1], d) # but it works :(
      parent[folders[-1]] = subdir
      for f in files:
        full_path = os.path.join(root, f)
        if full_path.endswith('OSSEM/README.md'): continue # skip OSSEM/README.md
        print("parsing {}".format(full_path))
        self.parse_md_file(full_path)
    from pprint import pprint
    pprint(d)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='parse markdown file')
  parser.add_argument('--ossem', type=str, help='base directory containing the OSSEM project')
  args = parser.parse_args()

  if args.ossem:
    parser = OSSEMParser()
    ossem = parser.parse_ossem(args.ossem)
  else:
    import unittest
    #from tests.test_cim import TestOSSEMCIM
    from tests.test_data_dictionaries import TestOSSEMDataDictionaries
    unittest.main()
