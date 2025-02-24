from urlextract import URLExtract
from wordcloud import WordCloud, wordcloud
extract = URLExtract()

def fetch_stats(selected_user, df):
    # Ensure DataFrame is not empty
    if df.empty:
        return 0, 0, 0

    # Ensure 'messages' column exists
    if 'messages' not in df.columns:
        return 0, 0, 0  # Avoid KeyError

    # Apply filter only if a specific user is selected
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # If filtering made the DataFrame empty, return 0 values
    if df.empty:
        return 0, 0, 0

    # Count total messages
    num_messages = df.shape[0]

    # Count total words
    words = []
    for message in df['messages']:
        if isinstance(message, str):  # Ensure only strings are split
            words.extend(message.split())

    # Count media messages
    num_media_messages = df[df['messages'].str.contains("image omitted", na=False, case=False)].shape[0]

    links = []
    for message in df['messages']:
        links.extend(extract.find_urls(message)) 

    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    return x

def create_wordcloud(selected_user,df):
        if selected_user != 'Overall':
            df = df[df['user'] == selected_user]

        wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
        df_wc = wc.generate(df['messages'].str.cat(sep=" "))
        return df_wc


    # if selected_user == 'overall':
    #     num_messages = df.shape[0] 
    #     words = []
    #     for messages in df['messages']:
    #         words.extend(messages.split())
    #     return num_messages , len(words)
    # else:
    #    new_df = df[df['user'] == selected_user]
    #    num_messages = new_df.shape[0]
    #    words = []
    #    for messages in new_df['messages']:
    #        words.extend(messages.split())
    #    return num_messages , len(words)


