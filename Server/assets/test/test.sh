#!/bin/sh

TARGET_DIR=$(dirname $(readlink -f "${BASH_SOURCE[0]}"))

COMMAND="python ${TARGET_DIR}/test.py"

${COMMAND}