"""
Generates a report with all-time stats
"""
import sys
import os
import chatstat
import loader
import plotly.offline as po
from pathlib import Path
from plotly.subplots import make_subplots
from tkinter import Tk
from tkinter.filedialog import askdirectory

if __name__ == "__main__":
    Tk().withdraw() 
    msg_dir = askdirectory(title="Select message directory", initialdir=os.getcwd())
    try:
        print(f"Parsing data from {msg_dir}")
        chat_df, msg_df = loader.parse_from_json(msg_dir)
    except Exception as e:
        print("Could not load messenger data")
        print(f"Exception caught: {e}")
        quit()

    cs = chatstat.ChatStat(chat_df, msg_df)

    # who are you chatting with?
    html = ''
    who = make_subplots(rows=2, cols=2, specs=[[{"type": "bar"}, {"type": "bar"}], [{"type": "bar", "colspan": 2}, None]],
                        subplot_titles=['# of Messages by Sender', '# of Chats by Sender', '# of Messages by Chat'])
    who.add_trace(cs.sent_from(top=10, omit_first=True, kind='bar', show=False), row=1, col=1)
    who.add_trace(cs.chat_counts(top=10, omit_first=True, show=False), row=1, col=2)
    who.add_trace(cs.biggest_chat(top=30, kind='bar', show=False), row=2, col=1)
    who.update_layout(height=950, width=950, showlegend=False, title_text="Who are you chatting with?")
    html += po.plot(who, output_type='div')
    # proportional
    who_pct = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]])
    who_pct.add_trace(cs.sent_from(top=10, omit_first=True, kind='pie', show=False), row=1, col=1)
    who_pct.add_trace(cs.biggest_chat(top=10, kind='pie', show=False), row=1, col=2)
    who_pct.update_layout(height=475, width=950, showlegend=True, title_text="Stats by Proportion of Messages")
    html += po.plot(who_pct, output_type='div')

    # how are you chatting?
    how = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]])
    how.add_trace(cs.msg_types(show=False), row=1, col=1)
    how.add_trace(cs.chat_types(show=False), row=1, col=2)
    how.update_layout(height=475, width=950, showlegend=True, title_text="How are you chatting with them?")
    html += po.plot(how, output_type='div')

    # when are you chatting?
    yearly_graph, monthly_graph, hourly_graph, minutely_graph, daily_graph, weekday_graph = cs.time_stats(show=False)
    when = make_subplots(
        rows=3, cols=2, specs=[[{"type": "bar"}] * 2] * 3,
        subplot_titles=['Yearly', 'Monthly', 'Hourly', 'Minute-by-Minute', 'Single Day', 'Day of Week']
    )
    when.add_trace(yearly_graph, row=1, col=1)
    when.add_trace(monthly_graph, row=1, col=2)
    when.add_trace(hourly_graph, row=2, col=1)
    when.add_trace(minutely_graph, row=2, col=2)
    when.add_trace(daily_graph, row=3, col=1)
    when.add_trace(weekday_graph, row=3, col=2)
    when.update_layout(height=950, width=950, title_text="When are you chatting?", showlegend=False)
    html += po.plot(when, output_type='div')

    # what are you saying?
    lengths = [3,5,7]
    three, five, seven = cs.word_counts(top=20, length=lengths, show=False)
    what = make_subplots(
        rows=len(lengths), cols=1, specs=[[{'type': 'bar'}]] * 3,
        subplot_titles=[f"Top words with {l} or more letters" for l in lengths],
    )
    what.add_trace(three, row=1, col=1)
    what.add_trace(five, row=2, col=1)
    what.add_trace(seven, row=3, col=1)
    what.update_layout(height=1200, width=950, title_text="What are you chatting about?", showlegend=False)
    html += po.plot(what, output_type='div')

    with open("facebook_messenger_usage_report.html", "w+") as report:
        report.write(html)
        print("Report generated successfully!")

