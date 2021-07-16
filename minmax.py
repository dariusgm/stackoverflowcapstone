import json
import os

import numpy as np


def main():
    max_dict = {}
    min_dict = {}
    sigma = 3
    for f in os.listdir(os.path.join("data", "preprocessing")):
        temp = {}
        path = os.path.join("data", "preprocessing", f)
        with open(path, 'rt') as json_file:
            print(path)
            line: str
            for line in json_file:
                data: dict = json.loads(line)
                for k, v in data.items():
                    if k not in temp:
                        temp[k] = [float(v)]
                    else:
                        temp[k].append(float(v))

            # calculate filtering criteria
            for k, v in temp.items():
                # only calculate it once
                if k not in max_dict:
                    np_array = np.array(v, dtype=np.float64)
                    mean = np.mean(np_array, axis=0)
                    sd = np.std(np_array, axis=0)

                    product = sigma * sd
                    # Fake min value, when we only have NA "positives"
                    if (mean - product) < 0 or min(np_array) == 1.:
                        min_value = 0
                    else:
                        min_value = mean - product

                    max_value = mean + product
                    min_dict[k] = min_value
                    max_dict[k] = max_value

    with open(os.path.join("data", "meta", "max.json"), 'wt') as max_writer:
        max_writer.write(json.dumps(max_dict, indent=4))

    with open(os.path.join("data", "meta", "min.json"), 'wt') as min_writer:
        min_writer.write(json.dumps(min_dict, indent=4))


if __name__ == '__main__':
    main()
