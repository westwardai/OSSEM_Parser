#!/usr/bin/env python3

import argparse, os, sys, json, yaml
from functools import reduce
import mistune
from mistune import Markdown
from bs4 import BeautifulSoup

__version__ = '0.0.1'
__author__ = 'Zack Payton <zack.payton@westward.ai>'

VERBOSE = False
#VERBOSE = True

def detect_language(code):
  ''' this simple function does its best
      to detect the event output...
      generally xml or json '''
  code = code.strip().rstrip()
  if code.startswith('<'):
    return 'xml'
  if code.startswith('{'):
    return 'json'
  else:
    return 'unknown'
  

class DictRenderer(mistune.Renderer):
  def __init__(self, renderer=None, inline=None, block=None, **kwargs):
    super().__init__(**kwargs)
    self.object_data = {}
    self.fields_key = None
    self.table_headers_done = None
    self.table_headers = []
    self.current_table_entry = {}
    self.current_table_entry_index = 0
  def lower_under_joined(self, text):
    return '_'.join(list(map(lambda w: w.lower(), text.split(' ')))) # this will convert something like 'Blase Blah' to 'blase_blah'
  def get_python_dict(self):
    return self.object_data
  def block_code(self, code, lang=None):
    if VERBOSE:
      print("block_code: {} lang: {}".format(code, lang))
    return code
  def block_quote(self, text):
    if VERBOSE:
      print("block_quote: {}".format(text))
    return text
  def block_html(self, html):
    raise NotImplementedError("block_html has not been implemented")
  def hrule(self):
    if VERBOSE:
      print("hrule")
    return ''
  def list(self, body, ordered=True):
    if VERBOSE:
      print("body: {} ordered: {}".format(body, ordered))
    return body
  def list_item(self, text):
    if VERBOSE:
      print("list_item: {}".format(text))
    return text
  def paragraph(self, text):
    if VERBOSE:
      print("paragraph: {}".format(text))
    return text
  def table(self, header, body):
    if VERBOSE:
      print("table header: {} table body: {}".format(header, body))
    return body
  def double_emphasis(self, text):
    if VERBOSE:
      print("double_emphasis: {}".format(text))
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
    return text
  def autolink(self, link, is_email=False):
    if VERBOSE:
      print("auto_link: {} is_email: {}".format(link, is_email))
    return link
  def link(self, link, title, text):
    if VERBOSE:
      print("link: {} title: {} text: {}".format(link, title, text))
    return link
  def image(self, src, title, text):
    if VERBOSE:
      print("image src: {} title: {} text: {}".format(src, title, text))
    return src
  def inline_html(self, html):
    if VERBOSE:
      print("inline_html: {}".format(html)) 
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
  def header(self, text, level, raw=None):
    raise NotImplementedError("header has not been implemented")
  def table_row(self, content):
    raise NotImplementedError("table_row has not been implemented")
  def table_cell(self, content, **flags):
    raise NotImplementedError("table_cell has not been implemented")
  def text(self, text):
    raise NotImplementedError("text has not been implemented")

  def table_row(self, content):
    if VERBOSE:
      print("table_row: {}".format(content))
    self.table_headers_done = True #table_row gets called by mistune at the end of the row
    self.entry_length = len(self.table_headers)
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
          try:
            self.current_table_entry['sample_value'] = int(self.current_table_entry['sample_value'], 0)
          except Exception as e:
            self.current_table_entry['sample_value'] = None
        del self.current_table_entry['standard_name']
        self.object_data[self.fields_key][standard_name] = self.current_table_entry
        self.current_table_entry = {}
        self.current_table_entry_index = 0
    return content
 

class CIMDictRenderer(DictRenderer):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.description_next = False
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
  def text(self, text):
    if self.description_next == True:
      self.object_data['description'] = text
      self.description_next = False
    if VERBOSE:
      print("text: {}".format(text))
    return text

class DataDictionaryDictRenderer(DictRenderer):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.meta_complete = False
    self.got_meta_date = False
    self.seen_title = False
    self.description_next = False
    self.description_done = False
    self.evi_next = False
  def text(self, text):
    if VERBOSE:
      print("text: '{}'".format(text))
    if not self.meta_complete:
      if ":" in text:
        meta = {}
        for e in text.split('\n'):
          k,v = e.split(':')
          k = k.replace('.', '_') # dots sometimes have special implications like in Elastic Search so we use _ instead
          meta[k] = v.rstrip().strip()
        self.meta_complete = True
        self.object_data['meta'] = meta
        return text
      else:
        # we don't appear to have metadata
        self.meta_complete = True
    if not self.got_meta_date and text.startswith('date:'):
      k,v = text.split(":")
      v = v.rstrip().strip()
      self.object_data['meta']['date'] = v
      self.got_meta_date = True
      return text

    if self.description_next:
      description = text
      self.object_data['description'] = {'text': description}

      self.description_next = False
      return text

    if self.evi_next:
      evi = text
      self.evi_next = False
      return text

    return text
  def header(self, text, level, raw=None):
    if VERBOSE:
      print("header: {} level: {}".format(text, level))
    if level == 1 and not self.seen_title:
      self.object_data['title'] = text
      self.seen_title = True
      return text
    if level == 2 and text.startswith('Desc'):
      self.description_next = True
      return text
    if level == 2 and text.startswith("Event"):
      self.evi_next = True
      self.description_done = True
    if level == 2 and text.startswith("Data"): # not in self.object_data::
      text = self.lower_under_joined(text)
      self.fields_key = self.lower_under_joined(text)
      self.object_data[self.fields_key] = {}
    return text
  def link(self, link, title, text):
    if VERBOSE:
      print("link: {} title: {} text: {}".format(link, title, text))
    if not self.description_done:
      if  'links' not in self.object_data['description']:
        self.object_data['description']['links'] = []
      self.object_data['description']['links'].append({'link': link, 'text': text})
  def inline_html(self, html):
    if self.evi_next:
      soup = BeautifulSoup(html, 'html.parser')
      img = soup.find('img')
      self.object_data['event_log_illustration'] = {
        'image': {
          'link': img['src'],
          'alt': img['alt'],
          'width': int(img['width']),
          'height': int(img['height'])
        }
      }
      self.evi_next = False
      return html
  def block_code(self, code, lang=None):
    if self.evi_next:
      language = detect_language(code)
      self.object_data['event_data' ] = { 'type': language, 'data': code }

    return code

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
  def parse_data_dictionaries(self, ossem_dir):
    dd_dir = os.path.join(ossem_dir, 'data_dictionaries')
    dd = {'os': {} }
    oses = [f for f in os.listdir(dd_dir) if os.path.isdir(os.path.join(dd_dir, f))]
    for o in oses:
      dd[o] = {}
      for data_source in os.listdir(os.path.join(dd_dir,o)):
        data_source_dir = os.path.join(dd_dir, o, data_source)
        #print("data_source_dir: {}".format(data_source_dir))
        dd[o][data_source] = {}
        start = data_source_dir.rfind(os.sep) + 1
        print("walking: {}".format(data_source_dir))
        for root, subdirs, files in os.walk(data_source_dir):
          folders = root[start:].split(os.sep)
          subdir = dict.fromkeys(files)
          parent = reduce(dict.get, folders[:1], dd)
          parent[folders[-1]] = subdir
          #print("root: {} subdirs: {} files: {}".format(root, subdirs, files))
    print("dd: {}".format(dd))
    return dd

  def parse_ossem(self, ossem_dir):
    ossem = {} # data stucture to maintain representation of OSSEM
    ossem_dir = ossem_dir.rstrip(os.sep)
    start = ossem_dir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(ossem_dir):
      dirs[:] = [d for d in dirs if not d.startswith('.')]
      files[:] = [f for f in files if not f.startswith('.')]
      folders = path[start:].split(os.sep)
      key_names = []
      for f in files:
        k = f
        if k.lower().endswith('.md'):
          k = k[:-3]
        if k.lower().startswith('event-'):
          k = k[6:]
        key_names.append({'file': f, 'key': k})
      subdir = dict.fromkeys([k['key'] for k in key_names])

      if 'data_dictionaries' in path:
        for f in files:
          if not f.lower() == 'readme.md' and f.lower().endswith('.md'):
            p = os.path.join(path, f)
            for k in key_names:
              if k['file'] == f:
                subdir[k['key']] = self.parse_dd_md(self.read_file(p))

      parent = reduce(dict.get, folders[:-1], ossem)
      parent[folders[-1]] = subdir

    return ossem

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='parse markdown file')
  parser.add_argument('--ossem', type=str, help='base directory containing the OSSEM project')
  parser.add_argument('--shell', type=str, help='open an interactive shell to browse ossem data')
  parser.add_argument('--output', type=str, help='output format (json, yaml, xml, or python supported)', default='yaml')
  args = parser.parse_args()

  valid_output = ['json', 'yaml', 'xml', 'python'] # should we add markdown as output?
  output_format = args.output.lower()
  if not output_format in valid_output:
    print("not a valid output format, must me one of {}".format(valid_output))
    sys.exit()

  if args.ossem:
    parser = OSSEMParser()
    ossem = parser.parse_ossem(args.ossem)
    if output_format == 'json':
      print(json.dumps(ossem))
    elif output_format == 'yaml':
      print(yaml.dump(ossem, default_flow_style=False))
    elif output_format == 'xml':
      from dicttoxml import dicttoxml # we conditionally import this because it's not in python core
      print(dicttoxml(ossem))
    elif output_format == 'python':
      print("{}".format(ossem))
  else:
    import unittest
    from tests.test_cim import TestOSSEMCIM
    from tests.test_data_dictionaries import TestOSSEMDataDictionaries
    unittest.main()
