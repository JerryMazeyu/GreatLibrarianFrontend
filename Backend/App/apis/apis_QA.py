# @Author: LiXiang
# @Time: 2023/12/22 14:43
# @version: 1.0
import re
import pandas as pd
from flask import jsonify, request
from flask_restful import Resource
from datetime import datetime
from App.models import *


# 采用正则化，进行log日志内容的读取
def readLog(logURL):
    with open(logURL, 'r', encoding="utf-8") as file:
        content = file.read()
    question = re.compile(r'To LLM:\s+(.*?)(?=\s+from thread 1)').findall(content)
    answer = re.compile(r'To User:\s+"(.*?)"\s+from thread 1').findall(content)
    field = re.compile(r'field:(.*?)(?=\s|$)').findall(content)
    thread = re.compile(r'New Epoch ---------- from thread\s+(\d+)').findall(content)
    return pd.DataFrame({'Q': question, 'A': answer, 'field': field, 'thread': thread})


# df = readLog('../data/log/dialog_init.log')
# # 使用iterrows()遍历行
# for index, row in df.iterrows():
#     print(f"Index: {index}, Q: {row['Q']}, A: {row['A']}, field: {row['field']},thread: {row['thread']}")


# 人工审核
class QAOperation(Resource):
    # 实验完成，进入到人工审核      接收参数【json格式  用户:uid，实验:TPid】
    def post(self):
        uid, TPid = request.json['uid'], request.json['TPid']
        url = 'APP/data/log/dialog_init.log'
        for index, row in readLog(url).iterrows():
            print(f"Index: {index}, Q: {row['Q']}, A: {row['A']}, field: {row['field']},thread: {row['thread']}")
            qa = QA(uid=uid, TPid=TPid, QA_time=datetime.now(),
                    QA_question=row['Q'], QA_answer=row['A'], QA_field=row['field'], QA_thread=row['thread'])
            try:
                db.session.add(qa)  # 加入数据库
                db.session.commit()
            except Exception as e:  # 数据库操作异常处理
                db.session.rollback()  # 回滚
                db.session.flush()  # 刷新，清空缓存
                return jsonify({'success': False, 'message': e})
        return jsonify({'success': True})

    # 查询审核任务  接收参数【url追加  审核人:uid】
    def get(self):
        qaList = QA.query.filter(QA.uid == request.args['uid'])
        data = [{'QAid': qa.QA_id, 'Q': qa.QA_question, 'A': qa.QA_answer} for qa in qaList]
        return jsonify({'data': data, 'success': True})

    # 修改审核人  接收参数【json格式  审核id值:QAid， 目标审核人:uid】
    def put(self):
        qa = QA.query.filter(QA.QA_id == request.json['QAid'])[0]
        qa.uid = request.json['uid']
        try:
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:  # 数据库操作异常处理
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': e})

    # 提交打分结果(一条一条)   接收参数【url追加  审核id值:QAid， 分数:score】
    def delete(self):
        qa = QA.query.filter(QA.QA_id == request.args['QAid'])[0]
        logData = 'To LLM:' + qa.QA_question + 'from thread ' + str(qa.QA_thread) + '\n' + \
                  'To User:"' + qa.QA_answer + '"from thread ' + str(qa.QA_thread) + '\n' + \
                  'The final score of this testcase is ' + request.args['score'] + \
                  ', in ' + qa.QA_field + ' field.from thread ' + str(qa.QA_thread) + '\n'
        with open('APP/data/log/new.log', "a", encoding="utf-8") as file:
            file.write(logData)
        try:
            db.session.delete(qa)
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:  # 数据库操作异常处理
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': e})
