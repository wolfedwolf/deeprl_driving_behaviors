# -*- coding: utf-8 -*-
"""
@file    __init__.py
@author  Michael Behrisch
@author  Jakob Erdmann
@date    2011-06-23
@version $Id: __init__.py 23999 2017-04-21 09:04:47Z behrisch $

Python interface to SUMO especially for parsing output files.

SUMO, Simulation of Urban MObility; see http://sumo.dlr.de/
Copyright (C) 2011-2017 DLR (http://www.dlr.de/) and contributors

This file is part of SUMO.
SUMO is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""
from __future__ import print_function
from __future__ import absolute_import
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from . import dump, inductionloop, convert
from sumolib.xml import *


class AbstractHandler__byID(ContentHandler):

    def __init__(self, element_name, idAttr, attributes):
        self._element_name = element_name
        self._attributes = attributes
        self._idAttr = idAttr
        self._values = {}

    def startElement(self, name, attrs):
        if name != self._element_name:
            return
        cid = float(attrs[self._idAttr])
        self._values[cid] = {}
        if self._attributes:
            for a in self._attributes:
                self._values[cid][a] = float(attrs[a])
        else:
            for a in attrs.keys():
                if a != self._idAttr:
                    self._values[cid][a] = float(attrs[a])


class AbstractHandler__asList(ContentHandler):

    def __init__(self, element_name, attributes):
        self._element_name = element_name
        self._attributes = attributes
        self._values = []

    def startElement(self, name, attrs):
        if name != self._element_name:
            return
        tmp = {}
        if self._attributes:
            for a in self._attributes:
                try:
                    tmp[a] = float(attrs[a])
                except:
                    tmp[a] = attrs[a]
        else:
            for a in attrs.keys():
                try:
                    tmp[a] = float(attrs[a])
                except:
                    tmp[a] = attrs[a]
        self._values.append(tmp)


def parse_sax(xmlfile, handler):
    myparser = make_parser()
    myparser.setContentHandler(handler)
    myparser.parse(xmlfile)


def parse_sax__byID(xmlfile, element_name, idAttr, attrnames):
    h = AbstractHandler__byID(element_name, idAttr, attrnames)
    parse_sax(xmlfile, h)
    return h._values


def parse_sax__asList(xmlfile, element_name, attrnames):
    h = AbstractHandler__asList(element_name, attrnames)
    parse_sax(xmlfile, h)
    return h._values


def toList(mapList, attr):
    ret = []
    for a in mapList:
        ret.append(a[attr])
    return ret


def prune(fv, minV, maxV):
    if minV is not None:
        for i, v in enumerate(fv):
            fv[i] = max(v, minV)
    if maxV is not None:
        for i, v in enumerate(fv):
            fv[i] = min(v, maxV)
