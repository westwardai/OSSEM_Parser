#!/usr/bin/env python3

import argparse, os, sys
from functools import reduce
import mistune

__version__ = '0.0.1'
__author__ = 'Zack Payton <zack.payton@westward.ai>'


class DictRenderer(mistune.Renderer):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.object_data = {}
  #def placeholder(self):
  #  return
    #raise NotImplementedError("placeholder has not been implemented")
  def block_code(self, code, lang=None):
    print("block_code: {} lang: {}".format(code, lang))
    #raise NotImplementedError("block_code has not been implemented")
    return code
  def block_quote(self, text):
    print("block_quote: {}".format(text))
    #raise NotImplementedError("block_quote has not been implemented")
    return text
  def block_html(self, html):
    raise NotImplementedError("block_html has not been implemented")
  def header(self, text, level, raw=None):
    print("header: {} level: {}".format(text, level))
    if not 'header' in self.object_data:
      self.object_data['headers'] = []
    self.object_data['headers'].append({'text': text, 'level': level})
    return text
  def hrule(self):
    print("hrule")
    #raise NotImplementedError("hrule has not been implemented")
    return ''
  def list(self, body, ordered=True):
    print("body: {} ordered: {}".format(body, ordered))
    #raise NotImplementedError("list has not been implemented")
    return body
  def list_item(self, text):
    print("list_item: {}".format(text))
    #raise NotImplementedError("list_item has not been implemented")
    return text
  def paragraph(self, text):
    print("paragraph: {}".format(text))
    #raise NotImplementedError("paragraph has not been implemented")
    return text
  def table(self, header, body):
    print("table header: {} table body: {}".format(header, body))
    #raise NotImplementedError("table has not been implemented")
    return body
  def table_row(self, content):
    print("table_row: {}".format(content))
    #raise NotImplementedError("table_row has not been implemented")
    return content
  def table_cell(self, content, **flags):
    print("table_cell: {}".format(content))
    if not "table_cells" in self.object_data:
      self.object_data['table_cells'] = []
      self.object_data['table_cells'].append(content)
    return content
  def double_emphasis(self, text):
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
  def text(self, text):
    print("text: {}".format(text))
    return text
    #raise NotImplementedError("text has not been implemented")
  def escape(self, text):
    print("escape: {}".format(text))
    #raise NotImplementedError("escape has not been implemented")
    return text
  def autolink(self, link, is_email=False):
    print("link: {} is_email: {}".format(link, is_email))
    #raise NotImplementedError("autolink has not been implemented")
    return link
  def link(self, link, title, text):
    print("link: {} title: {} text: {}".format(link, title, text))
    #raise NotImplementedError("link has not been implemented")
    return link
  def image(self, src, title, text):
    print("image src: {} title: {} text: {}".format(src, title, text))
    #raise NotImplementedError("image has not been implemented")
    return src
  def inline_html(self, html):
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



class OSSEMParser(object):
  def parse_md_file(self, filename):
    ''' parse a markdown file '''
    try:
      with open(filename) as file:
        file_content = file.read()
        self.parse_md(file_content)
    except FileNotFoundError as e:
        print("File not found: {0}".format(filename))

  def parse_md(self, markdown):
    dict_renderer = DictRenderer()
    print(mistune.markdown(markdown, renderer=dict_renderer))

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
    from tests.test_cim import TestOSSEMCIM
    unittest.main()
