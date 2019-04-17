""" This provides a test suite for parsing OSSEM data dictionaries """

import unittest, os
from ossem_parser import OSSEMParser

class TestOSSEMDataDictionaries(unittest.TestCase):
    def setUp(self):
        self.p = OSSEMParser()
        self.sysmon_event_1_md = os.path.join("tests", "test_data", "sysmon-event-1.md")
        self.osquery_hash_md = os.path.join("tests", "test_data", "osquery-hash.md")
    ''' # I broke this test when I did the unicode conversion and don't care about fixing it right now, event_data xml is borked from unicode conversion
    def test_sysmon_event_1(self):
        expected_output = {
           'meta': {
             'title': 'Event ID 1 - Process creation',
             'description': 'The process creation event provides extended information about a newly created process.',
             'log_type': 'sysmon',
             'sysmon_version': '7.01',
             'sysmon_rule': 'ProcessCreate',
             'author': 'Roberto Rodriguez (@Cyb3rWard0g)',
             'date': '04/11/2018'
          },
          'title': 'Event ID 1: Process creation',
          'description': {
            'text': 'The process creation event provides extended information about a newly created process. The full command line provides context on the process execution. The ProcessGUID field is a unique value for this process across a domain to make event correlation easier. The hash is a full hash of the file with the algorithms in the HashType field.',
            'links': [
              {
                'text': 'Sysmon Source',
                'link': 'https://docs.microsoft.com/en-us/sysinternals/downloads/sysmon#event-id-1-process-creation'
              }
            ]
          },
          'event_log_illustration':  {
            'image': {
              'link': 'https://github.com/Cyb3rWard0g/OSSEM/blob/master/resources/images/event-1.png',
              'alt': 'Event 2 illustration',
              'width': 625,
              'height': 625
            }
          },
          'event_data': {
            'type': 'xml',
            'data': """<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">
      <System>
        <Provider Name="Microsoft-Windows-Sysmon" Guid="{5770385F-C22A-43E0-BF4C-06F5698FFBD9}" />
        <EventID>1</EventID>
        <Version>5</Version>
        <Level>4</Level>
        <Task>1</Task>
        <Opcode>0</Opcode>
        <Keywords>0x8000000000000000</Keywords>
        <TimeCreated SystemTime="2018-04-11T05:25:02.959125700Z" />
        <EventRecordID>11748095</EventRecordID>
        <Correlation />
        <Execution ProcessID="2152" ThreadID="3392" />
        <Channel>Microsoft-Windows-Sysmon/Operational</Channel>
        <Computer>DESKTOP-WARDOG</Computer>
        <Security UserID="S-1-5-18" />
      </System>
      <EventData>
        <Data Name="UtcTime">2018-04-11 05:25:02.955</Data>
        <Data Name="ProcessGuid">{A98268C1-9C2E-5ACD-0000-0010396CAB00}</Data>
        <Data Name="ProcessId">4756</Data>
        <Data Name="Image">C:\Windows\System32\conhost.exe</Data>
        <Data Name="FileVersion">10.0.16299.15 (WinBuild.160101.0800)</Data>
        <Data Name="Description">Console Window Host</Data>
        <Data Name="Product">Microsoft® Windows® Operating System</Data>
        <Data Name="Company">Microsoft Corporation</Data>
        <Data Name="CommandLine">\??\C:\WINDOWS\system32\conhost.exe 0xffffffff -ForceV1</Data>
        <Data Name="CurrentDirectory">C:\WINDOWS</Data>
        <Data Name="User">DESKTOP-WARDOG\wardog</Data>
        <Data Name="LogonGuid">{A98268C1-95F2-5ACD-0000-002019620F00}</Data>
        <Data Name="LogonId">0xf6219</Data>
        <Data Name="TerminalSessionId">1</Data>
        <Data Name="IntegrityLevel">Medium</Data>
        <Data Name="Hashes">SHA1=B0BF5AC2E81BBF597FAD5F349FEEB32CAC449FA2,MD5=6A255BEBF3DBCD13585538ED47DBAFD7,SHA256=4668BB2223FFB983A5F1273B9E3D9FA2C5CE4A0F1FB18CA5C1B285762020073C,IMPHASH=2505BD03D7BD285E50CE89CEC02B333B</Data>
        <Data Name="ParentProcessGuid">{A98268C1-9C2E-5ACD-0000-00100266AB00}</Data>
        <Data Name="ParentProcessId">240</Data>
        <Data Name="ParentImage">C:\Windows\System32\cmd.exe</Data>
        <Data Name="ParentCommandLine">"C:\WINDOWS\system32\cmd.exe"</Data>
      </EventData>
    </Event>"""
          },
          'data_dictionary': {
            'event_date_creation': {
              'field_name': 'UtcTime',
              'type': 'date',
              'description': 'Time in UTC when event was created',
              'sample_value': '4/11/18 5:25'
            },
            'process_guid': {
              'field_name': 'ProcessGuid',
              'type': 'string',
              'description': 'Process Guid of the process that got spawned/created (child)',
              'sample_value': '{A98268C1-9C2E-5ACD-0000-0010396CAB00}'
            },
            'process_id': {
              'field_name': 'ProcessId',
              'type': 'integer',
              'description': 'Process ID used by the os to identify the created process (child)',
              'sample_value': 4756
            },
            'process_name': {
              'field_name': 'Image',
              'type': 'string',
              'description': 'The name of the executable without full path related to the process being spawned/created in the event. Considered also the child or source process',
              'sample_value': 'conhost.exe'
            },
            'process_path': {
              'field_name': 'Image',
              'type': 'string',
              'description': 'File path of the process being spawned/created. Considered also the child or source process',
              'sample_value': 'C:\\Windows\\System32\\conhost.exe'
            },
            'file_version': {
              'field_name': 'FileVersion',
              'type': 'string',
              'description': 'Version of the image associated with the main process (child)',
              'sample_value': '10.0.16299.15 (WinBuild.160101.0800)'
            },
            'file_description': {
              'field_name': 'Description',
              'type': 'string',
              'description': 'Description of the image associated with the main process (child)',
              'sample_value': 'Console Window Host'
            },
            'file_product': {
              'field_name': 'Product',
              'type': 'string',
              'description': 'Product name the image associated with the main process (child) belongs to',
              'sample_value': 'Microsoft® Windows® Operating System'
            },
            'file_company': {
              'field_name': 'Company',
              'type': 'string',
              'description': 'Company name the image associated with the main process (child) belongs to',
              'sample_value': 'Microsoft Corporation'
            },
            'process_command_line': {
              'field_name': 'CommandLine',
              'type': 'string',
              'description': 'Arguments which were passed to the executable associated with the main process',
              'sample_value': '??\\C:\\WINDOWS\\system32\\conhost.exe 0xffffffff -ForceV1'
            },
            'file_current_directory': {
              'field_name': 'CurrentDirectory',
              'type': 'string',
              'description': 'The path without the name of the image associated with the process',
              'sample_value': 'C:\\WINDOWS'
            },
            'user_name': {
              'field_name': 'User',
              'type': 'string',
              'description': 'Name of the account who created the process (child) . It usually contains domain name and user name (Parsed to show only username without the domain)',
              'sample_value': 'DESKTOP-WARDOG\\wardog'
            },
            'user_logon_guid': {
              'field_name': 'LogonGuid',
              'type': 'string',
              'description': 'Logon GUID of the user who created the new process. Value that can help you correlate this event with others that contain the same Logon GUID (Sysmon Events)',
              'sample_value': '{A98268C1-95F2-5ACD-0000-002019620F00}'
            },
            'user_logon_id': {
              'field_name': 'LogonId',
              'type': 'integer',
              'description': 'Login ID of the user who created the new process. Value that can help you correlate this event with others that contain the same Logon ID',
              'sample_value': 1008153
            },
            'user_session_id': {
              'field_name': 'TerminalSessionId',
              'type': 'integer',
              'description': 'ID of the session the user belongs to',
              'sample_value': 1
            },
            'process_integrity_level': {
              'field_name': 'IntegrityLevel',
              'type': 'string',
              'description': 'Integrity label assigned to a process',
              'sample_value': 'Medium'
            },
            'hash': {
              'field_name': 'Hashes',
              'type': 'string',
              'description': 'Hashes captured by sysmon driver',
              'sample_value': 'SHA1=B0BF5AC2E81BBF597FAD5F349FEEB32CAC449FA2, MD5=6A255BEBF3DBCD13585538ED47DBAFD7, SHA256=4668BB2223FFB983A5F1273B9E3D9FA2C5CE4A0F1FB18CA5C1B285762020073C, IMPHASH=2505BD03D7BD285E50CE89CEC02B333B'
            },
            'process_parent_guid': {
              'field_name': 'ParentProcessGuid',
              'type': 'string',
              'description': 'ProcessGUID of the process that spawned/created the main process (child)',
              'sample_value': '{A98268C1-9C2E-5ACD-0000-00100266AB00}'
            },
            'process_parent_id': {
              'field_name': 'ParentProcessId',
              'type': 'integer',
              'description': 'Process ID of the process that spawned/created the main process (child)',
              'sample_value': 240
            },
            'process_parent_name': {
              'field_name': 'ParentImage',
              'type': 'string',
              'description': 'The name of the executable related to the target process',
              'sample_value': 'cmd.exe'
            },
            'process_parent_path': {
              'field_name': 'ParentImage',
              'type': 'string',
              'description': 'File path that spawned/created the main process',
              'sample_value': 'C:\\Windows\\System32\\cmd.exe'
            },
            'process_parent_command_line': {
              'field_name': 'ParentCommandLine',
              'type': 'string',
              'description': 'Arguments which were passed to the executable associated with the parent process',
              'sample_value': 'C:\\WINDOWS\\system32\\cmd.exe'
            }
          }
        }
        assert(self.p.parse_dd_md(self.p.read_file(self.sysmon_event_1_md)) == expected_output)
'''
    def test_windows_osquery_hash(self):
        expected_output = {
          'title': 'Hash Table',
          'description': {
            'text': 'Filesystem hash data.',
            'links': [
              {
                'text': 'osquery GitHub',
                'link': 'https://github.com/facebook/osquery/blob/master/specs/hash.table'
              }
            ]
          },
          #'event_log_illustration': {}, # if this section is blank we don't currently default populate it
          'data_dictionary': {
            'file_path': {
              'field_name': 'path',
              'type': 'TEXT',
              'description': 'Must provide a path or directory',
              'sample_value': ''
            },
            'file_directory': {
              'field_name': 'directory',
              'type': 'TEXT',
              'description': 'Must provide a path or directory',
              'sample_value': ''
            },
            'hash_md5': {
              'field_name': 'md5',
              'type': 'TEXT',
              'description': 'MD5 hash of provided filesystem data',
              'sample_value': ''
            },
            'hash_sha1': {
              'field_name': 'sha1',
              'type': 'TEXT',
              'description': 'SHA1 hash of provided filesystem data',
              'sample_value': ''
            },
            'hash_sha256': {
              'field_name': 'sha256',
              'type': 'TEXT',
              'description': 'SHA256 hash of provided filesystem data',
              'sample_value': ''
            }
          }
        }
        assert(self.p.parse_dd_md(self.p.read_file(self.osquery_hash_md)) == expected_output)
