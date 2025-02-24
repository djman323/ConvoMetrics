from pydoc import Helper
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import preprocessor , helper 
 # Importing the preprocess function

# Streamlit App UI
st.sidebar.title("📊 WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("📂 Upload WhatsApp Chat File (.txt)", type=["txt"])

if uploaded_file is not None:
    # Read file contents
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")  # Convert bytes to string

    st.write("📂 **File Uploaded Successfully!**")  


    # Process the chat data
    df = preprocessor.preprocess(data)
    st.dataframe(df)

    user_list = df['user'].unique().tolist()
    if user_list[0] == 'Nerds 🤫':
        user_list.remove('Nerds 🤫')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox("show user", user_list)

    if st.sidebar.button("Show Analysis"):
        print("Selected User:", selected_user)
        print(df.head())  # See if data is properly loaded
        print(df.shape)   # Check total rows & columns


        num_messages , words , num_media_messages , num_links= helper.fetch_stats(selected_user,df)

        print(f"Total Messages: {num_messages}")
        print(f"Total Words: {words}")
        print(f"Total Media Shared: {num_media_messages}")
        print(df.columns)  # This will show all column names


        col1 , col2, col3 , col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)
            
        if selected_user == 'Overall':
            st.title('Most busy Users')
            x = helper.most_busy_users(df)
            fig , ax = plt.subplots()
            
            col1 , col2 = st.columns(2)

            with col1:
                ax.bar(x.index , x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(df)

        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig) 




    # if df.empty:
    #     st.error("⚠️ No messages found! Please check your file format.")
    # else:
    #     st.success("✅ Data Loaded Successfully!")
    #     st.dataframe(df)  # Display DataFrame in Streamlit
    #     user_list = df['user'].unique().tolist()
    #     user_list.remove(' Nerds 🤫')
    #     user_list.sort()
    #     user_list.insert(0, 'Overall')
    #     st.sidebar.selectbox("show user", user_list)  

    #     if st.sidebar.button("Show Analysis"):
    #         st.write("### 📌 Chat Statistics")
    #     st.write(f"**Total Messages:** {df.shape[0]}")
    #     st.write(f"**Total Users:** {df['user'].nunique()}")
        
    #     # Show top users by message count
    #     st.write("### 🏆 Top Users by Message Count")
    #     st.bar_chart(df['user'].value_counts())

    #     # Show messages over time
    #     st.write("### 📈 Messages Over Time")
    #     df['date_only'] = df['date'].dt.date
    #     daily_counts = df.groupby('date_only').count()
    #     st.line_chart(daily_counts['messages'])

            
      
        
  



