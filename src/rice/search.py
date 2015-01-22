import json


def get_software(software_name):
    """
    Searches index.json for a software of specified name.
    It will return the the 'software_name' part of the json file or None
    if the user input is correct or not.

    ARGUMENTS:
        'software_name': User input of a specific software.
    """
    json_data = open("conf/index.json")
    data = json.load(json_data)
    json_data.close()

    target = data.get(software_name)

    return target


def search_keywords(packages, keywords):
    """
    Return the mosts relevant packages according to the specified keyword.

    ARGUMENTS:
        'packages': Dictionnary of packages with package name for the dict key.
                    'packages' should be a part of the index.json
                    file wich contain package name by program name.

        'keywords': List of keywords input by the user to search
                    packages that will suit their needs
                    example: ['blue', 'gapps']
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


def get_package(packages, rice_name):
    """
    Get the 'rice_name' package in 'packages' dict else it return None.

    ARGUMENTS:
        'packages': Dictionnary of packages of a software (package name are
                    the dict key).
                    'packages' should be a part of the index.json
                    file wich contain package name by program name.

        'rice_name': String of the specific package name input by the user.
    """

    return packages.get(rice_name, None)


def search_packages(softwareName, riceName, mode_function):
    """
    Searches index.json for package(s) of 'software_name'.
    It will return relevant packages according to the mode specified
    in 'modeFunction'.
    If the user enter something wrong it return None.

    ARGUMENTS:
        'software_name': String of the specific software to look after
                         the packages
        'rice_name': Keywords lists or specific package according to the mode
        'modeFunction': Function passed as an argument to pass the mode of
                        package search (could be direct search or a search by
                        keyword).
    """

    riceHits = None
    queryResult = get_software(softwareName)

    if queryResult is not None:
        # Launch find function according to 'mode_function'
        riceHits = mode_function(queryResult['packages'], riceName)

    return riceHits
