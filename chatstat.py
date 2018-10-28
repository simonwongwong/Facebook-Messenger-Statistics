import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime


class ChatStat:
    def __init__(self, chat_df, msg_df):
        self.chat_df = chat_df
        self.msg_df = msg_df

    def print_df(self):
        print("------ CHATS DATAFRAME ------")
        print(self.chat_df)
        print("------ MESSAGES DATAFRAME ------")
        print(self.msg_df)

    def biggest_chat(self, top=10):
        count_df = self.msg_df.groupby("thread_path").count()
        count_df.sort_values("msg", inplace=True, ascending=False)
        count_df = count_df[:top]
        count_df = count_df.join(self.chat_df)
        count_df.plot(x="title", y="msg", kind="bar", legend=False)

    def sent_from(self, top=10, omit_first=False):
        count_df = self.msg_df.groupby("sender").count()
        count_df.sort_values("msg", inplace=True, ascending=False)
        count_df = count_df[1:top] if omit_first else count_df[:top]
        count_df = count_df.join(self.chat_df)
        count_df.plot(y="msg", kind="bar", legend=False)

    def msg_types(self, df):
        """ Takes a filtered msg_df (based on sender or chat title) and breaks down the type of messages """
        type_dict = {"type": {"stickers": df.sticker.count(), "photos": df.photos.count(), "videos": df.videos.count(), "links": df[[("http" in str(msg)) for msg in df.msg]].msg.count()}}
        type_df = pd.DataFrame(type_dict)
        plot = type_df.plot(kind='pie', y='type', figsize=(8, 8), title="Types of Multimedia")
        plot.set_ylabel("")

    def personal_stats(self, name):
        from_sender = self.msg_df[self.msg_df['sender'] == name]
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

        _fig, proportions = plt.subplots(nrows=1, ncols=2, figsize=(20, 10))
        pie.plot(ax=proportions[0], kind='pie', y='proportion', legend=False, labeldistance=0.2, rotatelabels=True).set_ylabel("")
        proportions[1].axis('off')
        full = (full * 100).round(4)
        proportions[1].table(cellText=full.values, rowLabels=full.index, loc='right', colLabels=full.columns, colWidths=[0.2]).scale(1.2, 1.2)

        self.msg_types(from_sender)
        self.time_stats(from_sender)

    def stat_by_chat(self, chat):
        thread = self.chat_df[self.chat_df.title == chat].index[0]
        from_chat = self.msg_df[self.msg_df.thread_path == thread]
        self.msg_types(from_chat)
        self.time_stats(from_chat)

    def time_stats(self, df):
        _, axes = plt.subplots(nrows=2, ncols=2, figsize=(16, 10))
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


if __name__ == "__main__":
    import loader

    stat = ChatStat(*loader.load_from_csv())
    stat.personal_stats("Dilip Rathinakumar")
