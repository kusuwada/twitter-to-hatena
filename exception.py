#!/usr/bin/env python3
# -*- coding:utf-8 -*-

class RequestExceededError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
