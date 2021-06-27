package blog.murawski

import org.apache.spark.sql.SparkSession
import org.scalatest.{FunSuite, Matchers}

class AppSpec extends FunSuite with Matchers {
  implicit lazy val spark: SparkSession = SparkSession
    .builder()
    .master("local[*]")
    .getOrCreate()

  test("runs") {
    val options = AppOptions(
      inputPath = "./cache",
      outputPath = "out"
    )

    App.run(options)
  }
}
