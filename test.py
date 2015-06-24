#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from PyQt5.QtCore import (Qt, QAbstractListModel, QVariant, QModelIndex,
                          QSortFilterProxyModel, QSize)
from PyQt5.QtGui import QColor, QFont

from modeltest import ModelTest
import random


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
        elif role in [Qt.ToolTipRole, Qt.StatusTipRole, Qt.WhatsThisRole]:
            return "foobar"
        elif role == Qt.SizeHintRole:
            return QSize()
        elif role == Qt.FontRole:
            return QFont()
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignLeft
        elif role in [Qt.BackgroundColorRole, Qt.TextColorRole]:
            return QColor()
        elif role == Qt.CheckStateRole:
            return Qt.Checked
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

    def setData(self, index, value, role):
        if index.isValid() and role == Qt.EditRole:
            self._storage[index.row()] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def sorted(self):
        proxy_model = QSortFilterProxyModel(self)
        proxy_model.setSourceModel(self)
        proxy_model.setDynamicSortFilter(True)
        proxy_model.sort(0)
        return proxy_model


def run():
    model = DummyModel()

    # pass the model to ModelTest, it will automatically trigger recheck on
    # every model change; note that it must be assigned to variable to avoid gc
    modeltest = ModelTest(model, verbose=False)

    assert model.rowCount() == 0
    assert len(model._storage) == 0

    element_count = 15

    # insert and remove at the beginning
    for i in range(element_count):
        model.insertRows(0, i, None)

    assert model.rowCount() == sum(range(element_count))
    assert len(model._storage) == sum(range(element_count))

    for i in range(element_count):
        model.removeRows(0, i, None)

    assert model.rowCount() == 0
    assert len(model._storage) == 0

    # insert and remove from the end
    for i in range(element_count):
        model.insertRows(model.rowCount(), i, None)

    assert model.rowCount() == sum(range(element_count))
    assert len(model._storage) == sum(range(element_count))

    for i in range(element_count):
        model.removeRows(model.rowCount() - i, i, None)

    assert model.rowCount() == 0
    assert len(model._storage) == 0

    # assign random data
    random_data = list(range(element_count))
    random.shuffle(random_data)
    model.insertRows(0, len(random_data), None)

    for i, n in enumerate(random_data):
        model.setData(model.index(i), n, Qt.EditRole)
        # assert that all upto i are assigned and rest are empty strings
        for j in range(i + 1):
            assert model.data(model.index(j), Qt.DisplayRole) == random_data[j]
        for j in range(i + 1, len(random_data)):
            assert model.data(model.index(j), Qt.DisplayRole) == ""

    # derived model sorted by default
    sorted_model = model.sorted()
    assert sorted_model.rowCount() == len(random_data)

    sorted_model_data = []
    for i, n in enumerate(sorted(random_data)):
        assert sorted_model.data(sorted_model.index(i, 0), Qt.DisplayRole) == n
        sorted_model_data.append(n)
    assert sorted_model_data == sorted(random_data)

    # inserting rows reflected in derived model
    old_len = model.rowCount()
    model.insertRows(0, 1, None)
    assert sorted_model.rowCount() == old_len + 1
    assert sorted_model.data(sorted_model.index(0, 0), Qt.DisplayRole) == ""

    # element should be at the beginning even though it was added to the end
    model.insertRows(model.rowCount(), 1, None)
    assert sorted_model.rowCount() == old_len + 2
    assert sorted_model.data(sorted_model.index(0, 0), Qt.DisplayRole) == ""

    # changing row value reflected in derived model
    model.setData(model.index(0), 1234, Qt.EditRole)
    assert sorted_model.data(sorted_model.index(model.rowCount() - 1, 0),
                             Qt.DisplayRole) == 1234
    model.setData(model.index(model.rowCount() - 1), -3, Qt.EditRole)
    assert sorted_model.data(sorted_model.index(0, 0), Qt.DisplayRole) == -3

if __name__ == '__main__':
    run()
