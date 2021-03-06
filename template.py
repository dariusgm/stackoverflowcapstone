# generate template

import json
import os
from string import Template

from config import config

header = Template('<html><head><title>Stackoveflow capstone project by Darius '
                  'Murawski</title>'
                  '<script>window.config = {'
                  '  "max_dict": $max_dict, '
                  '  "model_path": "$model_path", '
                  '  "feature_list": $feature_list'
                  '}</script>\n'
                  '<script src="js/tf.min.js"></script>\n'
                  '<script src="js/capstone.js"></script>\n'
                  '</head>'
                  '<body>Welcome to your salary prediction. '
                  'This data is based on the stackoverflow survey of 2020 - '
                  'If you are interested in the source code, stay tuned!\n'
                  'Pick <b>NA</b> when you don\'t want to give an answer'
                  '<br />')


group_header = Template('<h4>$group</h4><div>$description</div>')

checkbox_start_template = Template("<fieldset>")
checkbox_value_template = Template('<div>'
                             '<input type="checkbox" id="$key" name="$key" value="$value">'
                             '<label for="$value">$value</label>'
                                   '</div>')
input_text = Template('<input type="text" id="$key-numeric" name="$key-numeric" size="3">'
                      '<label for="$key-numeric">Any Numeric value</label>')
checkbox_end_template = Template("</fieldset>")

select_start_template = Template('<fieldset><select name="$key" id="$key">')
select_option_template = Template('<option value="$value">$value</option>')
select_end_template = Template('</select></fieldset>')


footer = Template('<button id="submit">Submit</button></html>')

def render_checkbox(key, values, description, numeric):
    html = group_header.substitute(group=key, description=description)
    html += checkbox_start_template.substitute()
    # in case we have a numeric value, add it here as well for any input
    if key in numeric:
        html += input_text.substitute(key=key, value=0)

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
    for k in feature_list:

        # is numeric value
        if k in year_2020['numeric_columns']:
            numeric.append(k)
        # is one hot encoded
        if k not in year_2020['leave_columns'] and '_' in k:
            splitted = k.split("_")
            group_key, group_value = splitted[0], splitted[1]

            # remove the obvious columns
            if group_key == 'CompTotal' or group_key == 'ConvertedComp' or group_key == "Respondent":
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
        feature_list=feature_list,
        max_dict=json.dumps(max_dict, indent=4)
    )

    for k, v in single_answer.items():
        html += render_select_box(k, v, description[k])

    for k, v in multi_answer.items():
        html += render_checkbox(k, v, description[k], numeric)
    html += footer.substitute()

    with open("index.html", "wt") as html_file:
        html_file.write(html)


if __name__ == '__main__':
    main()
