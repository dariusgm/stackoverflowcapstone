#!/usr/bin/env bash
echo "copy source to cluster"
set -e -x

USER=$(whoami)
ssh -o StrictHostKeyChecking=no -o LogLevel=ERROR -o UserKnownHostsFile=/dev/null linux-rdp4 -C "mkdir -p ~/$USER/"
scp -o StrictHostKeyChecking=no -o LogLevel=ERROR -o UserKnownHostsFile=/dev/null Pipfile linux-rdp4:~/$USER/Pipfile
scp -o StrictHostKeyChecking=no -o LogLevel=ERROR -o UserKnownHostsFile=/dev/null Pipfile.lock linux-rdp4:~/$USER/Pipfile.lock
scp -o StrictHostKeyChecking=no -o LogLevel=ERROR -o UserKnownHostsFile=/dev/null *.py linux-rdp4:~/$USER/
scp -o StrictHostKeyChecking=no -o LogLevel=ERROR -o UserKnownHostsFile=/dev/null *.sh linux-rdp4:~/$USER/
scp -o StrictHostKeyChecking=no -o LogLevel=ERROR -o UserKnownHostsFile=/dev/null pom.xml linux-rdp4:~/$USER/
scp -r -o StrictHostKeyChecking=no -o LogLevel=ERROR -o UserKnownHostsFile=/dev/null src linux-rdp4:~/$USER/src
