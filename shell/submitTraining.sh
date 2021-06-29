#!/usr/bin/env bash
#
# Usage:
#
# submitTraining.sh [options]
#
# Options:
# * input path (required)       The the input folder.
# * output path (required)      The the output folder.

set -e -x

INPUT_PATH=${1:-"capstone_merge"}
OUTPUT_PATH=${2:-"capstone_train"}
JAR_FILE=${3}

SPARK_OPTIONS="--master yarn --deploy-mode cluster \
--queue prd-etl --conf spark.dynamicAllocation.enabled=true \
--conf spark.dynamicAllocation.initialExecutors=1 \
--conf spark.dynamicAllocation.maxExecutors=10 \
--executor-memory 16g --conf spark.files.overwrite=true \
--conf spark.executor.memoryOverhead=0g \
--driver-memory 4g  --conf spark.shuffle.blockTransferService=nio \
--conf spark.sql.warehouse.dir=./spark-warehouse --conf spark.eventLog.enabled=true \
--conf spark.eventLog.dir=hdfs://xplosion/user/spark/spark2ApplicationHistory \
--conf spark.shuffle.service.enabled=true"
#

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------



# assuming spark 2.3+
/opt/spark/bin/spark-submit ${SPARK_OPTIONS} --class blog.murawski.Training target/${JAR_FILE} \
--inputPath ${INPUT_PATH} \
--outputPath ${OUTPUT_PATH}
