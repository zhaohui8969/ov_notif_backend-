from datetime import datetime
from typing import List

import requests

from ABC import Node


class BearClient(object):
    def __init__(self, hook):
        self.hook = hook
        self.s = requests.Session()

    def send(self, data_dict):
        req = self.s.post(self.hook, json=data_dict)
        if req.status_code != 200:
            print(req)
        pass

    def notify_node(self, node: Node, is_online: bool):
        title = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
        title += "设备接入" if is_online else "设备下线"
        self.send({
            "text": title,
            "attachments": [
                {
                    "title": "内部IP",
                    "text": node.inner_ip,
                    "color": "#ffa500"
                },
                {
                    "title": "内部名称",
                    "text": node.name,
                    "color": "#00ff40"
                },
                {
                    "title": "接入设备公网IP",
                    "text": node.outer_ip,
                    "color": "#0040ff"
                }
            ]
        })

    def notify_all_online_nodes_attachments(self, node_list: List[Node]):
        title = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
        title += "当前在线设备"
        attachments = []
        for node in node_list:
            attachments += [
                {
                    "title": "内部IP",
                    "text": node.inner_ip,
                    "color": "#ffa500"
                },
                {
                    "title": "内部名称",
                    "text": node.name,
                    "color": "#00ff40"
                },
                {
                    "title": "接入设备公网IP",
                    "text": node.outer_ip,
                    "color": "#0040ff"
                }
            ]
        self.send({
            "text": title,
            "attachments": attachments
        })
        pass

    def notify_all_online_nodes_markdown(self, node_list: List[Node]):
        title = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
        title += "当前在线设备\n---"
        table = "---\n".join(["名称:{}\n内网:{}\n外网:{}\n".format(i.name, i.inner_ip, i.outer_ip) for i in node_list])
        text = "{}\n{}".format(title, table)
        print(text)
        self.send({
            "text": text
        })

    pass


if __name__ == '__main__':
    client = BearClient(r'https://hook.bearychat.com/=bwGiZ/incoming/1c5c53191dbb9371f29eda1004719f03')
    # client.send()
    nodes = [
                Node(inner_ip="10.8.0.1",
                     name="test",
                     outer_ip="142.123.112.12",
                     online_time=datetime.now())
            ] * 3
    client.notify_all_online_nodes_markdown(nodes)
    pass
