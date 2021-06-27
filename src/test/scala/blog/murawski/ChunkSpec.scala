package blog.murawski

import org.apache.spark.sql.SparkSession
import org.scalatest.{FunSuite, Matchers}

class ChunkSpec extends FunSuite with Matchers {
  implicit lazy val spark = SparkSession
    .builder()
    .master("local[*]")
    .getOrCreate()

  test("runs") {
    val options = AppOptions(
      inputPath = "cache/2020_Age.json",
      outputPath = "out"
    )

    Chunk.run(options)
  }
}
