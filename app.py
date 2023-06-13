import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import preprocessor
import helper

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # Show Analysis wrt
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_users = st.sidebar.selectbox("Show Analysis wrt", user_list)
    if st.sidebar.button("Show Analysis"):


        #stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_users, df)
        st.markdown(f'<h1 style="color: red; text-align: center; font-size: 70px;text-decoration: underline;">TOP  STATISTICS</h1>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f'<h1 style="color: skyblue; font-size: 40px;">Total Messages</h1>', unsafe_allow_html=True)
            st.markdown(f'<h1 style="color: purple; font-size: 38px;">{num_messages}</h1>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<h1 style="color: skyblue; font-size: 40px;">Total Words</h1>', unsafe_allow_html=True)
            st.markdown(f'<h1 style="color: purple; font-size: 38px;">{words}</h1>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<h1 style="color: skyblue; font-size: 40px;">Total links Shared</h1>', unsafe_allow_html=True)
            st.markdown(f'<h1 style="color: purple; font-size: 38px;">{num_links}</h1>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f'<h1 style="color: skyblue; font-size: 35px;">Total Media Shared</h1>', unsafe_allow_html=True)
            st.markdown(f'<h1 style="color: purple; font-size: 38px;">{num_media_messages}</h1>', unsafe_allow_html=True)
        with col2:
            avg_messages_per_day = helper.avg_messages_per_day(selected_users,df)
            st.markdown(f'<h1 style="color: skyblue; font-size: 35px;">Avg No of Messages Per day</h1>', unsafe_allow_html=True)
            st.markdown(f'<h1 style="color: purple; font-size: 38px;">{avg_messages_per_day}</h1>', unsafe_allow_html=True)

        if selected_users == 'Overall':
            col1, col2, col3 = st.columns(3)
            with col1:
                first_last_msg = helper.first_last_msg(df)
                st.markdown(f'<h1 style="color: skyblue; font-size: 35px;">First Message Sent</h1>', unsafe_allow_html=True)
                st.dataframe(first_last_msg.head(1))
            with col2:
                first_last_msg = helper.first_last_msg(df)
                st.markdown(f'<h1 style="color: skyblue; font-size: 35px;">Last Message Sent</h1>', unsafe_allow_html=True)
                st.dataframe(first_last_msg.tail(1))
            with col3:
                connected_days = helper.connected_days(df)
                st.markdown(f'<h1 style="color: skyblue; font-size: 35px;">Total Connected Days</h1>', unsafe_allow_html=True)
                st.markdown(f'<h1 style="color: purple; font-size: 38px;">{connected_days}</h1>', unsafe_allow_html=True)

            with col1:
                max_active_day = helper.max_active_day(df)
                st.markdown(f'<h1 style="color: skyblue; font-size: 35px;">Most Active Day</h1>', unsafe_allow_html=True)
                st.dataframe(max_active_day.head(1))
            with col2:
                max_active_month = helper.max_active_month(selected_users,df)
                st.markdown(f'<h1 style="color: skyblue; font-size: 35px;">Most Active Month</h1>', unsafe_allow_html=True)
                st.dataframe(max_active_month.head(1))


        # month wise
        st.markdown(f'<h1 style="color: red; text-align: center; font-size: 50px;text-decoration: underline;">MONTH  WISE</h1>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f'<h1 style="color: skyblue; text-align: center; font-size: 40px;">GRAPH</h1>', unsafe_allow_html=True)
            timeline = helper.monthly_timeline(selected_users, df)
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'], color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            timeline = helper.monthly_timeline_msg(selected_users, df)
            st.markdown(f'<h1 style="color: skyblue; font-size: 40px;">Message  Counts</h1>', unsafe_allow_html=True)
            st.dataframe(timeline)


        # finding the busiest people in the group(Group Level)
        if selected_users == 'Overall':
            st.markdown(f'<h1 style="color: red; text-align: center; font-size: 50px;text-decoration: underline;">MOST  BUSY  USERS</h1>', unsafe_allow_html=True)
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f'<h1 style="color: skyblue; text-align: center; font-size: 40px;">GRAPH</h1>', unsafe_allow_html=True)
                num_bars = len(x)
                colors = plt.cm.rainbow(np.linspace(0, 1, num_bars))
                ax.bar(x.index, x.values, color=colors,alpha=0.5)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.markdown(f'<h1 style="color: skyblue; font-size: 35px;">CONTRIBUTIONS</h1>', unsafe_allow_html=True)
                st.dataframe(new_df)


        # WordCloud
        st.markdown(f'<h1 style="color: red; text-align: center; font-size: 50px;text-decoration: underline;">WORD WISE ANALYSIS</h1>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f'<h1 style="color: skyblue;text-align: center; font-size: 40px;">WordCloud</h1>', unsafe_allow_html=True)
            df_wc = helper.create_wordcloud(selected_users, df)
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)
        # with col2:
        #     st.markdown(f'<h1 style="color: skyblue; font-size: 40px;">Top 10 Used Words</h1>', unsafe_allow_html=True)
        #     most_common_words = helper.most_common_words(selected_users, df)
        #     st.dataframe(most_common_words)


        # # Emoji analysis
        # st.markdown(f'<h1 style="color: red; text-align: center; font-size: 50px;text-decoration: underline;">EMOJI ANALYSIS</h1>', unsafe_allow_html=True)

        # col1,col2 = st.columns(2)

        # with col1:
        #     st.markdown(f'<h1 style="color: skyblue; font-size: 40px;">Top 5 Emojis Used</h1>', unsafe_allow_html=True)
        #     emoji_df = helper.emoji_helper(selected_users, df)
        #     st.dataframe(emoji_df.head(5))
        # with col2:
        #     st.markdown(f'<h1 style="color: skyblue; font-size: 40px;">Pie Chart</h1>', unsafe_allow_html=True)
        #     fig, ax = plt.subplots()
        #     ax.pie(emoji_df['Count     '], labels=emoji_df['Emoji     '], autopct='%1.2f%%', startangle=90)
        #     ax.axis('equal')
        #     st.pyplot(fig)
        
        st.markdown(f'<h1 style="color: red; text-align: center; font-size: 40px;text-decoration: underline;">More features will be added soon</h1>', unsafe_allow_html=True)

