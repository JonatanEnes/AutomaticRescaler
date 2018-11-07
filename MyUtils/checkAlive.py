# /usr/bin/python
import time
import requests
import StateDatabase.couchDB as couchDB

time_window_allowed = 30  # seconds
POLLING_TIME = 5
REST_SERVICES = [("orchestrator", "orchestrator", "5000"), ("c14-13-rescaler", "c14-13-rescaler", "8000"),
                 ("c14-12-rescaler", "c14-12-rescaler", "8000")]


def check_rest_api(service_endpoint, service_port):
    try:
        endpoint = "http://{0}:{1}/heartbeat".format(service_endpoint, service_port)
        r = requests.get(endpoint, headers={'Accept': 'application/json'}, timeout=2)
        if r.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.ConnectionError:
        print("WARNING -> host at {0} is unresponsive".format(service_endpoint))
        return False
    except Exception:
        return False


def classify_service(service_name):
    if service_name.startswith("Atop"):
        return "Atops"
    elif service_name.startswith("Turbostat"):
        return "Turbostats"
    elif service_name.endswith("rescaler"):
        return "Node-Rescalers"
    else:
        return "Others"


def print_services(services):
    for service_type in services:
        if services[service_type]:
            print("\t-- {0} --".format(service_type))
            for s in services[service_type]:
                print("\t" + s)
            print("")


def service_is_alive(service, time_window):
    if "heartbeat" not in service:
        return False
    elif not isinstance(service["heartbeat"], int) and not isinstance(service["heartbeat"], float):
        return False
    elif int(service["heartbeat"]) <= 0:
        return False
    elif service["heartbeat"] < time.time() - time_window:
        return False
    else:
        return True


def main():
    db = couchDB.CouchDBServer()
    while True:

        dead, alive = list(), list()
        services = db.get_services()

        for service in services:
            if service_is_alive(service, time_window_allowed):
                alive.append(service["name"])
            else:
                dead.append(service["name"])

        for REST_service in REST_SERVICES:
            service_name, service_endpoint, service_port = REST_service
            if check_rest_api(service_endpoint, service_port):
                alive.append(service_name)
            else:
                dead.append(service_name)

        print("AT: " + str(time.strftime("%D %H:%M:%S", time.localtime())))
        print("")

        print("!---- ALIVE ------!")
        alive_services = {"Atops": list(), "Turbostats": list(), "Node-Rescalers": list(), "Others": list()}
        for a in alive:
            alive_services[classify_service(a)].append(a)
        print_services(alive_services)
        print("")

        print("!---- DEAD -------!")
        dead_services = {"Atops": list(), "Turbostats": list(), "Node-Rescalers": list(), "Others": list()}
        for d in dead:
            dead_services[classify_service(d)].append(d)
        print_services(dead_services)
        print("")

        time.sleep(POLLING_TIME)


if __name__ == "__main__":
    main()
