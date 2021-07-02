import json
import os

def main():
    best_n = 15
    scores = []

    for f in os.listdir("metrics"):
        with open(f"metrics/{f}", 'rt') as reader:
            # this is not a helpful feature, as its acutally the same without converting to the label
            if f != "2020_ConvertedComp":
                data = json.loads(reader.read())
                data["file"] = f
                scores.append(data)


    newlist = sorted(scores, key=lambda k: k['val_mean_squared_error'])
    relevent_features = map(lambda x: x['file'], newlist[0:best_n+1])

    result = {}
    for f in relevent_features:
        with open(f"features/{f}", 'rt') as json_reader:
            print(f"Merging {f}")
            for line in json_reader:
                data = json.loads(line)
                key = data['Respondent']
                if key in result:
                    result[key] = {**result[key], **data}
                else:
                    result[key] = data

    print("Writing all.json")
    with open("all.json", 'wt') as writer:
        for _respondent, v in result.items():
            data = json.dumps(v)
            writer.write(data + '\n')

if __name__ == '__main__':
    main()