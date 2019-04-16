""" This provides a test suite for parsing OSSEM detction data models """

import unittest, os
from main import OSSEMParser

class TestDetectionDataModels(unittest.TestCase):
  def setUp(self):
    self.p = OSSEMParser()
    self.object_relationships_md = os.path.join("tests", "test_data", "object_relationships.md")

  def test_detection_data_models_1(self):
    expected_output = {
      'name': 'Data Object Relationships',
      'object_relationships': {
        'process creation': {
          'data_objects_origin': 'process',
          'relationship': 'created',
          'data_objects_destination': 'process'
        },
        'process termination': {
          'data_objects_origin': 'process',
          'relationship': 'terminated',
          'data_objects_destination': ''
        },
        'process write to process': {
          'data_objects_origin': 'process',
         'relationship': 'wrote_to',
          'data_objects_destination': 'process'
        }
      }
    }
    from pprint import pprint
    pprint(self.p.parse_ddm_md(self.p.read_file(self.object_relationships_md)))
 
   #assert(desired_output == self.p.parse_ddm_md(self.p.read_file(self.object_relationships_md))
