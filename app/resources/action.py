from flask import Blueprint, jsonify, make_response

from flask import request as r

import logging

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from common import log_handler, LOG_LEVEL, \
    response_ok, response_fail, CODE_OK, CODE_BAD_REQUEST, CONSENSUS_PLUGINS, \
    CONSENSUS_MODES, CLUSTER_SIZES, request_debug, request_get

from modules import cluster_handler
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(log_handler)

action_v1 = Blueprint('action_v1', __name__, url_prefix='/{}'.format("v1"))
action_v2 = Blueprint('action_v2', __name__, url_prefix='/{}'.format("v2"))


@action_v1.route('/cluster_apply', methods=['GET'])
@action_v2.route('/cluster_apply', methods=['GET', 'POST'])
def cluster_apply():
    """
    Return a Cluster json body.
    """
    request_debug(r, logger)
    user_id = request_get(r, "user_id")
    if not user_id:
        logger.warn("cluster_apply without user_id")
        response_fail["error"] = "No user_id is given"
        response_fail["data"] = r.args
        return jsonify(response_fail), CODE_BAD_REQUEST

    consensus_plugin = request_get(r, "consensus_plugin") or CONSENSUS_PLUGINS[0]
    consensus_mode = request_get(r, "consensus_mode") or CONSENSUS_MODES[0]
    cluster_size = int(request_get(r, "size") or CLUSTER_SIZES[0])
    c = cluster_handler.apply_cluster(user_id=user_id,
                                      consensus_plugin=consensus_plugin,
                                      consensus_mode=consensus_mode,
                                      size=cluster_size)
    if not c:
        logger.warn("cluster_apply failed")
        response_fail["error"] = "No available res for " + user_id
        response_fail["data"] = {
            "user_id": user_id,
            "consensus_plugin": consensus_plugin,
            "consensus_mode": consensus_mode,
            "size": cluster_size,
        }
        return jsonify(response_fail), CODE_BAD_REQUEST
    else:
        response_ok["data"] = c
        return jsonify(response_ok), CODE_OK


@action_v1.route('/cluster_release', methods=['GET'])
@action_v2.route('/cluster_release', methods=['GET', 'POST'])
def cluster_release():
    """
    Return status.
    """
    request_debug(r, logger)
    user_id = request_get(r, "user_id")
    cluster_id = request_get(r, "cluster_id")
    if not user_id and not cluster_id:
        logger.warn("cluster_release without id")
        response_fail["error"] = "No id in release"
        response_fail["data"] = r.args
        return make_response(jsonify(response_fail), CODE_BAD_REQUEST)
    else:
        result = None
        if cluster_id:
            result = cluster_handler.release_cluster(cluster_id=cluster_id)
        elif user_id:
            result = cluster_handler.release_cluster_for_user(user_id=user_id)
        if not result:
            logger.warn("cluster_release failed user_id={} cluster_id={"
                        "}".format(user_id, cluster_id))
            response_fail["error"] = "release fail"
            response_fail["data"] = {
                "user_id": user_id,
                "cluster_id": cluster_id,
            }
            return jsonify(response_fail), CODE_BAD_REQUEST
        else:
            return jsonify(response_ok), CODE_OK


@action_v2.route('/cluster_list', methods=['POST'])
def cluster_list():
    """
    Return status.
    """
    request_debug(r, logger)
    user_id = request_get(r, "user_id")
    logger.warn("user_id={}".format(user_id))
    if not user_id:
        logger.warn("cluster_apply without user_id")
        response_fail["error"] = "No user_id is given"
        response_fail["data"] = r.args
        return jsonify(response_fail), CODE_BAD_REQUEST

    cluster_handler.list(filter_data={})

    pass
