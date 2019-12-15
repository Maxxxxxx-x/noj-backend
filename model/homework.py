from flask import Blueprint, request
import jwt
from .auth import *
from mongo import User, HomeWork
from .utils import HTTPResponse, HTTPRedirect, HTTPError, Request
import os

JWT_ISS = os.environ.get('JWT_ISS')
JWT_SECRET = os.environ.get('JWT_SECRET')

__all__ = ['hw_api']

hw_api = Blueprint('hw_api', __name__)


@hw_api.route('/<course_name>', methods=['POST', 'PUT', 'DELETE', 'GET'])
@Request.json('name', 'newname', 'markdown', 'start', 'end', 'problemIds',
              'scoreboardStatus')
@login_required
def add_hw(user,
           course_name,
           name,
           newname,
           markdown,
           start,
           end,
           problemIds=[],
           scoreboardStatus=0):
    scoreboard_status = scoreboardStatus
    if request.method == 'POST':
        try:
            verify = identity_verify(2)
            homework = HomeWork.add_hw(course_name, markdown, name, start, end,
                                       problemIds, scoreboard_status)
        except FileExistsError:
            return HTTPError('homework exists in this course', 400)
        except Exception as ex:
            return (ex, 500)
        return HTTPResponse(
            'Add homework Success',
            200,
            'ok',
        )
    if request.method == 'PUT':
        try:
            verify = identity_verify(2)
            homework = HomeWork.update(course_name, markdown, name, newname,
                                       start, end, problemIds,
                                       scoreboard_status)
        except FileNotFoundError:
            return HTTPResponse('course not exist', 404)
        except FileExistsError:
            return HTTPResponse(
                'the homework with the same name exists in this course', 400,
                'err')
        except Exception as ex:
            return HTTPError(ex, 500)
        return HTTPResponse('Update homework Success', 200, 'ok')
    if request.method == 'DELETE':
        try:
            verify = identity_verify(2)
            homework = HomeWork.delete_problems(course_name, name)
        except FileNotFoundError:
            return HTTPResponse('homework not exists,unable delete', 404,
                                'err')
        except Exception as ex:
            return HTTPError(ex, 500)
        return HTTPResponse('Delete homework Success', 200, 'ok')
    if request.method == 'GET':
        try:
            homeworks = HomeWork.getHomeworks(course_name)
            data = []
            homework = {}
            for i in range(0, len(homeworks)):
                homework = {
                    "name": homeworks[i].name,
                    "markdown": homeworks[i].markdown,
                    "start": homeworks[i].duration.start,
                    "end": homeworks[i].duration.end,
                    "problemIds": homeworks[i].problem_ids,
                    "scoreboard_status": homeworks[i].scoreboard_status
                }
                if (user.role == 1):
                    homework["studentStatus"] = homeworks[i].student_status
                data.append(homework)
        except Exception as ex:
            return HTTPError(ex, 500)
        return HTTPResponse('get homeworks', 200, 'ok', data)


@hw_api.route('/get/<id>', methods=['GET'])
@login_required
def get_homework(user, id):
    try:
        homework = HomeWork.getSignalHomework(id)
    except Exception as ex:
        return HTTPError(ex, 500)
    return HTTPResponse('get homeworks',
                        200,
                        'ok',
                        data={
                            "name": homework.name,
                            "start": homework.duration.start,
                            "end": homework.duration.end,
                            "problemIds": homework.problem_ids
                        })
