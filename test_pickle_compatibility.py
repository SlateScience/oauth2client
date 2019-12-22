# -- encoding: utf-8
from __future__ import unicode_literals, print_function
import pickle
from six import PY2


class A(object):
    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c

    def __eq__(self, other):
        return (
            isinstance(other, A) and
            (self.a, self.b, self.c) == (other.a, other.b, other.c)
        )


def main():
    # We include three types of strings:
    # - A simple ASCII string (as bytes)
    # - A Unicode string
    # - A bytes string which is not valid UTF-8
    py2def = A(b'py2 default', 'תוים מעניינים', b'\xd7d')
    py2pro2 = A(b'py2 protocol 2', 'תוים מעניינים', b'\xd7d')
    py3pro2 = A(b'py3 protocol 2', 'תוים מעניינים', b'\xd7d')

    if PY2:
        try:
            f = open('py2-default.pickle')
        except IOError:
            print('Py2 default not there, creating')
            with open('py2-default.pickle', 'w') as f:
                pickle.dump(py2def, f)
        else:
            print('Py2 default found, verifying')
            with f:
                loaded = pickle.load(f)
                assert py2def == loaded

        try:
            f = open('py2-protocol2.pickle')
        except IOError:
            print('Py2 protocol2 not there, creating')
            with open('py2-protocol2.pickle', 'w') as f:
                pickle.dump(py2pro2, f, protocol=2)
        else:
            print('Py2 protocol2 found, verifying')
            with f:
                loaded = pickle.load(f)
                assert py2pro2 == loaded

        try:
            f = open('py3-protocol2.pickle')
        except IOError:
            print('Py3 protocol2 not found, I am python 2, skipping')
        else:
            print('Py3 protocol2 found, verifying')
            with f:
                loaded = pickle.load(f)
                assert py3pro2 == loaded
    else:
        try:
            f = open('py2-default.pickle', 'rb')
        except IOError:
            print('Py2 default not there, I am python 3, skipping')
        else:
            print('Py2 default found, verifying')
            with f:
                loaded = pickle.load(f, encoding="bytes")
                d = loaded.__dict__
                for k in list(d.keys()):
                    if isinstance(k, bytes):
                        d[k.decode()] = d.pop(k)
                assert py2def == loaded

        try:
            f = open('py2-protocol2.pickle', 'rb')
        except IOError:
            print('Py2 protocol2 not there, I am python 3, skipping')
        else:
            print('Py2 protocol2 found, verifying')
            with f:
                loaded = pickle.load(f, encoding="bytes")
                d = loaded.__dict__
                for k in list(d.keys()):
                    if isinstance(k, bytes):
                        d[k.decode()] = d.pop(k)
                assert py2pro2 == loaded

        try:
            f = open('py3-protocol2.pickle', 'rb')
        except IOError:
            print('Py3 protocol2 not found, creating')
            with open('py3-protocol2.pickle', 'wb') as f:
                pickle.dump(py3pro2, f, protocol=2)
        else:
            print('Py3 protocol2 found, verifying')
            with f:
                loaded = pickle.load(f, encoding="bytes")
                assert py3pro2 == loaded
