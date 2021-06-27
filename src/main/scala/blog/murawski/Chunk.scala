package blog.murawski

import org.apache.hadoop.fs.{FileSystem, Path}
import org.apache.spark.sql.functions.col
import org.apache.spark.sql.{DataFrame, SparkSession}



object Chunk {
  def main(args: Array[String]): Unit = {
    val options = AppOptions.options(args.toSeq)

    implicit val spark: SparkSession = SparkSession
      .builder()
      .appName("Preprocess Chunk for spark")
      .getOrCreate()

    run(options)
  }

  def preprocessing(path: String)(implicit spark: SparkSession): DataFrame = {
    var preprocesing = spark
      .read
      .json(path)

    for (column <- preprocesing.columns) {
      // Removing rejected chars for spark
      var cleanedName = column.replace(".", "")
      // Removing rejected chars for parquet
      for (t <- Seq(" ", ",", ";", "{", "}", "(", ")", "\n", "\t")) {
        cleanedName = cleanedName.replace(t, "")
      }

      preprocesing = preprocesing.withColumnRenamed(column, cleanedName).withColumn(cleanedName, col(cleanedName).cast("float"))
    }

    preprocesing.show(10, false)

    println("renaming complete")
    preprocesing = preprocesing.na.fill(0.0).cache()
    println("filling complete")
    println("write complete")
    preprocesing
  }

  def run(options: AppOptions)(implicit spark: SparkSession): Unit = {
    // spark.sparkContext.setLogLevel("ERROR")
    val conf = spark.sparkContext.hadoopConfiguration
    val fs = FileSystem.get(conf)
    val files = fs.listFiles(new Path("cache"), false)

    val preprocessingDf = preprocessing("")

    preprocessingDf.printSchema()
    preprocessingDf.show(10, false)
    print(preprocessingDf.count())

    preprocessingDf.write.parquet(options.outputPath)

  }
}