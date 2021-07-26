import re
import os

def main():
    model_path = os.listdir(os.path.join("data", "model"))[0]
    with open("capstone.html", "wt") as html_writer:
        with open("index.html", "rt") as html_reader:
            for line in html_reader:
                if "model_path" in line:
                    line = line.replace(os.path.join("data", "model", model_path), os.path.join("js"))
                html_writer.write(line)


if __name__ == '__main__':
    main()
