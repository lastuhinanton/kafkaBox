import re
import requests
from bs4 import BeautifulSoup

def parse_kafka_versions():
  url = "https://kafka.apache.org/downloads"
  response = requests.get(url)
  response.raise_for_status()
    
  soup = BeautifulSoup(response.text, 'html.parser')

  versions = dict()
  page_lines = soup.get_text().split('\n')
  number_version = 0
  for line in page_lines:
    if 'Source download:' in line and re.search(r'kafka-[234]\.', line):
      version = line.split('-')[1]
      versions[number_version] =  version
      number_version += 1
  return versions    

def receive_version():
  versions = parse_kafka_versions()
  c = 0
  for k,v in versions.items():
    if c < 2:
      end = '   '
      c += 1
    else:
      end = '\n'
      c = 0
    print(f'{k}. {v}', end=end)
  version = input("\n\nEnter the point of the version ... ")
  return versions[int(version)]

if __name__ == "__main__":
  version = receive_version() 
  print(f"The version is {version}")

