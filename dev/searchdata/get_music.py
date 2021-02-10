# -*- coding:utf-8 -*-
import bs4
import json
import requests
import os
from savedata import db_action


def get_music_163_json(music_dict: dict, header: dict):
    """:param music_dict is urls"""
    processed_music_data = []
    for i in music_dict.keys():
        top_path = requests.get(music_dict[i], headers=header)  # 这个连接为网易云歌单列表
        bs_body = bs4.BeautifulSoup(top_path.text, "lxml")  # 获取bs4对象
        music_data_for_json = bs_body.find("textarea", {"id": "song-list-pre-data"})  # 获取歌曲信息json数据
        processed_music_data.append(json.loads(music_data_for_json.text))  # json转python字典
    return processed_music_data


def insert_music_data_to_db(music_data: list, music_db: object):
    """
        :param music_data is list
        :param music_db is object
    """
    for single_music_data in music_data:
        for single_music_data_sub in single_music_data:
            music_db.exec_sql(f'''
                insert into MusicInfo(name, music_url,sing_name) values 
                ("{single_music_data_sub['artists'][0]['name']}",
                "http://music.163.com/song/media/outer/url?id={single_music_data_sub['id']}.mp3",
                "{single_music_data_sub['album']['name']}")''')


if __name__ == '__main__':
    music_163_dict = {
        "top": "https://music.163.com/discover/toplist?id=19723756",
        "new": "https://music.163.com/discover/toplist?id=3779629",
        "origin": "https://music.163.com/discover/toplist?id=2884035",
        "hot": "https://music.163.com/discover/toplist?id=3778678",
        "blackvip": "https://music.163.com/discover/toplist?id=5453912201",
        "cloud": "https://music.163.com/discover/toplist?id=991319590",
        "classically": "https://music.163.com/discover/toplist?id=71384707",
        "electronic": "https://music.163.com/discover/toplist?id=1978921795",
        "acg": "https://music.163.com/discover/toplist?id=71385702",
        "korea": "https://music.163.com/discover/toplist?id=745956260",
        "nation": "https://music.163.com/discover/toplist?id=10520166",
        "uk": "https://music.163.com/discover/toplist?id=180106",
        "ktv": "https://music.163.com/discover/toplist?id=21845217",
        "itunes": "https://music.163.com/discover/toplist?id=11641012",
        "oumeihot": "https://music.163.com/discover/toplist?id=2809513713",
        "oumeinew": "https://music.163.com/discover/toplist?id=2809577409",
        "gamekaton": "https://music.163.com/discover/toplist?id=3001835560",
        "gameacg": "https://music.163.com/discover/toplist?id=3001795926",
        "acgvocal": "https://music.163.com/discover/toplist?id=3001890046",
        "janp": "https://music.163.com/discover/toplist?id=5059644681",
        "rock": "https://music.163.com/discover/toplist?id=5059633707",
        "gufeng": "https://music.163.com/discover/toplist?id=5059642708",
        "capacity": "https://music.163.com/discover/toplist?id=5338990334",
        "country": "https://music.163.com/discover/toplist?id=5059661515"

    }
    header = {
        "origin": "https://music.163.com",
        "referer": "https://music.163.com",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63",
        "cookie": "nts_mail_user=diwang839639311@163.com:-1:1; _iuqxldmzr_=32; "
                  "_ntes_nnid=e61d35402eccd8900358bd926e1737fc,1612263449181; "
                  "_ntes_nuid=e61d35402eccd8900358bd926e1737fc; NMTID=00OEFS1YSsour9CR0zkk9iuzYcF_WoAAAF3YmPaBA; "
                  "WM_TID=i7N9qHWRqE5BQRRRQQZufyLQsL283Oyw; "
                  "P_INFO=diwang839639311@163.com|1612270695|0|mail163|00&99|CN&1612241772&mail_client#bej&null#10#0"
                  "#0|&0|mail163|diwang839639311@163.com; WEVNSM=1.0.0; WNMCID=nbakcf.1612700293244.01.0; "
                  "WM_NI=6aOPWIWCuzTYVHEuSfXV7zZxbDsSvENvhAZ93gSFPAt3i9POpQVDxPS6b/FGcaW9u5C1IhVyTWqOXQwzdw2K+OhkWl"
                  "/sgjd5fT99wbXOPph6Qb9aZHsShs1+9KfaSV0UU04=; "
                  "WM_NIKE"
                  "=9ca17ae2e6ffcda170e2e6ee85aa3cf796b6b2b73c879e8eb2c44a838b8a85ae41aaeaa5b0e46a98e8f98ed22af0fea7c3b92af6bf81b1d643959dbb9bd75396988b96d26e9c8af99bd974a29cbdb4f54f8eaaa8a2d933f1b99da7d34bb8eda7dad345b48f9aa5fb5c91eaaed0c54da1bf99daf83f81ef8789d5739889bfb0db5bb5a6ac98b141e991a88cd668edada98be73fa68cf7daf66a9c91a091eb3e93bef782d944b18da894b421fb95aa82d25ef48b9bd1b737e2a3; playerid=91230275; JSESSIONID-WYYY=NIatiKy1Bq7hEim5WwOhBi5Mr0rD6r8uhexCPOzszGU//SYW7Rjr3ekmtyjezAhZZjT2saPiy2p++K0f9izZ+Cq9E1JM9qyC2mJBjGsFnEEqvXIH4RkrnjUvXdGf5GSsEXVMpwFdIw23ia8YrZ98M+EJ0KUBqKMm5gJWbUe/satCH8tX:1612716057836 "
    }
    music_db = db_action.SqliteDatabase(f'{os.path.abspath(os.path.dirname(os.getcwd()))}\\savedata\\music.db')

    insert_music_data_to_db(get_music_163_json(music_163_dict, header=header), music_db)
    print("今日网易云歌曲已成功添加到数据库！")
