#!/usr/bin/env python -tt -u

from flask import Flask, request, json
import uuid
import redis
import json


app = Flask(__name__)
r = redis.StrictRedis(host='redis', port=6379, db=0)

@app.route(u'/upload', methods=['POST', 'PUT'])
def api_upload():
    if request.headers['Content-Type'] != 'application/json':
        return "Unsupported Media Type", 415
    elif len(request.json['tempurl']) == 0:
        return "tempurl cannot be null", 415
    elif len(request.json['data']) == 0:
        return "415 data cannot be null", 415
    else:
        contents = request.json
        ttl = contents['ttl'] if 'ttl' in contents else 3600

        r.setex(
            contents['tempurl'],
            ttl,
            contents['data']
        )
        return "OK", 200


@app.route(u'/download', methods=['GET'])
def api_download():
    if request.headers['Content-Type'] != 'application/json':
        return "Unsupported Media Type", 415
    elif len(request.json['tempurl']) == 0:
        return "tempurl cannot be null", 415
    else:
        contents = request.json
        data = r.get(contents['tempurl'])
        r.delete(contents['tempurl'])
        if data:
            return data, 200
        else:
            return 404


if __name__ == "__main__":
    # add the handlers to the console for local debug
    app.debug = True
    app.run(host="0.0.0.0", port=6222)