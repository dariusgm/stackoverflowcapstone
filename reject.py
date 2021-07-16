import json
import os


def main():
    with open(os.path.join("data", "meta", "max.json")) as max_dict_file:
        max_dict = json.loads(max_dict_file.read())

    with open(os.path.join("data", "meta", "min.json")) as min_dict_file:
        min_dict = json.loads(min_dict_file.read())

    reject = set()
    for f in os.listdir(os.path.join("data", "preprocessing")):
        path = os.path.join("data", "preprocessing", f)
        with open(path, 'rt') as data_json:
            print(path)
            for line in data_json:
                data = json.loads(line)
                respondent = data['Respondent']
                for k, v in data.items():
                    if float(data[k]) < min_dict[k] or float(data[k]) > max_dict[k]:
                        reject.add(respondent)

    with open(os.path.join("data", "meta", "reject.json"), 'wt') as reject_file:
        reject_file.write(json.dumps(list(reject), indent=4))


if __name__ == '__main__':
    main()
