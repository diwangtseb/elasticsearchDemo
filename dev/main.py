# -*- coding:utf-8 -*-
import os

from flask import Flask, jsonify, request
# from elasticsearchdata import add_to_esdata
from flask_cors import CORS
from flask_request_params import bind_request_params

from savedata import db_action

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.before_request(bind_request_params)
cors = CORS(app)  # 跨域

music_db = db_action.SqliteDatabase(f'{os.getcwd()}\\savedata\\music.db')


@app.route('/')
def homepage():
    res = music_db.select_sql("select *from MusicInfo")
    return jsonify(res)


# @app.route('/search_sings')
# def search_sings():
#     # 获取request中的查询参数
#     name = request.values.get('Name')
#     query = {
#         "query": {
#             "match_phrase_prefix": {
#                 "Name": f"{name}"
#             }
#         }
#     }
#
#     music_info = add_to_esdata.es.search(index="music", doc_type="musicInfo", body=query,
#                                          filter_path=["hits.hits._source"])
#     return jsonify(music_info)


@app.route('/user', methods=['POST'])
def create_user():
    user = request.params.require('user').permit('name', 'password')
    return jsonify(user)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
