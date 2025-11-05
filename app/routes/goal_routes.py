from flask import Blueprint,request,make_response,abort,Response
from ..models.goal import Goal
from ..models.task import Task
from .routes_utilities import validate_model, create_model, get_model_with_filters
from ..db import db

bp = Blueprint("goal_bp",__name__,url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)


# @goal_bp.post("/<goal_id>/tasks")
# def create_task_with_goal(goal_id):
#     goal = validate_model(Goal, goal_id)

#     request_body = request.get_json()
#     request_body["goal_id"] = goal.id

#     return  create_model(Task, request_body)



@bp.get("")
def get_all_goals():
    return get_model_with_filters(Goal, request.args)
    # query = db.select(Goal)

    # goals = db.session.scalars(query)
    # result_list = []
    # for goal in goals:
    #     result_list.append(goal.to_dict())
    
    # return result_list


@bp.get("/<id>")
def get_one_goal(id):
    goal = validate_model(Goal, id)
    goal_dict = goal.to_dict()
    return goal_dict


@bp.get("/<id>/tasks")
def get_all_tasks_with_one_goal(id):
    goal = validate_model(Goal, id)
    goal_dict = goal.to_dict()
    goal_dict["tasks"] = [task.to_dict() for task in goal.tasks]
    
    return goal_dict

@bp.put("/<id>")
def replace_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.post("/<goal_id>/tasks")
def match_tasks_with_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    query = db.select(Task).where(Task.goal_id == goal_id)
    old_tasks = db.session.scalars(query)
    for old_task in old_tasks:
        old_task.goal_id = None

    request_body = request.get_json()
    ids = request_body["task_ids"]

    for id in ids:
        task = validate_model(Task, id)
        task.goal_id = goal_id
        db.session.commit()
    
    request_body["id"] = goal.id
    
    return request_body
        
    




@bp.delete("/<id>")
def delete_goal(id):
    goal = validate_model(Goal, id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")