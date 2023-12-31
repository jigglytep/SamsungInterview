import pandas as pd
import re


def bodyParse(body):
    table_MN = pd.read_html(body.replace("<tr></tr>", ""), header=0)
    print(f'Total tables: {len(table_MN)}')
    df = table_MN[0]
    data = {
        'SourceSoftware': df['Source  software'].to_string(header=False, index=False).replace('\n', ', '),
        'TargetSoftware': df['Target  software'].to_string(header=False, index=False).replace('\n', ', '),
        'BinaryName': df['Binary  Name'].to_string(header=False, index=False).replace('\n', ', '),
        'BinarySize': df['Binary  size'].to_string(header=False, index=False).replace('\n', ', ')
    }
    if data:
        return data
    else:
        return {}


def subjectParse(subject):
    # Extracting data using regular expressions
    result = re.match(
        r"\[(.*?)\] \[(.*?)\] (\d+) \((.*?)\) (.*?) (\d+/\d+/\d+)", subject)

    if result:
        data = {
            'EVT_TYPE': result.group(1),
            'MODEL_LIST': result.group(2),
            'SU_NO': result.group(3),
            'SUType': result.group(4),
            'request': result.group(5),
            'dueDate': result.group(6)
        }
        return data
    else:
        return {}
