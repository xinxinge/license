#!/usr/bin/env python3
'''
功能: APP入口
'''
import sys
import os
import logging
import yaml
from flask import Flask, request
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from resource import *
from common.route import ROUTES

from app import app, api, db

for route in ROUTES.routedict.values():
    api.add_resource(route['class'], route['url'], methods=route['methods'])

if __name__ == '__main__':
    app.run(host='0.0.0.0')

