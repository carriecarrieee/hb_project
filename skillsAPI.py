"""Get skills/job titles from Skills API."""

import requests, json
from pprint import pprint

def get_titles(search_input):
    """Queries API to return related job titles."""

    # search_input = 'grape'
    params = {'contains': search_input}
    r = requests.get('http://api.dataatwork.org/v1/jobs/autocomplete',
                     params)

    results = r.json()

    titles_list = []
    uuid_list = []

    for result in results:
        uuid_list.append(str(result.get('uuid', '')))
        titles_list.append(str(result.get('suggestion', '')))
 
    return titles_list, uuid_list


def get_skills(search_input):
    """Based on titles list from skills_api(), returns list of skills related
       to each job title."""

    titles_list_ignore, uuid_list = get_titles(search_input)

    id_to_skills = {}
    counter = 0

    for uuid in uuid_list:
        if counter >= 20:
            break

        r = requests.get('http://api.dataatwork.org/v1/jobs/'
            + uuid
            + '/related_skills')

        response = r.json() # Convert json to dict
        counter += 1

        id_to_skills[uuid] = [str(skill["skill_name"]) \
            for skill in response.get("skills", []) \
            if skill.get.sort("importance", 0) > 3.3]

        # id_to_skills[uuid] = [skill for skill in response.get("skills", []) \
        #     if skill.get("importance", 0) > 3.3]

        # id_to_skills[uuid].sort(key=lambda skill: skill.get("importance", 0))
        # id_to_skills[uuid] = [str(skill["skill_name"]) for skill in id_to_skills[uuid]]

    pprint(id_to_skills)
    return id_to_skills

