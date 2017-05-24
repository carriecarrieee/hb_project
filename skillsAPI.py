"""Get skills/job titles from Skills API."""

import requests, json
from pprint import pprint

def query_titles(search_input):
    """Queries API to return related job titles."""

    # search_input = 'grape'
    params = {'contains': search_input}
    r = requests.get('http://api.dataatwork.org/v1/jobs/autocomplete',
                     params)

    results = r.json()

    titles_list = []
    uuid_list = []
    # pprint(results)
    for result in results:
        print type(result)
        uuid_list.append(result.get('uuid', None))
        titles_list.append(result.get('suggestion'.decode('unicode-escape'), None).encode('utf-8'))
    pprint(titles_list)
    return titles_list, uuid_list

def query_skills_from_title(search_input):
    """Based on titles list from skills_api(), returns list of skills related
       to each job title."""

    titles_list_ignore, uuid_list = query_titles(search_input)

    id_to_skills = {}

    for uuid in uuid_list:
        r = requests.get('http://api.dataatwork.org/v1/jobs/'
            + uuid
            + '/related_skills')
        r = r.json()


        id_to_skills[uuid] = [skill["skill_name"] for skill in r["skills"] \
            if skill["importance"] > 3.5]
            
        # pprint(id_to_job_obj[uuid]["job_title"])
        # for skill in sdict[uuid]["skills"]:
        #     skill_names_list.append(skill["skill_name"]) if skill["importance"] > 3.5
    return id_to_skills

