package blog.murawski

import org.apache.hadoop.fs.{FileSystem, Path}
import org.apache.spark.sql.{SaveMode, SparkSession}


object Merge {
  val trainSplit = 0.7
  val testSplit = 0.2
  val hyperparameterSplit = 0.1
  val labelColumn = "ConvertedComp"
  val dropNAlabelColumn = "ConvertedComp_NA"
  val featureColumn = "features"


  def main(args: Array[String]): Unit = {
    val options = AppOptions.options(args.toSeq)

    implicit val spark: SparkSession = SparkSession
      .builder()
      .appName("Merge all parts together as total df")
      .getOrCreate()

    run(options)
  }

  def run(options: AppOptions)(implicit spark: SparkSession): Unit = {
    spark.sparkContext.setLogLevel("ERROR")
    println("Merging")
    val conf = spark.sparkContext.hadoopConfiguration
    val fs = FileSystem.get(conf)
    val inputPath = options.inputPath
    val files = fs.listStatus(new Path(inputPath))
    val parquetFiles = files.filter(_.getPath.getName.contains(".parquet"))

    val dfs = parquetFiles.map(
      file => {
        val fileName = inputPath + "/" + file.getPath.getName
        val data = spark.read.parquet(fileName)
        (fileName, data)
      })

    // extract labels
    val labelFile = dfs
      .filter { case (fileName, _data) => fileName.contains(labelColumn) }
      .map { case (_fileName, data) => data }.head

    val broadcastedLabels = spark.sparkContext.broadcast(labelFile)

    // Process all features
      dfs
        .filter { case (fileName, _data) => !fileName.contains(labelColumn) }
        .foreach { case (fileName, data) =>
          val outputPath = options.outputPath + "/" + fileName.split("/").reverse.head
          data.join(broadcastedLabels.value, "Respondent")
            .write.mode(SaveMode.Overwrite).parquet(outputPath)
        }
  }
}