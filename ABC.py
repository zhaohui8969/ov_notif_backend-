from collections import namedtuple
import datetime

class Node(namedtuple('node', 'name inner_ip outer_ip online_time')):
    pass

def node_to_dict(node:Node):
    return {
        'name':node.name,
        'inner_ip':node.inner_ip,
        'outer_ip':node.outer_ip,
        'online_time': node.online_time.strftime("%Y-%m-%d %H:%M:%S")
    }