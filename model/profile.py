from flask import Blueprint

from mongo import User

from .utils import HTTPResponse, HTTPRedirect, HTTPError, Request
from .auth import login_required

profile_api = Blueprint('profile_api', __name__)


@profile_api.route('/', methods=['GET'])
@profile_api.route('/<username>', methods=['GET'])
@login_required
def view_profile(user, username=None):
    try:
        user = user if username is None else User(username)
        data = {
            'username': user.username,
            'email': user.obj.email,
            'displayed_name': user.obj.profile.displayed_name,
            'bio': user.obj.profile.bio
        }
    except:
        return HTTPError('Profile not exist.', 404)

    return HTTPResponse('Profile exist.', data=data)


@profile_api.route('/', methods=['POST'])
@login_required
@Request.json(['bio'], vars_dict={'displayed_name': 'displayedName'})
def edit_profile(user, displayed_name, bio):
    try:
        profile = user.obj.profile

        if displayed_name is not None:
            profile['displayed_name'] = displayed_name
        elif displayed_name == "":
            profile['displayed_name'] = user.username
        if bio is not None:
            profile['bio'] = bio

        user.obj.update(profile=profile)
    except:
        return HTTPError('Upload fail.', 400)

    return HTTPResponse('Uploaded.')
