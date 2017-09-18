'''
Select made easy


Register handlers with a Selector to have them executed when the read, write,
or exception condition occurs on the object.
'''
import select

class InvalidAction(Exception): pass

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
        handlers_and_clients = [(self.handlers[j[0]][i], i) for j in ready \
                for i in j[1] if i in self.handlers[j[0]]]
        return [(client, handler, handler(client)) \
                for handler, client in handlers_and_clients]
