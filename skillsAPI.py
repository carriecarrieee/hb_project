"""Get skills/job titles from Skills API."""

import requests, json
from pprint import pprint

def query_titles():
    """Queries API to return related job titles."""

    # search_input = request.form.get('search_input')
    search_input = 'grape'
    params = {'contains': search_input}
    r = requests.get('http://api.dataatwork.org/v1/jobs/autocomplete',
                     params)
    results = r.json()

    titles_list = []
    uuid_list = []
    for result in results:
        uuid_list.append(result.get('uuid', None))
        titles_list.append(result.get('suggestion', None))

    return titles_list, uuid_list

def query_skills_from_title():
    """Based on titles list from skills_api(), returns list of skills related
       to each job title."""

    titles_list_ignore, uuid_list = query_titles()
    sdict = {}
    skill_names_list = []

    for uuid in uuid_list:
        r = requests.get('http://api.dataatwork.org/v1/jobs/'
            + uuid
            + '/related_skills')
        sdict[uuid] = r.json()
        pprint(sdict[uuid]["job_title"])

        for skill in sdict[uuid]["skills"]:
            skill_names_list.append(skill["skill_name"])
    
    return skill_names_list

query_skills_from_title()

