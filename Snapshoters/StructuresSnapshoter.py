# /usr/bin/python
from __future__ import print_function

from threading import Thread

import requests
import json
import time
import traceback
import logging
import StateDatabase.couchDB as couchDB
import MyUtils.MyUtils as MyUtils

db_handler = couchDB.CouchDBServer()
rescaler_http_session = requests.Session()
RESOURCES = ["cpu", "mem", "net", "disk"]
translate_map = {
    "cpu": {"metric": "structure.cpu.current", "limit_label": "effective_cpu_limit"},
    "mem": {"metric": "structure.mem.current", "limit_label": "mem_limit"},
    "disk": {"metric": "structure.disk.current", "limit_label": "disk_read_limit"},  # FIXME missing write value
    "net": {"metric": "structure.net.current", "limit_label": "net_limit"}
}
SERVICE_NAME = "structures_snapshoter"
CONFIG_DEFAULT_VALUES = {"POLLING_FREQUENCY": 10, "DEBUG": True}
MAX_FAIL_NUM = 5
debug = True


def generate_timeseries(container_name, resources):
    timestamp = int(time.time())

    for resource in RESOURCES:
        value = resources[resource][translate_map[resource]["limit_label"]]
        metric = translate_map[resource]["metric"]
        timeseries = dict(metric=metric, value=value, timestamp=timestamp, tags=dict(host=container_name))

        print(json.dumps(timeseries))


def update_container_current_values(container_name, resources):
    database_structure = db_handler.get_structure(container_name)
    new_structure = MyUtils.copy_structure_base(database_structure)
    new_structure["resources"] = dict()
    for resource in RESOURCES:
        if resource not in new_structure:
            new_structure["resources"][resource] = dict()

        new_structure["resources"][resource]["current"] = resources[resource][
            translate_map[resource]["limit_label"]]

    MyUtils.update_structure(new_structure, db_handler, debug, max_tries=3)


def thread_persist_container(container):
    container_name = container["name"]

    # Try to get the container resources, if unavailable, continue with others
    resources = MyUtils.get_container_resources(container, rescaler_http_session, debug)
    if not resources:
        MyUtils.logging_error("Couldn't get container's {0} resources".format(container_name), debug)
        return

    # Persist by updating the Database current value
    update_container_current_values(container_name, resources)

    # Persist through time series sent to OpenTSDB
    # generate_timeseries(container_name, resources)


def persist_containers():
    # Try to get the containers, if unavailable, return
    containers = MyUtils.get_structures(db_handler, debug, subtype="container")
    if not containers:
        return

    # Retrieve each container resources, persist them and store them to generate host info
    container_resources_dict = dict()

    # UNTHREADED, allows cacheable container information
    # for container in containers:
    #    thread_persist_container(container, container_resources_dict)
    # return container_resources_dict

    # THREADED, doesn't allow cacheable container information
    threads = []
    for container in containers:
        process = Thread(target=thread_persist_container, args=(container,))
        process.start()
        threads.append(process)

    for process in threads:
        process.join()


def persist_applications(container_resources_dict):
    # Try to get the applications, if unavailable, return
    applications = MyUtils.get_structures(db_handler, debug, subtype="application")
    if not applications:
        return

    # Generate the applications current resource values
    for app in applications:
        for resource in RESOURCES:
            app["resources"][resource]["current"] = 0

        application_containers = app["containers"]
        for container_name in application_containers:

            if container_name not in container_resources_dict:
                MyUtils.logging_error(
                    "Container info {0} is missing for app : {1}".format(container_name, app["name"])
                    + " app info will not be totally accurate", debug)
                continue

            for resource in RESOURCES:
                try:
                    current_resource_label = translate_map[resource]["limit_label"]
                    container_resources = container_resources_dict[container_name]["resources"]
                    app["resources"][resource]["current"] += container_resources[resource][current_resource_label]
                except KeyError:
                    if "name" in container_resources_dict[container_name] and "name" in app:
                        MyUtils.logging_error(
                            "Container info {0} is missing for app : {1} and resource {2} resource,".format(
                                container_name, app["name"], resource)
                            + " app info will not be totally accurate", debug)
                    else:
                        MyUtils.logging_error("Error with app or container info", debug)
                        # TODO this error should be more self-explanatory

        MyUtils.update_structure(app, db_handler, debug)


def get_container_resources_dict():
    containers = MyUtils.get_structures(db_handler, debug, subtype="container")
    if not containers:
        return

    # Retrieve each container resources, persist them and store them to generate host info
    container_resources_dict = dict()
    host_node_resources_dict = dict()

    for container in containers:
        container_name = container["name"]
        container_host_name = container["host"]

        if container_host_name not in host_node_resources_dict:
            container_host_ip = container["host_rescaler_ip"]
            container_host_port = container["host_rescaler_port"]
            container_host_resources = MyUtils.get_host_containers(container_host_ip, container_host_port,
                                                                   rescaler_http_session, debug)

            host_node_resources_dict[container_host_name] = container_host_resources

        if container_name in host_node_resources_dict[container_host_name]:
            resources = host_node_resources_dict[container_host_name][container_name]
            # resources = MyUtils.get_container_resources(container, rescaler_http_session, debug)
            container_resources_dict[container_name] = container
            container_resources_dict[container_name]["resources"] = resources
        else:
            MyUtils.logging_error("Couldn't get container's {0} resources".format(container_name), debug)

    return container_resources_dict


def persist_thread():
    # Process and measure time
    epoch_start = time.time()

    # UNTHREDAED for cacheable container information
    # container_resources_dict = persist_containers()
    # persist_applications(container_resources_dict)

    # FULLY THREADED, more requests but faster due to parallelism
    persist_containers()
    container_resources_dict = get_container_resources_dict()
    persist_applications(container_resources_dict)

    epoch_end = time.time()
    processing_time = epoch_end - epoch_start
    MyUtils.logging_info("It took {0} seconds to snapshot structures".format(str("%.2f" % processing_time)), debug)


def persist():
    logging.basicConfig(filename=SERVICE_NAME + '.log', level=logging.INFO)

    global debug
    while True:
        # Get service info
        service = MyUtils.get_service(db_handler, SERVICE_NAME)

        # Heartbeat
        MyUtils.beat(db_handler, SERVICE_NAME)

        # CONFIG
        config = service["config"]
        polling_frequency = MyUtils.get_config_value(config, CONFIG_DEFAULT_VALUES, "POLLING_FREQUENCY")
        debug = MyUtils.get_config_value(config, CONFIG_DEFAULT_VALUES, "DEBUG")

        thread = Thread(target=persist_thread, args=())
        thread.start()
        MyUtils.logging_info("Structures snapshoted at {0}".format(MyUtils.get_time_now_string()), debug)
        time.sleep(polling_frequency)

        if thread.isAlive():
            delay_start = time.time()
            MyUtils.logging_warning(
                "Previous thread didn't finish before next poll is due, with polling time of {0} seconds, at {1}".format(
                    str(polling_frequency), MyUtils.get_time_now_string()), debug)
            MyUtils.logging_warning("Going to wait until thread finishes before proceeding", debug)
            thread.join()
            delay_end = time.time()
            MyUtils.logging_warning("Resulting delay of: {0} seconds".format(str(delay_end - delay_start)), debug)


def main():
    try:
        persist()
    except Exception as e:
        MyUtils.logging_error("{0} {1}".format(str(e), str(traceback.format_exc())), debug=True)


if __name__ == "__main__":
    main()
