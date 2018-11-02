import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime


class ChatStat:
    def __init__(self, chat_df, msg_df):
        self.chat_df = chat_df
        self.msg_df = msg_df

    def print_df(self):
        """ prints both dataframes """
        print("------ CHATS DATAFRAME ------")
        print(self.chat_df)
        print("------ MESSAGES DATAFRAME ------")
        print(self.msg_df)

    def biggest_chat(self, top=10, ax=None):
        """ plots the largest chats overall. by default, only plots top 10 """
        count_df = self.msg_df.groupby("thread_path").count()
        count_df.sort_values("msg", inplace=True, ascending=False)
        count_df = count_df[:top]
        count_df = count_df.join(self.chat_df)
        plot = count_df.plot(ax=ax, x="title", y="msg", kind="bar", legend=False, title="Largest Chats (top %d)" % top, rot=70)
        plot.set_ylabel("Total number of messages")
        plot.set_xlabel("Chat name")

    def sent_from(self, chat, top=10, omit_first=False, ax=None):
        """ plots the number of messages received based on sender for the DF passed in. Can be used on filtered DataFrames or filtered. by default, only plots top 10 senders """
        start = int(omit_first)
        count_df = chat.groupby("sender").count()
        count_df.sort_values("msg", inplace=True, ascending=False)
        count_df = count_df[start:top]
        count_df = count_df.join(self.chat_df)
        plot = count_df.plot(ax=ax, y="msg", kind="bar", legend=False, title="Number of messages by sender (top %d)" % top, rot=70)
        plot.set_ylabel("Total number of messages")
        plot.set_xlabel("Message Sender")

    def msg_types(self, df, ax=None, fsize=None):
        """ Takes a filtered msg_df (based on sender or chat title) and breaks down the type of messages """
        type_dict = {"type": {"stickers": df.sticker.count(), "photos": df.photos.count(), "videos": df.videos.count(), "links": df[[("http" in str(msg)) for msg in df.msg]].msg.count()}}
        type_df = pd.DataFrame(type_dict)
        plot = type_df.plot(ax=ax, kind='pie', figsize=fsize, y='type', title="Types of Multimedia")
        plot.set_ylabel("")

    def chat_types(self, messages, ax=None, fsize=None):
        grouped = messages.groupby("thread_path").count().join(self.chat_df).groupby("thread_type").sum()
        plot = grouped.plot(ax=ax, kind='pie', figsize=fsize, y='msg', title='Chat Type')
        plot.set_ylabel("")

    def personal_stats(self, name):
        """ Plots a bunch of different plots based on a fitlered DataFrame of messages from `name` """
        from_sender = self.msg_df[self.msg_df['sender'] == name]
        print("Total # of messages: %d" % from_sender.msg.size)

        if from_sender.empty:
            print("Could not find any messages from %s" % name)
            return ""

        chat_count = from_sender.groupby("thread_path").count()
        chat_count = chat_count.join(self.chat_df)
        total_msg = chat_count["msg"].sum()
        chat_count['proportion'] = chat_count["msg"] / total_msg
        full = chat_count.loc[:, ["title", "proportion"]].set_index("title").sort_values('proportion', ascending=False)
        if full.size > 6:
            pie = full[:5]
            pie = pie.append(pd.DataFrame([['others', 1 - sum(pie.proportion)]], columns=['title', 'proportion']).set_index('title'))
        else:
            pie = full

        fig, proportions = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
        fig.suptitle("Where are %s's messages going?" % name, fontsize=20)
        pie.plot(ax=proportions[0], kind='pie', y='proportion', legend=False, labeldistance=0.2, rotatelabels=True).set_ylabel("")
        proportions[1].axis('off')
        full = (full * 100).round(4)[:20]
        proportions[1].table(cellText=full.values, rowLabels=full.index, loc='right', colLabels=["percentage"], colWidths=[0.2]).scale(1.2, 1.2)

        _, pieax = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
        self.msg_types(from_sender, pieax[0])
        self.chat_types(from_sender, pieax[1])
        self.time_stats(from_sender)
        self.word_counts(from_sender)

    def stat_by_chat(self, chat):
        """ Plots a bunch of different plots based on a fitlered DataFrame of messages in the chat `chat` """
        thread = self.chat_df[self.chat_df.title == chat].index[0]
        from_chat = self.msg_df[self.msg_df.thread_path == thread]
        print("Total # of messages: %d" % from_chat.msg.size)
        self.sent_from(from_chat, top=10)
        self.msg_types(from_chat, fsize=(8, 8))
        self.time_stats(from_chat)
        self.word_counts(from_chat)

    def time_stats(self, df):
        """ Plots the time-based activity of the passed in DataFrame `df` """
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(16, 10))
        fig.suptitle("Time-based Stats: Procrastination Metrics", fontsize=20)
        time_indexed = df.set_index('timestamp')
        time_indexed['year'] = time_indexed.index.year
        time_indexed['month'] = time_indexed.index.strftime("%b")
        time_indexed['hour'] = time_indexed.index.hour
        time_indexed['minute'] = time_indexed.index.minute

        yearly = time_indexed.groupby("year").count()
        yearly.plot(ax=axes[0][0], kind='bar', y='msg', legend=False)
        axes[0][0].set_ylabel("Number of Messsages")

        monthly = time_indexed.groupby("month").count()
        monthly = monthly.reindex(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
        monthly.plot(ax=axes[0][1], kind='bar', y='msg', legend=False)
        axes[0][1].set_ylabel("Number of Messsages")

        hourly = time_indexed.groupby("hour").count()
        hourly.plot(ax=axes[1][0], kind='bar', y='msg', legend=False)
        axes[1][0].set_ylabel("Number of Messsages")

        minutely = time_indexed.groupby("minute").count()
        minutely.plot(ax=axes[1][1], kind='bar', y='msg', legend=False)
        axes[1][1].set_ylabel("Number of Messsages")

    def word_counts(self, chat, lengths=[1, 3, 5, 7], top=10):
        """ Counts the word usage based on the passed in DataFrame `chat` and plots words that are longer than `lengths` """
        messages = chat.msg
        words = {'count': {}}
        for msg in messages:
            msg = str(msg).encode('latin1').decode('utf8')  # need this to get around poor encoding by Facebook
            for word in msg.split(" "):
                word = word.lower()
                word = word.rstrip('?:!.,;')
                if word in words['count']:
                    words['count'][word] += 1
                else:
                    words['count'][word] = 1

        word_df = pd.DataFrame(words).sort_values("count", ascending=False)
        num_plots = len(lengths)
        numrows = num_plots // 2 + num_plots % 2
        fig, ax = plt.subplots(nrows=numrows, ncols=2, figsize=(16, 5 * numrows))
        if num_plots % 2 != 0:
            if numrows > 1:
                ax[numrows - 1][1].axis("off")
            else:
                ax[1].axis("off")
        fig.suptitle("Word Counts", fontsize=20)
        plot_index = 0

        def create_word_df(l):
            len_bool = [(len(word) >= l) for word in word_df.index]
            df = word_df[len_bool][:top]
            return df

        for l in lengths:
            r = plot_index // 2
            c = 0 if plot_index % 2 == 0 else 1
            plot_index += 1
            if numrows > 1:
                create_word_df(l).plot(ax=ax[r][c], kind="bar", y="count", legend=False, rot=50, title="Top words %d letters or more" % l)
            else:
                create_word_df(l).plot(ax=ax[c], kind="bar", y="count", legend=False, rot=50, title="Top words %d letters or more" % l)

    def chat_counts(self, top=10, omit_first=False, ax=None):
        """ counts the number of chats each person is in and plots the top x people in the most chats """
        start = int(omit_first)
        counts = self.msg_df.groupby(["sender", "thread_path"]).size().reset_index().groupby("sender").count().sort_values('thread_path', ascending=False)
        counts[start:top].plot(ax=ax, kind="bar", y="thread_path", title="Number of group chats by person", legend=False, rot=50).set_ylabel("Count")


if __name__ == "__main__":
    import loader

    stat = ChatStat(*loader.load_from_csv())
    stat.personal_stats("Dilip Rathinakumar")
