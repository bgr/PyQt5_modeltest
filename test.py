#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import random

from PyQt5.QtCore import Qt, QAbstractListModel, QVariant, pyqtSlot, QModelIndex

from modeltest import ModelTest


class DummyModel(QAbstractListModel):

    ROLES = ('hello',)
    _ROLE_MAP = {}

    def __init__(self, parent=None):
        self._init_roles()
        self._items = []
        super(DummyModel, self).__init__(parent)

    def _init_roles(self):
        keys = list(range(Qt.UserRole + 1, Qt.UserRole + 1 + len(self.ROLES)))
        self._ROLE_MAP = dict(list(zip(keys, self.ROLES)))

    def roleNames(self):
        return self._ROLE_MAP

    @pyqtSlot(QModelIndex, result=int)
    def rowCount(self, parent=None):
        #if parent is None or not parent.isValid():
            #return 0
        return len(self._items)

    #@pyqtSlot(QModelIndex, result=bool)
    #def hasChildren(self, parent=None):
        #return self.rowCount(parent) > 0

    def data(self, index, role):
        # sanity checks
        if not index.isValid():
            return QVariant()

        if role not in self._ROLE_MAP:
            return QVariant()

        # get item & value
        #attr = self._ROLE_MAP[role]
        #item = self._items[index.row()]
        #value = getattr(item, attr)
        #return value
        return self._items[index.row()]

    @pyqtSlot(int)
    def add_random_items(self, n):
        self.beginInsertRows(
            QModelIndex(), self.rowCount(), self.rowCount() + n - 1)
        self._items.extend([random.randint(1, 100) for _ in range(n)])
        self.endInsertRows()


def run():
    model = DummyModel()
    modeltest = ModelTest(model)  # will trigger recheck on every model change

    model.add_random_items(5)


if __name__ == '__main__':
    run()
