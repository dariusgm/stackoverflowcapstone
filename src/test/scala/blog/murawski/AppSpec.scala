package blog.murawski

import org.apache.spark.sql.SparkSession
import org.scalatest.{FunSuite, Matchers}

class AppSpec extends FunSuite with Matchers {
  implicit lazy val spark = SparkSession
    .builder()
    .master("local[*]")
    .getOrCreate()

  test("runs") {
    val options = AppOptions(
      inputPath = "src/test/resources/2020.json",
      outputPath = "out"
    )

    App.run(options)
  }
}
