#!/usr/bin/env bash
./shell/build.sh
./shell/copy_hdfs.sh
./shell/submitPreprocessing.sh capstone capstone
./shell/submitMerge.sh capstone capstone