package blog.murawski

import org.apache.hadoop.fs.{FileSystem, Path}
import org.apache.spark.ml.classification.{LogisticRegression, LogisticRegressionModel}
import org.apache.spark.ml.feature.VectorAssembler
import org.apache.spark.sql.functions.col
import org.apache.spark.sql.{DataFrame, SaveMode, SparkSession}


object App {
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
      .appName("Merge Spot and View Data")
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

  def columnPreprocessing(path: String, outputPath: String)(implicit spark: SparkSession) = {
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

  def labelPreproccessing(path: String, outputPath: String)(implicit spark: SparkSession) = {
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

  def fitAssembler(df: DataFrame, columns: Array[String]): DataFrame = {
    new VectorAssembler().setInputCols(columns).setOutputCol(featureColumn).transform(df)
  }

  def preprocessing(options: AppOptions)(implicit spark:SparkSession) = {
    val conf = spark.sparkContext.hadoopConfiguration
    val fs = FileSystem.get(conf)

    val files = fs.listStatus(new Path(options.inputPath))
    for (f <- files) {
      if (f.isFile) {
        val path = options.inputPath + "/" + f.getPath.getName

        println(path)
        if (path.contains(labelColumn)) {
          labelPreproccessing(path, path + ".parquet")
        } else {
          columnPreprocessing(path, path + ".parquet")
        }
      }
    }
  }

  def merge(options: AppOptions)(implicit spark:SparkSession) {
    println("Merging")
    val conf = spark.sparkContext.hadoopConfiguration
    val fs = FileSystem.get(conf)
    val files = fs.listStatus(new Path(options.inputPath))
    val parquetFiles = files.filter(_.getPath.getName.contains(".parquet"))
    val dfs = parquetFiles.map(file => spark.read.parquet(options.inputPath + "/" +file.getPath.getName))
    val joined = dfs.reduce((a,b) => {
      a.join(b, "Respondent")
    })

    joined.drop("Respondent").write.mode(SaveMode.Overwrite).parquet("total.parquet")

  }


  def train(options: AppOptions)(implicit spark:SparkSession): Unit = {
    println("Training")
    val dfs = spark
      .read
      .parquet("total.parquet")
      .randomSplitAsList(Array(trainSplit, testSplit, hyperparameterSplit), seed = 42)

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

    lrModel.save("model")

  }

  def run(options: AppOptions)(implicit spark: SparkSession): Unit = {
    spark.sparkContext.setLogLevel("ERROR")
    //preprocessing(options)


    //merge(options)

    train(options)

    /*



    val trainDf = df.get(0).cache()
    val testDf = df.get(1).cache()
    val hyperparameterDf = df.get(2).cache()

    println("total: " + preprocessingDf.count())
    println("Train: " + trainDf.count())
    println("Test: " + testDf.count())
    println("Hyperparameter: " + hyperparameterDf.count())

    val lr = new LogisticRegression()
      .setMaxIter(10)
      .setRegParam(0.3)
      .setElasticNetParam(0.8)
      .setLabelCol(labelColumn)
      .setFeaturesCol(featureColumn)*/

    // Fit the model
    // val lrModel = lr.fit(trainDf)


    //val pmml = new PMMLBuilder(preprocessingDf.schema, lrModel).build()
    //JAXBUtil.marshalPMML(pmml, new StreamResult(System.out))


  }


  def metric(model: LogisticRegressionModel) = {
    // Print the coefficients and intercept for multinomial logistic regression
    println(s"Coefficients: \n${model.coefficientMatrix}")
    println(s"Intercepts: \n${model.interceptVector}")

    val trainingSummary = model.summary

    // Obtain the objective per iteration
    val objectiveHistory = trainingSummary.objectiveHistory
    println("objectiveHistory:")
    objectiveHistory.foreach(println)

    // for multiclass, we can inspect metrics on a per-label basis
    println("False positive rate by label:")
    trainingSummary.falsePositiveRateByLabel.zipWithIndex.foreach { case (rate, label) =>
      println(s"label $label: $rate")
    }

    println("True positive rate by label:")
    trainingSummary.truePositiveRateByLabel.zipWithIndex.foreach { case (rate, label) =>
      println(s"label $label: $rate")
    }

    println("Precision by label:")
    trainingSummary.precisionByLabel.zipWithIndex.foreach { case (prec, label) =>
      println(s"label $label: $prec")
    }

    println("Recall by label:")
    trainingSummary.recallByLabel.zipWithIndex.foreach { case (rec, label) =>
      println(s"label $label: $rec")
    }


    println("F-measure by label:")
    trainingSummary.fMeasureByLabel.zipWithIndex.foreach { case (f, label) =>
      println(s"label $label: $f")
    }

    val accuracy = trainingSummary.accuracy
    val falsePositiveRate = trainingSummary.weightedFalsePositiveRate
    val truePositiveRate = trainingSummary.weightedTruePositiveRate
    val fMeasure = trainingSummary.weightedFMeasure
    val precision = trainingSummary.weightedPrecision
    val recall = trainingSummary.weightedRecall
    println(s"Accuracy: $accuracy\nFPR: $falsePositiveRate\nTPR: $truePositiveRate\n" +
      s"F-measure: $fMeasure\nPrecision: $precision\nRecall: $recall")

  }

}