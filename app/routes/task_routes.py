from flask import Blueprint,request,request,Response
from ..models.task import Task
from ..db import db
from .routes_utilities import validate_model, create_model, slack_send_mark_complete, get_model_with_filters#, update_complete_time
from datetime import date


bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()

    return create_model(Task, request_body)


@bp.get("")
def get_all_task():
    sort = request.args.get("sort")
    
    return get_model_with_filters(Task, sort=sort)


@bp.get("/<id>")
def get_single_task(id):
    task = validate_model(Task, id)
    return task.to_dict()


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


#  Do I need a helper function to reduce the repeated part of patch in task_routes.py 
# @bp.patch("/<id>/mark_complete")
# def mark_complete_task(id):
#     task = validate_model(Task, id)
#     response = update_complete_time(Task, date.today())

#     slack_send_mark_complete(task.title)
#     return response


# @bp.patch("/<id>/mark_incomplete")
# def mark_incomplete_task(id):
#     task = validate_model(Task, id)

#     return update_complete_time(task, None)


@bp.delete("/<id>")
def delete_task(id):
    task =validate_model(Task, id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


