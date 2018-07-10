# /usr/bin/python
import StateDatabase.couchDB as couchDB
import StateDatabase.initializers.initializer_utils as CouchDB_Utils

initializer_utils = CouchDB_Utils.CouchDB_Utils()
handler = couchDB.CouchDBServer()
database = "rules"
initializer_utils.remove_db(database)
initializer_utils.create_db(database)

# CREATE RULES
if handler.database_exists("rules"):
    print ("Adding 'rules' documents")

    # CPU
    cpu_exceeded_upper = dict(
        _id='cpu_exceeded_upper',
        type='rule',
        resource="cpu",
        name='cpu_exceeded_upper',
        rule=dict(
            {"and": [
                {">": [
                    {"var": "structure.cpu.usage"},
                    {"var": "limits.cpu.upper"}]},
                {"<": [
                    {"var": "limits.cpu.upper"},
                    {"var": "structure.cpu.max"}]},
                {"<": [
                    {"var": "structure.cpu.current"},
                    {"var": "structure.cpu.max"}]}
                ]
            }),
        generates="events", action={"events": {"scale": {"up": 1}}},
        active=True
    )

    cpu_dropped_lower = dict(
        _id='cpu_dropped_lower',
        type='rule',
        resource="cpu",
        name='cpu_dropped_lower',
        rule=dict(
            {"and": [
                {">": [
                    {"var": "structure.cpu.usage"},
                    0]},
                {"<": [
                    {"var": "structure.cpu.usage"},
                    {"var": "limits.cpu.lower"}]},
                {">": [
                    {"var": "limits.cpu.lower"},
                    {"var": "structure.cpu.min"}]}]}),
        generates="events",
        action={"events": {"scale": {"down": 1}}},
        active=True
    )

    handler.add_rule(cpu_exceeded_upper)
    handler.add_rule(cpu_dropped_lower)

    # Avoid hysteresis by only rescaling when X underuse events and no bottlenecks are detected, or viceversa
    CpuRescaleUp = dict(
        _id='CpuRescaleUp',
        type='rule',
        resource="cpu",
        name='CpuRescaleUp',
        rule=dict(
            {"and": [
                {">": [
                    {"var": "events.scale.up"},
                    2]},
                {"<=": [
                    {"var": "events.scale.down"},
                    2]}
            ]}),
        events_to_remove=2,
        generates="requests",
        action={"requests": ["CpuRescaleUp"]},
        amount=75,
        rescale_by="amount",
        active=True
    )

    CpuRescaleDown = dict(
        _id='CpuRescaleDown',
        type='rule',
        resource="cpu",
        name='CpuRescaleDown',
        rule=dict(
            {"and": [
                {">": [
                    {"var": "events.scale.down"},
                    8]},
                {"==": [
                    {"var": "events.scale.up"},
                    0]}
            ]}),
        events_to_remove=8,
        generates="requests",
        action={"requests": ["CpuRescaleDown"]},
        amount=-20,
        rescale_by="fit_to_usage",
        active=True,
    )

    handler.add_rule(CpuRescaleUp)
    handler.add_rule(CpuRescaleDown)

    # MEM
    mem_exceeded_upper = dict(
        _id='mem_exceeded_upper',
        type='rule',
        resource="mem",
        name='mem_exceeded_upper',
        rule=dict(
            {"and": [
                {">": [
                    {"var": "structure.mem.usage"},
                    {"var": "limits.mem.upper"}]},
                {"<": [
                    {"var": "limits.mem.upper"},
                    {"var": "structure.mem.max"}]},
                {"<": [
                    {"var": "structure.mem.current"},
                    {"var": "structure.mem.max"}]}

            ]
            }),
        generates="events",
        action={"events": {"scale": {"up": 1}}},
        active=True
    )

    mem_dropped_lower = dict(
        _id='mem_dropped_lower',
        type='rule',
        resource="mem",
        name='mem_dropped_lower',
        rule=dict(
            {"and": [
                {">": [
                    {"var": "structure.mem.usage"},
                    0]},
                {"<": [
                    {"var": "structure.mem.usage"},
                    {"var": "limits.mem.lower"}]},
                {">": [
                    {"var": "limits.mem.lower"},
                    {"var": "structure.mem.min"}]}]}),
        generates="events",
        action={"events": {"scale": {"down": 1}}},
        active=True
    )

    handler.add_rule(mem_exceeded_upper)
    handler.add_rule(mem_dropped_lower)

    MemRescaleUp = dict(
        _id='MemRescaleUp',
        type='rule',
        resource="mem",
        name='MemRescaleUp',
        rule=dict(
            {"and": [
                {">": [
                    {"var": "events.scale.up"},
                    2]},
                {"<=": [
                    {"var": "events.scale.down"},
                   2]}
            ]}),
        generates="requests",
        events_to_remove=2,
        action={"requests": ["MemRescaleUp"]},
        amount=2048,
        rescale_by="amount",
        active=True
    )

    MemRescaleDown = dict(
        _id='MemRescaleDown',
        type='rule',
        resource="mem",
        name='MemRescaleDown',
        rule=dict(
            {"and": [
                {">": [
                    {"var": "events.scale.down"},
                    8]},
                {"==": [
                    {"var": "events.scale.up"},
                    0]}
            ]}),
        generates="requests",
        events_to_remove=8,
        action={"requests": ["MemRescaleDown"]},
        amount=-512,
        percentage_reduction=50,
        rescale_by="fit_to_usage",
        active=True
    )

    handler.add_rule(MemRescaleUp)
    handler.add_rule(MemRescaleDown)

    # ENERGY
    energy_exceeded_upper = dict(
        _id='energy_exceeded_upper',
        type='rule',
        resource="energy",
        name='energy_exceeded_upper',
        rule=dict(
            {"and": [
                {">": [
                    {"var": "structure.energy.current"},
                    {"var": "structure.energy.max"}]}]}),
        generates="events", action={"events": {"scale": {"up": 1}}},
        active=True
    )
    handler.add_rule(energy_exceeded_upper)


