""" This provides a test suite for verifying the correctness
    of the OSSEM Common Information Model conversion from markdown
    to our desired output """

import unittest, os
from main import OSSEMParser

class TestOSSEMCIM(unittest.TestCase):
    def setUp(self):
        self.p = OSSEMParser()
        self.alert_md = os.path.join("tests", "test_data", "alert.md")
        self.destination_md = os.path.join("tests", "test_data", "destination.md")
        self.event_md = os.path.join("tests", "test_data", "event.md")

    def test_alert_conversion(self):
        desired_output = {
          'name': 'Alert Schema',
          'description': 'Alert fields that describe an indicator from a tool of a possible issue.',
          'data_fields': {
            'alert_id': {
              'type': 'integer',
              'description': 'Alert ids might repeat across different data sources',
              'sample_value': 1234
            },
            'alert_signature': {
              'type': 'string',
              'description': 'The name or title of an alert',
              'sample_value': 'EvilActor:CnCv2'
            },
            'alert_message': { 'type': 'string',
              'description': 'The message provided by the alert',
              'sample_value': 'A file exhibiting behaviour of the evilactor command and control framework 2 was detected.'
            },
            'alert_description': {
              'type': 'string',
              'description': 'The expanded description of the event',
              'sample_value': '...'
            },
            'alert_severity': {
              'type': 'string',
              'description': 'The severity of an alert',
              'sample_value': 'Priority 5'
            },
            'alert_category': {
              'type': 'string',
              'description': 'The category of an alert',
              'sample_value': 'Malware'
            },
            'alert_version': {
              'type': 'string',
              'description': 'A signature or alert version',
              'sample_value':'1.2'
            }
          }
        }
        assert(desired_output == self.p.parse_cim_md(self.p.read_file(self.alert_md)))

    def test_destination_conversion(self):
        desired_output = {
          'name': 'Destination Schema',
          'description': 'Event fields used to define the destination in a network connection event.',
          'data_fields': {
            'dst_ip': {
              'type': 'ip',
              'description': 'Destination IP in a network connection (IPv4)',
              'sample_value': '8.8.8.8'
            },
            'dst_ipv6': {
              'type': 'ip',
              'description': 'Destination IP in a network connection (IPv6)',
              'sample_value': 'a968:8228:c46d:95a8:d8ef:30ab:dab3:17f2'
            },
            'dst_host_name': {
              'type': 'string',
              'description': 'Destination host name in a network connection',
              'sample_value': 'WKHR001'
            },
            'dst_port': {
              'type': 'integer',
              'description': 'Destination port number used in a network connection',
              'sample_value': 53
            },
            'dst_port_name': {
              'type': 'string',
              'description': 'Destination port name used in a network connection',
              'sample_value': 'DNS'
            }
          }
        }
        assert(desired_output == self.p.parse_cim_md(self.p.read_file(self.destination_md)))

    #def test_event_conversion(self):
    #  print(self.p.parse_md_file(self.event_md))
