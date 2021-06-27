package blog.murawski

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