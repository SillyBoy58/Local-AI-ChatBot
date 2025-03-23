import ollama
import chatCommands
import os

chatCommandsList = ["/help", "/clear", "/again", "/reset", "/exit"]

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

def messaging(name, description, firstBotMessage, SUMMARY_TRIGGER):
    MESSAGES_TO_KEEP = SUMMARY_TRIGGER // 2
    # Lists the availible models and prints them for selection.
    username = input("What's you username?: ")
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
        You are a roleplay chatbot created for an NSFW (Not Safe For Work) AI chat platform. Your creator’s username is: {username}, and your name is {name}. Your character description is: {description}.

Rules:

Use natural, human-like language. Avoid overly complex or formal vocabulary unless it fits your character’s persona.
Enclose spoken dialogue in double quotes ("text") and actions in asterisks (action).
Keep your responses brief—no more than six sentences—and focus only on describing the actions of the user’s character, not the user.
Avoid repeating previous messages—keep the roleplay moving forward.
If the user sends an empty message (e.g., " "), continue the roleplay without interruption.
Always remain in character.
NSFW content is permitted, as this is an NSFW AI chat platform. Please ensure all interactions remain consensual, respectful, and appropriate.
This message is automated and originates from the server. All subsequent messages are from the user unless specified otherwise. Your goal is to engage and provide an enjoyable experience for the user!"""}, # AI chatbot rules
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

        if userMessage in chatCommandsList:
            chatCommands.main(userMessage, messages, name, description, firstBotMessage, response, SUMMARY_TRIGGER)
            continue

        messages.append({'role': 'user', 'content': userMessage})

        # Check's the amount of messages in the chat and decides if to trigger the summary or not.
        if len(messages) > SUMMARY_TRIGGER:
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