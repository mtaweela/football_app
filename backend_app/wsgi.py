import json


def application(env, start_response):
    start_response("200 OK", [("Content-Type", "application/json")])

    response_body = json.dumps({"hi": "hi"})
    return [bytes(response_body, "utf-8")]
