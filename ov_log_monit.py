import argparse
import json
import threading
import re
import flask
import socket
import time
import traceback
from datetime import datetime
from typing import List

from flask import Flask, make_response, request
from flask_cors import CORS

from ABC import Node, node_to_dict
from bearClient import BearClient

app = Flask(__name__)

class StandardResponse(Exception):
    status_code = 200

    def __init__(
            self,
            is_success: bool = True,
            msg=None,
            status_code: int = 200,
            data=None
    ):
        Exception.__init__(self)
        if status_code is not None:
            self.status_code = status_code
        self.msg = msg
        self.data = data
        self.is_success = is_success

    def to_dict(self):
        rv = dict()
        rv["code"] = 0 if self.is_success else 1
        rv["data"] = self.data
        rv["msg"] = self.msg
        return rv


@app.errorhandler(StandardResponse)
def handle_standard_response(resp):
    resp_dict = resp.to_dict()
    result_json = json.dumps(resp_dict, ensure_ascii=False)
    response = make_response(result_json)
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    response.status_code = resp.status_code
    return response


@app.route("/status", methods=["GET"])
def get_status():
    request_data = request.json
    key = request.args.get("key")
    if key == app_key:
        data = {
            'node': [node_to_dict(i) for i in csm.nodes],
            'update_time': csm.update_time.strftime("%Y-%m-%d %H:%M:%S") if csm.update_time else None
        }
    else:
        data = {

        }
    return handle_standard_response(
        StandardResponse(
            data=data
        )
    )


class CoreStateMachine(object):
    nodes: List[Node]

    def __init__(self, srv_list, bear_hook_uri):
        self.node_list_now = []
        self.nodes = list()
        self.bear_hook_uri = bear_hook_uri
        self.re_routing_table = r"^ROUTING_TABLE,(.*?),(.*?),(.*?),"
        self.srv_list = self.parse_srv_list(srv_list)
        self.bear = None
        self.update_time = None
        if bear_hook_uri is not None:
            self.bear = BearClient(bear_hook_uri)

    @staticmethod
    def parse_srv_list(srv_list):
        srv_parsed = []
        for srv in srv_list:
            lsp = srv.split(':')
            host = lsp[0]
            port = int(lsp[1])
            srv_parsed.append((host, port))
        return srv_parsed

    def notify_online(self, node):
        print("node online :", node)
        if self.bear is not None:
            self.bear.notify_node(node, is_online=True)

    def notify_offline(self, node):
        print("node offline :", node)
        if self.bear is not None:
            self.bear.notify_node(node, is_online=False)
        pass

    def parse_status_log(self, log_str):
        for line in log_str.split("\n"):
            matches = list(re.finditer(self.re_routing_table, line, re.MULTILINE))
            if len(matches) > 0:
                pass
                for matchNum, match in enumerate(matches, start=1):

                    # print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum,
                    #                                                                     start=match.start(),
                    #                                                                     end=match.end(),
                    #                                                                     match=match.group()))
                    #
                    # for groupNum in range(0, len(match.groups())):
                    #     groupNum = groupNum + 1
                    #
                    #     print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
                    #                                                                     start=match.start(groupNum),
                    #                                                                     end=match.end(groupNum),
                    #                                                                     group=match.group(groupNum)))
                    node = Node(inner_ip=match.group(1),
                                name=match.group(2),
                                outer_ip=match.group(3),
                                online_time=datetime.now())
                    # print(node)
                    if 'C' in node.inner_ip or '/' in node.inner_ip:
                        continue
                    self.node_list_now.append(node)

    def check_node_state_change_and_notify(self):
        self.update_time = datetime.now()
        something_change = False
        for i in self.nodes:
            still_online = False
            for j in self.node_list_now:
                if i.inner_ip == j.inner_ip:
                    still_online = True
                    break
                    pass
                pass
            if not still_online:
                self.notify_offline(i)
                something_change = True
        for j in self.node_list_now:
            is_old = False
            for i in self.nodes:
                if i.inner_ip == j.inner_ip:
                    is_old = True
                    break
                    pass
                pass
            if not is_old:
                self.notify_online(j)
                something_change = True
        self.nodes = self.node_list_now
        if something_change:
            if self.bear is not None:
                self.bear.notify_all_online_nodes_markdown(self.nodes)
        pass

    @staticmethod
    def read_status(srv):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(srv)
        # data = s.recv(2048).decode()
        # print(data)
        s.send("status\n".encode())
        status_log = ""
        while True:
            rbuf = s.recv(40960).decode()
            status_log += rbuf
            if len(rbuf) > 3:
                if rbuf[-5:] == "END\r\n":
                    break
        return status_log

    def main_loop(self):
        while True:
            try:
                self.node_list_now = []
                for srv in self.srv_list:
                    status_log = self.read_status(srv)
                    # print(status_log)
                    self.parse_status_log(status_log)
                self.check_node_state_change_and_notify()
            except Exception as ignore:
                traceback.print_exc()
            time.sleep(1)
        pass


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bear_hook', type=str, help="bearychat api hook URI", default=None)
    parser.add_argument('--port', default="7789")
    parser.add_argument('--host', default="0.0.0.0")
    parser.add_argument('--app_key', default="whoami")
    parser.add_argument('--openvpn_service_list', type=str, nargs='+', default=[])
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()
    print(args)
    bear_hook = args.bear_hook
    openvpn_service_list = args.openvpn_service_list
    global csm
    global app_key
    app_key = args.app_key
    csm = CoreStateMachine(srv_list=openvpn_service_list,
                           bear_hook_uri=bear_hook)
    threading.Thread(target=csm.main_loop).start()
    CORS(app)
    app.run(port=args.port, host=args.host, debug=False, threaded=True)
