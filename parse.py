import requests
from bs4 import BeautifulSoup

res = []


def get_val(tag):
    return tag.string.split('<')[0].split('>')[-1].strip()


for i in range(1, 9):
    vgm_url = f'http://theworkoutdictionary.com/moves/?page={i}'
    html_text = requests.get(vgm_url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    divs = soup.find_all('div', {'class': 'mdl-card__supporting-text'})
    for div in divs:
        res.append({'link': div.findChildren('a')[0]['href'],
                    'name': get_val(div.findChildren('a')[0]),
                    'img': div.previous_sibling()[0]['src']})

for d in res:
    resp = requests.post('https://workouts-dfj7zf72dq-uc.a.run.app/exercises', json={'name': d['name']})
    print(resp.json())
print(res)
