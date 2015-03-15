import json
#PLACE HOLDER ALGORITHM, TO BE REPLACED


def search_software(software_name):
    """
    Searches index.json for a software of specified name.
    Returns a tuple containing a boolean value indicating whether
    or not a complete match was made and a json with exact or partial matches
    """

    json_data = open("conf/index.json")
    data = json.load(json_data)
    json_data.close()

    target = data.get(software_name, False)

    return target
# Searches for a config name within a software. Returns either software_fail, rice_fail, or success depending on what it fines.


def search_rice(software_name, rice_name):
    """
    Searches index.json for a software of specified name and a specific rice.
    Returns a string and a json file.
    The string will be contain the value 'software_fail',
    indicating a failure to match the software name, 'rice_fail',
    indicating a failure to match a specific rice_name, or 'success',
    indicating succesful matches of both the software and configuration names
    """

    queryResult = search_software(software_name)
    if queryResult:
        # We won't search for a specific package if the user don't specified
        # a package
        rice_hits = queryResult['packages'].get(rice_name, False)

    else:
        return "software_fail"

    if rice_hits:
        return ("success", rice_hits)

    else:
        return "rice_fail"
