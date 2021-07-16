import json
import os


def main():
    with open(os.path.join("data", "meta", "max.json"), 'rt') as max_reader:
        max_dict: dict = json.loads(max_reader.read())

    with open(os.path.join("data", "meta", "reject.json"), 'rt') as reject_reader:
        reject_list: list = json.loads(reject_reader.read())

    for f in os.listdir(os.path.join("data", "preprocessing")):
        with open(os.path.join("data", "features", f), 'wt') as writer:
            print(f)
            with open(os.path.join("data", "preprocessing", f), 'rt') as reader:
                for line in reader:
                    scaled = {}
                    data = json.loads(line)
                    respondent = data['Respondent']
                    if respondent in reject_list:
                        continue

                    for key, original_value in data.items():
                        scaled_value = float(original_value) / float(
                            max_dict[key])
                        scaled[key] = scaled_value

                    writer.write(json.dumps(scaled) + '\n')


if __name__ == '__main__':
    main()
