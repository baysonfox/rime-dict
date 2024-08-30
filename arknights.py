import requests
from pypinyin import lazy_pinyin
from datetime import datetime

def get_all_characters():
    """
    Get a list of all characters in the game.
    """
    url = "https://prts.wiki/api.php"
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": "Category:干员",
        "cmlimit": "max",
        "format": "json"
    }
    
    characters = []
    # Get the list of characters from the wiki
    response = requests.get(url, params=params).json()
    members = response.get('query', {}).get('categorymembers', [])
    # Add the characters to the list
    characters.extend([member['title'] for member in members])
    
    # 过滤所有带()的干员（目前都为特殊模式下独占/阿米娅升变）
    characters = [character for character in characters if '(' not in character]

    return characters

def return_pinyin(word: str) -> str:
    return " ".join(lazy_pinyin(word))

def create_dict(character: str) -> dict:
    ...

dict_file = 'arknights.dict.yaml'
weight = 10000
character_dict = {}

all_characters = get_all_characters()

for character in all_characters:
    character_dict[character] = return_pinyin(character)

with open(dict_file, 'w', encoding='utf-8') as dict_zh:

    # Header metadta
    dict_zh.write(
"""name: arknights
version: {}
sort: by_weight
...
""".format(datetime.now().strftime('%Y-%m-%d')))

    for character, pinyin in character_dict.items():
        dict_zh.write(f"{character}\t{pinyin}\t{weight}\n")



