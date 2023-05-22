from selenium import webdriver as wd
from webdriver_manager.chrome import ChromeDriverManager as cdm
from bs4 import BeautifulSoup as bs
import requests as r
import csv

researchTitle = []
hRef = []
authors = []
publishDate = []
abstract = []
assignedKeyword = []

keywords = []
urls = []

keywordsFile = open('Keywords.csv')
reader = csv.reader(keywordsFile, delimiter=',')
for row in reader:
    keywords.append(row[0])
    urls.append(row[1])
keywords.pop(0)
urls.pop(0)
keywordsFile.close()

keywordCount = 0

for url in urls:
    
    print(keywords[keywordCount])

    urlLink = url
    browser = wd.Chrome(executable_path=cdm().install())
    browser.get(urlLink)
    researchList = bs(browser.page_source, 'html.parser')   
    browser.close()

    listOfResults = researchList.find('ul', class_='list-results')
    resultsInContainer = listOfResults.find_all('div', class_='result-container')    
    nextPages = researchList.find('nav', class_='pages')
    
    for result in resultsInContainer:
    
        date = result.find('span', class_='date')
        date = str(date.text.strip())
        publishDate.append(date)
    
        title = result.find('h3', class_='title')
        strTitle = str(title.text.strip())
        researchTitle.append(strTitle)
    
        hRefLink = title.find('a')
        hRefLink = hRefLink['href']
        hRefLink = str(hRefLink)
        hRef.append(hRefLink)
    
        researchPage = r.get(hRefLink)
        researchResult = bs(researchPage.content, 'html.parser')
    
        relatedPersons = researchResult.find('p', class_='relations persons')
        relatedPersons = str(relatedPersons.text.strip())
        authors.append(relatedPersons)
    
        researchAbstract = str(researchResult.find('div', class_='textblock'))
        researchAbstract = researchAbstract[23:-6]
        researchAbstract = researchAbstract.replace('<br/>', ' ')
        researchAbstract = researchAbstract.replace('</p>', '')
        researchAbstract = researchAbstract.replace('<p>', '')
        researchAbstract = str(researchAbstract.strip())
        researchAbstract = researchAbstract.encode('utf-8')
        researchAbstract = repr(researchAbstract)[2:-1]
        abstract.append(researchAbstract)
        
        assignedKeyword.append(keywords[keywordCount])

    pagesText = []
    if nextPages is None:
        numPages = 0
    else:
        pages = nextPages.find_all('a')
        for page in pages:
            pagesText.append(page.text)
        numPages = pagesText[-2]
    numPages = int(numPages)
    pageCount = numPages - 1        
        
    if numPages > 0:
        for count in range(pageCount):
            
            print(count + 1)
            
            pageOn = count + 1
            urlLink = url + '&format=&page=' + str(pageOn) 
            browser = wd.Chrome(executable_path=cdm().install())
            browser.get(urlLink)
            researchList = bs(browser.page_source, 'html.parser')   
            browser.close()

            listOfResults = researchList.find('ul', class_='list-results')
            resultsInContainer = listOfResults.find_all('div', class_='result-container')            
            
            for result in resultsInContainer:

                date = result.find('span', class_='date')
                date = str(date.text.strip())
                publishDate.append(date)

                title = result.find('h3', class_='title')
                strTitle = str(title.text.strip())
                researchTitle.append(strTitle)

                hRefLink = title.find('a')
                hRefLink = hRefLink['href']
                hRefLink = str(hRefLink)
                hRef.append(hRefLink)

                researchPage = r.get(hRefLink)
                researchResult = bs(researchPage.content, 'html.parser')
                
                relatedPersons = researchResult.find('p', class_='relations persons')
                relatedPersons = str(relatedPersons.text.strip())
                authors.append(relatedPersons)
                
                researchAbstract = str(researchResult.find('div', class_='textblock'))
                researchAbstract = researchAbstract[23:-6]
                researchAbstract = researchAbstract.replace('<br/>', ' ')
                researchAbstract = researchAbstract.replace('</p>', '')
                researchAbstract = researchAbstract.replace('<p>', '')
                researchAbstract = str(researchAbstract.strip())
                researchAbstract = researchAbstract.encode('utf-8')
                researchAbstract = repr(researchAbstract)[2:-1]
                abstract.append(researchAbstract)

                assignedKeyword.append(keywords[keywordCount])
                
        keywordCount = keywordCount + 1
                
    else:
        keywordCount = keywordCount + 1

with open('Strathclyde_Research.csv', 'w', encoding='utf-8', newline='') as researchFile:
    writer = csv.writer(researchFile)
    
    writer.writerow(['Title', 'Href', 'Author', 'Date', 'Abstract', 'Keyword', 'University'])   
    for indexNum in range(len(authors)):      
        writer.writerow([researchTitle[indexNum], hRef[indexNum], authors[indexNum], publishDate[indexNum], abstract[indexNum], assignedKeyword[indexNum], 'Strathclyde'])
        
researchFile.close()
