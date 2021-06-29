#!/usr/bin/env bash
#
# Usage:
#
# submitMerge.sh [options]
#
# Options:
# * input path (required)       The the input folder.
# * output path (required)      The the output folder.

set -e -x

INPUT_PATH=${1:-'capstone_preprocessing'}
OUTPUT_PATH=${2:-"capstone_merge"}


SPARK_OPTIONS="--master yarn --deploy-mode cluster \
--queue prd-etl --conf spark.dynamicAllocation.enabled=true \
--conf spark.dynamicAllocation.initialExecutors=1 \
--conf spark.dynamicAllocation.maxExecutors=10 \
--executor-memory 12g --conf spark.files.overwrite=true \
--conf spark.executor.memoryOverhead=4g \
--driver-memory 4g  --conf spark.shuffle.blockTransferService=nio \
--conf spark.sql.warehouse.dir=./spark-warehouse --conf spark.eventLog.enabled=true \
--conf spark.eventLog.dir=hdfs://xplosion/user/spark/spark2ApplicationHistory \
--conf spark.shuffle.service.enabled=true"
#

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


JAR_FILE=$(ls target | grep uber)
# assuming spark 2.3+
/opt/spark/bin/spark-submit ${SPARK_OPTIONS} --class blog.murawski.Merge target/${JAR_FILE} \
--inputPath ${INPUT_PATH} \
--outputPath ${OUTPUT_PATH}
