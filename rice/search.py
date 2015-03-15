import json
#PLACE HOLDER ALGORITHM, TO BE REPLACED


def get_software(software_name):
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

    sortedPackages = sorted(packagesRelevance,
                            key=packagesRelevance.__getitem__, reverse=True)

    if sortedPackages:
        res = list(map(lambda x: packages[x], sortedPackages))
    else:
        res = None

    return res


def get_package(queryResult, rice_name):
    return queryResult.get(rice_name, None)


def search_packages(software_name, rice_name, modeFunction):
    """
    Searches index.json for a software of specified name and return, packages
    according to the mode we specified in 'modeFunction'.
    """

    rice_hits = None
    queryResult = get_software(software_name)

    if queryResult is not None:
        # Launch fuzzy find
        rice_hits = modeFunction(queryResult['packages'], rice_name)

    return rice_hits
