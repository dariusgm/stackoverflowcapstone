import json


def main():
    keys = set()
    with open("2020.json", 'rt') as json_reader:
        for line in json_reader:
            data = json.loads(line)
            keys = keys.union(set(data.keys()))

    print("Hashing keys")
    print(len(keys))
    keys_list = list(keys)
    # sorted keys, references as index for tensorflow
    keys_list.sort()
    vector_size = len(keys_list)
    print("filling...")
    with open("2020_filled.csv", "wt") as filled:
        filled.write(",".join(keys_list) + '\n')
        with open("2020.json", 'rt') as json_reader:
            for line in json_reader:
                data = json.loads(line)
                vector = ["0" for _ in range(vector_size)]
                for k, v in data.items():
                    index = keys_list.index(k)
                    vector[index] = str(v)

                filled.write(",".join(vector) + '\n')


if __name__ == '__main__':
    main()
