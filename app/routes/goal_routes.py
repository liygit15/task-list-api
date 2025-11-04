from flask import Blueprint,request,make_response,abort,Response
from ..models.goal import Goal
from .routes_utilities import validate_model, create_model, get_model_with_filters
from ..db import db

goal_bp = Blueprint("goal_bp",__name__,url_prefix="/goals")

@goal_bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)


@goal_bp.get("")
def get_all_goals():
    return get_model_with_filters(Goal, request.args)
    # query = db.select(Goal)

    # goals = db.session.scalars(query)
    # result_list = []
    # for goal in goals:
    #     result_list.append(goal.to_dict())
    
    # return result_list


@goal_bp.get("/<id>")
def get_one_goal(id):
    goal = validate_model(Goal, id)
    goal_dict = goal.to_dict()
    return goal_dict




@goal_bp.put("/<id>")
def replace_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")


@goal_bp.delete("/<id>")
def delete_goal(id):
    goal = validate_model(Goal, id)

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")