#!/usr/bin/env bash
echo "Building Jar"
USER=$(whoami)
mvn -Djavacpp.platform=linux-x86_64 -DskipTests clean package
scp -o StrictHostKeyChecking=no -o LogLevel=ERROR -o UserKnownHostsFile=/dev/null target/capstone-*uberjar.jar linux-rdp4:~/$USER/capstone.jar