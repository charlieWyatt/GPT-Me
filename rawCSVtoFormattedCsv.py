import pandas

if __name__ == "__main__":
    data = pandas.read_csv('messages.csv', encoding="utf-8")
    maxStringLength = 0
    for x in data['text']:
        if len(x) > maxStringLength:
            maxStringLength = len(x)
    print(maxStringLength)
    data = data[['sender_id', 'text']]
    data.rename(columns={'sender_id': 'name', 'text': 'line'}, inplace=True)
    print(data.sample(15))
    data.to_csv('formattedMessages.csv', index=False)