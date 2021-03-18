################################################################################
##                                                                            ##
##                                                                            ##
##                                                                            ##
## THIS IS A WEB SCRAPER THAT TAKES THE FIRST N PAGES OF JOB APPLICATIONS FOR ##
## ANY KEYWORDS. FOR EXAMPLE: #PYTHON DEVELOPER#.                             ##
## IT THEN TAKES THOSE KEYWORDS AND FINDS THE CORRESPONDING LINKS TO THOSE    ##
## JOB APPLICATIONS ON REED.CO.UK.                                            ##
## USING BEAUTIFUL SOUP, THE SCRIPT FINDS ALL THE TEXT ASSOCIATED WITH THE    ##
## JOB DESCRIPTION ON EACH PAGE. THEN, USING A MAN-MADE FILTER, A WORDCLOUD   ##
## CAN BE GENERATED TO FIND OUT WHAT THE MOST COMMON WORDS ARE, THUS GIVING   ##
## THE USER SOME INSIGHT INTO JOB REQUIREMENTS. FUTURE ITERATIONS COULD       ##
## EASILY INCLUDE THE USE OF A MORE SPECIFIC FILTER, USING ONLY WORDS FOUND   ##
## K WORDS AFTER THE WORD 'EXEPRIENCE' OR 'REQUIREMENTS' ETC. HOWEVER, DUE TO ##
## OTHER PROJECTS THAT HAS NOT YET BEEN IMPLEMENETED.                         ## 
##                                                                            ##
##                                                                            ##
##  WILL MANGION  - WMANGION@GMAIL.COM                                        ##
##                                                                            ##
##                                                                            ##
################################################################################

#!pip install requests
#!pip3 install beautifulsoup4
#!pip install wordcloud
#Get the key words for the users' input.

#search_keywords = str(input('Enter the search keywords: '))
search_keywords = 'Python Developer'
print('Your search keywords are: ' + search_keywords)

#Number of pages of results you want to scoop up - recommend manually checking
#how many pages show relevant results 
num_page = 19


#To fit the reed.co.uk search link format, you must hyphenate these words
def search_keyword_processing(search_keywords):
  #Split the string up in to individual words.
  search_keywords = search_keywords.lower()
  search_keywords_list = search_keywords.split()
  


  #Hyphenate these words
  for i in range(len(search_keywords_list)):
    search_keywords_list[i]= search_keywords_list[i] + '-'
    

  #URL string then becomes all hyphenated words added together
  URL_STRING_PRECURSOR = ''
  for i in range(len(search_keywords_list)):
    URL_STRING_PRECURSOR += search_keywords_list[i]
    
  return URL_STRING_PRECURSOR



URL_STRING_PRECURSOR = search_keyword_processing(search_keywords)

URL = 'https://www.reed.co.uk/jobs/'+URL_STRING_PRECURSOR+'jobs'
print(URL)


import requests
from bs4 import BeautifulSoup


def GetJobLinks(URL_STRING_PRECURSOR,num_page):
  #We must slight edit the format to get all pages, as only some listed per page

  #Create list that will store our URLS for all the job adverts
  job_links = []

  #Add pagenumber to end of link
  for page_number in range(1,num_page):
    #initialise temp link to store job links from a certain page
    temp_links = []

    #GET URL AND PARSE using BS4
    URL = 'https://www.reed.co.uk/jobs/'+URL_STRING_PRECURSOR+'jobs?pageno='+str(
        page_number)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    #Find all the URL links in the html page, most not relevant
    for link in soup.find_all('a'):
      temp_links.append(link.get('href')) 
  
    #Remove duplicates
    temp_links = set(temp_links)
    temp_links = list(temp_links)


    #Remove None type objects in the list of all links
    temp_NULL = []
    for a in range(len(temp_links)):
      if temp_links[a] != None:
        temp_NULL.append(temp_links[a])
    temp_links = temp_NULL

    del temp_NULL
    #Seperate useful job advert links from other links.
    temp = []
    qualifier = 'source=searchResults'
    for j in range(len( temp_links)):
      if qualifier in temp_links[j]:
        temp.append(temp_links[j])
    temp_links = temp
    del temp

    #Append temp_links to job_links
    
    job_links.append(temp_links)

    #Flatten nested list
    flat_job_link_list = [item for sublist in job_links for item in sublist]

  return flat_job_link_list

job_links = GetJobLinks(URL_STRING_PRECURSOR,num_page)

import urllib
import string 



#Function to format all the text from the Beautiful Soup Parser
def GetText(table):
  text = table.get_text()
  text = text.lower()
  text = text.translate(str.maketrans('','', string.punctuation))
  text_list = list(text.split())
  return text_list



#Function to get all the text using the Beautiful Soup Library 

def BS4(num_page):
  #Initialise list of experiences
  experiences = []



  for j_link in range(num_page):
    URL_JOB = 'http://www.reed.co.uk'+ job_links[j_link]
    url = urllib.request.urlopen(URL_JOB)
    content = url.read()
    soup = BeautifulSoup(content, 'html')
    table = soup.find("span", itemprop="description")
    #The above opens job specific links and gets all the text in the description
    #box

    #Use GetText to format the text
    text_list = GetText(table)
    #append to experiences list
    experiences.append(text_list)
  return experiences

experiences = BS4(num_page)


remove_list = ['senior', 'digital','remote','and','if','for','developer','looking'
,'role','uk','look','the','join','salary','competitive','working','work'
,'within','global','years','based','will','company','growth','structure',
'overview','flexibility','interested','apply','email','me','am','experience','/'
,'you','are','a','in','then','no','further','i','on','they','skilled','way',
'with','have','flat','it','is','an','time','search','development',
'role','opportunity','will','within','leading','succesful','of','up','to',
'salaries','what','lockdown', 'recruiting','their','so','office','platform',
'team','software','london','project','office','exciting','python','be','as'
,'this','that','or','your','new','technology']

#Remove the above list of words from the experiences list
flat_text_list = [item for sublist in experiences for item in sublist]
for y in remove_list:
  for x in flat_text_list:
    if x == y:
      flat_text_list.remove(x) 

#Generate word cloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt

unique_string=(" ").join(flat_text_list)


wordcloud = WordCloud().generate(unique_string)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

from collections import Counter 
Counter = Counter(flat_text_list)
most_occur = Counter.most_common(10) 
  
print(most_occur) 
