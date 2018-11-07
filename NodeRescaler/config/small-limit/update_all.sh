#!/usr/bin/env bash

nodes=( node0 node1 node2 node3 node4 node5 )
for i in "${nodes[@]}"
do
	curl -X PUT -H "Content-Type: application/json" -d @$HOME/production/automatic-rescaler/NodeRescaler/config/small-limit/$i.json http://c14-13:8000/container/$i
    echo
done

nodes=( node6 node7 node8 node9 node10 node11 )
for i in "${nodes[@]}"
do
	curl -X PUT -H "Content-Type: application/json" -d @$HOME/production/automatic-rescaler/NodeRescaler/config/small-limit/$i.json http://c14-12:8000/container/$i
    echo
done


#curl -X PUT -H "Content-Type: application/json" -d @$HOME/production/automatic-rescaler/NodeRescaler/config/small-limit/node0.json http://c14-13:8000/container/node0
#curl -X PUT -H "Content-Type: application/json" -d @$HOME/production/automatic-rescaler/NodeRescaler/config/small-limit/node1.json http://c14-13:8000/container/node1
#curl -X PUT -H "Content-Type: application/json" -d @$HOME/production/automatic-rescaler/NodeRescaler/config/small-limit/node2.json http://c14-13:8000/container/node2
#curl -X PUT -H "Content-Type: application/json" -d @$HOME/production/automatic-rescaler/NodeRescaler/config/small-limit/node3.json http://c14-13:8000/container/node3
#curl -X PUT -H "Content-Type: application/json" -d @$HOME/production/automatic-rescaler/NodeRescaler/config/small-limit/node4.json http://c14-13:8000/container/node4
#curl -X PUT -H "Content-Type: application/json" -d @$HOME/production/automatic-rescaler/NodeRescaler/config/small-limit/node5.json http://c14-13:8000/container/node5
#
#curl -X PUT -H "Content-Type: application/json" -d @$HOME/production/automatic-rescaler/NodeRescaler/config/small-limit/node6.json http://c14-12:8000/container/node6
#curl -X PUT -H "Content-Type: application/json" -d @$HOME/production/automatic-rescaler/NodeRescaler/config/small-limit/node7.json http://c14-12:8000/container/node7
#curl -X PUT -H "Content-Type: application/json" -d @$HOME/production/automatic-rescaler/NodeRescaler/config/small-limit/node8.json http://c14-12:8000/container/node8
#curl -X PUT -H "Content-Type: application/json" -d @$HOME/production/automatic-rescaler/NodeRescaler/config/small-limit/node9.json http://c14-12:8000/container/node9
#curl -X PUT -H "Content-Type: application/json" -d @$HOME/production/automatic-rescaler/NodeRescaler/config/small-limit/node10.json http://c14-12:8000/container/node10
#curl -X PUT -H "Content-Type: application/json" -d @$HOME/production/automatic-rescaler/NodeRescaler/config/small-limit/node11.json http://c14-12:8000/container/node11

