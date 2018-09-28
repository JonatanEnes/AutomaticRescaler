# /usr/bin/python
import requests
import json
import time


class BDWatchdog:
    OPENTSDB_URL = "opentsdb"
    OPENTSDB_PORT = 4242
    NO_METRIC_DATA_DEFAULT_VALUE = 0  # -1

    def __init__(self, server="http://{0}:{1}".format(OPENTSDB_URL, str(int(OPENTSDB_PORT)))):
        self.server = server
        self.session = requests.Session()

    def get_points(self, query):
        r = self.session.post(self.server + "/api/query", data=json.dumps(query),
                          headers={'content-type': 'application/json', 'Accept': 'application/json'})
        if r.status_code == 200:
            return json.loads(r.text)
        else:
            r.raise_for_status()

    def get_structure_usages(self, tags, window_difference, window_delay, retrieve_metrics, generate_metrics,
                             downsample=5):
        usages = dict()
        subquery = list()
        for metric in retrieve_metrics:
            usages[metric] = self.NO_METRIC_DATA_DEFAULT_VALUE
            subquery.append(dict(aggregator='zimsum', metric=metric, tags=tags, downsample=str(downsample) + "s-avg"))

        start = int(time.time() - (window_difference + window_delay))
        end = int(time.time() - window_delay)
        query = dict(start=start, end=end, queries=subquery)
        result = self.get_points(query)

        for metric in result:
            dps = metric["dps"]
            summatory = sum(dps.values())
            if len(dps) > 0:
                average_real = summatory / len(dps)
            else:
                average_real = 0
            usages[metric["metric"]] = average_real

        final_values = dict()

        for value in generate_metrics:
            final_values[value] = self.NO_METRIC_DATA_DEFAULT_VALUE
            for metric in generate_metrics[value]:
                if metric in usages and usages[metric] != self.NO_METRIC_DATA_DEFAULT_VALUE:
                    final_values[value] += usages[metric]

        return final_values
