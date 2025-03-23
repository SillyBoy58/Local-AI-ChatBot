import os
import main
import chatMan
import json

def deleteChar():
    # Get the directory of the saved characters
    script_dir = os.path.dirname(os.path.realpath(__file__))
    saved_models_dir = os.path.join(script_dir, "Saved_Charcaters")

    # List to store the paths of all the character JSON files
    char_files = []

    # Loops through each folder inside Saved_Charcaters directory then checks if it has a json and adds it to char_files[]
    for folder in os.listdir(saved_models_dir):
        folder_path = os.path.join(saved_models_dir, folder)

        if os.path.isdir(folder_path):
            char_file = os.path.join(folder_path, f"{folder}_info.json")

            if os.path.exists(char_file):
                char_files.append(char_file)

    # If no saved characters exist, lets the user know
    if not char_files:
        print("No saved characters found.")
        return

        # Shows the user a list of available characters (numbered)
    print("Available characters:")
    for i, char_file in enumerate(char_files, 1):
        char_name = os.path.basename(char_file).replace("_info.json", "")
        print(f"{i}. {char_name}")

    # Asks the user to pick a character to delete
    while True:
        try:
            choice = int(input("Enter the number of the character you want to delete: "))

            # Makes sure the choice is valid
            if 1 <= choice <= len(char_files):
                selected_file = char_files[choice - 1]
                char_name = os.path.basename(selected_file).replace("_info.json", "")
                char_folder = os.path.join(saved_models_dir, char_name)

                # Confirm before deleting
                confirm = input(f"Are you sure you want to delete '{char_name}'? This cannot be undone. (y/n): ")
                if confirm.lower() == 'y':
                    os.remove(char_file)  # Delete the JSON file
                    os.rmdir(char_folder)  # Delete the character's folder (must be empty)
                    print(f"Character '{char_name}' deleted successfully!")
                else:
                    print("Deletion canceled.")

                break  # Exit loop after handling the deletion

            else:
                print("Invalid choice. Please select a valid number.")

        except ValueError:
            print("Invalid input. Please enter a number.")

def charSelect(SUMMARY_TRIGGER):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    saved_models_dir = os.path.join(script_dir, "Saved_Charcaters")
    
    # List to store the paths of all the character JSON files
    char_files = []

    # Loops through each folder inside Saved_Charcaters directory then checks if it has a json and adds it to char_files[]
    for folder in os.listdir(saved_models_dir):
        folder_path = os.path.join(saved_models_dir, folder)

        if os.path.isdir(folder_path):
            char_file = os.path.join(folder_path, f"{folder}_info.json")

            if os.path.exists(char_file):
                char_files.append(char_file)

    # If no saved characters exist, lets the user know
    if not char_files:
        print("No saved characters found.")
        return

    # Shows the user a list of available characters (numbered)
    print("Available characters:")
    for i, char_file in enumerate(char_files, 1):
        char_name = os.path.basename(char_file).replace("_info.json", "")
        print(f"{i}. {char_name}")

    # Asks the user to pick a character
    while True:
        try:
            # Asks the user for their choice
            choice = int(input("Enter the number of the character you want to select: "))

            # Makes sure the choice is valid (within the range)
            if 1 <= choice <= len(char_files):
                selected_file = char_files[choice - 1]
                
                # Load the data from the selected JSON file
                with open(selected_file, "r") as file:
                    character_data = json.load(file)
                
                # Assigns the character data to variables
                botName = character_data["botName"]
                botDescription = character_data["botDescription"]
                BotFirstMessage = character_data["BotFirstMessage"]
                
                break  # Exit the loop after a valid selection
                
            else:
                print("Invalid choice. Please select a valid number.")
        
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Call the messaging function with the selected character's data
    chatMan.messaging(botName, botDescription, BotFirstMessage, SUMMARY_TRIGGER)

def saveChar(botName, botDescription, BotFirstMessage):
    # Creates the saved characters' directory - created characters are stored here.
    script_dir = os.path.dirname(os.path.realpath(__file__))
    saved_models_dir = os.path.join(script_dir, "Saved_Charcaters")

    if not os.path.exists(saved_models_dir):
        os.makedirs(saved_models_dir)
        print(f"Directory '{saved_models_dir}' created.")

    # Creates a character specific directory where the information and message history is stored.
    bot_dir = os.path.join(saved_models_dir, botName)

    if not os.path.exists(bot_dir):
        os.makedirs(bot_dir)
        print(f"Directory '{botName}' created inside '{saved_models_dir}'.")

    # The data that will be stored
    character_data = {
        "botName": botName,
        "botDescription": botDescription,
        "BotFirstMessage": BotFirstMessage
    }

    json_file_path = os.path.join(bot_dir, f"{botName}_info.json")

    with open(json_file_path, "w") as json_file:
        json.dump(character_data, json_file, indent=4)

    print(f"Character '{botName}' saved successfully in {json_file_path}!")