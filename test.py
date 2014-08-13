from PyQt5.QtCore import Qt, QAbstractListModel, pyqtSlot, QVariant

from modeltest import ModelTest


class TestModel(QAbstractListModel):

    ROLES = ()
    _ROLE_MAP = {}

    def __init__(self, parent=None):
        self._init_roles()
        self._items = []
        super(TestModel, self).__init__(parent)

    def _init_roles(self):
        keys = list(range(Qt.UserRole + 1, Qt.UserRole + 1 + len(self.ROLES)))
        self._ROLE_MAP = dict(list(zip(keys, self.ROLES)))

    def roleNames(self):
        return self._ROLE_MAP

    @pyqtSlot(result=int)
    def rowCount(self, parent=None):
        return len(self._items)

    def data(self, index, role):
        #if role == Qt.DisplayRole:  # http://stackoverflow.com/a/2334179/858766
            #return index.internalPointer()

        # sanity checks
        if not index.isValid():
            return QVariant()

        if role not in self._ROLE_MAP:
            return QVariant()

        # get item & value
        attr = self._ROLE_MAP[role]
        item = self._items[index]
        value = getattr(item, attr)

        return value

model = TestModel()
modeltest = ModelTest(model)
