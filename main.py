#!/usr/bin/env python3

import argparse, os
import mistune

__version__ = '0.0.1'
__author__ = 'Zack Payton <zack.payton@westward.ai>'


class YAMLRenderer(mistune.Renderer):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
  #def placeholder(self):
  #  return
    #raise NotImplementedError("placeholder has not been implemented")
  def block_code(self, code, lang=None):
    raise NotImplementedError("block_code has not been implemented")
  def block_quote(self, text):
    raise NotImplementedError("block_quote has not been implemented")
  def block_html(self, html):
    raise NotImplementedError("block_html has not been implemented")
  def header(self, text, level, raw=None):
    raise NotImplementedError("header has not been implemented")
  def hrule(self):
    raise NotImplementedError("hrule has not been implemented")
  def list(self, body, ordered=True):
    raise NotImplementedError("list has not been implemented")
  def list_item(self, text):
    raise NotImplementedError("list_item has not been implemented")
  def paragraph(self, text):
    raise NotImplementedError("paragraph has not been implemented")
  def table(self, header, body):
    raise NotImplementedError("table has not been implemented")
  def table_row(self, content):
    raise NotImplementedError("table_row has not been implemented")
  def table_cell(self, content, **flags):
    raise NotImplementedError("table_cell has not been implemented")
  def double_emphasis(self, text):
    raise NotImplementedError("double_emphasis has not been implemented")
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
    raise NotImplementedError("escape has not been implemented")
  def autolink(self, link, is_email=False):
    raise NotImplementedError("autolink has not been implemented")
  def link(self, link, title, text):
    raise NotImplementedError("link has not been implemented")
  def image(self, src, title, text):
    raise NotImplementedError("image has not been implemented")
  def inline_html(self, html):
    raise NotImplementedError("inline_html has not been implemented")
  def newline(self):
    raise NotImplementedError("newline has not been implemented")
  def footnote_ref(self, key, index):
    raise NotImplementedError("footnote_ref has not been implemented")
  def footnote_item(self, key, text):
    raise NotImplementedError("footnote_item has not been implemented")
  def footnotes(self, text):
    raise NotImplementedError("footnotes has not been implemented")




def parse_md_file(filename):
  ''' parse a markdown file '''
  try:
    with open(filename) as file:
      file_content = file.read()
      parse_md(file_content)
  except FileNotFoundError as e:
      print("File not found: {0}".format(filename))

def parse_md(markdown):
  yaml_renderer = YAMLRenderer()
  print(mistune.markdown(markdown, renderer=yaml_renderer))

def parse_ossem(ossem_dir):
  for root, subdirs, files in os.walk(ossem_dir):
    subdirs[:] = [d for d in subdirs if not d.startswith('.')] # skip hidden directories
    files =  [f for f in files if f.lower().endswith('.md')] # only process markdown files
    for f in files:
      full_file_path = os.path.join(root, f)
      if full_file_path.endswith(os.path.join('OSSEM', 'README.md')): continue # skip the main OSSEM/README.md for now
      print("parsing: {}".format(full_file_path))
      ds = parse_md_file(full_file_path)
      print("ds: {}".format(ds))
      import sys
      sys.exit()


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='parse markdown file')
  parser.add_argument('--ossem', type=str, help='base directory containing the OSSEM project')
  args = parser.parse_args()
  print(args)

  if args.ossem:
    parse_ossem(args.ossem)
