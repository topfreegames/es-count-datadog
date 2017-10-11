es-count-datadog
================

### Purpose
This datadog agent plugin will connect to elasticsearch and count occurrences of configurable terms given a time range (now-interval till now) and push the counts to datadog.
An example of use case is to send counts of occurrences of events from a logstash and create alarms that will be triggered every time the occurrences have abnormal values.

### Metrics
This plugin will push a metric called "es-count.count" tagged with the term, stash and time_range, e.g.

```
 ('es-count.count',
  1502229650,
  0,
  {'hostname': '9b5b7bde1a6a',
   'tags': ['instance:9b5b7bde1a6a',
            'term:test2',
            'stash:test',
            'time_range:1m'],
   'type': 'count'})]
```

es-count.count contains the count of occurrences of {term} in the interval {now-timerange ~ now} on a given index.

**IMPORTANT:** The index must contain time based events and a "timestamp" field for the check to work.

### Tags

Extra tags can be passed to the metrics sent by specifying them into the config file, e.g.


### Names

Names can be passed to be sent to datadog instead of using the term as the name

```
init_config:
instances:
  - es_address: http://elasticsearch:9200
    match:
      - index: test
        terms:
          - test1
          - test2
        names:
          - test_name_1
        time_range: 1m
      - index: test2
        terms:
          - test3
        time_range: 1m
    tags:
      - foo
      - bar
      - extra:tag
```

### Development

1. Start elasticsearch
```
docker-compose up -d elasticsearch
```
2. Execute es-count check
```
docker-compose run datadog-agent /opt/datadog-agent/agent/agent.py check es-count
```
