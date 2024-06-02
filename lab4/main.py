from bs4 import BeautifulSoup
import pandas as pd
from seleniumbase import Driver
import time

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0','accept': '*/*'}
driver = Driver(uc=True)

def Get_soup(url,driver):
    driver.get(url.replace(' ', ''))
    time.sleep(5)
    source_data = driver.page_source
    soup = BeautifulSoup(source_data, features="html.parser")
    return soup

def Parse_data(soup):
    news_blocks = soup.find_all('li', class_='col-xs-12 col-sm-12 col-md-12 col-lg-12 fui-grid__inner')
    result = []
    for block in news_blocks:
        title_tag = block.find('h4', class_='media-block__title')
        perex_tag = block.find('p', class_='perex perex--mb perex--size-3')
        date_tag = block.find('span', class_='date date--mb date--size-3')
        link_tag = block.find('a', href=True)

        title = title_tag.get_text(strip=True) if title_tag else None
        perex = perex_tag.get_text(strip=True) if perex_tag else None
        date = date_tag.get_text(strip=True) if date_tag else None
        link = link_tag['href'] if link_tag else None
        result.append({
            'title': title,
            'perex': perex,
            'date': date,
            'link': 'https://www.radiosvoboda.org'+link
            })

    return pd.DataFrame(result)


def Get_data(year,month):
    result_df = pd.DataFrame()
    for day in range (1,31):
        try:
            print('Parse date: '+year+'.'+month+'.'+str(day))
            soup = Get_soup(f"https://www.radiosvoboda.org/z/630/{year}/{month}/{day}", driver)
            result_df = pd.concat([result_df, Parse_data(soup)], ignore_index=True)
        except Exception as e:
            print(f"Error occurred for {month}/{day}: {e}")
    return result_df

result=Get_data('2024','5')
result.to_csv('news_df.csv', index=False,encoding='utf-8')