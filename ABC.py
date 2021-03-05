from collections import namedtuple


class Node(namedtuple('node', 'name inner_ip outer_ip online_time')):
    pass
