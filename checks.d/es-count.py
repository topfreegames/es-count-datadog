import requests
import json

from checks import AgentCheck

DEFAULT_ELASTICSEARCH_ADDRESS = 'http://elasticsearch:9200'
DEFAULT_ELASTICSEARCH_index = 'test'
DEFAULT_TIME_RANGE = '1m'

class ESCountCheck(AgentCheck):
    '''
    Count the number of each term in the last minute
    '''

    def check(self, instance):
        self.log.info("starting es-count check")
        self.es_address = instance.get("es_address", DEFAULT_ELASTICSEARCH_ADDRESS)
        self.es_index = instance.get("es_index", DEFAULT_ELASTICSEARCH_index)
        self.log.debug("elasticsearch_address: " + self.es_address)
        self.extra_tags = instance.get("tags", [])
        match = instance.get("match", [])
        tags = ['instance:%s' % self.hostname] + self.extra_tags
        for target in match:
            for term in target['terms']:
                res = self.get_number_of_occurrences('%s/%s/_search' % (self.es_address, target['index']), term, target['time_range'])
                print res
                if res != None and u'hits' in res:
                    occurrences = res[u'hits'][u'total']
                    self.count('es-count.count', occurrences,
                            tags=tags + ['term:%s' % term.lower(),
                                'index:%s' % target['index'].lower(),
                                'time_range:%s' % target['time_range']])

    def get_number_of_occurrences(self, uri, term, time_range):
        self.log.debug("getting occurrences for: " + term)
        query = json.dumps({
          "query": {
            "bool": {
              "must": [{
                "query_string": {
                  "query": '%s' % term,
                  "analyze_wildcard": "true"
                }
              }, {
                "range": {
                  "@timestamp": {"gt": 'now-%s' % time_range}
                }
              }]
            }
          },
          "size": 0
        })
        results = None
        try:
            response = requests.get(uri, data=query)
            results = json.loads(response.text)
        except Exception as e:
            self.log.error("es_check failed to grab info from es: %s" % str(e))
        else:
            self.log.debug("es_check grabbed info from es successfully")
        return results
