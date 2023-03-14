import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd

# scraping the data of to 25 repositories of each trending topics
github_topics_url = 'https://github.com/topics'
r = requests.get(url = github_topics_url)
# print(len(r.text)) 
page_content = r.text

# # print(page_content[:1000])
# with open('webpage.html', 'w') as f:
#     f.write(page_content[:10000])

soup1 = BeautifulSoup(page_content, 'html.parser')
soup= BeautifulSoup(soup1.prettify(), 'html.parser')

# scraping topic title tags 
title_class ="f3 lh-condensed mb-0 mt-1 Link--primary"
topic_title_tags = soup.find_all('p',{'class' :title_class})
topic_title = []
for tag in topic_title_tags:
    topic_title.append(tag.text.strip( ))
# print(topic_title)


# scraping topic description
descp_class = "f5 color-fg-muted mb-0 mt-1"
topic_descp_tags= soup.find_all('p', {'class': descp_class})
topic_descp = []
for descp in topic_descp_tags:
    topic_descp.append(descp.text.strip( ))
# print(topic_descp)


# scraping topic links
link_class = "no-underline flex-grow-0"
topic_links_tags= soup.find_all('a', {'class': link_class})
topic_links = []
base_link = "http://github.com"
for link in topic_links_tags:
    topic_links.append(base_link+ link['href'].strip())
# print(topic_links)

# creating a dataframe to store it as a .csv file
topics_dict = {'Title':topic_title, 'Description': topic_descp, 'Url': topic_links}
scraped_topics_df = pd.DataFrame(topics_dict)
# print(scraped_df)
scraped_topics_df.to_csv("Topics.csv",index=None)


# Scraping the next page
for j in range(len(topic_title_tags)):
    topic_url= topic_links[j]
    r1 = requests.get(url = topic_url)
    topic_htmlcontent = r1.content
    topic_soup = BeautifulSoup(topic_htmlcontent,'html.parser')

    repo_tags = topic_soup.find_all('h3' , {'class' : "f3 color-fg-muted text-normal lh-condensed"})

    # scraping different details of this page
    # like username, urls, stars etc.

    def repo__details(i):
        repo_name_tag = repo_tags[i]
        repo_atag = repo_name_tag.find_all('a')

        username = repo_atag[0].get_text().strip()
        repo_name = repo_atag[1].get_text().strip()
        repo_url = base_link + repo_atag[1]['href']

        star_tags = topic_soup.find_all('span',{'id': 'repo-stars-counter-star'})
        repo_stars = star_tags[i].text

        def star_number(stars):
            if "k" in stars:
                return int(float(stars[:-1])*1000)
            else:
                return stars


        repo_stars_num = star_number(repo_stars)
        return username, repo_name, repo_url, repo_stars_num


    username_list=[]
    reponame_list=[]
    repourl_list=[]
    repostars_list=[]
    for i in range(len(repo_tags)):
        
        username_list.append(repo__details(i)[0])
        reponame_list.append(repo__details(i)[1])
        repourl_list.append(repo__details(i)[2])
        repostars_list.append(repo__details(i)[3])

    repo_details_dict = {'User Name': username_list, 
                        'Repository Name': reponame_list,
                        'Repository Url' : repourl_list,
                        'Stars' : repostars_list}

    Repo_df = pd.DataFrame(repo_details_dict)

    # creating .csv file
    Repo_df.to_csv(f'{topic_title[j]}.csv',index = None) 
