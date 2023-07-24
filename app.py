import streamlit as st
import preprocessor, helper

import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

# uploaded_file = st.file_uploader("Choose a file")    # this will give the upload option in central screen
# to get upload file option in sidebar
uploaded_file = st.sidebar.file_uploader("Choose a file")

st.title("Welcome to the Whatsapp Chat Analyzer !!")
st.markdown("#### Plz select a file to continue")

if uploaded_file is not None:

    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    # as the data is in stream we need to convert it into text
    data = bytes_data.decode("utf-8")
    # st.text(data)  # this will show the data on screen

    df = preprocessor.preprocess(data)
    # st.dataframe(df)


    # ! fetch user list
    user_list = df['Users'].unique().tolist()

    # removing the 'Group-Notification' from users
    user_list.remove('Group-Notification')

    # sorting in ascending order according to names
    user_list.sort()

    # adding 'overall' for group analysis
    user_list.insert(0,'Overall')

    # display a selectbox to select the user
    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    # display a button to start analysis
    if st.sidebar.button("Show Analysis"):

        # stats
        st.title("Top Statistics")

        # calling the fetch_stats() fn. from 'helper.py' file and passing selected user
        # to it to calculate total number of message according to the 'selecte_user'
        num_messages, words, num_media_msgs, num_shared_links = helper.fetch_stats(selected_user, df)

        # col1, col2, col3, col4 = st.beta_columns(4)  #This was the beta function and is now removed
        col1, col2, col3, col4 = st.columns(4)

        # Total Msgs
        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        # Total words
        with col2:
            st.header("Total Words")
            st.title(words)

        # Total media
        with col3:
            st.header("Total Media Shared")
            st.title(num_media_msgs)

        # Total Links
        with col4:
            st.header("Total Links Shared")
            st.title(num_shared_links)


        # Monthly timeline
        st.header("Monthly Timeline")
        monthly_timeline_df = helper.monthly_timeline(selected_user, df)
        plt.figure(figsize=(10,6))
        fig, ax1 = plt.subplots()
        ax1.plot(monthly_timeline_df['Time'], monthly_timeline_df['Messages'], color = 'purple')
        plt.xticks(rotation = 'vertical')
        st.pyplot()


        # Daily Timeline
        st.header("Daily Timeline")
        daily_timeline_df = helper.daily_timeline(selected_user, df)
        plt.figure(figsize=(30,10))
        fig, ax2  = plt.subplots()
        ax2.plot(daily_timeline_df['Only_date'], daily_timeline_df['Messages'], color = 'aqua')
        plt.xticks(rotation = 40)
        st.pyplot()


        # Activity Map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        # monthly activity map
        with col1:
            st.header("Monthly Activity Map")
            monthly_activity_df = helper.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(monthly_activity_df['Month'], monthly_activity_df['Messages'], color = 'crimson')
            plt.xticks(rotation = 40)
            st.pyplot(fig)

        # daily activity map
        with col2:
            st.header("Daily Activity Map")
            daily_activity_df = helper.daily_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(daily_activity_df['Day_name'], daily_activity_df['Messages'], color = 'orange')
            plt.xticks(rotation = 40)
            st.pyplot(fig)

        # Weekly Heatmap
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


        # find busiest user in the group(Group Level)
        if selected_user == 'Overall':
            st.title('Most Busy User')
            col1, col2 = st.columns(2)

            name, count, new_df = helper.most_busy_user(df)
            # fig, ax = plt.subplots()

            # bar chart of top 5 users
            with col1:
                st.header("Busiest Users")
                # sns.barplot(x = name, y = count, data = df)
                fig, ax = plt.subplots()
                ax.bar(name, count, color = 'pink')
                # ax.bar(name, count)   # this line will be used when we plot using matplotlib

                # # below line will hide the depreceation warning
                # st.set_option('deprecation.showPyplotGlobalUse', False)

                plt.xlabel('Users')
                plt.ylabel('No. of Msgs')
                plt.xticks(rotation = 40)
                st.pyplot(fig)

            # User wise msg percentage
            with col2:
                st.header("Msgs Percentage")
                new_df = new_df.rename(columns={'Users' : 'Username', 'count' : 'Percentage'})
                st.dataframe(new_df)


        # Wordcloud
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        # Top 20 most used words
        most_used_words_df = helper.most_used_words(selected_user, df)
        st.title("Most Used Words")
        fig, ax = plt.subplots()
        ax.barh(most_used_words_df[0], most_used_words_df[1])
        plt.xticks(rotation = 10)
        st.pyplot(fig)


        col1, col2 = st.columns(2)

        # most used emojis
        with col1:
            most_used_emojis_df = helper.most_used_emojis(selected_user, df)
            st.title("Most used emojis")
            st.dataframe(most_used_emojis_df)

        # emoji pie chart
        with col2:
            st.title("Emoji Pie Chart")
            fig,ax = plt.subplots()
            ax.pie(most_used_emojis_df[1].head(),labels=most_used_emojis_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)

















