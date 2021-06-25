#!/usr/bin/env bash
echo "copy data to cluster"
set -e -x
mvn -Djavacpp.platform=linux-x86_64 -DskipTests clean package

USER=$(whoami)
ssh -o StrictHostKeyChecking=no -o LogLevel=ERROR -o UserKnownHostsFile=/dev/null linux-rdp3 -C "mkdir -p ~/$USER/"
scp -o StrictHostKeyChecking=no -o LogLevel=ERROR -o UserKnownHostsFile=/dev/null target/capstone-*uberjar.jar linux-rdp3:~/$USER/capstone.jar
scp -o StrictHostKeyChecking=no -o LogLevel=ERROR -o UserKnownHostsFile=/dev/null src/main/resources/shell/* airflow@airflow-m1-smarties:~/$USER/