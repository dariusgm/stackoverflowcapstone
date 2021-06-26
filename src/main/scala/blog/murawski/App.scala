package blog.murawski

import org.apache.hadoop.fs.{FileSystem, Path}
import org.apache.spark.ml.classification.LogisticRegression
import org.apache.spark.ml.feature.VectorAssembler
import org.apache.spark.sql.catalyst.ScalaReflection.Schema
import org.apache.spark.sql.functions.col
import org.apache.spark.sql.{DataFrame, SparkSession}
import org.jpmml.model.JAXBUtil
import org.jpmml.sparkml.PMMLBuilder
import scopt.OptionParser

import javax.xml.transform.stream.StreamResult

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

  def export(schema : Schema, model: LogisticRegression) = {

  }

  def preprocessing(path: String)(implicit spark: SparkSession): DataFrame = {
    val cacheFile = "data/2020_preprocessing.parquet"
    val conf = spark.sparkContext.hadoopConfiguration
    val fs = FileSystem.get(conf)
    // skip preprocessing in case we did that already
    if (fs.exists(new Path(cacheFile))) {
      spark.read.parquet(cacheFile)
    } else {
      var preprocesing = spark
        .read
        .json(path)
        .filter(col(labelColumn).isNotNull)
        .withColumn(labelColumn, col(labelColumn).cast("float"))
        // This is not a feature, its just the survey identifier / user
        .drop("Respondent")

      val featureColumns = preprocesing.columns.toSet.diff(Set(labelColumn)).toArray
      println("Using following feature columns:")
      println(featureColumns.mkString(","))
      println("clean column names")


      for (column <- featureColumns) {
        // Removing rejected chars for spark
        var cleanedName = column.replace(".", "")
        // Removing rejected chars for parquet
        for (t <- Seq(" ", ",", ";", "{", "}", "(", ")", "\n", "\t")) {
          cleanedName = cleanedName.replace(t, "")
        }

        preprocesing = preprocesing.withColumnRenamed(column, cleanedName).withColumn(cleanedName, col(cleanedName).cast("float"))
      }
      preprocesing = preprocesing.na.fill(0.0).cache()
      preprocesing.write.parquet(cacheFile)
      preprocesing
    }
  }

  def fitAssembler(df: DataFrame, columns: Array[String]): DataFrame = {
    new VectorAssembler().setInputCols(columns).setOutputCol(featureColumn).transform(df)
  }

  def run(options: AppOptions)(implicit spark: SparkSession): Unit = {
    // spark.sparkContext.setLogLevel("ERROR")
    val preprocessingDf = preprocessing(options.inputPath)
    val cleanedColumns = preprocessingDf.columns

    preprocessingDf.printSchema()
    preprocessingDf.show(10, false)
    print(preprocessingDf.count())

    val fittedAssember = fitAssembler(preprocessingDf, cleanedColumns)


    val df = fittedAssember.randomSplitAsList(Array(trainSplit, testSplit, hyperparameterSplit), seed = 42)
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
      .setFeaturesCol(featureColumn)

    // Fit the model
    val lrModel = lr.fit(trainDf)



    val pmml = new PMMLBuilder(preprocessingDf.schema, lrModel).build()
    JAXBUtil.marshalPMML(pmml, new StreamResult(System.out))

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