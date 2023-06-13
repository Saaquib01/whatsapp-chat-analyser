from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

extract = URLExtract()


def fetch_stats(selected_users, df):

    if selected_users != 'Overall':
        df = df[df['user'] == selected_users]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the number of words
    words = []
    for i in df['message']:
        words.extend(i.split())

    # fetch the number of media messages
    num_media_messages = df[df['message'] == 'voice omitted'].shape[0]

    # fetch the number of link shared
    links = []
    for i in df['message']:
        links.extend(extract.find_urls(i))

    return num_messages, len(words), num_media_messages, len(links)

def first_last_msg (df):
    first_last_msg  = df.drop(columns=['date', 'month_num'], axis=1)[1:]
    first_last_msg = first_last_msg[~first_last_msg['user'].str.startswith('Group')]
    first_last_msg = first_last_msg[~first_last_msg['message'].str.endswith('contact')]
    first_last_msg ['date'] = first_last_msg [['year', 'month', 'day']].astype(str).agg('-'.join, axis=1)
    first_last_msg ['time'] = first_last_msg [['hour', 'minute']].astype(str).agg(':'.join, axis=1)
    first_last_msg  = first_last_msg [['user', 'message', 'date', 'time']]

    return first_last_msg  

def connected_days(df):
    first_date = pd.to_datetime(df['date'].min().date())
    last_date = pd.to_datetime(df['date'].max().date())
    connected_days = (last_date - first_date).days

    return connected_days


def avg_messages_per_day(selected_users,df):

    if selected_users != 'Overall':
        df = df[df['user'] == selected_users]

    first_date = pd.to_datetime(df['date'].min().date())
    last_date = pd.to_datetime(df['date'].max().date())
    num_days = (last_date - first_date).days

    num_messages = df.shape[0]
    avg_messages_per_day = num_messages / num_days
    
    return round(avg_messages_per_day)

def max_active_day(df):
    df['only_date'] = df['date'].dt.date
    daily_timeline = df.groupby(['only_date']).count()['message'].reset_index().rename(columns={'only_date':'Date','message':'Message Counts'})
    max_active_day = daily_timeline.nlargest(1, 'Message Counts')
    
    return max_active_day

def max_active_month(selected_users, df):
    timeline = monthly_timeline_msg(selected_users, df)
    max_month = timeline.loc[timeline['Message Count'].idxmax()]
    year = max_month['Year']
    month = max_month['Month']
    message_count = max_month['Message Count']
    max_active_month = pd.DataFrame({'Year': [year], 'Month': [month], 'Message Count': [message_count]})

    return max_active_month



def most_busy_users(df):
    df['user'] = df['user'].astype(str)
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'user': 'Name', 'count': 'Percentage'}
    )
    df = df[~df['Name'].str.startswith('Group')]
    
    return x, df


def create_wordcloud(selected_users, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_users != 'Overall':
        df = df[df['user'] == selected_users]

    temp = df[df['message'] != 'group_notification']
    temp = temp[temp['message'] != '<Media_omitted>\n']

    def remove_stopwords(message):
        y = []
        for i in message.lower().split():
            if i not in stop_words:
                y.append(i)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10,
                   background_color='White')
    temp['message'] = temp['message'].apply(remove_stopwords)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc


def most_common_words(selected_users, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_users != 'Overall':
        df = df[df['user'] == selected_users]

    temp = df[df['message'] != 'group_notification']
    temp = temp[temp['message'] != '<Media_omitted>\n']

    words = []

    for i in temp['message']:
        for word in i.lower().split():
            # Exclude words that contain emojis
            if word not in stop_words and not any(c for c in word if c in emoji.UNICODE_EMOJI['en']):
                words.append(word)

    most_common_words = pd.DataFrame(Counter(words).most_common(10)).rename(columns={0:'Words',1:'Counts'}).add_suffix('     ')

    return most_common_words



def emoji_helper(selected_users, df):

    if selected_users != 'Overall':
        df = df[df['user'] == selected_users]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_counts = Counter(emojis)
    top_5_emojis = emoji_counts.most_common(5)

    emoji_df = pd.DataFrame(top_5_emojis, columns=['Emoji     ', 'Count     '])

    return emoji_df


def monthly_timeline_msg(selected_users, df):

    if selected_users != 'Overall':
        df = df[df['user'] == selected_users]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+' - '+str(timeline['year'][i]))
    timeline = timeline.drop(columns=['month_num'],axis=1)
    timeline = timeline.rename(columns={'year': 'Year', 'month': 'Month', 'message': 'Message Count'})

    return timeline


def monthly_timeline(selected_users, df):

    if selected_users != 'Overall':
        df = df[df['user'] == selected_users]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+' - '+str(timeline['year'][i]))

    timeline['time'] = time

    timeline = timeline.drop(columns=['month_num'],axis=1)

    return timeline



def daily_message(selected_users, df):

    if selected_users != 'Overall':
        df = df[df['user'] == selected_users]
    
    df['only_date'] = df['date'].dt.date

    daily_message = df.groupby(['only_date']).count()['message'].reset_index().rename(columns={'only_date':'Date','message':'Message Counts'})
    
    return daily_message
