# from flask import make_response, jsonify
# from werkzeug.exceptions import abort
from pymysql.constants import ER


def err(status=None, errcode=None, msg=None, data=None):
    return dict(status=status, errcode=errcode, msg=msg, data=data)


DEFAULT_ERROR = err(500, 99999, 'InternalServerError')
UNKNOWN_ERROR = err(500, 99999, 'UNKNOWN_ERROR')
NOTFOUND_ERROR = err(404, 99999, 'NOTFOUND_ERROR')

LOGIN_FAILED = err(401, 20001, 'LOGIN_FAILED')
NOITEM_ERROR = err(202, 20002, 'DatabaseNoTargetItem')
INSERT_FAILED = err(202, 20003, 'DatabaseInsertFailed')
UPDATE_FAILED = err(202, 20004, 'DatabaseUpdateFailed')
DELETE_FAILED = err(202, 20005, 'DatabaseDeleteFailed')

NO_TARGET_TASK = err(202, 20006, 'NoTargetTaskInDatabase')
CANNOT_DO_OPERATION = err(202, 20007, 'CannotDoOperationToTask')
TASK_INFO_ERROR = err(202, 20008, 'TaskInfoError')

EMPTY_INPUT = err(403, 20010, 'EMPTY_INPUT')

TOKEN_EXPIRED = err(401, 20011, 'TOKEN_EXPIRED')
NO_CURRUSER = err(403, 20012, 'NO_CURRUSER')
WRONG_PASSWORD =  err(403, 20013, 'WRONG_PASSWORD')
TOKEN_INVAILD = err(401, 20014, 'TOKEN_INVAILD')
TOKEN_MISSING = err(401, 20015, 'TOKEN_MISSING')
NO_PERMISSION = err(403, 20016, 'NO_PERMISSION')
USERNAME_INVAILD = err(403, 20017, 'USERNAME_INVAILD')
WRONG_PHONE = err(403, 20018, 'WRONG_PHONE')
WRONG_USERID = err(403, 20019, 'WRONG_USERID')

DATABASE_ERROR = {}
for error in dir(ER):
    if isinstance(error, str) and error[0] != '_':
        DATABASE_ERROR = {**DATABASE_ERROR, **{ getattr(ER, error): err(403, '3%s' % getattr(ER, error), error) }}

def errordict(err_detail=None, query=None, data=None):
    if err_detail is None:
        err_detail = DEFAULT_ERROR
    else:
        if query is not None:
            err_detail['query'] = query
        if data is not None:
            err_detail['data'] = data
    return err_detail

# def error(err_detail=None, query=None, data=None):
#     if err_detail is None:
#         err_detail = DEFAULT_ERROR
#     else:
#         if query is not None:
#             err_detail['query'] = query
#         if data is not None:
#             err_detail['data'] = data
#     abort(make_response(jsonify(err_detail), err_detail['status']))