import re
import os
import socket
import time
import traceback
from datetime import datetime
from typing import List

from ABC import Node
from bearClient import BearClient


class CoreStateMachine(object):
    nodes: List[Node]

    def __init__(self, srv, bear_hook):
        self.nodes = list()
        self.re_routing_table = r"^ROUTING_TABLE,(.*?),(.*?),(.*?),"
        self.srv = srv
        self.bear = BearClient(bear_hook)
        # self.notify_online = lambda x: print(x)
        # self.notify_offline = lambda x: print(x)

    def notify_online(self, node):
        print("node online :", node)
        self.bear.notify_node(node, is_online=True)
        pass

    def notify_offline(self, node):
        print("node offline :", node)
        self.bear.notify_node(node, is_online=False)
        pass

    def parse_status_log(self, log_str):
        node_list_now = []
        something_change = False
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
                    node_list_now.append(node)
                    pass
            pass
        for i in self.nodes:
            still_online = False
            for j in node_list_now:
                if i.inner_ip == j.inner_ip:
                    still_online = True
                    break
                    pass
                pass
            if not still_online:
                self.notify_offline(i)
                something_change = True
        for j in node_list_now:
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
        self.nodes = node_list_now
        if something_change:
            self.bear.notify_all_online_nodes_markdown(self.nodes)

    def main_loop(self):
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(self.srv)
                data = s.recv(2048).decode()
                # print(data)
                s.send("status\n".encode())
                status_log = ""
                while True:
                    rbuf = s.recv(40960).decode()
                    status_log += rbuf
                    if len(rbuf) > 3:
                        if rbuf[-5:] == "END\r\n":
                            break
                # print(status_log)
                self.parse_status_log(status_log)
            except Exception as e:
                traceback.print_exc()
            time.sleep(1)
        pass


if __name__ == '__main__':
    srv_host = os.getenv("OV_HOST", "127.0.0.1")
    srv_port = int(os.getenv("OV_TEL_PORT", "7505"))
    bear_hook = os.getenv("BEAR_HOOK", "test")
    print(srv_host, srv_port)
    print(bear_hook)
    csm = CoreStateMachine(srv=(srv_host, srv_port),
                           bear_hook=bear_hook)
    csm.main_loop()
