import json, copy
from flask import make_response
from werkzeug.exceptions import abort

from _functional._database import DecimalEncoder

def response_body(status=None, query=None, data=None):
    return dict(status=status, query=query, data=data)

DEFAULT_RESPONSE = response_body(200, None, None)

def api(res_detail=None):
    if res_detail is None:
        res_detail = DEFAULT_RESPONSE
    abort(make_response(json.dumps(res_detail, cls=DecimalEncoder), res_detail['status']))


def database_response_reformat(formatName, originalResponse):
    print(formatName, 'databaseResponseReformat')
    finalResponse = []
    if formatName == 'area':
        res = copy.deepcopy(originalResponse)
        res_reformat = []
        for item in res:
            item_reformat = {
                'id': item['id'],
                'type': item['type'],
                'name': item['name'],
                'size': {
                    'length': item['length'],
                    'width': item['width'],
                    'height': item['height'],
                },
                'position': {
                    'xAxis': item['xAxis'],
                    'yAxis': item['yAxis'],
                    'zAxis': item['zAxis'],
                    'degree': item['degree'],
                },
                'centerPosition': {
                    'xAxis': item['xAxis'],
                    'yAxis': item['yAxis'],
                    'zAxis': item['zAxis'],
                },
                'comment': item['comment'],
                'warehouse': {
                    'id': item['warehouse_id'],
                },
                'material_count': item['material_count'],
            }
            res_reformat.append(item_reformat)
        finalResponse = copy.deepcopy(res_reformat)
    if formatName == 'equipment':
        res = copy.deepcopy(originalResponse)
        res_reformat = []
        for item in res:
            item_reformat = {
                'id': item['id'],
                'type': item['type'],
                'model': {
                    'id': item['model_id'],
                    'name': item['model_name'],
                    'properties': eval(item['model_properties'].replace("'", '"').replace("True", "true").replace("false", "False")),
                },
                'usage': {
                    'status': item['status'],
                    'purchaseTime': item['purchaseTime'],
                    'startTime': item['startTime'],
                    'lastModifiedTime': item['lastModifiedTime'],
                    'expiredTime': item['expiredTime'],
                },
                'comment': item['comment'],
                'maxHeight': item['maxHeight'],
                'warehouse': { 'id': item['warehouse_id'], },
            }
            res_reformat.append(item_reformat)
        finalResponse = copy.deepcopy(res_reformat)
    if formatName == 'equipmentmodel':
        res = copy.deepcopy(originalResponse)
        res_reformat = []
        for item in res:
            if item['properties']:
                item_reformat = {
                    'id': item['id'],
                    'name': item['name'],
                    'type': item['type'],
                    'properties': eval(item['properties'].replace("'", '"').replace("True", "true").replace("false", "False")),
                }
            else:
                item_reformat = {
                    'id': item['id'],
                    'name': item['name'],
                    'type': item['type'],
                    'properties': None,
                }
            res_reformat.append(item_reformat)
        finalResponse = copy.deepcopy(res_reformat)
    if formatName == 'material':
        res = copy.deepcopy(originalResponse)
        res_reformat = []
        for item in res:
            item_reformat = {
                'id': item['id'],
                'model': {
                    'id': item['model_id'],
                    'name': item['model_name'],
                    'raws': item['model_raws'],
                    'thickness': item['model_thickness'],
                    'size': {
                        'length': item['model_length'],
                        'width': item['model_width'],
                        'height': item['model_height']
                    },
                    'delta': {
                        'xAxis': item['model_xAxisDelta'],
                        'yAxis': item['model_yAxisDelta'],
                        'zAxis': item['model_zAxisDelta'],
                    }
                },
                'area': {
                    'id': item['area_id'],
                    'type': item['area_type'],
                    'name': item['area_name'],
                    'comment': item['area_comment']
                },
                'areaSeq': item['areaSeq'],
                'createTime': item['createTime'],
                'removeTime': item['removeTime'],
            }
            res_reformat.append(item_reformat)
        finalResponse = copy.deepcopy(res_reformat)
    if formatName == 'materialmodel':
        res = copy.deepcopy(originalResponse)
        res_reformat = []
        res_reformat = res
        finalResponse = copy.deepcopy(res_reformat)
    if formatName == 'task':
        res = copy.deepcopy(originalResponse)
        res_reformat = []
        for item in res:
            item_reformat = {
                'id': item['id'],
                'crane': {
                    'id': item['crane_id'],
                    'model': {
                        'id': item['model_id'],
                        'name': item['model_name'],
                        'properties': item['model_properties'],
                    },
                    'usage': {
                        'status': item['model_status'],
                    },
                },
                'sourceArea': {
                    'id': item['sourceArea_id'],
                    'type': item['sourceArea_type'],
                    'name': item['sourceArea_name'],
                    'size': {
                        'length': item['sourceArea_length'],
                        'width': item['sourceArea_width'],
                        'height': item['sourceArea_height']
                    },
                    'position': {
                        'xAxis': item['sourceArea_xAxis'],
                        'yAxis': item['sourceArea_yAxis'],
                        'zAxis': item['sourceArea_zAxis'],
                        'degree': item['sourceArea_degree'],
                    },
                    'centerPosition': {
                        'xAxis': item['sourceArea_xAxisCenter'],
                        'yAxis': item['sourceArea_yAxisCenter'],
                        'zAxis': item['sourceArea_zAxisCenter'],
                    },
                    'comment': item['sourceArea_comment']
                },
                'targetArea': {
                    'id': item['targetArea_id'],
                    'type': item['targetArea_type'],
                    'name': item['targetArea_name'],
                    'size': {
                        'length': item['targetArea_length'],
                        'width': item['targetArea_width'],
                        'height': item['targetArea_height']
                    },
                    'position': {
                        'xAxis': item['targetArea_xAxis'],
                        'yAxis': item['targetArea_yAxis'],
                        'zAxis': item['targetArea_zAxis'],
                        'degree': item['targetArea_degree'],
                    },
                    'centerPosition': {
                        'xAxis': item['targetArea_xAxisCenter'],
                        'yAxis': item['targetArea_yAxisCenter'],
                        'zAxis': item['targetArea_zAxisCenter'],
                    },
                    'comment': item['targetArea_comment']
                },
                'materials': item['materials'],
                'actionSeq': item['actionSeq'],
                'sendTime': item['sendTime'],
                'startTime': item['startTime'],
                'endTime': item['endTime'],
                'status': item['status'],
                'warehouse': {
                    'id': item['warehouse_id'],
                },
            }
            res_reformat.append(item_reformat)
        finalResponse = copy.deepcopy(res_reformat)
    if formatName == 'warehouse':
        res = copy.deepcopy(originalResponse)
        res_reformat = []
        for item in res:
            item_reformat = {
                'id': item['id'],
                'name': item['name'],
                'address': item['address'],
                'size': {
                    'length': item['length'],
                    'width': item['width'],
                    'height': item['height'],
                },
                'maxHeight': item['maxHeight'],
                'comment': item['comment'],
            }
            res_reformat.append(item_reformat)
        finalResponse = copy.deepcopy(res_reformat)
    if formatName == 'GeoJSON-area':
        res = copy.deepcopy(originalResponse)
        res_reformat = {}
        bunker_res_reformat = []
        center_res_reformat = []
        data_res_reformat = []
        for item in res:
            bunker_item_reformat = {
                'type': 'Feature',
                'id': item['id'],
                'properties': {
                    'name': item['name'],
                    'type': item['type'],
                    'length': float(item['length']),
                    'width': float(item['width']),
                    'height': float(item['height']),
                    'comment': item['comment'],
                },
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': [
                        [
                            [ 
                                float(item['xAxis'] - item['length'] / 2), 
                                float(item['yAxis'] - item['width'] / 2) 
                            ],
                            [ 
                                float(item['xAxis'] - item['length'] / 2), 
                                float(item['yAxis'] + item['width'] / 2) 
                            ],
                            [ 
                                float(item['xAxis'] + item['length'] / 2), 
                                float(item['yAxis'] + item['width'] / 2) 
                            ],
                            [ 
                                float(item['xAxis'] + item['length'] / 2), 
                                float(item['yAxis'] - item['width'] / 2) 
                            ],
                            [ 
                                float(item['xAxis'] - item['length'] / 2), 
                                float(item['yAxis'] - item['width'] / 2) 
                            ],
                        ]
                    ]
                }
            }
            center_item_reformat = {
                'type': 'Feature',
                'id': 'C-%s' % item['id'],
                'properties': {
                    'name': 'C-%s' % item['name'],
                },
                'geometry': {
                    'type': 'Point',
                    'coordinates': [
                        float(item['xAxisCenter']), float(item['yAxisCenter']), float(item['zAxisCenter'])
                    ]
                }
            }
            data_item_reformat = {
                'name': item['name'],
                'type': item['type'],
                'length': float(item['length']),
                'width': float(item['width']),
                'height': float(item['height']),
                'comment': item['comment'],
            }
            bunker_res_reformat.append(bunker_item_reformat)
            center_res_reformat.append(center_item_reformat)
            data_res_reformat.append(data_item_reformat)
        res_reformat = {
            'bunker': bunker_res_reformat,
            'center': center_res_reformat,
            'data': data_res_reformat,
        }
        finalResponse = copy.deepcopy(res_reformat)
    if formatName == 'GeoJSON-warehouse':
        res = copy.deepcopy(originalResponse)
        res_reformat = {}
        warehouse_res_reformat = [
        {
            'type': 'Feature',
            'id': res[0]['id'],
            'properties': {
                'name': res[0]['id'],
                'address': res[0]['address'],
                'length': float(res[0]['length']),
                'width': float(res[0]['width']),
                'height': float(res[0]['height']),
                'maxHeight': float(res[0]['maxHeight']),
                'comment': res[0]['comment'],
            },
            'geometry': {
                'type': 'Polygon',
                'coordinates': [[
                    [0, 0],
                    [float(res[0]['length']), 0],
                    [float(res[0]['length']), float(res[0]['width'])],
                    [0, float(res[0]['width'])],
                    [0, 0],
                ]]
            }
        }]
        res_reformat = {
            'warehouse': warehouse_res_reformat,
        }
        finalResponse = copy.deepcopy(res_reformat)
    if formatName == 'user':
        res = copy.deepcopy(originalResponse)
        res_reformat = []
        for item in res:
            item_reformat = {
                'id': item['id'],
                'username': item['username'],
                'isFullAuthority': item['is_full_authority'],
                'authorities': item['authorities'],
                'phone': item['phone'],
                'email': item['email'],
                'isActive': item['is_active'],
            }
            res_reformat.append(item_reformat)
        finalResponse = copy.deepcopy(res_reformat)
    return finalResponse