#!/usr/bin/env bash
DEV_PATH=$HOME/development
RESCALER_PATH=$DEV_PATH/automatic-rescaler
BDWACHDOG_PATH=$DEV_PATH/metrics-to-time-series
export PYTHONPATH=$RESCALER_PATH:$BDWACHDOG_PATH

tmux new -d -s "Guardian" "python Guardian/Guardian.py"
tmux new -d -s "Scaler" "python Rescaler/ClusterScaler.py"
tmux new -d -s "SanityChecker" "python SanityChecker/SanityChecker.py"

