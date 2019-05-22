# OSSEM_Parser
Parser that takes the OSSEM data model as input and generates a YAML file as output.


## Usage:
```python3 ossem_parser.py --ossem ../<path-to-ossem> --output yaml```
Supported output formats are python, yaml, xml, and json.

Extract a subset of data. For example, just sysmon events:
```python3 ossem_parser.py --ossem ../OSSEM --subset data_dictionaries.windows.sysmon```

## Some use cases:
Write all sysmon events to their own json files:
```from data.ossem import ossem
import json
sysmon_events = ossem['OSSEM']['data_dictionaries']['windows']['sysmon']
sysmon_events = {key: sysmon_events[key] for key in sysmon_events.keys() if key.isnumeric()}
for event in sysmon_events:
    with open("event-{}.json".format(event), 'w') as fh:
        fh.write(json.dumps(sysmon_events[event]))
```
