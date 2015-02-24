#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from PyQt5.QtCore import Qt, QAbstractListModel, QVariant, QModelIndex

from modeltest import ModelTest


class DummyModel(QAbstractListModel):

    #ROLES = ('hello',)
    #_ROLE_MAP = {}

    def __init__(self, parent=None):
        self._storage = []
        super(DummyModel, self).__init__(parent)

    #def _init_roles(self):
        #keys = list(range(Qt.UserRole + 1, Qt.UserRole + 1 + len(self.ROLES)))
        #self._ROLE_MAP = dict(list(zip(keys, self.ROLES)))

    #def roleNames(self):
        #return self._ROLE_MAP

    def rowCount(self, parent=None):
        if not parent or not parent.isValid():
            return len(self._storage)
        return 0

    def data(self, index, role):
        # sanity checks
        if not index.isValid():
            return QVariant()

        if index.row() >= len(self._storage):
            return QVariant()

        if role == Qt.DisplayRole:
            return self._storage[index.row()]
        else:
            return QVariant()

    def insertRows(self, position, rows, parent_index):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for _ in range(rows):
            self._storage.insert(position, "")
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent_index):
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        for _ in range(rows):
            del self._storage[position]
        self.endRemoveRows()
        return True


def run():
    model = DummyModel()

    # pass the model to ModelTest, it will automatically trigger recheck on
    # every model change; note that it must be assigned to variable to avoid gc
    modeltest = ModelTest(model, verbose=False)

    element_count = 20

    # insert and remove at the beginning
    for i in range(element_count):
        model.insertRows(0, i, None)

    for i in range(element_count):
        model.removeRows(0, i, None)

    # insert and remove from the end
    for i in range(element_count):
        model.insertRows(model.rowCount(), i, None)

    for i in range(element_count):
        model.removeRows(model.rowCount() - i, i, None)


if __name__ == '__main__':
    run()
