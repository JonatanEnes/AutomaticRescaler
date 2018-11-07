# /usr/bin/python
import StateDatabase.couchDB as couchDB
import StateDatabase.initializers.initializer_utils as couchdb_utils

initializer_utils = couchdb_utils.CouchDBUtils()
handler = couchDB.CouchDBServer()
database = "structures"
initializer_utils.remove_db(database)
initializer_utils.create_db(database)

containers = [("node0", "c14-13"), ("node1", "c14-13"), ("node2", "c14-13"), ("node3", "c14-13"), ("node4", "c14-13"),
              ("node5", "c14-13"), ("node6", "c14-12"), ("node7", "c14-12"), ("node8", "c14-12"), ("node9", "c14-12"),
              ("node10", "c14-12"), ("node11", "c14-12")]
hosts = ["c14-13", "c14-12"]

# CREATE STRUCTURES
if handler.database_exists("structures"):
    print("Adding 'structures' documents")
    for c in containers:
        container_name, container_host = c
        container = dict(
            type='structure',
            subtype='container',
            guard_policy="serverless",
            host=container_host,
            host_rescaler_ip=container_host,
            host_rescaler_port='8000',
            name=container_name,
            guard=True,
            resources=dict(
                cpu=dict(max=200, min=40, fixed=150, guard=True),
                mem=dict(max=10240, min=1024, fixed=6144, guard=True),
                disk=dict(max=100, min=20, guard=False),
                net=dict(max=200, min=100, guard=False),
                energy=dict(max=20, min=0, guard=False)
            )
        )
        handler.add_structure(container)

    for h in hosts:
        host = dict(
            type='structure',
            subtype='host',
            name=h,
            host=h,
            resources=dict(
                cpu=dict(max=1200),
                mem=dict(max=49152)
            )
        )
        handler.add_structure(host)

    app = dict(
        type='structure',
        subtype='application',
        name="app1",
        guard=True,
        guard_policy="serverless",
        resources=dict(
            cpu=dict(max=1200, min=400, guard=False),
            mem=dict(max=49152, min=24576, guard=False),
            disk=dict(max=600, min=120, guard=False),
            net=dict(max=1200, min=600, guard=False),
            energy=dict(max=120, min=0, guard=True)
        ),
        containers=["node0", "node1", "node2", "node3", "node4", "node5", "node6", "node7", "node8", "node9", "node10",
                    "node11"]
    )
    handler.add_structure(app)
