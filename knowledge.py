import requests
from bs4 import BeautifulSoup

def fetch_knowledge_base(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    paragraphs = []
    about_hrone_content = ""
    h1_tag = soup.find('h1', text='About HROne')
    if h1_tag:
        next_ul = h1_tag.find_next('ul')
        if next_ul:
            p_tag = next_ul.find('p')
            if p_tag:
                about_hrone_content = p_tag.text.strip()
                paragraphs.append(about_hrone_content)
    our_mission_items = [li.text for li in soup.select('h2#our-mission + ul > li')]
    paragraphs.append('.'.join(our_mission_items))
    return paragraphs
