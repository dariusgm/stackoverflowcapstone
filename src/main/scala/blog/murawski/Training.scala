package blog.murawski

import org.apache.spark.ml.classification.LogisticRegression
import org.apache.spark.ml.feature.VectorAssembler
import org.apache.spark.sql.functions.col
import org.apache.spark.sql.{DataFrame, SparkSession}


object Training {
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
      .appName("Training on capstone")
      .getOrCreate()

    run(options)
  }


  def fitAssembler(df: DataFrame, columns: Array[String]): DataFrame = {
    new VectorAssembler().setInputCols(columns).setOutputCol(featureColumn).transform(df)
  }

  def run(options: AppOptions)(implicit spark: SparkSession): Unit = {
    spark.sparkContext.setLogLevel("ERROR")

    val inputPath = options.inputPath
    val df = spark.read.parquet(inputPath)

    val dfs = df.randomSplitAsList(Array(trainSplit, testSplit, hyperparameterSplit), seed = 42)
    val trainDf = dfs.get(0).cache()
    val testDf = dfs.get(1).cache()
    val hyperparameterDf = dfs.get(2).cache()
    val fittedAssember = fitAssembler(trainDf, trainDf.columns)
    val trainPair = fittedAssember.select(col(labelColumn), col(featureColumn))
    val lr = new LogisticRegression()
      .setMaxIter(10)
      .setRegParam(0.3)
      .setElasticNetParam(0.8)
      .setLabelCol(labelColumn)
      .setFeaturesCol(featureColumn)

    val lrModel = lr.fit(trainPair)

    lrModel.save(options.outputPath)

  }
}