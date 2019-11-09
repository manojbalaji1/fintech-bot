'''
Dated: Nov05-2018
Auhor: Mahesh Babu Mariappan (https://www.linkedin.com/in/mahesh-babu-mariappan)
Source code for AI Chatbot

References:
https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DatetimeIndex.html#pandas.DatetimeIndex
http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases

Attributes of DatetimeIndex

year	The year of the datetime
month	The month as January=1, December=12
day	The days of the datetime
hour	The hours of the datetime
minute	The minutes of the datetime
second	The seconds of the datetime
microsecond	The microseconds of the datetime
nanosecond	The nanoseconds of the datetime
date	Returns numpy array of python datetime.date objects (namely, the date part of Timestamps without timezone information).
time	Returns numpy array of datetime.time.
dayofyear	The ordinal day of the year
weekofyear	The week ordinal of the year
week	The week ordinal of the year
dayofweek	The day of the week with Monday=0, Sunday=6
weekday	The day of the week with Monday=0, Sunday=6
quarter	The quarter of the date
freq	Return the frequency object if it is set, otherwise None
freqstr	Return the frequency object as a string if it is set, otherwise None
is_month_start	Logical indicating if first day of month (defined by frequency)
is_month_end	Indicator for whether the date is the last day of the month.
is_quarter_start	Indicator for whether the date is the first day of a quarter.
is_quarter_end	Indicator for whether the date is the last day of a quarter.
is_year_start	Indicate whether the date is the first day of a year.
is_year_end	Indicate whether the date is the last day of the year.
is_leap_year	Boolean indicator if the date belongs to a leap year.
inferred_freq	Tries to return a string representing a frequency guess, generated by infer_freq.

Test results:
average balance 2 days --> What was my balance at the start of the month ? (WITHOUT scorer=fuzz.token_sort_ratio)
average balance 2 days --> What is my average account balance over the past 2 days ? (WITH scorer=fuzz.token_sort_ratio)

average last month
[('What was my balance last Monday ?', 53), ('Which category has the highest spend last month ?', 52), ('What is my average account balance over the last month ?', 50)]	### FIXED WITH scorer=fuzz.token_set_ratio

balance end of month
[('What is my average account balance at the end of the month ?', 100), ('What was my balance at the end of last month ?', 100), ('What was my balance at the beginning of the month ?', 89)]



'''

# import matplotlib
# from matplotlib import pyplot as plt
import numpy as np  # linear algebra
from fuzzywuzzy import fuzz, process
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import os


class Bot(object):
    def __init__(self):
        self.df = pd.read_csv("aug01-2018-sept30-2018-banking-chatbot-dataset.csv", sep=',')
        print("Checking for nulls:\n", self.df.isnull().sum())
        print('\nStandardizing column names')
        self.df.columns = [c.lower().replace(' ', '_') for c in self.df.columns]
        self.df['date'] = pd.to_datetime(self.df['date'], format='%d/%m/%y')
        return

    def answer_user_question(self, user_question):  # returns question
        '''retrieve user entered questions through interactive console and sends them to '''
        question_dict = {"What is my current account balance ?": 1,
                         "What was my balance at the ( start / beginning ) of this month ?": 2,
                         "What was my balance five ( 5 ) days back ( ago ) ?": 3,
                         "What was my balance at the ( start / beginning ) of this week ?": 4,
                         "What was my balance at the end of ( past / last ) week ?": 401,
                         "What was my balance last wednesday ?": 5,
                         "What is my average account balance over the ( last / past ) one ( 1 ) week ?": 6,
                         "What is my average account balance over the ( last / past ) two ( 2 ) days ?": 7,
                         "What is my average account balance at the end of the month ?": 801,
                         "What was my balance at the ( start / beginning ) of ( last / past ) month ?": 9,
                         "Which category has the highest spend this month ?": 10,
                         "Which category has the lowest spend this month ?": 36,
                         "Which category has the lowest spend last month ?": 37,
                         "Which category has the highest spend last month ?": 38,
                         "What was my balance at the end of ( last / past ) month ?": 12,
                         "What was my balance yesterday ?": 14,
                         "What was my balance two ( 2 ) days back ( ago ) ?": 15,
                         "What was my balance three ( 3 ) days back ( ago ) ?": 16,
                         "What was my balance four ( 4 ) days back ( ago ) ?": 17,
                         "What was my balance six ( 6 ) days back ( ago ) ?": 19,
                         "What was my balance at the beginning of the week ?": 20,
                         "What was my balance ( last / past ) Monday ?": 22,
                         "What was my balance ( last / past ) Thursday ?": 23,
                         "What was my balance ( last / past ) Friday ?": 24,
                         "What was my balance ( last / past ) Saturday ?": 25,
                         "What was my balance ( last / past ) Sunday ?": 26,
                         "What is my average account balance over the ( last / past ) two ( 2 ) weeks ?": 27,
                         "What is my average account balance over the ( last / past ) three ( 3 ) weeks ?": 28,
                         "What is my average account balance over the ( last / past ) four ( 4 ) weeks ?": 29,
                         "What is my average account balance over the ( last / past ) three ( 3 ) days ?": 30,
                         "What is my average account balance over the ( last / past ) four ( 4 ) days ?": 31,
                         "What is my average account balance over the ( last / past ) five ( 5 ) days ?": 32,
                         "What is my average account balance over the ( last / past ) six ( 6 ) days ?": 33,
                         "What is my average account balance over the ( last / past ) seven ( 7 ) days ?": 34,
                         "What is my average account balance over the ( last / past ) month ?": 35,

                         "What was my total ( expense / expenses / debit / debits / spend / expenditure / outflow / outflows / outgoing ) this week ?": 46,
                         "What was my total ( expense / expenses / debit / debits / spend / expenditure / outflow / outflows / outgoing ) this month ?": 47,
                         "What was my total ( expense / expenses / debit / debits / spend / expenditure / outflow / outflows / outgoing ) last week ?": 48,
                         "What was my total ( expense / expenses / debit / debits / spend / expenditure / outflow / outflows / outgoing ) last month ?": 49,
                         "how much ( expense / did I spend ) this week ?": 46,
                         "how much ( expense / did I spend ) this month ?": 47,
                         "how much ( expense / did I spend ) last week ?": 48,
                         "how much ( expense / did I spend ) last month ?": 49,
                         "What was my total ( earning / earnings / credit / credits / inbound / inbounds / inflow / inflows ) this week ?": 50,
                         "What was my total ( earning / earnings / credit / credits / inbound / inbounds / inflow / inflows ) this month ?": 51,
                         "What was my total ( earning / earnings / credit / credits / inbound / inbounds / inflow / inflows ) last week ?": 52,
                         "What was my total ( earning / earnings / credit / credits / inbound / inbounds / inflow / inflows ) last month ?": 53,
                         "how much did I ( earn / earning / earnings / credit / credits / inbound / inbounds / inflow / inflows ) this week ?": 50,
                         "how much did I ( earn / earnings / credit / credits / inbound / inbounds / inflow / inflows ) this month ?": 51,
                         "how much did I ( earn / earnings / credit / credits / inbound / inbounds / inflow / inflows ) last week ?": 52,
                         "how much did I ( earn / earnings / credit / credits / inbound / inbounds / inflow / inflows ) last month ?": 53,
                         "Which category has the highest spend this week ?": 58,
                         "Which category has the highest spend last week ?": 59,
                         "Show me all expense categories": 60,
                         "how much did I spend on shopping this week ?": 61,
                         "how much did I spend on shopping this month ?": 62,
                         "how much did I spend on shopping last week ?": 63,
                         "how much did I spend on shopping last month ?": 64,
                         "how much did I spend on restaurant this week ?": 65,
                         "how much did I spend on restaurant this month ?": 66,
                         "how much did I spend on restaurant last week ?": 67,
                         "how much did I spend on restaurant last month ?": 68,
                         "how much did I spend on fuel this week ?": 69,
                         "how much did I spend on fuel this month ?": 70,
                         "how much did I spend on fuel last week ?": 71,
                         "how much did I spend on fuel last month ?": 72,
                         "how much did I spend on entertainment this week ?": 73,
                         "how much did I spend on entertainment this month ?": 74,
                         "how much did I spend on entertainment last week ?": 75,
                         "how much did I spend on entertainment last month ?": 76,
                         "how much did I spend on medical this week ?": 77,
                         "how much did I spend on medical this month ?": 78,
                         "how much did I spend on medical last week ?": 79,
                         "how much did I spend on medical last month ?": 80,
                         "how much did I withdraw from ATM this week ?": 81,
                         "how much did I withdraw from ATM this month ?": 82,
                         "how much did I withdraw from ATM last week ?": 83,
                         "how much did I withdraw from ATM last month ?": 84,
                         "how much did I spend on travel this week ?": 85,
                         "how much did I spend on travel this month ?": 86,
                         "how much did I spend on travel last week ?": 87,
                         "how much did I spend on travel last month ?": 88,
                         "shopping expenses this week ?": 61,
                         "shopping expenses this month ?": 62,
                         "shopping expenses last week ?": 63,
                         "shopping expenses last month ?": 64,
                         "restaurant expenses this week ?": 65,
                         "restaurant expenses this month ?": 66,
                         "restaurant expenses last week ?": 67,
                         "restaurant expenses last month ?": 68,
                         "fuel expenses this week ?": 69,
                         "fuel expenses this month ?": 70,
                         "fuel expenses last week ?": 71,
                         "fuel expenses last month ?": 72,
                         "entertainment expenses this week ?": 73,
                         "entertainment expenses this month ?": 74,
                         "entertainment expenses last week ?": 75,
                         "entertainment expenses last month ?": 76,
                         "medical expenses this week ?": 77,
                         "medical expenses this month ?": 78,
                         "medical expenses last week ?": 79,
                         "medical expenses last month ?": 80,
                         "Withdrawals from ATM this week ?": 81,
                         "Withdrawals from ATM this month ?": 82,
                         "Withdrawals from ATM last week ?": 83,
                         "Withdrawals from ATM last month ?": 84,
                         "travel expenses this week ?": 85,
                         "travel expenses this month ?": 86,
                         "travel expenses last week ?": 87,
                         "travel expenses last month ?": 88

                         }

        fuzz_result_3tuple_list = process.extract(user_question, list(question_dict.keys()),
                                                  scorer=fuzz.token_set_ratio, limit=1)
        fuzz_matched_q1 = fuzz_result_3tuple_list[0][0]
        fuzz_matched_q1_confidence = fuzz_result_3tuple_list[0][1]

        if fuzz_matched_q1_confidence < 60:
            print("\n\nNo luck. Please re-phrase your question or try another question")
            return "Sorry, I did not understand!"
        else:
            # invoke pandas_dataframe_IR() once
            answer_q1 = self.pandas_dataframe_IR(question_dict[fuzz_matched_q1], self.df)
            return answer_q1

    def pandas_dataframe_IR(self, question_index, df):  # queries df and returns answer
        '''runs pandas statements on dataframe for the question asked, and returns the answer'''
        if question_index == 1:  # "What is my current account balance ?"
            # start time 1:37pm
            # end time: 1:57pm
            # elapsed time: 20 mins

            # Strategy: in order to extract the current account balance, fetch the last 'closing_balance' cell value
            answer = df['closing_balance'].iloc[-1]
            return answer
        elif question_index == 2:  # "What was my balance at the ( start / beginning ) of this month ?"
            # start time 1:59pm
            # end time: 4:09pm
            # elapsed time: 2h 10m

            # Expected answer: 279065.59
            # Strategy: 1) find first date of current month 2) retrieve 'closing_balance' using this date
            '''current_month = df['Date'][-1] # get last 'Date' value
            print(type(current_month))'''
            # print(df.tail(), df.info())
            # print(type(df.index))
            # print(df.index)
            '''current_date = df.index[-1]
            print(current_date.month)'''
            # print(df['Date'])
            # print(df.tail(), df.info())

            end_dates_of_months = []
            for date in df['date']:
                # print(date)
                if date.is_month_end == True:
                    # print("Found an end date")
                    end_dates_of_months.append(date)
            # print(date.is_month_end)
            # print (end_dates_of_months)
            # print(end_dates_of_months[-1])
            # print("df.loc[df['date'] == end_dates_of_months[-1]].closing_balance.iloc[-1]", df.loc[df['date'] == end_dates_of_months[-1]].closing_balance.iloc[-1])

            answer = (df.loc[df['date'] == end_dates_of_months[-1]].closing_balance.iloc[-1])
            return answer
        elif question_index == 3:
            # "What was my balance five (5) days back ?"
            # start time 05:11pm
            # end time: pm
            # elapsed time:

            # Strategy: .to_perioddelta(freq) # date_five_days_back = current_date - 5
            # print(type(df['date']), df['date'])
            current_date = df['date'].unique()[-1]

            date_five_days_back = df['date'].unique()[-6]
            # print('current_date: ', current_date, "date_five_days_back: ", date_five_days_back)

            answer = (df.loc[df['date'] == date_five_days_back].closing_balance.iloc[-1])
            return answer

        elif question_index == 4:
            # print ("\n\nResponse: \n\nI will execute pandas statement 4")
            answer = 4999
            return answer
        elif question_index == 5:
            # print ("\n\nResponse: \n\nI will execute pandas statement 5")
            answer = 5999
            return answer
        elif question_index == 6:
            # print ("\n\nResponse: \n\nI will execute pandas statement 6")
            answer = 6999
            return answer
        elif question_index == 7:
            # print ("\n\nResponse: \n\nI will execute pandas statement 7")
            answer = 7999
            return answer
        elif question_index == 8:
            # print ("\n\nResponse: \n\nI will execute pandas statement 8")
            answer = 8999
            return answer
        elif question_index == 9:
            # "What was my balance at the ( start / beginning ) of ( last / past ) month ?"
            print("I understand your question. I am waiting for the developer to add this code block")
            return
        elif question_index == 10:
            # print ("\n\nResponse: \n\nI will execute pandas statement 10")
            answer = 10999
            return answer
        else:
            # print ("\n\nImplementation on the way\n")
            answer = -1.00010001
            return answer


