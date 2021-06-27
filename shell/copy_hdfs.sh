#!/usr/bin/env bash
echo "copy data to cluster"
set -e -x

hdfs dfs -mkdir -p  capstone
hdfs dfs -copyFromLocal cache/*.json capstone