# /usr/bin/python
import StateDatabase.couchDB as couchDB

handler = couchDB.CouchDBServer()

c14_13_resources = {
    "mem": {
        "max": 61440,
        "free": 0
    },
    "cpu": {
        "core_usage_mapping": {
            "0": {
                "node0": 100,
                "free": 0
            },
            "1": {
                "node0": 100,
                "free": 0
            },
            "2": {
                "node1": 100,
                "free": 0
            },
            "3": {
                "node1": 100,
                "free": 0
            },
            "4": {
                "node2": 100,
                "free": 0
            },
            "5": {
                "node2": 100,
                "free": 0
            },
            "6": {
                "node3": 100,
                "free": 0
            },
            "7": {
                "node3": 100,
                "free": 0
            },
            "8": {
                "node4": 100,
                "free": 0
            },
            "9": {
                "node4": 100,
                "free": 0
            },
            "10": {
                "node5": 100,
                "free": 0
            },
            "11": {
                "node5": 100,
                "free": 0
            }
        },
        "max": 1200,
        "free": 0
    }
}

c14_12_resources = {
    "mem": {
        "max": 61440,
        "free": 0
    },
    "cpu": {
        "core_usage_mapping": {
            "0": {
                "node6": 100,
                "free": 0
            },
            "1": {
                "node6": 100,
                "free": 0
            },
            "2": {
                "node7": 100,
                "free": 0
            },
            "3": {
                "node7": 100,
                "free": 0
            },
            "4": {
                "node8": 100,
                "free": 0
            },
            "5": {
                "node8": 100,
                "free": 0
            },
            "6": {
                "node9": 100,
                "free": 0
            },
            "7": {
                "node9": 100,
                "free": 0
            },
            "8": {
                "node10": 100,
                "free": 0
            },
            "9": {
                "node10": 100,
                "free": 0
            },
            "10": {
                "node11": 100,
                "free": 0
            },
            "11": {
                "node11": 100,
                "free": 0
            }
        },
        "max": 1200,
        "free": 0
    }
}

c14_13 = handler.get_structure("c14-13")
c14_13["resources"] = c14_13_resources
handler.update_structure(c14_13)

c14_12 = handler.get_structure("c14-12")
c14_12["resources"] = c14_12_resources
handler.update_structure(c14_12)
