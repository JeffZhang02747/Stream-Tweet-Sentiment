# -*- coding: utf-8 -*-
import csv


# emoji  ->decode to utf-8 code
# utf-8 code ->encode to emoji
#sentiment_score = p(positive) - p(negative)

#read the file Emoji_Sentiment_Data_v1.0.csv and output the list of emoji with sentiment_score meet the threshold
def emoji_filter(least_number, greater_than, score):
    filter_list = []
    with open('Emoji_Sentiment_Data_v1.0.csv') as csvfile:
        dict_read = csv.DictReader(csvfile)
        for row in dict_read:
            total_occurs = int(row["Occurrences"])
            positive_occurs = int(row['Positive'])
            negative_occurs = int(row['Negative'])
            if total_occurs > least_number:
                sentiment_score =  float(positive_occurs - negative_occurs) / total_occurs

                if greater_than:
                    if sentiment_score > score:
                        filter_list.append( row["Emoji"].decode('utf-8') )

                else:
                    if sentiment_score < score:
                        filter_list.append( row["Emoji"].decode('utf-8') )
    return filter_list


emoji_filter(100, True, 0.49)
emoji_filter(100, False, -0.1)