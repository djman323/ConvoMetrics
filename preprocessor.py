import re
import pandas as pd

def preprocess(data):
    # Corrected pattern to match timestamps with seconds
    pattern = r'\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\]'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Convert extracted dates to datetime format
    df = pd.DataFrame({'user_messages': messages, 'date': dates})
    df['date'] = df['date'].str.strip('[]')  # Remove square brackets
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %H:%M:%S')

    users = []
    messages = []
    for message in df['user_messages']:
        entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)
        if len(entry) > 1:  # If user name is present
            users.append(entry[1])
            messages.append(entry[2].strip())  # Remove extra spaces
        else:
            users.append('group_notification')
            messages.append(entry[0].strip())

    df['user'] = users
    df['messages'] = messages
    df.drop(columns=['user_messages'], inplace=True)

    # Extracting additional date components
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['second'] = df['date'].dt.second  # Added second column for accuracy

    return df
