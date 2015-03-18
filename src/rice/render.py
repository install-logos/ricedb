def transform(user_choice):
    #parses statements like (a-b) and turns the resulting string containing numbers into a list of ints without duplicates
    l = user_choice.replace(' ','').split(',')
    user_choice  = []
    for n in l:
        v = []
        if('-' in n):
            v.append(n)
            for c in v:
                temp = c.split('-')
                temp[1] = int(temp[1]) + 1
                for i in range(int(temp[0]),temp[1]):
                    user_choice.append(i)
        else:
            user_choice.append(int(n))
    user_choice = list(set(user_choice)) #remove duplicates
    user_choice.sort
    return user_choice

def check(user_choice, rice_list):
    #checks if user_choice contains out of range indexes of rice_list
    is_in_list = (user_choice[len(user_choice) - 1] <= len(rice_list))
    return is_in_list

def render_dict(rice_list):
    i = 0
    for rice in rice_list:
        name = rice['Name']
        desc = rice['Description']
        version = rice['Version']
        display_string = '({}) {}: \n\tVersion : {}\n\tDescription : \n\t\t {}'.format(i, name, version, desc)
        print(display_string)
        i += 1

def select_options(rice_list):
    rices = []
    # Need to handle 3 cases: One for software search, which returns a primary dict entry,
    # Another for a list which is returned for a rice query
    # and a last one for the -S option which is a single rice dict entry
    if type(rice_list) is dict:
        if 'packages' in rice_list:
            packs = rice_list['packages']
            for key, rice in packs.items():
                rices.append(rice)
        else:
            rices.append(rice_list)
            return(rices, True, "")
    else:
        rices = rice_list
    #renders a formated rice list then prompts user for rices to choose, checks user input and finally creates a list containing the rice names
    render_dict(rices)
    print('Please type in the number corresponding to the rice you want to choose (range with a-b, multiple choices with a,b,c):')
    print("Please choose from the results (q to quit)")
    user_choice = input()
    if(user_choice == 'q' or user_choice.isalpha()):
            return(None,False, "Quitting riceDB")
    user_input = transform(user_choice)

    
    chosen_rices = []
    for i in user_input:
        chosen_rices.append(rices[i])
    return(chosen_rices, True, "")

