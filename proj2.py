#proj2.py
from bs4 import BeautifulSoup
import requests

#### Problem 1 ####
print('\n*********** PROBLEM 1 ***********')
print('New York Times -- First 10 Story Headings\n')

### Your Problem 1 solution goes here

base_url = 'http://www.nytimes.com'
r = requests.get(base_url)
soup = BeautifulSoup(r.text, "html.parser")

count = 0
for story_heading in soup.find_all(class_="story-heading"):
    if story_heading.a:
        print(story_heading.a.text.replace("\n", " ").strip())
    else:
        print(story_heading.contents[0].strip())

    count +=1
    if count >= 10:
        break


#### Problem 2 ####
print('\n*********** PROBLEM 2 ***********')
print('Michigan Daily -- MOST READ\n')

### Your Problem 2 solution goes here

base_url = 'https://www.michigandaily.com/'
r = requests.get(base_url)
soup = BeautifulSoup(r.text, "html.parser")

divSoup= soup.find_all("div", {"class": "panel-pane pane-mostread"})

for tag in divSoup:
    headlines = tag.find_all("a")
    for headline in headlines:
        print(headline.text)


#### Problem 3 ####
print('\n*********** PROBLEM 3 ***********')
print("Mark's page -- Alt tags\n")

### Your Problem 3 solution goes here

base_url = 'http://newmantaylor.com/gallery.html'
r = requests.get(base_url)
soup = BeautifulSoup(r.text, "html.parser")

for image in soup.find_all("img"):
    if image.get('alt', '') == "":
        print("No alternative text provided!!")
    else:
        print(image.get('alt', ''))


#### Problem 4 ####
print('\n*********** PROBLEM 4 ***********')
print("UMSI faculty directory emails\n")

### Your Problem 4 solution goes here

base_url = 'https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=4'
stem_url = 'https://www.si.umich.edu'
r = requests.get(base_url)
soup = BeautifulSoup(r.text, "html.parser")
allEmails = []
allContactLinks = []
count = 1

def ContactDetailsLinks(allContactLinks):
    divSoup = soup.find_all("div", {"class": "field field-name-contact-details field-type-ds field-label-hidden"})

    for tag in divSoup:
        contactLinks = tag.find_all("a")
        for link in contactLinks:
            allContactLinks.append(stem_url + link['href'])

    return allContactLinks

ContactDetailsLinks(allContactLinks)

while True:
    nextPage = soup.find_all(title="Go to next page")
    if nextPage == []:
        break
    else:
        r = requests.get(stem_url + nextPage[0]['href'])
        soup = BeautifulSoup(r.text, "html.parser")
        ContactDetailsLinks(allContactLinks)

for link in allContactLinks:
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "html.parser")

    divSoup= soup.find_all("div", {"class": "field field-name-field-person-email field-type-email field-label-inline clearfix"})

    for tag in divSoup:
        emails = tag.find_all("a")
        for email in emails:
            allEmails.append(email.text)

for email in allEmails:
    print(str(count) + " " + email)
    count += 1