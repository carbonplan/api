import json
import gspread
import requests
import jsonschema
from pandas import DataFrame, MultiIndex

from oauth2client.service_account import ServiceAccountCredentials


def ffill(data):
    """
    helper function to forward fill column labels
    """
    last = data[0]
    new = []
    for line in data:
        if line:
            new.append(line)
            last = line
        else:
            new.append(last)
    return new

def get_sheet(sheet, doc):
    """
    helper function to open a specific google sheet
    """
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
             'key.json', scope) # Your json file here

    gc = gspread.authorize(credentials)
    wks = gc.open(doc)
    sheet = wks.worksheet(sheet)
    data = sheet.get_all_values()
    h1 = ffill(data[0])
    columns = MultiIndex.from_tuples(zip(h1, data[1]))
    df = DataFrame(data[2:], columns=columns)
    return df

def make_project(name):
    """
    return a template project
    """
    return {
        'type': 'Project',
        'name': name,
        'metrics': [],
        'geometry': { 'type': None },
        'tags': [],
        'id': '',
        'description': ''
    }


def make_metric(name):
    """
    return a template metric
    """
    return {
        'type': 'Metric',
        'name': name,
        'value': '',
        'units': '',
        'rating': '',
        'notes': '',   
        'comment': ''   
    }

def maybe_float(value):
    new = value.replace('$', '').replace(',', '')
    try:
        return float(new)
    except:
        return value.strip()

if __name__ == '__main__':

    data = get_sheet('Sheet1', 'Stripe reports 0.1 [internal]').loc[:23]

    metrics = [
        'mechanism',
        'volume',
        'negativity',
        'permanence',
        'additionality',
        'cost',
        'transparency',
    ]

    metric_keys = ['name', 'geometry', 'value', 'units', 'notes', 'comment', 'rating', 
         'removal', 'emissions', 'kind', 'counterfactual', 'removal', 'avoided']

    tag_keys = data.columns.levels[0][data.columns.levels[0].str.startswith('tag')]
    tag_keys = [(t, '') for t in tag_keys]

    projects = []
    for i, row in data.iterrows():
        project = make_project(row[('name', '')])
        tags = row[tag_keys].to_list()
        if '' in tags:
            tags.remove('')
        tags = [t.lower().strip() for t in tags]
        project['tags'].extend(tags)
        project['id'] = row[('id', '')]
        project['description'] = row[('description', '')]
        project['location'] = {'name': row[('location', 'name')], 'geometry': json.loads(row[('location', 'geometry')])}
        project['source'] = {'name': row[('source', 'name')], 'url': row[('source', 'url')]}
        for name in metrics:
            m = make_metric(name)
            for key in metric_keys:
                try:
                    val = row[(name, key)]
                except KeyError:
                    continue
                else:
                    m[key] = maybe_float(val)
                
            project['metrics'].append(m)
        projects.append(project)

    project_collection = {
        'type': 'ProjectCollection',
        'projects': projects
    }

    with open('app/projects.json', 'w') as outfile:
        json.dump(project_collection, outfile, indent=2)

    # validate against schema
    # schema = requests.get('https://api.carbonplan.now.sh/schema/ProjectCollection.json').json()
    # jsonschema.validate(project_collection, schema=schema)