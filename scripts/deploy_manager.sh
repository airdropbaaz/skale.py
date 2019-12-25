#!/usr/bin/env bash

set -e

: "${ETH_PRIVATE_KEY?Need to set ETH_PRIVATE_KEY}"
: "${DOCKER_USERNAME?Need to set DOCKER_USERNAME}"
: "${DOCKER_PASSWORD?Need to set DOCKER_PASSWORD}"
: "${MANAGER_BRANCH?Need to set MANAGER_BRANCH}"

docker run -d -p 8545:8545 --name ganache trufflesuite/ganache-cli:latest  \
    --account="${ETH_PRIVATE_KEY},100000000000000000000000000" -l 80000000

docker ps -a
curl 127.0.0.1:8545

echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin

export DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

docker run \
    -v $DIR/contracts_data:/usr/src/manager/data \
    --network host -it \
    skalelabshub/skale-manager:$MANAGER_BRANCH-latest \
    npx truffle migrate --network test

cp $DIR/contracts_data/test.json $DIR/../test_abi.json
