""" This provides a test suite for verifying the correctness
    of the OSSEM Common Information Model conversion from markdown
    to our desired output """

import unittest, os
from ossem_parser import OSSEMParser

class TestOSSEMCIM(unittest.TestCase):
    def setUp(self):
        self.p = OSSEMParser()
        self.alert_md = os.path.join("tests", "test_data", "alert.md")
        self.destination_md = os.path.join("tests", "test_data", "destination.md")
        self.event_md = os.path.join("tests", "test_data", "event.md")
        self.process_md = os.path.join("tests", "test_data", "process.md")

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

    def test_process_cim(self):
        desired_output = {
            'name': 'Process Schema',
            'description': 'Event fields used to define metadata about processes in an system.',
            'data_fields': {
                'process_guid': {
                    'type': 'string',
                    'description': 'Process Guid of the main process that got spawned/created (child)',
                    'sample_value': '{A98268C1-9C2E-5ACD-0000-0010396CAB00}'
                },
                'process_id': {
                    'type': 'integer',
                    'description': 'Process ID used by the operating system to identify the created process (child)',
                    'sample_value': 4756
                },
                'process_name': {
                    'type': 'string',
                    'description': 'The name of the executable without full path related to the process being spawned/created in the event. Considered also the child or source process',
                    'sample_value': 'conhost.exe'
                },
                'process_path': {
                    'type': 'string',
                    'description': 'The complete path and name of the executable related to the main process in the event. Considered also the child or source process path',
                    'sample_value': 'C:\Windows\System32\conhost.exe'
                },
                'process_command_line': {
                    'type': 'string',
                    'description': 'Command arguments that were were executed by the main process in the event (child process)',
                    'sample_value': '??\C:\WINDOWS\system32\conhost.exe 0xffffffff -ForceV1'
                },
                'process_integrity_level': {
                    'type': 'string',
                    'description': 'Integrity label assigned to a process',
                    'sample_value': 'Medium'
                },
                'process_parent_guid': {
                    'type': 'string',
                    'description': 'ProcessGUID of the process that spawned/created the main process (child)',
                    'sample_value': '{A98268C1-9C2E-5ACD-0000-00100266AB00}'
                },
                'process_parent_id': {
                    'type': 'integer',
                    'description': 'Process ID of the process that spawned/created the main process (child)',
                    'sample_value': 240
                },
                'process_parent_name': {
                    'type': 'string',
                    'description': 'The name of the executable without full path related to the process that spawned/created the main process (child)',
                    'sample_value': 'cmd.exe'
                },
               'process_parent_path': {
                   'type': 'string',
                   'description': 'The complete path and name of the executable related to the the process that spawned/created the main process (child)',
                   'sample_value': 'C:\Windows\System32\cmd.exe'
               },
               'process_parent_command_line': {
                   'type': 'string',
                   'description': 'Command arguments that were passed to the executable related to the parent process',
                   'sample_value': 'C:\WINDOWS\system32\cmd.exe'
               },
               'target_process_guid': {
                   'type': 'string',
                   'description': 'Process Guid of the target process',
                   'sample_value': '{A98268C1-9C2E-5ACD-0000-00100266AB00}',
               },
               'target_process_id': {
                   'type': 'integer',
                   'description': 'Process ID used by the os to identify the target process',
                   'sample_value': 240
               },
               'target_process_name': {
                   'type': 'string',
                   'description': 'The name of the executable related to the target process',
                   'sample_value': 'cmd.exe'
               },
               'target_process_path': {
                   'type': 'string',
                   'description': 'The complete path and name of the executable associated with the target process',
                   'sample_value': 'C:\Windows\System32\cmd.exe'
               },
               'target_process_address': {
                   'type': 'string',
                   'description': 'The memory address where the subprocess is injected',
                   'sample_value': '0xFFFFBC6422DD9C20'
               },
               'process_granted_access': {
                   'type': 'string',
                   'description': 'granted access code requested/used to open a target process',
                   'sample_value': '0x1000'
               },
               'process_call_trace': {
                   'type': 'string',
                   'description': 'Stack trace of where open process is called',
                   'sample_value': 'C:\WINDOWS\SYSTEM32\\ntdll.dll+a0344 | C:\WINDOWS\System32\KERNELBASE.dll+64794| c:\windows\system32\lsm.dll+10e93| c:\windows\system32\lsm.dll+f9ea| C:\WINDOWS\System32\RPCRT4.dll+76d23| C:\WINDOWS\System32\RPCRT4.dll+d9390| C:\WINDOWS\System32\RPCRT4.dll+a81c| C:\WINDOWS\System32\RPCRT4.dll+273b4| C:\WINDOWS\System32\RPCRT4.dll+2654e| C:\WINDOWS\System32\RPCRT4.dll+26cfb| C:\WINDOWS\System32\RPCRT4.dll+3083f| C:\WINDOWS\System32\RPCRT4.dll+313a6| C:\WINDOWS\System32\RPCRT4.dll+2d12e| C:\WINDOWS\System32\RPCRT4.dll+2e853| C:\WINDOWS\System32\RPCRT4.dll+5cc68| C:\WINDOWS\SYSTEM32\\ntdll.dll+365ce| C:\WINDOWS\SYSTEM32\\ntdll.dll+34b46| C:\WINDOWS\System32\KERNEL32.DLL+11fe4| C:\WINDOWS\SYSTEM32\\ntdll.dll+6efc1'
               }
            },
            'applicable_data_sources': [
                {
                    'source_entity': 'process',
                    'relationship': 'created',
                    'destination_entity': 'process',
                    'data_source': 'Windows Security Event Log',
                    'event_name/id': {
                        'link': '../data_dictionaries/windows/security/events/event-4688.md',
                        'text': '4688'
                    }                        
                },
                {
                    'source_entity': 'process',
                    'relationship': 'created',
                    'destination_entity': 'process',
                    'data_source': 'Carbon Black',
                    'event_name/id': {
                        'link': '../data_dictionaries/windows/carbonblack/procstart.md',
                        'text': 'procstart'
                    }
                },
                {
                    'source_entity': 'process',
                    'relationship': 'created',
                    'destination_entity': 'process',
                    'data_source': 'Carbon Black',
                    'event_name/id': {
                        'link': '../data_dictionaries/windows/carbonblack/childproc.md',
                        'text': 'childproc'
                    }
                },
                {
                    'source_entity': 'process',
                    'relationship': 'created',
                    'destination_entity': 'process',
                    'data_source': 'Sysmon',
                    'event_name/id': {
                        'link': '../data_dictionaries/windows/sysmon/event-1.md',
                        'text': '1'
                    }
                },
                {
                    'source_entity': '',
                    'relationship': 'terminated',
                    'destination_entity': 'process',
                    'data_source': 'Windows Security Event Log',
                    'event_name/id': {
                        'link': '../data_dictionaries/windows/security/events/event-4689.md',
                        'text': '4689'
                    }
                },
                {
                    'source_entity': '',
                    'relationship': 'terminated',
                    'destination_entity': 'process',
                    'data_source': 'Sysmon',
                    'event_name/id': {
                        'link': '../data_dictionaries/windows/sysmon/event-5.md',
                        'text': '5'
                    }
                },
                {
                    'source_entity': 'process',
                    'relationship': 'wrote_to',
                    'destination_entity': 'process',
                    'data_source': 'Sysmon',
                    'event_name/id': {
                        'link': '../data_dictionaries/windows/sysmon/event-8.md',
                        'text': '8'
                    }
                },
                {
                    'source_entity': 'process',
                    'relationship': 'opened',
                    'destination_entity': 'process',
                    'data_source': 'Sysmon',
                    'event_name/id': {
                        'link': '../data_dictionaries/windows/sysmon/event-10.md',
                        'text': '10'
                    }
                },
                {
                    'source_entity': 'process',
                    'relationship': 'opened',
                    'destination_entity': 'process',
                    'data_source': 'Carbon Black',
                    'event_name/id': {
                        'link': '../data_dictionaries/windows/carbonblack/crossprocopen.md',
                        'text': 'crossprocopen'
                    }
                }
            ]
        }
        assert(desired_output == self.p.parse_cim_md(self.p.read_file(self.process_md)))
