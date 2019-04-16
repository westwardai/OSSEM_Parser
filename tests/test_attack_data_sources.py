""" this provides a test for the correctness of parsing
    OSSEM attack_data_sources """


import unittest, os
from main import OSSEMParser

class TestOSSEMADS(unittest.TestCase):
    def setUp(self):
        self.p = OSSEMParser()
        self.ads_md = os.path.join("tests", "test_data", "attack_data_sources.md")
    def test_ads_conversion(self):
        expected_output = {
          'name': 'Data Sources',
          'description': 'Data sources names and association to techniques are determined by the MITRE ATTACK team.',
          # mistune is having trouble properly parsing recursive unordered lists - should maybe fix this
          #'description': {
            #'text': 'Data sources names and association to techniques are determined by the MITRE ATTACK team.',
            #'list': [
            #  {
            #    'text': 'Several data sources do not necessarily map directly to a physical data set or event log source. A few examples could be:',
            #    'list': [
            #      { 'text': 'Detonation Chamber' },
            #      { 'text': 'Malware reverse engineering' }
            #    ]
            #  },
            #  {
            #    'text': 'Multiple physical data sets also can map to the same data source. For example:',
            #    'list': [
            #      { 'text': 'The Anti-Virus data source can be provided by several AV companies (different data sets which also might mean different schemas).' }
            #    ]
            #  }
            #]
          #},
          'data_sources_definitions': {
            'Access Tokens': {
              'description': 'Logs tracking the identity and privileges of the user account associated with a process or thread.'
            },
            'Anti-virus': {
              'description': 'Logs provided by AV providers such as alerts that need to be investigated'
            },
            'API monitoring': {
              'description': 'Logs monitoring API calls on endpoints'
            },
            'Application Logs': {
              'description': 'TBD'
            },
            'Asset Management': {
              'description': 'Logs providing up to date information about active endpoints in an environment (Scope)'
            },
            'Authentication logs': {
              'description': 'Logs tracking log on activity in an environment. For example, users authenticating to other endpoints via WinRM, WMI, etc.'
            },
            'Binary file metadata': {
              'description': 'Information about binary files over the wire or locally on an endpoint.'
            },
            'BIOS': {
              'description': 'Logs providing information about the integrity of existing BIOs'
            },
            'Browser extensions': {
              'description': 'Logs monitoring for browser extensions or plugins that can add functionality and customize aspects of internet browsers. Monitoring for any new items written to the Registry or PE files written to disk could correlate with browser extension installation'
            },
            'Data loss prevention': {
              'description': 'Logs monitoring file access and removable media devices. Those could be similar to the ones from Windows security logs object access category'
            },
            'Detonation chamber': {
              'description': 'TBD'
            },
            'Digital Certificate Logs': {
              'description': 'Logs needed to detect primarily suspicious Root certificate installations. For example, you can get good information about the use of this technique from the HKLM\SOFTWARE\Microsoft\SystemCertificates\ROOT\Certificates registry keys'
            },
            'DLL monitoring': {
              'description': 'Logs monitoring the creation, modification or rename of DLLs. For example. One could monitor HKLM\SYSTEM\CurrentControlSet\Control\Print\Monitors for DLLs loaded by spoolsv.exe'
            },
            'DNS records': {
              'description': 'Logs monitoring for changes to DNS records in endpoints.'
            },
            'EFI': {
              'description': 'Logs providing information about the integrity of existing EFI. EFI modules can be collected and compared against a known-clean list of EFI executable binaries to detect potentially malicious modules'
            },
            'Email gateway': {
              'description': 'TBD'
            },
            'Environment variable': {
              'description': 'Logs tracking users checking or changing their environment variables (HISTCONTROL). (Lunix/MacOs)'
            },
            'File monitoring': {
              'description': 'Logs tracking any modification, creation or rename of files either locally or over the wire'
            },
            'Host network interface': {
              'description': 'Logs tracking changes to the host network interface. For example, an adversary may place a network interface into promiscuous mode'
            },
            'Kernel drivers': {
              'description': 'Logs monitoring the registry and file system for driver installs'
            },
            'Loaded DLLs': {
              'description': 'Logs monitoring dlls being loaded by process execution. Similar approach to DLL monitoring. They both can be used together in certain techniques.'
            },
            'Mail server': {
              'description': 'TBD'
            },
            'Malware reverse engineering': {
              'description': 'Information obtained by looking at samples of malware. For example, it may be possible to obtain the algorithm and key from samples of malware using custom encryption. This can help to decode network traffic.'
            },
            'MBR': {
              'description': 'Logs providing information about changes to the MBR (might not be provided by default logs on the endpoints)'
            },
            'Named Pipes': {
              'description': 'Logs tracking named pipes creation and connection events (i.e Sysmon Event IDs 17 and 18)'
            },
            'Netflow/Enclave netflow': {
              'description': 'Netflow logs - TBD'
            },
            'Network device logs': {
              'description': 'TBD'
            },
            'Network intrusion detection system': {
              'description': 'TBD'
            },
            'Network protocol analysis': {
              'description': 'Network logs prodiving information about protocols being used in network connections. This can be obtained from endpoint and network data sets'
            },
            'Packet capture': {
              'description': 'TBD'
            },
            'PowerShell logs': {
              'description': 'Windows PowerShell logs',
            },
            'Process command-line parameters': {
              'description': 'Logs monitoring process command line arguments'
            },
            'Process monitoring': {
              'description': 'Logs monitoring process execution'
            },
            'Process use of network': {
              'description': 'Logs tracking processes making network connections'
            },
            'Sensor health and status': {
              'description': 'Logs monitoring data sensor status in case they are disabled to stop collecting and sending logs to a SIEM. For example, Sysmon EID 4 tells you when its service stops'
            },
            'Services': {
              'description': 'Logs about services being installed or highjacked in a system (i.e Windows Security Log 4697 or Windows System log 7045)'
            },
            'SSL/TLS inspection': {
              'description': 'Information about encrypted channels being used by adversaries. This could be part of netflow data'
            },
            'System calls': {
              'description': 'TBD'
            },
            'Third-party application logs': {
              'description': 'Logs indicating the usage of third party software. For example, an adversary using VNC'
            },
            'User interface': {
              'description': 'Logs inidicating processes that normally require user-driven events. For example, clicking or typing a password in a fake credentials prompt. This might be provided by API monitoring data sources'
            },
            'VBR': {
              'description': 'Logs tracking changes to the VBR (might not be provided by default logs on the endpoints)'
            },
            'Web application firewall logs': {
              'description': 'TBD'
            },
            'Web logs': {
              'description': 'TBD'
            },
            'Web proxy': {
              'description': 'TBD'
            },
            'Windows Error Reporting': {
              'description': 'Logs providing software and operating system crash information. OS system crash reports (usually offline analysis of crash reports need to happen)'
            },
            'Windows event logs': {
              'description': 'Windows event logs used to track user creation, permissions modifications, and even changes to groups. Based on the techniques linked to this data source, it seemed to be also focused on scheduled tasks, account manipulations, account creation and SID-history logs. (We can say every Windows event log here)'
            },
            'Windows Registry': {
              'description': 'Logs tracking any creation, deletion and modification of registry keys in Windows environments'
            },
            'WMI Objects': {
              'description': 'Logs capturing WMI event subscription events'
            }
          }
        }
        assert(self.p.parse_ads_md(self.p.read_file(self.ads_md)) == expected_output)
