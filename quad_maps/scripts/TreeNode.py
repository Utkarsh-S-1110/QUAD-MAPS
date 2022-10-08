#! /usr/bin/env python3

class TreeNode:
    def __init__(self, data,box_pos = -1):
        self.data = data
        self.box_pos = box_pos
        self.children = []
        self.parent = None

    