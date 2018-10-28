import matplotlib.pyplot as plt
import pandas as pd


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
        return count_df.plot(x="title", y="msg", kind="bar", legend=False)

    def sent_from(self, top=10):
        count_df = self.msg_df.groupby("sender").count()
        count_df.sort_values("msg", inplace=True, ascending=False)
        count_df = count_df[:top]
        count_df = count_df.join(self.chat_df)
        return count_df.plot(y="msg", kind="bar", legend=False)

    def msg_types(self, df):
        """ Takes a filtered msg_df (based on sender or chat title) and breaks down the type of messages """
        type_dict = {"type": {"stickers": df.sticker.count(), "photos": df.photos.count(), "videos": df.videos.count(), "links": df[[("http" in str(msg)) for msg in df.msg]].msg.count()}}
        type_df = pd.DataFrame(type_dict)
        plot = type_df.plot(kind='pie', y='type')
        plot.set_ylabel("")

        return plot

    def personal_stats(self, name):
        from_sender = self.msg_df[self.msg_df['sender'] == name]
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
        pieplot = pie.plot(ax=proportions[0], kind='pie', y='proportion', legend=False, labeldistance=0.2, rotatelabels=True).set_ylabel("")
        proportions[1].axis('off')
        full = (full * 100).round(4)
        proportions[1].table(cellText=full.values, rowLabels=full.index, loc='right', colLabels=full.columns, colWidths=[0.2]).scale(1.2, 1.2)

        message_types = msg_types(from_sender)

        return proportions, message_types


if __name__ == "__main__":
    import loader

    stat = ChatStat(*loader.load_from_csv())
    stat.print_df()
