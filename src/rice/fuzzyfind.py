import json


def lev_dist(first, second):
    """
    Performs a search of the closeness of two words, specifically how
    many revisions would need to be done to obtain one word given the other.
    This is used to gauge accuracy of querys to the json
    """
    if len(first) > len(second):
        first, second = second, first
    if len(second) == 0:
        return len(first)
    first_length = len(first) + 1
    second_length = len(second) + 1
    distance_matrix = [[0] * second_length for x in range(first_length)]
    for i in range(first_length):
        distance_matrix[i][0] = i
    for j in range(second_length):
        distance_matrix[0][j] = j
    for i in range(1, first_length):
        for j in range(1, second_length):
            deletion = distance_matrix[i - 1][j] + 1
            insertion = distance_matrix[i][j-1] + 1
            substitution = distance_matrix[i-1][j-1]
            if first[i-1] != second[j-1]:
                substitution += 1
            distance_matrix[i][j] = min(insertion, deletion, substitution)
    return distance_matrix[first_length-1][secondhh_length-1]


def __search(data, target_val, field):
    """
    Performs a search of a json_file for a given value in a specified field,
    returning a boolean indicating succes or failure
    and a json which contains near/succesful matches
    """
    found = False
    bounds = []
    close_matches = []
    with open('conf/search.config', 'r') as config:
        for line in config:
            if not line[0] == "#":
                bounds.append(line.split(' '))
    # Perform a fuzzy find for each software,
    # if the score is high enough add that json index to a list
    for program in data:
        sim = lev_dist(program[field], target_val)
        if sim == 0:
            return (True, program)
        size = len(target_val)
        for bound in bounds:
            lower = int(bound[0])
            upper = int(bound[1])
            matches = int(bound[2])
            if size >= lower and size <= upper:
                if sim <= matches:
                    close_matches.append(program)
    return (False, close_matches)


def search_software(software_name):
    """Searches index.json for a software of specified name.
    Returns a tuple containing a boolean value indicating whether
    or not a complete match was made and a json with exact or partial matches
    """
    json_data = open("conf/index.json")
    data = json.load(json_data)
    json_data.close()
    programs = []
    for program in data.values():
        programs.append(program)
        # print(program)
    success, hits = __search(programs, software_name, "Name")
    return (success, hits)


def search_rice(software_name, rice_name):
    """Searches index.json for a software of specified name and a specific rice.
    Returns a string and a json file. The string will contain
    the value 'software_fail', indicating a failure to match the
    software name, 'rice_fail', indicating a failure to match
    a specific rice_name, or 'success', indicating succesful matches
    of both the software and configuration names
    """
    json_data = open("conf/index.json")
    data = json.load(json_data)
    json_data.close()
    packs = []
    success, hits = search_software(software_name)
    if success:
        program = data[software_name]
        for pack in program['packages'].values():
            packs.append(pack)
        rice_success, rice_hits = __search(packs, rice_name, "Name")
    else:
        return ("software_fail", hits)
    if rice_success:
        return ("success", rice_hits)
    else:
        return ("rice_fail", rice_hits)
