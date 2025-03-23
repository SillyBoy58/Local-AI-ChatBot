import os
import sys
import chatMan

def main(userMessage, messages, name, description, firstBotMessage, response, SUMMARY_TRIGGER):
    match userMessage:
        case "/exit":
            sys.exit()
        case "/restart":
            sys.stdout.flush()  
            os.execv(sys.executable, [sys.executable, __file__] + sys.argv) # No idea what any of this is, but it apperently works so ¯\(ツ)/¯
        case "/reset":
            return chatMan.messaging(name, description, firstBotMessage, SUMMARY_TRIGGER)
        case "/again":
            again(messages, userMessage)
            return
            # Generate a new response using the same context
        case "/clear":
            messages.pop()
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{name}: {response['message']['content']}\n")
            return
        case "/help":
            messages.pop()
            listCommands() # Lists the availible commands.
            return

def listCommands():
    print("""Currently available commands:
        /help - displays this screen;
        /exit - leaves the program;
        /restart - restarts the program;
        /reset - resets the current conversation, keeping the preferences.
        /again - generates another response to the latest message deleting the current generated response.
        /clear - clears all text (to make the terminal more clean).""")

def again(messages, userMessage):
    if len(messages) > 2:  # Ensures there's enough history to work with
        messages.pop()  # Removes "/again" (last user message)
        messages.pop()  # Removes the last AI response

        # Generate a new AI response to the last user message (which is still in messages)
        response = ollama.chat(model=model, messages=messages)
        botReply = response['message']['content']
        
        print(f"{name}: {botReply}\n")
        messages.append({'role': 'assistant', 'content': botReply})
    else:
        print("No previous AI response to regenerate.")