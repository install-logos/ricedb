import json
#PLACE HOLDER ALGORITHM, TO BE REPLACED
def lev_dist(first, second):
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
        distance_matrix[0][j]=j
    for i in range(1, first_length):
        for j in range(1, second_length):
            deletion = distance_matrix[i-1][j] + 1
            insertion = distance_matrix[i][j-1] + 1
            substitution = distance_matrix[i-1][j-1]
            if first[i-1] != second[j-1]:
                substitution += 1
            distance_matrix[i][j] = min(insertion, deletion, substitution)
    return distance_matrix[first_length-1][second_length-1]

def search_index(json_file,target_val,field):
    json_data = open(json_file)
    data = json.load(json_data)
    json_data.close()
    found = False
    bounds = []
    close_matches = {}

    with open('search.config','r') as config:
        for line in config:
            if not line[0] == "#":   
                bounds.append(line.split(' '))
    #Perform a fuzzy find for each software, if the score is high enough add that json index to a list
    for obj in data:
        sim = lev_dist(obj[field], target_val)
        if sim == 0:
            return (True,obj)
        size = len(target_val)
        for bound in bounds:
            lower = int(bound[0])
            upper = int(bound[1])
            matches = int(bound[2])
            if size >= lower and size <= upper:
                if sim <= matches:
                    close_matches.update(obj)
    return (False, close_matches)
