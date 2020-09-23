# -*- coding: utf-8 -*-
"""Library to write data pipelines to load a data nugflow.

Here is some introductory material for learning more about the `Data Vault
Modeling`_ methodology.

Todo:
    * Write an example method below.
    * Write more docs :).

Example:
    An example is part of the Todo

        >>> python nugflow.py  # TODO

Attributes:
    __version__ (str): We have adopted `Versioneer`_ to manage project versioning.
        Read more about the :doc:`versioning strategy here <../readme>`.

.. _Data Vault Modeling:
   https://en.wikipedia.org/wiki/Data_vault_modeling
.. _Versioneer:
    https://github.com/warner/python-versioneer
"""

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
