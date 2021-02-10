# -*- coding:utf-8 -*-
import os
from elasticsearch import Elasticsearch, TransportError, helpers
from savedata import db_action

# 首先你需要装es并且正确启动服务

es = Elasticsearch(hosts="localhost", port=9200)
es.indices.create(index="music", ignore=400)  # index名必须小写！


def into_esdata():
    # 首先从sqlite3中读取数据

    music_db = db_action.SqliteDatabase(f'{os.path.abspath(os.path.dirname(os.getcwd()))}\\savedata\\music.db')
    music_data = music_db.select_sql("select *from MusicInfo")

    # 现在给es中填充数据
    try:
        helpers.bulk(es, music_data, index="music", doc_type="musicInfo")
    except TransportError as e:
        print(e.info)


if __name__ == '__main__':
    query = {
        "query": {
            "match_all": {}
        }
    }
    music_info = es.search(index="music", doc_type="musicInfo", body=query)
    print(music_info)
