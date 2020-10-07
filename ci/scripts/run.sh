#!/bin/bash

die() {
	echo $* >&2
	exit 1
}

banner() {
	echo
	echo "*** $* ***"
	echo
}

# Wait on deps to start
./ci/scripts/start-deps.sh || die "Can't start dependencies"

banner "Running build-specific setup"

banner "Building tests"

# Run the tests and clean up
docker-compose -f ci/docker-compose.yml build tests
EXIT_CODE=$?

if [[ $EXIT_CODE -eq 0 ]]; then
	banner "Running tests"
	docker-compose -f ci/docker-compose.yml run tests
	EXIT_CODE=$?
	echo "Exited with exit code '${EXIT_CODE}'"
fi

if [[ $EXIT_CODE -eq 0 ]]; then
	banner "Running linter"
	docker-compose -f ci/docker-compose.yml run tests flake8
	EXIT_CODE=$?
	echo "Exited with exit code '${EXIT_CODE}'"
fi

test $EXIT_CODE -eq 0 || banner "FAILED"

banner "Cleaning up"
docker-compose -f ci/docker-compose.yml down

# Make sure we fail if the tests run failed
exit $EXIT_CODE