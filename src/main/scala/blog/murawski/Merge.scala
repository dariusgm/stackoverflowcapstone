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
    val files = fs.listStatus(new Path(options.inputPath))
    val parquetFiles = files.filter(_.getPath.getName.contains(".parquet"))
    val dfs = parquetFiles.map(file => spark.read.parquet(options.inputPath + "/" + file.getPath.getName))
    val joined = dfs.reduce((a, b) => {
      a.join(b, "Respondent")
    })

    joined.drop("Respondent").write.mode(SaveMode.Overwrite).parquet(options.outputPath + "/" + "total.parquet")

  }
}