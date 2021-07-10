# generate template

import json
import os
from string import Template

from config import config

header = Template('<html><head><title>Stackoveflow capstone project by Darius '
                  'Murawski</title>'
                  '<script>window.config = {'
                  '  "model_path": "$model_path", '
                  '  "feature_list": $feature_list'
                  '}</script>'
                  '<script src="js/tf.min.js"></script>'
                  '<script src="js/capstone.js"></script>'
                  '</head>'
                  '<body>Welcome to your salary prediction. '
                  'This data is based on the stackoverflow survey of 2020'
                  'if you are interested in the source code, stay tuned !'
                  '<form><button id="submit">Submit</button>')


group_header = Template('<div>$group</div><div>$description</div>')

checkbox_start_template = Template("<fieldset>")
checkbox_value_template = Template('<div>'
                             '<input type="checkbox" id="$key" name="$key" value="$value">'
                             '<label for="$value">$value</label></div>')
checkbox_end_template = Template("</fieldset>")

select_start_template = Template('<fieldset><select name="$key" id="$key">')
select_option_template = Template('<option value="$value">$value</option>')
select_end_template = Template('</select></fieldset>')


footer = Template('<button id="submit2">Submit</button></form></html>')

def render_checkbox(key, values, description):
    html = group_header.substitute(group=key, description=description)
    html += checkbox_start_template.substitute()
    html += "\n".join(
        map(lambda value: checkbox_value_template.substitute(key=key, value=value),
            values))
    html += checkbox_end_template.substitute()
    return html

def build_description(year):
    result = {}
    # fetch description from unzip file - why copy past?
    with open(os.path.join("data", "unpack", f'{year}.zip',
                           'survey_results_schema.csv'),
              'rt') as desciption_file:
        for line_number, line in enumerate(desciption_file):
            # skip header
            if line_number == 0:
                continue

            parts: str = line.split(",")
            key = parts[0]
            value = "".join(parts[1:]).replace('"', '')
            result[key] = value

    return result

def render_select_box(key, values, description):
    html = group_header.substitute(group=key, description=description)
    html += select_start_template.substitute(key=key)
    html += "\n".join(
        map(lambda value: select_option_template.substitute(key=key, value=value),
            values))
    html += select_end_template.substitute()
    return html


def main():
    year = '2020'
    year_2020 = list(filter(lambda x: x['year'] == str(year), config))[0]

    with open(os.path.join("data", "meta", "max.json")) as meta_file:
        max_dict: dict = json.loads(meta_file.read())

    with open(os.path.join("data", "meta", "feature_list.json")) as feature_file:
        feature_list: list = json.loads(feature_file.read())

    description = build_description(year)

    # build groups with one hot encoded values
    numeric = []
    single_answer = {}
    multi_answer = {}
    k: str
    for k in max_dict.keys():

        # make sure feature is set as important
        if k not in feature_list:
            continue

        # is numeric value
        if k in year_2020['numeric_columns']:
            numeric.append(k)
        # is one hot encoded
        if k not in year_2020['leave_columns'] and '_' in k:
            splitted = k.split("_")
            group_key, group_value = splitted[0], splitted[1]

            # remove the obvious columns
            if group_key == 'CompTotal' or group_key == 'ConvertedComp' :
                continue

            if group_key in year_2020['exclusive_columns']:
                if group_key in single_answer:
                    single_answer[group_key].append(group_value)
                else:
                    single_answer[group_key] = [group_value]

            else:
                if group_key in multi_answer:
                    multi_answer[group_key].append(group_value)
                else:
                    multi_answer[group_key] = [group_value]

    html = header.substitute(
        model_path=os.path.join("data", "model", "tfjs_2020.model", "model.json"),
        feature_list=feature_list
    )

    for k, v in single_answer.items():
        html += render_select_box(k, v, description[k])

    for k, v in multi_answer.items():
        html += render_checkbox(k, v, description[k])
    html += footer.substitute()

    with open("index.html", "wt") as html_file:
        html_file.write(html)


if __name__ == '__main__':
    main()
