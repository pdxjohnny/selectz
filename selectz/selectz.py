'''
Select made easy


Register handlers with a Selector to have them executed when the read, write,
or exception condition occurs on the object.
'''
import select

class InvalidAction(Exception): pass

class WantRemove(Exception):

    def __init__(self, sock=None):
        self.sock = sock

class WantRegister(Exception):

    def __init__(self, sock=None, handler=None):
        self.action = self.__class__.__name__.lower().replace('want', '')
        self.handler = handler
        self.sock = sock

class WantRead(WantRegister): pass

class WantWrite(WantRegister): pass

class Selector(object):
    '''
    Keeps track of handlers for events.
    '''

    def __init__(self, handlers={}):
        '''
        Initializes handlers structure.
        '''
        super().__init__()
        self.handlers = {'write': {}, 'read': {}, 'except': {}}
        self.handlers.update(handlers)

    def register(self, action, sock, handler):
        '''
        Register a handler for an action on a socket. When select.select()
        tells us that the specified action is ready on the socket that handler
        will be run.

        Example:

        >>> import selectz, multiprocessing
        >>> sel = selectz.Selector()
        >>> def read(client):
        ...     return client.recv().upper()
        ...
        >>> r, w = multiprocessing.Pipe()
        >>> sel.register('read', r, read)
        >>> w.send('test')
        >>> sel.select()
        [(<multiprocessing.connection.Connection object at 0x7f0e4851a4e0>,
            <function read at 0x7f0e485d8e18>, 'TEST')]
        '''
        action = action.lower()
        if action not in self.handlers:
            raise InvalidAction('handlers has no \'{}\' action'.format(action))
        self.handlers[action][sock] = handler

    def unregister(self, action, sock):
        '''
        Unregister a handler for a previously registered action. The handler
        will no longer be called when the action is triggered via select().

        Example:

        >>> import selectz, multiprocessing
        >>> sel = selectz.Selector()
        >>> def read(client):
        ...     return client.recv().upper()
        ...
        >>> r, w = multiprocessing.Pipe()
        >>> sel.register('read', r, read)
        >>> w.send('test')
        >>> sel.select()
        [(<multiprocessing.connection.Connection object at 0x7f0e4851a4e0>,
            <function read at 0x7f0e485d8e18>, 'TEST')]
        >>> sel.unregister('read', r)
        >>> w.send('test')
        >>> sel.select(timeout=0.1)
        >>> # After 0.1 seconds it times out because there was no read handler.
        '''
        action = action.lower()
        if action not in self.handlers:
            raise InvalidAction('handlers has no \'{}\' action'.format(action))
        if action in self.handlers and sock in self.handlers[action]:
            del self.handlers[action][sock]

    def remove(self, sock):
        '''
        Unregister all handlers associated with a socket.
        '''
        for action in self.handlers:
            if sock in self.handlers[action]:
                del self.handlers[action][sock]

    def select(self, timeout=None):
        '''
        Call select and call and handlers for the actions which are ready.

        See register() for example.
        '''
        r, w, e = select.select(
                [k for k, v in self.handlers['read'].items()],
                [k for k, v in self.handlers['write'].items()],
                [k for k, v in self.handlers['except'].items()],
                timeout)
        ready = [('read', r), ('write', w), ('except', e)]
        handlers_and_clients = []
        for action, sockets in ready:
            for client in sockets:
                if client in self.handlers[action]:
                    if getattr(self.handlers[action][client], 'unregister',
                            False) is True:
                        self.unregister(action, client)
                    handlers_and_clients.append((self.handlers[action][client],
                        client))
        ret = []
        for handler, client in handlers_and_clients:
            try:
                ret.append((client, handler, handler(client)))
            except WantRegister as e:
                if e.sock is None: e.sock = client
                if e.handler is None: e.handler = handler
                self.register(e.action, e.sock, e.handler)
            except WantRemove as e:
                if e.sock is None: e.sock = client
                self.remove(e.sock)
        return ret
