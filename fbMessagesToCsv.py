# written with chatgpt
import csv
import os
import json

def parse_message_folder(folderpath):
    messages = []
    for messageFolder in os.listdir(folderpath): # opened up message folder
        messagePath = os.path.join(folderpath, messageFolder) # opened up message path
        for filename in os.listdir(messagePath): # opened up file
            if filename.endswith(".json"):
                filepath = os.path.join(messagePath, filename)
                with open(filepath, "r") as f:
                    message_information = {"dialog_id": messagePath.replace(folderpath, '') + "/" + filename, "dialog": []}
                    data = json.load(f)
                    message_counter = len(data["messages"])-1
                    for message in data["messages"]:
                        if "content" in message:
                            if message["content"] == "You are now connected on Messenger":
                                message_counter -= 1 # if this pops up in the middle of the conversation, it will mess up the order of the messages
                            else:
                                sender_id = message["sender_name"]
                                timestamp = message["timestamp_ms"]
                                message_information['dialog'].insert(0, {"text": message["content"], "sender_id": sender_id, "timestamp": timestamp, "message_id": message_counter})
                                message_counter -= 1
                    messages.append(message_information)
    
    # write messages to CSV file
    with open('messages.csv', mode='w', encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['dialog_id', 'text', 'sender_id', 'timestamp', 'message_id'])
        for message in messages:
            for dialog in message['dialog']:
                if 'sender_id' not in dialog or dialog['sender_id'] == '':
                    dialog['sender_id'] = 'Unknown'
                if 'text' not in dialog or dialog['text'].encode('ascii', 'ignore').decode('ascii') == '': # the case when emoji stripping removes all text
                    dialog['text'] = ' '
                writer.writerow([message['dialog_id'], dialog['text'].encode('ascii', 'ignore').decode('ascii'), dialog['sender_id'], dialog['timestamp'], dialog['message_id']]) # note, the encode, decode here removes weird characters like emojis
            # writer.writerow(['Facebook Narrator', 'NA', 'NA', 'NA', 'NA']) # special row to indicate the conversation has ended and a new one is starting... Need to think of a better way to do this, but this is a cheap hacky solution for now
            # should just add padding rows = to the amount of context. That way it will never be seen 
            # might also need to consider the case when messages are deleted and it breaks because of that
    return messages

if __name__ == "__main__":
    folderpath = "./facebook-messages/messages/inbox"
    messages = parse_message_folder(folderpath)
    with open("messages.json", "w") as f:
        json.dump(messages, f, indent=4)

# import json
# import csv
# import os

# def parse_message_file(filepath):
#     with open(filepath, "r") as f:
#         data = json.load(f)
#         for message in data["messages"]:
#             if "content" in message:
#                 yield {
#                     "text": message["content"],
#                     "sender_id": message["sender_name"],
#                     "timestamp": message["timestamp_ms"]
#                 }

# def parse_message_folder(folderpath, outputfile):
#     with open(outputfile, "w", encoding="utf-8") as f: # without this specification, it cant read emojis
#         writer = csv.DictWriter(f, fieldnames=["text", "sender_id", "timestamp"])
#         writer.writeheader()
#         for messageFolder in os.listdir(folderpath):
#             messagePath = os.path.join(folderpath, messageFolder)
#             for filename in os.listdir(messagePath):
#                 if filename.endswith(".json"):
#                     filepath = os.path.join(messagePath, filename)
#                     for message in parse_message_file(filepath):
#                         writer.writerow(message)


# if __name__ == "__main__":
#     parse_message_folder("./facebook-messages/messages/inbox", "output.csv")



# def parse_message_folder(folderpath):
#     messages = []
#     for messageFolder in os.listdir(folderpath):
#         messagePath = os.path.join(folderpath, messageFolder)
#         for filename in os.listdir(messagePath):
#             if filename.endswith(".json"):
#                 filepath = os.path.join(messagePath, filename)
#                 with open(filepath, "r") as f:
#                     data = json.load(f)
#                     for message in data["messages"]:
#                         if "content" in message:
#                             messages.append({
#                                 "text": message["content"],
#                                 "sender_id": message["sender_name"],
#                                 "timestamp": message["timestamp_ms"]
#                             })
#     return messages

# if __name__ == "__main__":
#     folderpath = "./facebook-messages/messages/inbox"
#     messages = parse_message_folder(folderpath)
#     with open("messages.json", "w") as f:
#         json.dump(messages, f)