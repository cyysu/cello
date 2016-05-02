import logging
import os
import sys

from flask import Blueprint, render_template, request

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import log_handler, LOG_LEVEL

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)

from modules import cluster_handler

index = Blueprint('index', __name__)


@index.route('/', methods=['GET'])
@index.route('/admin', methods=['GET'])
@index.route('/index', methods=['GET'])
def show():
    logger.info("/clusters action=" + request.method)
    cluster_active = len(list(cluster_handler.list()))
    cluster_released = len(list(cluster_handler.list(collection="released")))

    #return render_template("test.html")
    return render_template("index.html", cluster_active=cluster_active,
                           cluster_released=cluster_released)
