#!/usr/bin/env bash

set -e

# Default values
PYTHON_EXEC=${PYTHON_EXEC:-python3}
VENV_DIR=${VENV_DIR:-venv}

# Update VENV if it changed or does not exist
REQUIREMENTS_HASH=$(md5sum requirements.txt)
EXISTING_REQUIREMENTS_HASH=$(cat ${VENV_DIR}/requirements.md5 2>/dev/null || true)

if [ ! "${REQUIREMENTS_HASH}" = "${EXISTING_REQUIREMENTS_HASH}" ]; then
	PYTHON_V=$(${PYTHON_EXEC} version-check.py)
	${PYTHON_EXEC} -m venv ${VENV_DIR}
	./${VENV_DIR}/bin/pip install --upgrade pip setuptools
	./${VENV_DIR}/bin/pip install -r requirements.txt
	echo -n "${REQUIREMENTS_HASH}" > ${VENV_DIR}/requirements.md5
fi

# Run program
CMD="./${VENV_DIR}/bin/python hab_server.py"

exec ${CMD}
