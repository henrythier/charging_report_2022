import requests
from config import config
from bs4 import BeautifulSoup
import pandas as pd

url = config["tesla_dc_id_url"]
fp = config["tesla_dc_id_fp"]

r = requests.get(url)

if r.status_code != 200:
    raise Exception(f'Request returned an error: {r.status_code} {r.text}')

html_doc = r.text

soup = BeautifulSoup(html_doc, 'html.parser')
links = [a['href'] for a in soup.find_all('a', href=True)]

ids = [link.split('/')[-1] for link in links if 'charger' in link]

df = pd.DataFrame(columns=['id'], data=ids)
df.to_csv(fp, index=None)
