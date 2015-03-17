def render(json, string):
    #TODO:display rice search results in a predefined manner
    print(string)
    user_choice = input()
    #TODO:check if user_choice is a valid choice
    while(!check(user_choice, json)):
        print("Please choose from the results (q to quit)")
        user_choice = input()
        if(user_choice == 'q'):
            return(None,False,"Exited due to user input")
    return(user_choice, True, "")
def check(user_choice, json):
    #TODO
