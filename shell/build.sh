#!/usr/bin/env bash
echo "Building Jar"
mvn -Djavacpp.platform=linux-x86_64 -DskipTests clean package
