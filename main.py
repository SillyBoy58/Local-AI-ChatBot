import ollama
import os
import sys
import json

username = input("What's your username?: ")

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

def charSelect():
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
    messaging(botName, botDescription, BotFirstMessage)

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

# Lists the commands
def listCommands():
    print("""Currently available commands:
        /help - displays this screen;
        /exit - leaves the program;
        /restart - restarts the program;
        /reset - resets the current conversation, keeping the preferences.
        /again - generates another response to the latest message deleting the current generated response.
        /clear - clears all text (to make the terminal more clean.)""")

# Gets user's preferences/bot information.
def get_user_information():
    # User describes the bot.
    botName = input("Enter bot name: ")
    botDescription = input("Description: ")
    BotFirstMessage = input("Enter the first robot message: ")

    return botName, botDescription, BotFirstMessage

# Function to summarize the last n messages for optimization.
def summarize_conversation(model, messages):
    # Formats the summary.
    summary_prompt = "Summarize the following conversation in a concise way while keeping key details:\n\n"
    history_text = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in messages])
    summary_input = summary_prompt + history_text

    try:
        summary_response = ollama.chat(model=model, messages=[{"role": "user", "content": summary_input}])
        return summary_response.get('message', {}).get('content', "Summary unavailable.")
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Summary unavailable."


# Function to actually chat to the AI.
def messaging(name, description, firstBotMessage):
    # Lists the availible models and prints them for selection. while True loop runs until user picks a valid model from the list.
    botModelOptions = [model.model for model in ollama.list().models]
    while True:
        model = input(f'Enter the model, options are: {botModelOptions}: ')
        if model in botModelOptions:
            break
        print("Invalid model. Please enter a valid model name.")
    
    # Gets users first message and clears the customization text from before.
    os.system('cls' if os.name == 'nt' else 'clear') # Clears the terminal
    print(f"{name}: {firstBotMessage}\n")
    firstUserMessage = input("You: ")
    print()

    # The list that stores chat's history.
    messages = [
        {'role': 'system', 'content': f"""
        You are a roleplay chatbot on an AI chat program, the user's who created you username is: {username}. Your name is {name}. And your description: {description}.
        Your rules are: 
        1. Make sure to use as close to human language as possible (do not use fancy words, unless it is appropriate with the characted).
        2. Enclose spoken dialogue in double quotes ("text") and actions in asterisks (*action*).
        3. Keep your messages to a maximum of six sentences and describe only the actions of the user-generated character, not the user.
        4. Do not repeat the previous messages, keep the roleplay going.
        5. Sometimes the user may put an empty message, for example: " ", in that case, continue the roleplay.
        
        This message is automatic and made from a server, all of the further messages are from the user, unless said otherwise."""}, # AI chatbot rules
        {'role': 'assistant', 'content': firstBotMessage},
        {'role': 'user', 'content': firstUserMessage}
    ]

    # Gets the response to the first user message and adds it to the history.
    response = ollama.chat(model=model, messages=messages)
    botReply = response['message']['content']
    print(f"{name}: {botReply}\n")
    messages.append({'role': 'assistant', 'content': botReply})

    # Starts the infinite messaging until user types "/exit".
    print("Type '/help' for a list of commands")
    while True:
        # Get's user's message and checks if user wants to leave.
        userMessage = input("You: ")
        print()
        match userMessage:
            case "/exit":
                sys.exit()
            case "/restart":
                sys.stdout.flush()  
                os.execv(sys.executable, [sys.executable, __file__] + sys.argv) # No idea what any of this is, but it apperently works so ¯\(ツ)/¯
            case "/reset":
                return messaging(name, description, firstBotMessage)
            case "/again":
                messages.pop() # Delete the latest message
                continue
                # Generate a new response using the same context
            case "/clear":
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"{name}: {response['message']['content']}\n")
                continue
            case "/help":
                listCommands() # Lists the availible commands.
                continue


        # Adds user's n'th message to the history.
        messages.append({'role': 'user', 'content': userMessage})

        # Check's the amount of messages in the chat and decides if to trigger the summary or not.
        if len(messages) > MESSAGE_HISTORY_LIMIT:
            old_messages = messages[1: SUMMARY_TRIGGER + 1]
            summary = summarize_conversation(model, old_messages)

            # Redefines messages so only the first system message (the rules) get kept also all of the summaries get kept and also the most recent messages get kept.
            messages = [
                messages[0],  # Keep first system message (rules)
                *[msg for msg in messages if msg['role'] == 'system' and 'Summary' in msg['content']],  # Keep past summaries
                {'role': 'system', 'content': f"Summary of past conversation: {summary}"},  # New summary
                *messages[-MESSAGES_TO_KEEP:]  # Keep recent messages
            ]


        # Gets AI's response to the user message. 
        response = ollama.chat(model=model, messages=messages)
        botReply = response['message']['content']
        print(f"{name}: {botReply}\n")
        messages.append({'role': 'assistant', 'content': botReply})

# Function to get the program started.
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        # Gets the messaqe history limit from the user and if it isn't a positive integer resets the loop and prints an error.
        try:
            MESSAGE_HISTORY_LIMIT = int(input("Enter the message history limit (integer): "))
            if MESSAGE_HISTORY_LIMIT <= 0:
                print("Please enter a positive integer.")
                continue
            break
        # Handles every other error that isn't a negative integer.
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    SUMMARY_TRIGGER = MESSAGE_HISTORY_LIMIT # Fix this so that it uses MESSAGE_HISTORY_LIMIT instead of SUMMARY_TRIGGER everywhere
    MESSAGES_TO_KEEP = MESSAGE_HISTORY_LIMIT // 2

    while True:
        choice = input("""What do you want to do? (1-3)
        1) Create a new character.
        2) Select an existing character.
        3) Delete an existing character.
        4) Exit: """)
        match choice:
            case "1": 
                botName, botDescription, BotFirstMessage = get_user_information()

                #Saves the character (or doesnt)
                checkSave = input("Do you want to save this character (y/n)?: ")
                if checkSave == "y":
                    saveChar(botName, botDescription, BotFirstMessage)
                continue

            case "2": 
                charSelect()
            case "3":
                deleteChar()
                continue
            case "4":
                sys.exit()

# Idk why this is here, I read that you need to have this in every program so here it is. 
if __name__ == "__main__":
    main()

# TO DO:
# 1. Move some of the functions to seperate files for epic gamer
# 2. Make is so that the user can modify the first prompt if he wants to
# 2. Saving chat history
# 3. UI