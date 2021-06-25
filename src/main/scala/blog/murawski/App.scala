package blog.murawski

import org.apache.spark.ml.classification.LogisticRegression
import org.apache.spark.ml.feature.VectorAssembler
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions.{col, udf}
import scopt.OptionParser
case class AppOptions(inputPath: String = "", outputPath: String = "")

object AppOptions {

  val optionsParser: OptionParser[AppOptions] =
    new OptionParser[AppOptions]("AppOptions") {
      head("Capstone", "Capstone")
      opt[String]('s', "inputPath")
        .action((x, o) => o.copy(inputPath = x)
        )
        .text("Path to spot data")
        .required()

      opt[String]('o', "outputPath")
        .action((x, o) => o.copy(outputPath = x)
        )
        .text("Path to write output data")
        .required()
    }

  def options(args: Seq[String]): AppOptions = {
    optionsParser.parse(args, AppOptions()).get
  }
}

object App {
  val trainSplit = 0.7
  val testSplit = 0.2
  val hyperparameterSplit = 0.1

  val toDouble = udf[Double, String]( _.toDouble)

  def main(args: Array[String]): Unit = {
    val options = AppOptions.options(args.toSeq)

    implicit val spark: SparkSession = SparkSession
      .builder()
      .appName("Merge Spot and View Data")
      .getOrCreate()

    run(options)
  }

  def run(options: AppOptions)(implicit spark: SparkSession) : Unit = {
    // spark.sparkContext.setLogLevel("ERROR")
    var preprocesing = spark
      .read
      .json(options.inputPath)
      .filter(col("ConvertedComp_NA") === 1)

    val featureColumns = preprocesing.columns.toSet.diff(Set("ConvertedComp")).toArray
    println("Using following feature columns:")
    println(featureColumns.mkString(","))

    for (column <- featureColumns) {
      val cleanedName = column.replace(".", "")
      preprocesing = preprocesing.withColumnRenamed(column, cleanedName).withColumn(cleanedName, toDouble(col(cleanedName)))
    }

    preprocesing.printSchema()
    preprocesing.show(10, false)



    val assembler = new VectorAssembler().setInputCols(featureColumns).setOutputCol("features")
    val out = assembler.transform(preprocesing)

    val df = out.randomSplitAsList(Array(trainSplit, testSplit, hyperparameterSplit), seed = 42)
    val trainDf = df.get(0).cache()
    val testDf = df.get(1).cache()
    val hyperparameterDf = df.get(2).cache()

    println("Train: " + trainDf.count())
    println("Test: " + testDf.count())
    println("Hyperparameter: " + hyperparameterDf.count())

    val lr = new LogisticRegression()
      .setMaxIter(10)
      .setRegParam(0.3)
      .setElasticNetParam(0.8)
      .setLabelCol("ConvertedComp")
      .setFeaturesCol("features")

    // Fit the model
    val lrModel = lr.fit(trainDf)

    // Print the coefficients and intercept for multinomial logistic regression
    println(s"Coefficients: \n${lrModel.coefficientMatrix}")
    println(s"Intercepts: \n${lrModel.interceptVector}")

    val trainingSummary = lrModel.summary

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