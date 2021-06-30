import json

import numpy as np
import os
import pandas as pd

def main():
    print("Merge by Chunks")
    os.makedirs("features", exist_ok=True)
    max_features = 10
    feature_index = 0
    result = {}
    features = set()

    for file in os.listdir("cache"):
        print(file)
        with open(f"cache/{file}", 'rt') as chunk_file:
            for line in chunk_file:
                data = json.loads(line)
                key = data['Respondent']
                features = features.union(data.keys())
                if key in result:
                    result[key] = {**result[key], **data}
                else:
                    result[key] = data

        if len(features) > max_features:
            with open(f"features/{feature_index}.json", 'wt') as feature_file:
                for k, v in result.items():
                    feature_file.write(json.dumps(v) + '\n')
            result = {}
            feature_index += 1
            features = set()




if __name__ == '__main__':
    main()