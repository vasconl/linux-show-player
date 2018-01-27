# -*- coding: utf-8 -*-
#
# This file is part of Linux Show Player
#
# Copyright 2012-2018 Francesco Ceruti <ceppofrancy@gmail.com>
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

from copy import deepcopy


class LiveProperty:
    """Descriptor used to define live-properties.

    Live-properties allow to manipulate parameters in a live context, without
    touching the values stored inside `Property` descriptors.

    This class doesn't implement any behavior, but it must be extended in order
    to correctly register live-properties.
    """
    def __init__(self, **meta):
        self.name = '_'
        self.meta = meta

    def __get__(self, instance, owner=None):
        pass

    def __set__(self, instance, value):
        pass


class Property:
    """Descriptor used to define properties.

    Properties allow to define "special" attributes for objects, to provide
    custom behaviors in a simple and reusable manner.

    .. warning::
        To be able to save properties into a session, the stored value
        MUST be JSON-serializable.
    """

    def __init__(self, default=None, **meta):
        self.name = '_'
        self.default = default
        self.meta = meta

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        elif self.name not in instance.__dict__:
            instance.__dict__[self.name] = deepcopy(self.default)

        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if instance is not None:
            # Only change the value if different
            if value != instance.__dict__.get(self.name, self.default):
                instance.__dict__[self.name] = value


class WriteOnceProperty(Property):
    """Property that can be modified only once.

    Obviously this is not really "write-once", but if used as normal attribute
    will ignore any change when the stored value is different from default.
    """

    def __set__(self, instance, value):
        if self.__get__(instance) == self.default:
            super().__set__(instance, value)
