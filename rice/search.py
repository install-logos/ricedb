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

    target = data.get(software_name, None)

    return target
# Searches for a config name within a software. Returns either software_fail, rice_fail, or success depending on what it fines.


def search_keywords(packages, keywords):
    """
    Return the bests packages according to the specified keyword
    """

    packagesRelevance = {}

    for package in packages:
        for keyword in keywords:
            nameCount = packages[package]["Name"].count(keyword)
            descriptionCount = packages[package]["Description"].count(keyword)
            bothSum = nameCount + descriptionCount

            if bothSum:
                # We don't want to put non relevant packages in
                # packagesRelevance
                packagesRelevance[package] = bothSum

    return sorted(packagesRelevance, key=packagesRelevance.__getitem__,
                  reverse=True)


def search_rice(software_name, rice_name):
    """
    Searches index.json for a software of specified name and a specific rice.
    Returns a string and a json file.
    The string will be contain the value 'software_fail',
    indicating a failure to match the software name, 'rice_fail',
    indicating a failure to match a specific rice_name, or 'success',
    indicating succesful matches of both the software and configuration names
    """

    rice_hits = None
    queryResult = search_software(software_name)

    if queryResult is not None:
        # We won't search for a specific package if the user don't specified
        # a package
        rice_hits = queryResult['packages'].get(rice_name, None)
        if rice_hits is None:
            # Launch fuzzy find
            rice_hits = search_keywords(queryResult['packages'], rice_name)
            if not rice_hits:
                # If nothing was found during the research
                rice_hits = None

    return rice_hits
