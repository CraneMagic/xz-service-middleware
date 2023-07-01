from flask import Flask, request, make_response, current_app
from flask_cors import *

import json
import re
import uuid
import jwt
import random
from functools import wraps
import datetime
from dotenv import load_dotenv

load_dotenv('./.env')

import os
env = os.environ

from werkzeug.security import check_password_hash, generate_password_hash

from _functional._algorithm import path_algorithm_easy, path_algorithm_two_point, path_algorithm_four_point
from _functional._database import query, mutate, FULLCOLS
from _functional._format import response_body, api, database_response_reformat
from _functional._error import error, DATABASE_ERROR, LOGIN_FAILED, UNKNOWN_ERROR, EMPTY_INPUT, TOKEN_EXPIRED, NO_CURRUSER, WRONG_PASSWORD, TOKEN_INVAILD, TOKEN_MISSING, USERNAME_INVAILD, WRONG_PHONE, WRONG_USERID
from _functional._mqtt import subscribeSingleMQTTMsgWithoutClient, transmitSingleMQTTMsgWithoutClient

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.after_request
def after_request(resp):
	resp = make_response(resp)
	resp.headers['Access-Control-Allow-Origin'] = '*'
	resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
	resp.headers['Access-Control-Allow-Headers'] = 'content-type,token,Authorization'
	return resp

def fetch_controller_list_operation(conditions=[]):
    viewname = 'view_controller'
    cols = ['id', 'username', 'password', 'token']
    (status, res) = query(env.get('DB_HOST'), env.get('DB_USER'), env.get('DB_PASS'), int(env.get('DB_PORT')), env.get('DB_NAME'), cols, viewname, conditions)
    if status:
        return res
    return []

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        print('token_required', args)
        token = None
        # print(args)
        # print(request.headers, type(request.headers), request.headers['Authorization'])
        reqJson = eval(str(request.data, 'utf-8'))
        if request.headers.get('Authorization', None):
            token = request.headers['Authorization']
        if not token:
            # 501 Token missing
            return json.dumps({
                'request_code': reqJson['request_code'],
                'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'response_result': 501,
                'response_data': {}
            })
        try:
            # print(token, current_app.config['SECRET_KEY'])
            user_data = jwt.decode(
                token, str(current_app.config['SECRET_KEY']), algorithms='HS256')
            all_users = fetch_controller_list_operation()
            # print(user_data, all_users)
            if len([user for user in all_users if user.get('id') == user_data.get('id')]):
                current_user = [user for user in all_users if user.get('id') == user_data.get('id')][0]
                print(current_user['token'], token)
                if not current_user['token'] == token:
                    # 500 Token invaild
                    return json.dumps({
                        'request_code': reqJson['request_code'],
                        'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'response_result': 500,
                        'response_data': {}
                    })
            else:
                # 503 no current user
                return json.dumps({
                    'request_code': reqJson['request_code'],
                    'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'response_result': 503,
                    'response_data': {}
                })
        except jwt.ExpiredSignatureError:
            # 502 Token expired
            return json.dumps({
                'request_code': reqJson['request_code'],
                'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'response_result': 502,
                'response_data': {}
            })
        except Exception as err:
            print(err)
            # 500 Token invaild
            return json.dumps({
                'request_code': reqJson['request_code'],
                'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'response_result': 500,
                'response_data': {}
            })
            # return jsonify({'message': 'token is invalid'})
        return f(current_user, *args, **kwargs)
    return decorator

@app.route('/')
def home():
    # error(LOGIN_FAILED)
	return 'Hello Middleware'


@app.route('/sendTask', methods=['POST'])
def sendTask():
    warehouseId = env.get('WAREHOUSE_ID')
    currentDateTime = datetime.datetime.now()
    
    # 下发行车任务接口
    reqJson = request.get_json(silent=True)
    print(reqJson)
    request_data = reqJson.get('request_data', None)
    # 获取型号库位对应信息
    area_cols = ['id', 'comment']
    area_conditions = ['warehouse_id=\'%s\'' % warehouseId]
    (status, area_res) = query(env.get('DB_HOST'), env.get('DB_USER'), env.get('DB_PASS'), int(env.get('DB_PORT')), env.get('DB_NAME'), area_cols, 'view_area', area_conditions)
    # print(area_res)
    if not status:
        # 999 未知错误
        return json.dumps({
            'request_code': reqJson['request_code'],
            'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'response_result': 999,
            'response_data': {'data': 1}
        })
    steel_model_to_area_id = dict()
    for item in area_res:
        if item['comment'] != '':
            steel_model_to_area_id.setdefault(item['comment'], item['id'])
    if steel_model_to_area_id == {}:
        steel_model_to_area_id = {
            '钢板6/Q235B': 'KW01',
            '钢板8/SS400P': 'KW02',
            '钢板10/SS400P': 'KW03',
            '钢板12/SS400P': 'KW04',
            '钢板12/Q345B': 'KW05',
            '钢板14/SS400P': 'KW06',
            '钢板14/Q345B': 'KW07',
            '钢板16/SS400P': 'KW08',
            '钢板20/Q345B': 'KW09',
            '钢板22/Q345B': 'KW10',
            '钢板25/Q345B': 'KW11',
            '钢板8/Q345B': 'KW12',
            '60358082': 'KW01',
            '110101020164AD26': 'KW02',
            '110101020237AD5': 'KW03',
            '110101020161AD29': 'KW04',
            '110101020170AD30': 'KW05',
            '110101020159AD17': 'KW06',
            '60358086': 'KW07',
            '60358117': 'KW08',
            # '钢板20/Q345B++': 'KW09',
            '110101020175AD20': 'KW10',
            # '钢板25/Q345B++': 'KW11',
            '110101020172AD23': 'KW12',
        }
    print(steel_model_to_area_id)
    # # 获取起重机信息
    # crane_cols = ['id', 'maxHeight']
    # crane_conditions = ['id=\'%s\'' % craneId, 'warehouse_id=\'%s\'' % warehouseId]
    # (status, crane_res) = query(env.get('DB_HOST'), env.get('DB_USER'), env.get('DB_PASS'), int(env.get('DB_PORT')), env.get('DB_NAME'), crane_cols, 'view_equipment', crane_conditions)
    # if not status:
    #     # 999 未知错误
    #     return json.dumps({
    #         'request_code': reqJson['request_code'],
    #         'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    #         'response_result': 999,
    #         'response_data': {'data': 2}
    #     })
    # if not len(crane_res) == 1:
    #     # 999 未知错误
    #     return json.dumps({
    #         'request_code': reqJson['request_code'],
    #         'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    #         'response_result': 999,
    #         'response_data': {'data': 3}
    #     })
    # craneMaxHeight = crane_res[0]['maxHeight']
    # 比对钢板型号
    print(request_data.get('steel_model', None), list(steel_model_to_area_id.keys()), request_data.get('steel_model', None) not in list(steel_model_to_area_id.keys()))
    if request_data.get('steel_model', None) not in list(steel_model_to_area_id.keys()):
        # 201 下发行车任务接口-钢板型号不存在
        return json.dumps({
            'request_code': reqJson['request_code'],
            'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'response_result': 201,
            'response_data': {}
        })
    # 获取钢板型号
    viewname = 'view_materialmodel'
    tablename = viewname.replace('view_', '')
    materialmodel_cols = ['id', 'length', 'width', 'height', 'xAxisDelta', 'yAxisDelta', 'zAxisDelta']
    materialmodel_conditions = ['name=\'%s\'' % request_data.get('steel_model', None)]
    (status, materialmodel_res) = query(env.get('DB_HOST'), env.get('DB_USER'), env.get('DB_PASS'), int(env.get('DB_PORT')), env.get('DB_NAME'), materialmodel_cols, viewname, materialmodel_conditions)
    if not status:
        # 999 未知错误
        return json.dumps({
            'request_code': reqJson['request_code'],
            'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'response_result': 999,
            'response_data': {'data': 4}
        })
    if not len(materialmodel_res) == 1:
        # 999 未知错误
        return json.dumps({
            'request_code': reqJson['request_code'],
            'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'response_result': 999,
            'response_data': {'data': 5}
        })
    print(materialmodel_res)
    # 获取库位信息
    area_cols = ['id', 'height', 'xAxis', 'yAxis', 'zAxis']
    area_conditions = ['id=\'%s\'' % steel_model_to_area_id[request_data.get('steel_model', None)], 'warehouse_id=\'%s\'' % warehouseId]
    (status, area_res) = query(env.get('DB_HOST'), env.get('DB_USER'), env.get('DB_PASS'), int(env.get('DB_PORT')), env.get('DB_NAME'), area_cols, 'view_area', area_conditions)
    if not status:
        # 999 未知错误
        return json.dumps({
            'request_code': reqJson['request_code'],
            'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'response_result': 999,
            'response_data': {'data': 6}
        })
    if not len(area_res) == 1:
        # 999 未知错误
        return json.dumps({
            'request_code': reqJson['request_code'],
            'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'response_result': 999,
            'response_data': {'data': 7}
        })
    areaMaxHeight = int(area_res[0]['height'])
    viewname = 'view_material'
    tablename = viewname.replace('view_', '')
    cols = FULLCOLS[viewname]
    # 计算 Area 高度
    areaHeight = 0
    conditions = ['warehouse_id=\'%s\'' % warehouseId, 'area_id=\'%s\'' % area_res[0]['id']]
    (status, res) = query(env.get('DB_HOST'), env.get('DB_USER'), env.get('DB_PASS'), int(env.get('DB_PORT')), env.get('DB_NAME'), cols, viewname, conditions)
    if not status:
        # 999 未知错误
        return json.dumps({
            'request_code': reqJson['request_code'],
            'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'response_result': 999,
            'response_data': {'data': 8}
        })
    res_reformat = database_response_reformat(tablename, res)
    for material in res_reformat:
        # print(int(material['model']['size']['height']))
        areaHeight += int(material['model']['size']['height'])
    # 判断任务类型
    if request_data.get('mission_type', None) == 1:
        craneId = env.get('CRANE_ID_MATERIAL_INPUTS')
        # 入库
        targetArea_id = steel_model_to_area_id[request_data.get('steel_model', None)]
        targetPosition = {
            'xAxis': int(area_res[0]['xAxis'] + int(materialmodel_res[0]['length'] / 2) + int(materialmodel_res[0].get('xAxisDelta', 0))),
            'yAxis': int(area_res[0]['yAxis'] + int(materialmodel_res[0]['width'] / 2) + int(materialmodel_res[0].get('yAxisDelta', 0))),
            'zAxis': int(areaMaxHeight - areaHeight - int(materialmodel_res[0]['height'])),
        }
        inarea_cols = ['id', 'height', 'xAxis', 'yAxis', 'zAxis']
        inarea_conditions = ['type=\'%s\'' % 'IN', 'warehouse_id=\'%s\'' % warehouseId]
        (status, inarea_res) = query(env.get('DB_HOST'), env.get('DB_USER'), env.get('DB_PASS'), int(env.get('DB_PORT')), env.get('DB_NAME'), inarea_cols, 'view_area', inarea_conditions)
        if not status:
            # 999 未知错误
            return json.dumps({
                'request_code': reqJson['request_code'],
                'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'response_result': 999,
                'response_data': {'data': 9}
            })
        inareaMaxHeight = int(inarea_res[0]['height'])
        sourceArea_id = 'IN'
        # 计算 SourceArea 高度
        sourceAreaHeight = 0
        conditions1 = ['warehouse_id=\'%s\'' % warehouseId, 'area_id=\'%s\'' % sourceArea_id]
        (status, res1) = query(env.get('DB_HOST'), env.get('DB_USER'), env.get('DB_PASS'), int(env.get('DB_PORT')), env.get('DB_NAME'), cols, viewname, conditions1)
        if not status:
            # 999 未知错误
            return json.dumps({
                'request_code': reqJson['request_code'],
                'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'response_result': 999,
                'response_data': {'data': 10}
            })
        res_reformat1 = database_response_reformat(tablename, res1)
        # print(res_reformat1)
        for material in res_reformat1:
            # print(int(material['model']['size']['height']))
            sourceAreaHeight += int(material['model']['size']['height'])
        sourcePosition = {
            'xAxis': int(inarea_res[0]['xAxis'] + int(materialmodel_res[0]['length'] / 2) + int(materialmodel_res[0].get('xAxisDelta', 0))),
            'yAxis': int(inarea_res[0]['yAxis'] + int(materialmodel_res[0]['width'] / 2) + int(materialmodel_res[0].get('yAxisDelta', 0))),
            'zAxis': int(inareaMaxHeight - sourceAreaHeight),
        }
    elif request_data.get('mission_type', None) == 2:
        craneId = int(env.get('CRANE_ID_MATERIAL_UPLOAD'))
        # 上料
        sourceArea_id = steel_model_to_area_id[request_data.get('steel_model', None)]
        sourcePosition = {
            'xAxis': int(area_res[0]['xAxis'] + int(materialmodel_res[0]['length'] / 2) + int(materialmodel_res[0].get('xAxisDelta', 0))),
            'yAxis': int(area_res[0]['yAxis'] + int(materialmodel_res[0]['width'] / 2) + int(materialmodel_res[0].get('yAxisDelta', 0))),
            'zAxis': int(areaMaxHeight - areaHeight),
        }
        outarea_cols = ['id', 'height', 'xAxis', 'yAxis', 'zAxis']
        outarea_conditions = ['id=\'%s\'' % request_data.get('station', None), 'warehouse_id=\'%s\'' % warehouseId]
        (status, outarea_res) = query(env.get('DB_HOST'), env.get('DB_USER'), env.get('DB_PASS'), int(env.get('DB_PORT')), env.get('DB_NAME'), outarea_cols, 'view_area', outarea_conditions)
        if not status:
            # 999 未知错误
            return json.dumps({
                'request_code': reqJson['request_code'],
                'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'response_result': 999,
                'response_data': {'data': 11}
            })
        if not len(outarea_res) == 1:
            # 202 station不存在
            return json.dumps({
                'request_code': reqJson['request_code'],
                'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'response_result': 202,
                'response_data': {'data': 12}
            })
        outareaMaxHeight = int(outarea_res[0]['height'])
        targetArea_id = request_data.get('station', None)
        # 计算 TargetArea 高度
        targetAreaHeight = 0
        conditions2 = ['warehouse_id=\'%s\'' % warehouseId, 'area_id=\'%s\'' % targetArea_id]
        (status, res2) = query(env.get('DB_HOST'), env.get('DB_USER'), env.get('DB_PASS'), int(env.get('DB_PORT')), env.get('DB_NAME'), cols, viewname, conditions2)
        if not status:
            # 999 未知错误
            return json.dumps({
                'request_code': reqJson['request_code'],
                'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'response_result': 999,
                'response_data': {'data': 13}
            })
        res_reformat2 = database_response_reformat(tablename, res2)
        # print(res_reformat2)
        for material in res_reformat2:
            # print(int(material['model']['size']['height']))
            targetAreaHeight += int(material['model']['size']['height'])
        targetPosition = {
            'xAxis': int(outarea_res[0]['xAxis'] + int(materialmodel_res[0]['length'] / 2) + int(materialmodel_res[0].get('xAxisDelta', 0))),
            'yAxis': int(outarea_res[0]['yAxis'] + int(materialmodel_res[0]['width'] / 2) + int(materialmodel_res[0].get('yAxisDelta', 0))),
            'zAxis': int(outareaMaxHeight - targetAreaHeight - int(materialmodel_res[0]['height'])),
        }
    else:
        # 1 输入参数格式错误
            return json.dumps({
                'request_code': reqJson['request_code'],
                'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'response_result': 1,
                'response_data': {}
            })
    # 获取行车信息
    dictpayload = eval(str(subscribeSingleMQTTMsgWithoutClient(), 'utf-8'))
    while not dictpayload.get('eventType', None) == 'Crone_Status' or not dictpayload.get('eventdata', None).get('CraneID') == craneId:
        dictpayload = eval(str(subscribeSingleMQTTMsgWithoutClient(), 'utf-8'))
    if dictpayload.get('eventdata', None):
        if int(dictpayload.get('eventdata', None).get('Crane_WorkStatus', None)) == 0:
            if dictpayload.get('eventdata', None).get('Crane_Position', None):
                cranePosition = {
                    'xAxis': int(dictpayload.get('eventdata', None).get('Crane_Position', None).split(',')[0]),
                    'yAxis': int(dictpayload.get('eventdata', None).get('Crane_Position', None).split(',')[1]),
                    'zAxis': int(dictpayload.get('eventdata', None).get('Crane_Position', None).split(',')[2]),
                }
        else:
            # 200 下发行车任务接口-行车现在无法接受任务
            return json.dumps({
                'request_code': reqJson['request_code'],
                'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'response_result': 200,
                'response_data': {}
            })
    else:
        # 999 未知错误
        return json.dumps({
            'request_code': reqJson['request_code'],
            'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'response_result': 999,
            'response_data': {'data': 16}
        })
    if request_data.get('mission_type', None) == 1:
        # 入库
        # 新增 material 直接加入 VIRTUAL 库位
        # 新增 material 表
        sql_new = "INSERT INTO material(id, model_id, area_id, warehouse_id, areaSeq, createTime) VALUES"
        for item in [{'id': materialId, 'model_id': request_data.get('steel_model', None), 'area_id': 'VIRTUAL', 'warehouse_id': warehouseId, 'areaSeq': 0}]:
            id, model_id, area_id, warehouse_id = item.get('id', None), item.get('model_id', None), item.get('area_id', None), item.get('warehouse_id', None)
            areaSeq = item.get('areaSeq', None)
            sql_new += "('%s', '%s', '%s', '%s', %d, '%s'), " % (id, model_id, area_id, warehouse_id, areaSeq, currentDateTime.strftime('%Y-%m-%d %H:%M:%S'))
        sql_new = sql_new[0: -2] + ';'
        (status, mutateRes) = mutate(env.get('DB_HOST'), env.get('DB_USER'), env.get('DB_PASS'), int(env.get('DB_PORT')), env.get('DB_NAME'), sql_new)
        if not status:
            print(mutateRes, DATABASE_ERROR[mutateRes[0]])
            # 999 未知错误
            return json.dumps({
                'request_code': reqJson['request_code'],
                'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'response_result': 999,
                'response_data': {'data': 17}
            })
        # # ======================================== 原始代码 ========================================
        # # 修改原 material 表 areaSeq 数据
        # materialId = 'AT-%s' % '{:0>6d}'.format(int(random.random() * 1000000))
        # materialsql = []
        # for item in [{'id': 'In', 'warehouse_id': warehouseId, 'deltaAreaSeq': 1}]:
        #     materialsql.append("UPDATE material SET `areaSeq`=`areaSeq`+%d WHERE `area_id`='%s' AND `warehouse_id`='%s';" % (item.get('deltaAreaSeq', 0), item.get('id', None), item.get('warehouse_id', None)))
        # # 新增 material 表
        # sql_new = "INSERT INTO material(id, model_id, area_id, warehouse_id, areaSeq, createTime) VALUES"
        # for item in [{'id': materialId, 'model_id': request_data.get('steel_model', None), 'area_id': 'In', 'warehouse_id': warehouseId, 'areaSeq': 0}]:
        #     id, model_id, area_id, warehouse_id = item.get('id', None), item.get('model_id', None), item.get('area_id', None), item.get('warehouse_id', None)
        #     areaSeq = item.get('areaSeq', None)
        #     sql_new += "('%s', '%s', '%s', '%s', %d, '%s'), " % (id, model_id, area_id, warehouse_id, areaSeq, currentDateTime.strftime('%Y-%m-%d %H:%M:%S'))
        # sql_new = sql_new[0: -2] + ';'
        # materialsql.append(sql_new)
        # print(materialsql)
        # # print('database')
        # for sqlItem in materialsql:
        #     (status, mutateResItem) = mutate(env.get('DB_HOST'), env.get('DB_USER'), env.get('DB_PASS'), int(env.get('DB_PORT')), env.get('DB_NAME'), sqlItem)
        #     if status:
        #         continue
        #     else:
        #         print(mutateResItem, DATABASE_ERROR[mutateResItem[0]])
        #         # 999 未知错误
        #         return json.dumps({
        #             'request_code': reqJson['request_code'],
        #             'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        #             'response_result': 999,
        #             'response_data': {'data': 17}
        #         })
        # # ======================================== 原始代码 ========================================
        materialWeight = '1000'
        id = currentDateTime.strftime('%Y%m%d%H%M%S')
        materials = ['%s,%s,%s' % (materialId, request_data.get('steel_info', None), materialWeight)]
        resetPositionStr = env.get('CRANE_MATERIAL_INPUTS_RESET_POSITION')
        priority = env.get('CRANE_MATERIAL_INPUTS_PRIORITY')
        resetPositionArr = resetPositionStr.split(',')
        resetPosition = {
            'xAxis': int(resetPositionArr[0]),
            'yAxis': int(resetPositionArr[1]),
            'zAxis': 0,
            'degree': 0,
        }
        print(cranePosition, sourcePosition, targetPosition, resetPosition, priority)
        actionSeq = path_algorithm_four_point(cranePosition, sourcePosition, targetPosition, resetPosition, priority)
    elif request_data.get('mission_type', None) == 2:
        # 上料
        # 获取材料信息
        material_cols = ['id']
        material_conditions = ['area_id=\'%s\'' % sourceArea_id, 'warehouse_id=\'%s\'' % warehouseId, 'areaSeq=0']
        (status, material_res) = query(env.get('DB_HOST'), env.get('DB_USER'), env.get('DB_PASS'), int(env.get('DB_PORT')), env.get('DB_NAME'), material_cols, 'view_material', material_conditions)
        if not status:
            # 999 未知错误
            return json.dumps({
                'request_code': reqJson['request_code'],
                'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'response_result': 999,
                'response_data': {'data': 18}
            })
        if not len(material_res) == 1:
            # 203 下发行车任务接口-无该钢板型号材料
            return json.dumps({
                'request_code': reqJson['request_code'],
                'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'response_result': 203,
                'response_data': {}
            })
        materialId = material_res[0]['id']
        # 修改材料位置至 VIRTUAL
        rmsql = "UPDATE material SET `area_id`='VIRTUAL' WHERE id='%s' AND `warehouse_id`='%s'" % (materialId, warehouseId)
        (status, mutateRes) = mutate(env.get('DB_HOST'), env.get('DB_USER'), env.get('DB_PASS'), int(env.get('DB_PORT')), env.get('DB_NAME'), rmsql)
        # 起始库位材料顺序变化
        materialsql = []
        for item in [{'id': sourceArea_id, 'warehouse_id': warehouseId, 'deltaAreaSeq': 1}]:
            materialsql.append("UPDATE material SET `areaSeq`=`areaSeq`-%d WHERE `area_id`='%s' AND `warehouse_id`='%s';" % (item.get('deltaAreaSeq', 0), item.get('id', None), item.get('warehouse_id', None)))
        for sqlItem in materialsql:
            (status, mutateResItem) = mutate(env.get('DB_HOST'), env.get('DB_USER'), env.get('DB_PASS'), int(env.get('DB_PORT')), env.get('DB_NAME'), sqlItem)
            if status:
                continue
            else:
                print(mutateResItem, DATABASE_ERROR[mutateResItem[0]])
                # 999 未知错误
                return json.dumps({
                    'request_code': reqJson['request_code'],
                    'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'response_result': 999,
                    'response_data': {'data': 182}
                })
        if not status:
            # 999 未知错误
            return json.dumps({
                'request_code': reqJson['request_code'],
                'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'response_result': 999,
                'response_data': {'data': 181}
            })
        materialWeight = '1000'
        id = currentDateTime.strftime('%Y%m%d%H%M%S')
        materials = ['%s,%s,%s' % (materialId, request_data.get('steel_info', None), materialWeight)]
        resetPositionStr = env.get('CRANE_MATERIAL_UPLOAD_RESET_POSITION')
        priority = env.get('CRANE_MATERIAL_UPLOAD_PRIORITY')
        resetPositionArr = resetPositionStr.split(',')
        resetPosition = {
            'xAxis': int(resetPositionArr[0]),
            'yAxis': int(resetPositionArr[1]),
            'zAxis': 0,
            'degree': 0,
        }
        print(cranePosition, sourcePosition, targetPosition, resetPosition, priority)
        actionSeq = path_algorithm_four_point(cranePosition, sourcePosition, targetPosition, resetPosition, priority)
    else:
        # 1 输入参数格式错误
            return json.dumps({
                'request_code': reqJson['request_code'],
                'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'response_result': 1,
                'response_data': {}
            })
    # 写入 task 数据库
    # materialWeight = '1000'
    # id = currentDateTime.strftime('%Y%m%d%H%M%S')
    # materials = ['%s,%s,%s' % (materialId, request_data.get('steel_info', None), materialWeight)]
    # print(cranePosition, sourcePosition, targetPosition)
    # actionSeq = path_algorithm_easy(cranePosition, sourcePosition, targetPosition, 'xy')
    sendTime = currentDateTime.strftime('%Y-%m-%d %H:%M:%S')
    tasksql = "INSERT INTO task(`id`, `crane_id`, `sourceArea_id`, `targetArea_id`, `materials`, `actionSeq`, `warehouse_id`, `sendTime`, `status`, `controller_task_id`) "\
          "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (id, craneId, sourceArea_id, targetArea_id, str(materials).replace("'", '"'), str(actionSeq).replace("'", '"'), warehouseId, sendTime, 'PENDING', request_data.get('mission_no', None))
    print(tasksql)
    # print('database')
    (status, mutateRes) = mutate(env.get('DB_HOST'), env.get('DB_USER'), env.get('DB_PASS'), int(env.get('DB_PORT')), env.get('DB_NAME'), tasksql)
    if not status:
        print(mutateRes)
        # 999 未知错误
        return json.dumps({
            'request_code': reqJson['request_code'],
            'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'response_result': 999,
            'response_data': {'data': 19}
        })
    # 发送 MQTT 消息
    payload = {
        'eventType': 'CroneControl',
        'siteIp': '192.168.0.1',
        'eventDate': sendTime,
        'eventdata': {
            'CraneID': craneId,
            'CraneTaskHanding': actionSeq,
            'Material_info': materials[0],
            'CraneTaskID': id,
        }
    }
    transmitSingleMQTTMsgWithoutClient('iot/crane_task', str(json.dumps(payload)))
    print(json.dumps(payload))
    responseBody = {
        'request_code': reqJson['request_code'],
        'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'response_result': 0,
        'response_data': {
            'CraneTaskID': id,
        }
    }
    return json.dumps(responseBody)

@app.route('/taskCancel', methods=['POST'])
def taskCancel():
    warehouseId = env.get('WAREHOUSE_ID')
    currentDateTime = datetime.datetime.now()
    craneId = env.get('CRANE_ID_MATERIAL_INPUTS')
    # 任务取消指令
    reqJson = request.get_json(silent=True)
    print(reqJson)
    request_data = reqJson.get('request_data', None)
    if not request_data.get('mission_no', None):
        # 1 输入参数格式错误
        return json.dumps({
            'request_code': reqJson['request_code'],
            'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'response_result': 1,
            'response_data': {'data': 20}
        })
    tasksql = "UPDATE task SET `status`='CANCELLED' WHERE `controller_task_id`='%s' AND `warehouse_id`='%s' AND `status`='PENDING'" % (request_data.get('mission_no', None), warehouseId)
    (status, mutateRes) = mutate(env.get('DB_HOST'), env.get('DB_USER'), env.get('DB_PASS'), int(env.get('DB_PORT')), env.get('DB_NAME'), tasksql)
    if not status:
        print(mutateRes)
        # 999 未知错误
        return json.dumps({
            'request_code': reqJson['request_code'],
            'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'response_result': 999,
            'response_data': {'data': 21}
        })
    responseBody = {
        'request_code': reqJson['request_code'],
        'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'response_result': 0,
        'response_data': {
            
        }
    }
    return json.dumps(responseBody)

@app.route('/taskChange', methods=['POST'])
def taskChange():
    warehouseId = env.get('WAREHOUSE_ID')
    # 任务暂停或恢复接口
    reqJson = request.get_json(silent=True)
    print(reqJson)
    responseBody = {
        'request_code': reqJson['request_code'],
        'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'response_result': 0,
        'response_data': {
            
        }
    }
    return json.dumps(responseBody)

@app.route('/auth', methods=['POST'])
def auth():
    warehouseId = env.get('WAREHOUSE_ID')
    craneId = env.get('CRANE_ID_MATERIAL_INPUTS')
    # 中控登录/退出登录智能行车接口
    reqJson = request.get_json(silent=True)
    print(reqJson)
    responseBody = {
        'request_code': reqJson['request_code'],
        'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'response_result': 0,
        'response_data': {
            
        }
    }
    # 获取行车信息
    dictpayload = eval(str(subscribeSingleMQTTMsgWithoutClient(), 'utf-8'))
    craneId = dictpayload.get('eventdata', None).get('CraneID')
    while not dictpayload.get('eventType', None) == 'Crone_Status' or not dictpayload.get('eventdata', None).get('CraneID') == craneId:
        dictpayload = eval(str(subscribeSingleMQTTMsgWithoutClient(), 'utf-8'))
    if dictpayload.get('eventdata', None):
        if not int(dictpayload.get('eventdata', None).get('Crane_WorkStatus', None)) == 0:
            # 505 中控登录/退出登录智能行车接口-行车目前无法登录/退出登录
            return json.dumps({
                'request_code': reqJson['request_code'],
                'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'response_result': 505,
                'response_data': {}
            })
    if reqJson['request_data']['type'] == 1:
        # 登录
        print('login')
        auth = reqJson['request_data']
        print(auth)
        if not auth or not auth['user'] or not auth['password']:
            responseBody['response_result'] = 1
            return json.dumps(responseBody)
            error(LOGIN_FAILED, 'auth')
        all_users = fetch_controller_list_operation()
        print(all_users)
        if len([user for user in all_users if user.get('username') == auth['user']]):
            user = [user for user in all_users if user.get('username') == auth['user']][0]
            if check_password_hash(user.get('password'), auth['password']):  
                token = jwt.encode({'id': user.get('id'), 'exp' : datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=120)}, str(current_app.config['SECRET_KEY']))  
                responseBody['response_result'] = 0
                responseBody['response_data'] = {
                    'token': token
                }
                controllersql = "UPDATE controller SET `token`='%s' WHERE `id`='%s'" % (token, user.get('id'))
                (status, mutateRes) = mutate(env.get('DB_HOST'), env.get('DB_USER'), env.get('DB_PASS'), int(env.get('DB_PORT')), env.get('DB_NAME'), controllersql)
                if not status:
                    print(mutateRes)
                    # 999 未知错误
                    return json.dumps({
                        'request_code': reqJson['request_code'],
                        'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'response_result': 999,
                        'response_data': {'data': 22}
                    })
                return json.dumps(responseBody)
                api(response_body(200, 'auth', { 'token' : token, 'user': database_response_reformat('controller', [user])[0] }))
        else:
            # 503 no current user
            return json.dumps({
                'request_code': reqJson['request_code'],
                'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'response_result': 503,
                'response_data': {}
            })
        # 504 no current user
        return json.dumps({
            'request_code': reqJson['request_code'],
            'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'response_result': 504,
            'response_data': {}
        })
    elif reqJson['request_data']['type'] == 2:
        controllersql = "UPDATE controller SET `token`='%s' WHERE `username`='%s'" % ('', reqJson['request_data']['user'])
        (status, mutateRes) = mutate(env.get('DB_HOST'), env.get('DB_USER'), env.get('DB_PASS'), int(env.get('DB_PORT')), env.get('DB_NAME'), controllersql)
        if not status:
            print(mutateRes)
            # 999 未知错误
            return json.dumps({
                'request_code': reqJson['request_code'],
                'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'response_result': 999,
                'response_data': {'data': 23}
            })
    else:
        # 1 输入参数格式错误
        return json.dumps({
            'request_code': reqJson['request_code'],
            'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'response_result': 1,
            'response_data': {}
        })


@app.route('/register', methods=['POST'])
def register():  
    reqJson = request.get_json(silent=True)    
    username, password  = reqJson.get('username', None), reqJson.get('password', None)
    if not all([username, password]):
        error(EMPTY_INPUT, 'register')
    if not (re.match('^[A-Za-z0-9]+$', username)):
        error(USERNAME_INVAILD, 'register')
    hashed_password = generate_password_hash(password, method='sha256')
    sql = "INSERT INTO controller(id, username, password) "\
          "VALUES('%s', '%s', '%s');" % (uuid.uuid4(), username, hashed_password)
    (status, mutateRes) = mutate(env.get('DB_HOST'), env.get('DB_USER'), env.get('DB_PASS'), int(env.get('DB_PORT')), env.get('DB_NAME'), sql)
    if status:
        api(response_body(200, 'register', None))
    elif DATABASE_ERROR.get(mutateRes[0], None):
        error(DATABASE_ERROR.get(mutateRes[0], None), 'register')
    else:
        error(UNKNOWN_ERROR, 'register')


@app.route('/manual', methods=['POST'])
@token_required
def manual(currentuser):
    warehouseId = env.get('WAREHOUSE_ID')
    currentDateTime = datetime.datetime.now()
    craneId = env.get('CRANE_ID_MATERIAL_INPUTS')
    action_to_area_id = {
        11: 'KW01',
        12: 'KW02',
        13: 'KW03',
        14: 'KW04',
        15: 'KW05',
        16: 'KW06',
        17: 'KW07',
        18: 'KW08',
        19: 'KW09',
        20: 'KW10',
        21: 'KW11',
        22: 'KW12',
    }
    # 中控手动操作智能行车接口
    reqJson = request.get_json(silent=True)
    print(reqJson)
    request_data = reqJson.get('request_data', None)
    # 获取行车信息
    dictpayload = eval(str(subscribeSingleMQTTMsgWithoutClient(), 'utf-8'))
    craneId = dictpayload.get('eventdata', None).get('CraneID')
    while not dictpayload.get('eventType', None) == 'Crone_Status' or not dictpayload.get('eventdata', None).get('CraneID') == craneId:
        dictpayload = eval(str(subscribeSingleMQTTMsgWithoutClient(), 'utf-8'))
    if dictpayload.get('eventdata', None):
        if not int(dictpayload.get('eventdata', None).get('Crane_WorkStatus', None)) == 0:
            # 600 中控手动操作智能行车接口-行车目前无法手动操作
            return json.dumps({
                'request_code': reqJson['request_code'],
                'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'response_result': 600,
                'response_data': {}
            })
    else:
        if dictpayload.get('eventdata', None).get('Crane_Position', None):
            cranePosition = {
                'xAxis': int(dictpayload.get('eventdata', None).get('Crane_Position', None).split(',')[0]),
                'yAxis': int(dictpayload.get('eventdata', None).get('Crane_Position', None).split(',')[1]),
                'zAxis': int(dictpayload.get('eventdata', None).get('Crane_Position', None).split(',')[2]),
            }
    if request_data.get('type', None) == 1:
        # 601 中控手动操作智能行车接口-暂不支持该操作类型
        return json.dumps({
            'request_code': reqJson['request_code'],
            'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'response_result': 601,
            'response_data': {}
        })
    elif request_data.get('type', None) == 2:
        # 601 中控手动操作智能行车接口-暂不支持该操作类型
        return json.dumps({
            'request_code': reqJson['request_code'],
            'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'response_result': 601,
            'response_data': {}
        })
        targetArea_id = action_to_area_id[request_data.get('action', None)]
        # 获取库位信息
        area_cols = ['id', 'xAxis', 'yAxis', 'zAxis']
        area_conditions = ['id=\'%s\'' % action_to_area_id[request_data.get('action', None)], 'warehouse_id=\'%s\'' % warehouseId]
        (status, area_res) = query(env.get('DB_HOST'), env.get('DB_USER'), env.get('DB_PASS'), int(env.get('DB_PORT')), env.get('DB_NAME'), area_cols, 'view_area', area_conditions)
        if not status:
            # 999 未知错误
            return json.dumps({
                'request_code': reqJson['request_code'],
                'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'response_result': 999,
                'response_data': {}
            })
        if not len(area_res) == 1:
            # 999 未知错误
            return json.dumps({
                'request_code': reqJson['request_code'],
                'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'response_result': 999,
                'response_data': {}
            })
        targetPosition = {
            'xAxis': area_res[0]['xAxis'],
            'yAxis': area_res[0]['yAxis'],
            'zAxis': area_res[0]['zAxis'],
        }
        # 写入 task 数据库
        materialWeight = '1000'
        id = 'S-%s' % currentDateTime.strftime('%Y%m%d%H%M%S')
        materials = ['fakematerial,0,0,0,%s' % materialWeight]
        print(cranePosition, targetPosition)
        actionSeq = path_algorithm_two_point(cranePosition, targetPosition)
        sendTime = currentDateTime.strftime('%Y-%m-%d %H:%M:%S')
        tasksql = "INSERT INTO task(`id`, `crane_id`, `sourceArea_id`, `targetArea_id`, `materials`, `actionSeq`, `warehouse_id`, `sendTime`, `status`) "\
            "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (id, craneId, None, targetArea_id, str(materials).replace("'", '"'), str(actionSeq).replace("'", '"'), warehouseId, sendTime, 'PENDING')
        print(tasksql)
        # print('database')
        (status, mutateRes) = mutate(env.get('DB_HOST'), env.get('DB_USER'), env.get('DB_PASS'), int(env.get('DB_PORT')), env.get('DB_NAME'), tasksql.replace("'None'", None))
        if not status:
            print(mutateRes)
            # 999 未知错误
            return json.dumps({
                'request_code': reqJson['request_code'],
                'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'response_result': 999,
                'response_data': {}
            })
        # 发送 MQTT 消息
        payload = {
            'eventType': 'CroneControl',
            'siteIp': '192.168.0.1',
            'eventDate': sendTime,
            'eventdata': {
                'CraneID': craneId,
                'CraneTaskHanding': actionSeq,
                'Material_info': materials[0],
                'CraneTaskID': id,
            }
        }
        transmitSingleMQTTMsgWithoutClient('iot/crane_task', str(json.dumps(payload)))
        print(json.dumps(payload))
        responseBody = {
            'request_code': reqJson['request_code'],
            'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'response_result': 0,
            'response_data': {
                'CraneTaskID': id,
            }
        }
    else:
        # 1 输入参数格式错误
        return json.dumps({
            'request_code': reqJson['request_code'],
            'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'response_result': 1,
            'response_data': {}
        })
    responseBody = {
        'request_code': reqJson['request_code'],
        'response_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'response_result': 0,
        'response_data': {
            
        }
    }
    return json.dumps(responseBody)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7667)
