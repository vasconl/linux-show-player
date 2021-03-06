# -*- coding: utf-8 -*-
#
# This file is part of Linux Show Player
#
# Copyright 2012-2016 Francesco Ceruti <ceppofrancy@gmail.com>
#
# Linux Show Player is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Linux Show Player is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Linux Show Player.  If not, see <http://www.gnu.org/licenses/>.

from lisp.core.actions_handler import MainActionsHandler
from lisp.core.memento_model_actions import AddItemAction, RemoveItemAction, \
    MoveItemAction
from lisp.core.proxy_model import ReadOnlyProxyModel


class MementoModel(ReadOnlyProxyModel):
    """ProxyModel that allow to register models changes in an ActionHandler

    The changes (add/remove) of the base model are registered as actions that
    can be undone/redone.
    If no handler is specified the MainActionHandler is used.

    ..note::
        The methods, locks and unlock, allow to avoid reentering when an action
        is undone/redone.
    """

    def __init__(self, model, handler=None):
        super().__init__(model)

        if handler is None:
            handler = MainActionsHandler

        self._handler = handler
        self._locked = False

    def _item_added(self, item):
        if not self._locked:
            self._handler.do_action(AddItemAction(self, self.model, item))

    def _item_removed(self, item):
        if not self._locked:
            self._handler.do_action(RemoveItemAction(self, self.model, item))

    def lock(self):
        self._locked = True

    def unlock(self):
        self._locked = False

    def _model_reset(self):
        """Reset cannot be reverted"""


class AdapterMementoModel(MementoModel):
    """Extension of the MementoModel that use a ModelAdapter as a base-model"""

    def __init__(self, model_adapter, handler=None):
        super().__init__(model_adapter, handler)
        self.model.item_moved.connect(self._item_moved)

    def _item_moved(self, old_index, new_index):
        if not self._locked:
            self._handler.do_action(MoveItemAction(self, self.model, old_index,
                                                   new_index))
