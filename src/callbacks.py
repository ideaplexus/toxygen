from PySide import QtCore
from notifications import *
# TODO: add all callbacks (replace test callbacks and use wrappers)


class InvokeEvent(QtCore.QEvent):
    EVENT_TYPE = QtCore.QEvent.Type(QtCore.QEvent.registerEventType())

    def __init__(self, fn, *args, **kwargs):
        QtCore.QEvent.__init__(self, InvokeEvent.EVENT_TYPE)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs


class Invoker(QtCore.QObject):

    def event(self, event):
        event.fn(*event.args, **event.kwargs)
        return True

_invoker = Invoker()


def invoke_in_main_thread(fn, *args, **kwargs):
    QtCore.QCoreApplication.postEvent(_invoker, InvokeEvent(fn, *args, **kwargs))


def repaint_widget(widget):
    return widget.repaint


def self_connection_status(st, tox_link):
    def wrapped(tox, connection, user_data):
        print 'Connection status: ', str(connection)
        invoke_in_main_thread(repaint_widget(st))
    return wrapped


def friend_status(a, b, c, d):
    print "Friend connected! Friend's data: ", str(a), str(b), str(c)


def friend_message(a, b, c, d, e, f):
    print 'Message: ', d.decode('utf8')
    tray_notification('Message', d.decode('utf8'))


def init_callbacks(tox, window):
    """
    :param tox: tox instance
    :param window: main window
    :return: None
    """
    tox.callback_friend_status(friend_status, 0)
    tox.callback_friend_message(friend_message, 0)
    tox.callback_self_connection_status(self_connection_status(window.connection_status, tox), 0)
