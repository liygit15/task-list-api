from flask import Blueprint,request,make_response,request,Response,abort
from ..models.task import Task
from ..db import db
from .routes_utilities import validate_model, create_model, slack_send_mark_complete
from sqlalchemy import asc, desc
from datetime import date
import requests
import os

bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()

    return create_model(Task, request_body)

    # try:
    #     new_task = Task.from_dict(request_body)
    # except KeyError as error:
    #     invalid = {"details": "Invalid data"}
    #     abort(make_response(invalid, 400))

    # db.session.add(new_task)
    # db.session.commit()

    # return new_task.to_dict(), 201


@bp.get("")
def get_all_task():
    # return get_model_with_filters(Task, request.args)
    query = db.select(Task)

    sorted = request.args.get("sort")
    if sorted == "asc":
        query = query.order_by(asc(Task.title))
    elif sorted == "desc":
        query = query.order_by(desc(Task.title))

    tasks = db.session.scalars(query)

    return [task.to_dict() for task in tasks]


@bp.get("/<id>")
def get_single_task(id):
    task = validate_model(Task, id)
    return Task.to_dict(task)


@bp.put("/<id>")
def replace_task(id):
    task = validate_model(Task, id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.patch("/<id>/mark_complete")
def mark_complete_task(id):
    task = validate_model(Task, id)

    task.completed_at = date.today()
    db.session.commit()

    slack_send_mark_complete(task.title)

    return Response(status=204, mimetype="application/json")

@bp.patch("/<id>/mark_incomplete")
def mark_incomplete_task(id):
    task = validate_model(Task, id)

    task.completed_at = None
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<id>")
def delete_task(id):
    task =validate_model(Task, id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")