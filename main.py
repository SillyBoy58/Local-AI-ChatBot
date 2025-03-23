import ollama
import os
import sys
import charMan
import chatCommands
import chatMan

# Gets user's preferences/bot information.
def get_user_information():
    botName = input("Enter bot name: ")
    botDescription = input("Description: ")
    BotFirstMessage = input("Enter the first robot message: ")

    return botName, botDescription, BotFirstMessage

def main():
    global SUMMARY_TRIGGER, MESSAGES_TO_KEEP  
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        try:
            SUMMARY_TRIGGER = int(input("Enter the message history limit (integer): "))
            if SUMMARY_TRIGGER <= 0:
                print("Please enter a positive integer.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    MESSAGES_TO_KEEP = SUMMARY_TRIGGER // 2

    while True:
        choice = input("""What do you want to do? (1-3)
        1) Create a new character.
        2) Select an existing character.
        3) Delete an existing character.
        4) Exit: """)
        match choice:
            case "1": 
                botName, botDescription, BotFirstMessage = get_user_information()

                checkSave = input("Do you want to save this character (y/n)?: ")
                if checkSave == "y":
                    charMan.saveChar(botName, botDescription, BotFirstMessage)
                continue

            case "2": 
                charMan.charSelect(SUMMARY_TRIGGER)
            case "3":
                charMan.deleteChar()
                continue
            case "4":
                sys.exit()

# Idk why this is here, I read that you need to have this in every program so here it is. 
if __name__ == "__main__":
    main()