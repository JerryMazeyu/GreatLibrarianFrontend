# @Author: LiXiang
# @Time: 2023/11/15 20:22
# @version: 1.0
from flask import jsonify, request
from flask_restful import Resource
from App.models import db, APIKey
from App.utils.MD5_ID import *


class APIKeyCRUD(Resource):
    # 添加
    def post(self):
        apiKey = APIKey(
            AK_id=creat_md5_id()[:8], AK_name=request.json['name'], AK_value=request.json['value'],
            AK_intro=request.json['intro'], userid=request.json['uid'])
        try:
            db.session.add(apiKey)  # 加入数据库
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:  # 数据库插入操作异常处理
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': str(e)})

    # 删除
    def delete(self):
        try:
            db.session.delete(APIKey.query.filter(APIKey.AK_id == request.json['id']).first())
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()  # 回滚
            db.session.flush()  # 刷新，清空缓存
            return jsonify({'success': False, 'message': str(e)})

    # 查询【参数:uid,返回:【uid下的所有apikey列表】
    def get(self):
        return jsonify({'data': [
            {'id': x.AK_id, 'name': x.AK_name, 'value': x.AK_value, 'intro': x.AK_intro}
            for x in APIKey.query.filter(APIKey.userid == request.args['uid'])], 'success': True})
