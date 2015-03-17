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
        print('(' + str(i) + ') ' + name + ':')
        print('\t' + 'Version : ' + version)
        print('\t' + 'Description :')
        print('\t\t' + desc)
        i += 1

def select_options(rice_list):
    #renders a formated rice list then prompts user for rices to choose, checks user input and finally creates a list containing the rice names
    render_dict(rice_list)
    print('Please type in the number corresponding to the rice you want to choose (range with a-b, multiple choices with a,b,c):')
    user_choice = input()
    user_input = transform(user_choice)
    while(not check(user_input, rice_list)):
        print("Please choose from the results (q to quit)")
        user_choice = input()
        user_input = transform(user_choice)
        if(user_choice == 'q'):
            return(None,False, "Quitting riceDB")
    chosen_rices = []
    for i in user_input:
        chosen_rices.append(rice_list[i])
    return(chosen_rices, True, "")

