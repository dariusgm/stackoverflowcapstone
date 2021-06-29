package blog.murawski

import org.apache.hadoop.fs.{FileSystem, Path}
import org.apache.spark.sql.functions.col
import org.apache.spark.sql.{SaveMode, SparkSession}


object Preprocessing {
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
      .appName("Preprocessing")
      .getOrCreate()

    run(options)
  }

  def renameColumns(inputName: String): String = {
    // Removing rejected chars for spark
    var cleanedName = inputName.replace(".", "")
    // Removing rejected chars for parquet
    for (t <- Seq(" ", ",", ";", "{", "}", "(", ")", "\n", "\t")) {
      cleanedName = cleanedName.replace(t, "")
    }

    cleanedName

  }

  private def columnPreprocessing(path: String, outputPath: String)(implicit spark: SparkSession) = {
    var df = spark
      .read
      .json(path)

    for (column <- df.columns) {
      val cleanedName = renameColumns(column)

      // Removing rejected chars for parquet
      df = df.withColumnRenamed(column, cleanedName).withColumn(cleanedName, col(cleanedName).cast("float"))
    }
    df
      .na
      .fill(0.0)
      .write
      .mode(SaveMode.Overwrite)
      .parquet(outputPath)
  }

  private def labelPreproccessing(path: String, outputPath: String)(implicit spark: SparkSession) = {
    var df = spark
      .read
      .json(path)
      .filter(col(labelColumn).isNotNull)
      .drop(dropNAlabelColumn)

    for (column <- df.columns) {
      val cleanedName = renameColumns(column)
      df = df.withColumnRenamed(column, cleanedName).withColumn(cleanedName, col(cleanedName).cast("float"))
    }

    df
      .write
      .mode(SaveMode.Overwrite)
      .parquet(outputPath)
  }

  def run(options: AppOptions)(implicit spark: SparkSession): Unit = {
    spark.sparkContext.setLogLevel("ERROR")
    val conf = spark.sparkContext.hadoopConfiguration
    val fs = FileSystem.get(conf)

    val files = fs.listStatus(new Path(options.inputPath))
    for (f <- files) {
      if (f.isFile) {
        val path = options.inputPath + "/" + f.getPath.getName
        val outputPath = f.getPath.getName.replace(".json", ".parquet")

        println(path)
        if (path.contains(labelColumn)) {
          labelPreproccessing(path, options.outputPath + "/" + outputPath)
        } else {
          columnPreprocessing(path, options.outputPath + "/" + outputPath)
        }
      }
    }
  }
}