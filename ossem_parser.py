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
    """ this simple function does its best
        to detect the event output...
        generally xml or json """
    code = code.strip().rstrip()
    if code.startswith('<'):
        return 'xml'
    if code.startswith('{'):
        return 'json'
    else:
        return 'unknown'

def convert_unicode_quotes_dashes(text):
    """ this function replaces unicode characters with their ascii counterparts """
    return text.replace(u'\u2019', "'").replace(u'\u2013', '-').replace(u'\u2014', '-').replace(u'\u201C', '"')\
            .replace(u'\u201D', '"').replace(u'\u200B', '').replace(u'\u2026', '...')

def lower_under_joined(text):
    """ silly function to convert dictionary keys to a more 'pythonic' representation"""
    return '_'.join(list(map(lambda w: w.lower(), text.split(' ')))) # this will convert something like 'Blase Blah' to 'blase_blah'

class DictRenderer(mistune.Renderer):
    """ base class that renders a python dictionary
        from markdown using mistune """
    def __init__(self, renderer=None, inline=None, block=None, **kwargs):
        super().__init__(**kwargs)
        self.object_data = {}
        self.fields_key = None
        self.table_headers_done = None
        self.table_headers = []
        self.current_table_entry = {}
        self.current_table_entry_index = 0
        self.table_count = 0
    def get_python_dict(self):
        """ this method can be called to extract the dictionary at the end of the parsing phase """
        return self.object_data
    def block_code(self, code, lang=None):
        """ handler that gets called when the parser hits markdown block code """
        if VERBOSE:
            print("block_code: {} lang: {}".format(code, lang))
        return code
    def block_quote(self, text):
        """ handler that gets called when the parser hits markdown block quote """
        if VERBOSE:
            print("block_quote: {}".format(text))
        return text
    def block_html(self, html):
        """ handler that gets called when the parser hits markdown block html """
        raise NotImplementedError("block_html has not been implemented")
    def hrule(self):
        """ handler that gets called when the parser hits hrule element in markdown """
        if VERBOSE:
            print("hrule")
        return ''
    def list(self, body, ordered=True):
        """ handler that gets called when it hits a markdown list """
        if VERBOSE:
            print("body: {} ordered: {}".format(body, ordered))
        return body
    def list_item(self, text):
        """ handler that gets called when mistune hits an item in a markdown list """
        if VERBOSE:
            print("list_item: {}".format(text))
        return text
    def paragraph(self, text):
        """ handler that gets called when mistune hits a paragraph in markdown """
        if VERBOSE:
            print("paragraph: {}".format(text))
        return text
    def table(self, header, body):
        """ handler that gets called when mistune hits a table in markdown.
            Note this actually gets called when the table is finished being processed """
        if VERBOSE:
            print("table header: {} table body: {}".format(header, body))
        self.table_headers_done = False
        self.table_headers = []
        self.current_table_index = 0
        if self.table_count == 0:
          self.current_table_entry = {}
        else:
          self.current_table_entry = []
        self.table_count += 1
        return body
    def double_emphasis(self, text):
        """ handler that gets called when mistune his double_emphasis in markdown """
        if VERBOSE:
            print("double_emphasis: {}".format(text))
        return text
    def emphasis(self, text):
        """ handler that gets called when mistune hits emphasis markdown element """
        raise NotImplementedError("emphasis has not been implemented")
    def codespan(self, text):
        """ handler called when mistune hits codespan """
        raise NotImplementedError("codespan has not been implemented")
    def linebreak(self):
        """ handler called when mistune hits linebreak markdown """
        raise NotImplementedError("linebreak has not been implemented")
    def strikethrough(self, text):
        """ handler called when mistune hits strikethrough element """
        raise NotImplementedError("strikethrough has not been implemented")
    def escape(self, text):
        """ handler called when mistune hits escape element """
        if VERBOSE:
            print("escape: {}".format(text))
        return text
    def autolink(self, link, is_email=False):
        """ handler called when mistune hits autolink markdown """
        if VERBOSE:
            print("auto_link: {} is_email: {}".format(link, is_email))
        return link
    def link(self, link, title, text):
        """ handler called when mistune hits link markdown element """
        if VERBOSE:
            print("link: {} title: {} text: {}".format(link, title, text))
        return link
    def image(self, src, title, text):
        """ handler called when mistune hits image markdown element """
        if VERBOSE:
            print("image src: {} title: {} text: {}".format(src, title, text))
        return src
    def inline_html(self, html):
        """ handler called when mistune hits inline_html markdown """
        if VERBOSE:
            print("inline_html: {}".format(html))
        return html
    def newline(self):
        """ handler called when mistune hits a newline """
        raise NotImplementedError("newline has not been implemented")
    def footnote_ref(self, key, index):
        """ handler called when mistune hits a footnote_ref markdown element """
        raise NotImplementedError("footnote_ref has not been implemented")
    def footnote_item(self, key, text):
        """ handler called when mistune hits footnote_item markdown element """
        raise NotImplementedError("footnote_item has not been implemented")
    def footnotes(self, text):
        """ handler called when mistune hits footnotes markdown element """
        raise NotImplementedError("footnotes has not been implemented")
    def header(self, text, level, raw=None):
        """ handler called when mistune hits header element in markdown """
        raise NotImplementedError("header has not been implemented")
    def header(self, text, level, raw=None):
        """ handler called when header element parsed by mistune """
        raise NotImplementedError("header has not been implemented")
    def text(self, text):
        """ handler called when text is reached during mistune parsing run """
        raise NotImplementedError("text has not been implemented")
    def table_row(self, content):
        """ handler called when table_row is parsed by mistune """
        if VERBOSE:
            print("table_row: {}".format(content))
        self.table_headers_done = True #table_row gets called by mistune at the end of the row
        self.entry_length = len(self.table_headers)
        self.first_table_column_name = self.table_headers[0]
        return content
    def table_cell(self, content, **flags):
        """ handler that gets called when mistune hits a table cell in markdown """
        if VERBOSE:
            print("table_cell: {}".format(content))
        if not self.table_headers_done:
            self.table_headers.append(lower_under_joined(content))
        else:
            content = convert_unicode_quotes_dashes(content)
            if self.table_count > 0 and ('http' in content or '..' in content):
              self.current_table_entry[self.table_headers[self.current_table_entry_index]] = self.current_link
            else:
              self.current_table_entry[self.table_headers[self.current_table_entry_index]] = convert_unicode_quotes_dashes(content)
            if VERBOSE:
                print("current_table_entry: {} current_table_entry_index: {}".format(self.current_table_entry, self.current_table_entry_index))
            self.current_table_entry_index += 1
            if self.current_table_entry_index >= self.entry_length:
                if self.table_count == 0:
                    first_table_column_value = self.current_table_entry[self.table_headers[0]]
                    if 'type' in self.current_table_entry and self.current_table_entry['type'].lower() == 'integer':
                        try:
                            self.current_table_entry['sample_value'] = int(self.current_table_entry['sample_value'], 0)
                        except Exception as e:
                            self.current_table_entry['sample_value'] = None
                    del self.current_table_entry[self.first_table_column_name]
                    self.object_data[self.fields_key][first_table_column_value] = self.current_table_entry
                else:
                    self.object_data[self.fields_key].append(self.current_table_entry)
                self.current_table_entry = {}
                self.current_table_entry_index = 0
        return content

class CIMDictRenderer(DictRenderer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.description_next = False
        self.current_link = None
    def header(self, text, level, raw=None):
        if VERBOSE:
            print("header: {} level: {}".format(text, level))
        if level == 1 and 'name' not in self.object_data:
            self.object_data['name'] = text
            self.description_next = True
        if level == 2 and text not in self.object_data:
            text = lower_under_joined(text)
            self.fields_key = lower_under_joined(text)
            if self.table_count == 0:
                self.object_data[self.fields_key] = {}
            else:
                self.object_data[self.fields_key] = []
        return text
    def text(self, text):
        if self.description_next == True:
            self.object_data['description'] = text
            self.description_next = False
        if VERBOSE:
            print("text: {}".format(text))
        return text
    def link(self, link, title, text):
        if VERBOSE:
            print("link: {} title: {} text: {}".format(link, title, text))
        self.current_link = {'link': link, 'text': text}

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
            self.object_data['description'] = {'text': convert_unicode_quotes_dashes(description)}

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
            text = lower_under_joined(text)
            self.fields_key = lower_under_joined(text)
            self.object_data[self.fields_key] = {}
        return text
    def link(self, link, title, text):
        if VERBOSE:
            print("link: {} title: {} text: {}".format(link, title, text))
        if not self.description_done:
            if 'links' not in self.object_data['description']:
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

class AttackDataSourceDictRenderer(DictRenderer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name_complete = False
        self.description_complete = False
    def text(self, text):
        if VERBOSE:
            print("text: '{}'".format(text))
        if self.name_complete and not self.description_complete:
            #self.object_data['description'] = { 'text': text }
            self.object_data['description'] = text
            self.description_complete = True
        return text
    def header(self, text, level, raw=None):
        if VERBOSE:
            print("header: {} level: {}".format(text, level))
        if level == 1:
            self.object_data['name'] = text
            self.name_complete = True
        if level == 2 and text not in self.object_data:
            text = lower_under_joined(text)
            self.fields_key = lower_under_joined(text)
            self.object_data[self.fields_key] = {}
        return text

class DetectionDataModelDictRenderer(DictRenderer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table_headers = []
        self.table_headers_complete = False
        self.table_rows = []
        self.current_table_row = {}
        self.column_index = 0
        self.object_data['rows'] = []
    def text(self, text):
        if VERBOSE:
            print("text: {}".format(text))
        return text
    def header(self, text, level, raw=None):
        if VERBOSE:
            print("haeder: {} level: {}".format(text, level))
        if level == 1:
            self.object_data['name'] = text
        return text
    def table_cell(self, content, **flags):
        if VERBOSE:
            print("table_cell: {}".format(content))
        if not self.table_headers_complete:
            self.table_headers.append(content)
        else:
            self.current_table_row[self.table_headers[self.column_index]] = content
            self.column_index += 1
        return content
    def table_row(self, content):
        if VERBOSE:
            print("table_row: {}".format(content))
        self.table_headers_complete = True
        if len(self.current_table_row) > 0:
            self.object_data['rows'].append(self.current_table_row)
        self.current_table_row = {}
        self.column_index = 0
        return content

class OSSEMParser(object):
    def read_file(self, filename):
        ''' read contents of a file '''
        try:
            with open(filename) as file:
                file_content = file.read()
                return file_content
        except FileNotFoundError as e:
            print("File not found: {0}".format(filename))

    def parse_cim_md(self, markdown):
        """ parse markdown structured for OSSEM common information model """
        return self.parse_md_file(CIMDictRenderer, markdown)
    def parse_dd_md(self, markdown):
        """ parse markdown structured for OSSEM data dictionaries """
        return self.parse_md_file(DataDictionaryDictRenderer, markdown)

    def parse_ads_md(self, markdown):
        """ parse markdown structured for OSSEM attack data sources """
        return self.parse_md_file(AttackDataSourceDictRenderer, markdown)

    def parse_ddm_md(self, markdown):
        """ parse markdown structured for OSSEM detection data model """
        return self.parse_md_file(DetectionDataModelDictRenderer, markdown)

    def parse_md_file(self, renderer, markdown):
        """ parse markdown file according to our renderer type """
        dict_renderer = renderer()
        md = Markdown(escape=True, renderer=dict_renderer)
        md.parse(markdown)
        return md.renderer.get_python_dict()

    def parse_ossem(self, ossem_dir):
        """ main method for controlling parsing of OSSEM markdown """
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

            for f in files:
                if not f.lower() == 'readme.md': # and f.lower().endswith('.md'):
                    p = os.path.join(path, f)
                    for k in key_names:
                        if k['file'] == f:
                            if 'data_dictionaries' in path and f.lower().endswith('.md'):
                                subdir[k['key']] = self.parse_dd_md(self.read_file(p))
                            if 'common_information_model' in path and f.lower().endswith('.md'):
                                subdir[k['key']] = self.parse_cim_md(self.read_file(p))
                            if 'attack_data_sources' in path and f.lower().endswith('.md'):
                                subdir[k['key']] = self.parse_ads_md(self.read_file(p))
                            if 'detection_data_model' in path and f.lower().endswith('.md'):
                                subdir[k['key']] = self.parse_ddm_md(self.read_file(p))
                            if 'resources/images' in path:
                                subdir[k['key']] = {'link': 'https://github.com/Cyb3rWard0g/OSSEM/blob/master/resources/images/{}'.format(f)}

            parent = reduce(dict.get, folders[:-1], ossem)
            parent[folders[-1]] = subdir

        return ossem

def subset(subset, ossem):
    ossem = ossem['OSSEM']
    keys = []
    if '.' in subset:
        keys = subset.split('.')
    else:
        keys = [subset]
    for k in keys:
        if k not in ossem:
            print("Invalid subset doesn't exist in OSSEM data model")
            sys.exit()
        else:
            ossem = ossem[k]
    return ossem

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='parse markdown file')
    parser.add_argument('--ossem', type=str, help='base directory containing the OSSEM project')
    parser.add_argument('--output', '-o', type=str, help='output format (json, yaml, xml, or python supported)', default='yaml')
    parser.add_argument('--subset', '-s', type=str, help='output only a subset of OSSEM. example data_dictionaries.windows.sysmon')
    args = parser.parse_args()

    valid_output = ['json', 'yaml', 'xml', 'python'] # should we add markdown as output?
    output_format = args.output.lower()
    if not output_format in valid_output:
        print("not a valid output format, must me one of {}".format(valid_output))
        sys.exit()

    if args.ossem:
        parser = OSSEMParser()
        ossem = parser.parse_ossem(args.ossem)
        if args.subset:
            ossem = subset(args.subset, ossem)
        if output_format == 'json':
            print(json.dumps(ossem))
        elif output_format == 'yaml':
            print(yaml.dump(ossem, default_flow_style=False))
        elif output_format == 'xml':
            from dicttoxml import dicttoxml # we conditionally import this because it's not in python core
            print(dicttoxml(ossem))
        elif output_format == 'python':
            print("ossem = {}".format(ossem))
    else:
        import unittest
        from tests.test_cim import TestOSSEMCIM
        from tests.test_data_dictionaries import TestOSSEMDataDictionaries
        from tests.test_attack_data_sources import TestOSSEMADS
        #from tests.test_detection_data_model import TestDetectionDataModels # didn't finish the tests
        unittest.main()
