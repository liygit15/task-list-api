from flask import abort, make_response
from sqlalchemy import asc, desc
from ..db import db
import os
import requests

def validate_model(cls, id):
    try:
        id = int(id)
    except ValueError:
        invalid = {"Message": f"{cls.__name__} id {id} is invalid."}
        abort(make_response(invalid, 400))

    query = db.select(cls).where(cls.id == id)
    model = db.session.scalar(query)

    if not model:
        not_fount = {"Message": f"{cls.__name__} with id {id} is not found."}
        abort(make_response(not_fount, 404))
    
    return model


def slack_send_mark_complete(task_title):
    slack_token = os.environ.get('SLACK_BOT_TOKEN')
    url = 'https://slack.com/api/chat.postMessage'
    headers = {"Authorization": f"Bearer {slack_token}"} 
    request_body = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task_title}"
        }
    
    response = requests.post(url, headers=headers, data=request_body)
    

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError as error:
        invalid = {"details": "Invalid data"}
        abort(make_response(invalid, 400))
    
    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201


def get_model_with_filters(cls, filters=None, sort=None):
    query = db.select(cls)

    if filters:
        for attribute, value in filters.items():
            if hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))
    
    if sort == "asc":
        query = query.order_by(asc(cls.title))
    elif sort == "desc":
        query = query.order_by(desc(cls.title))
    else:
        query = query.order_by(cls.id)
    
    models = db.session.scalars(query)
    models_response = [model.to_dict() for model in models]
    return models_response



#  Do I need a helper function to reduce the repeated part of patch in task_routes.py 
# def update_complete_time(cls,complete_time):
#     cls.completed_at = complete_time

#     db.session.commit()

#     return Response(status=204, mimetype="application/json")
