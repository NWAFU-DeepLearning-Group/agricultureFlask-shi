import json

from flask import Blueprint, jsonify
from flask import request

from model import AgriUser, db
from utils import query_and_build_nested_menu

user_bp = Blueprint('user_bp', __name__)


# 处理用户登录请求
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # 查询用户
    user = AgriUser.query.filter_by(username=username, password=password).first()

    if user:
        code = 200
        access_token = 'bqddxxwqmfncffacvbpkuxvwvqrhln'  # 生成访问令牌的逻辑
        message = '成功'
    else:
        code = 500
        access_token = None
        message = '用户名或密码错误'

    response_data = {
        'code': code,
        'data': {'access_token': access_token},
        'message': message
    }

    return jsonify(response_data)


# 处理用户注册请求
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # 检查用户名是否已存在
    existing_user = AgriUser.query.filter_by(username=username).first()
    if existing_user:
        code = 500
        message = '用户名已存在'
    else:
        # 创建新用户
        new_user = AgriUser(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        code = 200
        message = '注册成功'

    # 构建注册响应 JSON
    response_data = {
        'code': code,
        'message': message
    }

    return jsonify(response_data)


# 处理用户注销请求
@user_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({"code": 200, "message": "成功"})


# 处理用户数据导入请求
@user_bp.route('/user/import', methods=['POST'])
def import_data():
    return jsonify({"code": 200, "message": "成功"})


# 处理用户数据导出请求
@user_bp.route('/user/export', methods=['POST'])
def export_data():
    return jsonify({"code": 200, "message": "成功"})


# 返回 JSON 格式的数据
@user_bp.route('/menu/list', methods=['GET'])
def mock_response():
    headers = request.headers
    access_token = headers.get('X-Access-Token')
    if access_token == 'bqddxxwqmfncffacvbpkuxvwvqrhln':
        # 查询数据库中的菜单数据并构建嵌套菜单
        nested_menu = query_and_build_nested_menu()
        # 将嵌套菜单转换为 JSON 格式
        json_nested_menu = json.dumps({"code": 200, "data": nested_menu, "message": "成功"})
        return json_nested_menu
    else:
        return jsonify({"code": 401, "message": "Unauthorized"})
