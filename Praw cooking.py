import praw #PRAW provides Reddit API functionality
import datetime #Provides capability to easily formate timestamps of message postings

#Reddit API Credentials

reddit = praw.Reddit(user_agent='TeamD2',
                     client_id='1V6eUZDOl0zTLZMA6TEmtQ', client_secret="QBSPXzL21UQhdEiqfWEeH949WCOwJw",
                     username='TeamD2Ikya', password='CIS591MSISM')                
	           

#Change this variable to indicate what subreddit you want to collect
#Find the subreddit manually on Reddit
#Then change the subreddit name here to be exactly the same
#No white spaces! A multi-word subreddit will have underscores, e.g., "three_word_subreddit"
subreddit = "Cooking" 

#File gets written to the same directory this Python script is located. The file will be called "output.csv"
f = open('outputCooking1.csv','w', encoding='utf8')	
#In this next line we print out column headers
f.write("MsgID, Timestamp,Author,ThreadID,ThreadTitle,MsgBody,ReplyTo,Permalink\n")

#Begin streaming user-generated comments from the focal subreddit specified in the 'subreddit' variable earlier in this code
count = 1
for comment in reddit.subreddit(subreddit).stream.comments():
	#Refer to the documentation for PRAW to see what API commands are available
	commentID = str(comment.id) #Every Reddit post has an identification number. Here we extract it
	author = str(comment.author).replace(";", "").replace("'","").replace(",","").replace("\"","").replace("\n", " ").replace("\r"," ") #Name of message author
	timestamp = str(datetime.datetime.fromtimestamp(comment.created)) #Timestamp of when message was posted
	replyTo = "" #Whether the collected message was a direct reply to another existing message. 
	if not comment.is_root: #If it is indeed a reply, this column contains the message ID of the parent message. If it is not a reply, a '-' is written to this column
		replyTo = str(comment.parent().id)
	else:
		replyTo = "-"
	threadID = str(comment.submission.id) # The ID of the thread the message was posted in
	threadTitle = str(comment.submission.title).replace(";", "").replace("'","").replace(",","").replace("\"","").replace("\n", " ").replace("\r"," ") #The title of the thread the message was posted in
	msgBody = str(comment.body).replace(";", "").replace("'","").replace(",","").replace("\"","").replace("\n", " ").replace("\r"," ") #The message itself
	permalink = str(comment.permalink).replace(";", "").replace("'","").replace(",","").replace("\"","").replace("\n", " ").replace("\r"," ") #A URL you can follow directly to the message
	
	#Print all collected message data to console
	print("-------------------------------------------------------")
	print("Comment ID: " + str(comment.id))
	print("Comment Author: "+ str(comment.author))
	print("Timestamp: "+str(datetime.datetime.fromtimestamp(comment.created)))
	if not comment.is_root:
		print("Comment is a reply to: " + str(comment.parent().id))
	else:
		print("Comment is a reply to: -")
	print("Comment Thread ID: " + str(comment.submission.id))
	print("Comment Thread Title: " + str(comment.submission.title))
	print("Comment Body: " + str(comment.body))
	print("Comment Permalink: " + str(comment.permalink))
	
	#Write everything to a file (outpost.csv specified earlier)
	f.write("'"+commentID+"','"+timestamp+"','"+author+"','"+threadID+"','"+threadTitle+"','"+msgBody+"','"+replyTo+"','"+permalink+"'\n")
	print("Total messages collected from /r/"+subreddit+": " + str(count))
	count += 1

#Data analysis libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Data Preprocessing and Feature Engineering
from textblob import TextBlob
import re
import nltk
nltk.download('wordnet')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

#Model Selection and Validation
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, classification_report,accuracy_score


#Import data
input_csv = pd.read_csv('outputveganrecipies.csv', encoding='ISO-8859-1')

#Parse csv's to only extract column called 'message'
messages = input_csv['MsgBody']

#Text pre-processing functions
def text_processing(message):
    
    #Generating the list of words in the message (hastags and other punctuations removed) and convert to lowercase
    def form_sentence(message):
        message = message.lower() #Make messages lowercase 
        message_blob = TextBlob(message.lower()) #Convert to 'textblob' which provides a simple API for NLP tasks
        return ' '.join(message_blob.words)
    new_message = form_sentence(message)
    
    #Removing stopwords and words with unusual symbols
    def no_user_alpha(message):
        message_list = [item for item in message.split()] 
        clean_words = [word for word in message_list if re.match(r'[^\W\d]*$', word)] #remove punctuation and strange characters
        clean_sentence = ' '.join(clean_words) 
        clean_mess = [stopword for stopword in clean_sentence.split() if stopword not in stopwords.words('english')] #remove stopwords
        return clean_mess
    no_punc_message = no_user_alpha(new_message)
    
    #Normalizing the words in messages 
    def normalization(message_list):
        lem = WordNetLemmatizer()
        normalized_message = []
        for word in message_list:
            normalized_text = lem.lemmatize(word,'v') #lemmatize words
            normalized_message.append(normalized_text)
        return normalized_message
    
    
    return normalization(no_punc_message)

#Print to console and write to file
f = open('processed_text.csv','w', encoding='utf8')
for message in messages: 
	message = text_processing(message)
	for term in message:
		f.write(term+" ")
	f.write("\n")

	
