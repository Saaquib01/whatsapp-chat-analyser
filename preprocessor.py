import re
import pandas as pd

def preprocess(data):
    pattern = r'^\[(\d{2}\/\d{2}\/\d{2}, \d{1,2}:\d{2}:\d{2} [AP]M)\] (.+)$'

    # Read the contents of the text document with the appropriate encoding
    lines = data.splitlines()

    message = []
    timestamp = []

    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace if necessary
        m = re.match(pattern, line)
        if m:
            timestamp.append(m.group(1))
            message.append(m.group(2))

    df = pd.DataFrame({'user_messages': message, 'message_date': timestamp})

    df['message_date'] = pd.to_datetime(timestamp, format='%d/%m/%y, %I:%M:%S %p')
    df.rename(columns={'message_date':'date'}, inplace=True)

    df[['user', 'message']] = df['user_messages'].str.split(': ', n=1, expand=True)
    df.drop('user_messages', axis=1, inplace=True)

    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df

