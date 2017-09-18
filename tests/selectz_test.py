import sys
import unittest
import multiprocessing

import selectz

class TestSelectorMethods(unittest.TestCase):

    def toUpperRead(self, client):
        return client.recv().upper()

    def test_extra_handlers_on_init(self):
        sel = selectz.Selector({
            'write': {'write': 1},
            'read': {'read': 1},
            'except':{'except': 1}
            })
        for i in sel.handlers:
            self.assertIn(i, sel.handlers[i])

    def test_register_invalid_action(self):
        sel = selectz.Selector()
        with self.assertRaises(selectz.InvalidAction):
            sel.register('feadface', None, None)

    def test_register(self):
        sel = selectz.Selector()
        r, w = multiprocessing.Pipe()
        sel.register('read', r, self.toUpperRead)
        w.send('test')
        self.assertEqual(sel.select()[0][2], 'TEST')
        w.close()
        r.close()

    def test_unregister_invalid_action(self):
        sel = selectz.Selector()
        with self.assertRaises(selectz.InvalidAction):
            sel.unregister('feadface', None)

    def test_unregister(self):
        sel = selectz.Selector()
        r, w = multiprocessing.Pipe()
        sel.register('read', r, self.toUpperRead)
        w.send('test')
        self.assertEqual(sel.select()[0][2], 'TEST')
        sel.unregister('read', r)
        w.send('test')
        self.assertEqual(len(sel.select(timeout=0.1)), 0)
        w.close()
        r.close()

    def test_unregister_nonexistant(self):
        selectz.Selector().unregister('read', None)

    def test_remove(self):
        sel = selectz.Selector()
        sel.register('read', sys.stdin, self.toUpperRead)
        sel.register('write', sys.stdin, self.toUpperRead)
        sel.register('except', sys.stdin, self.toUpperRead)
        for action in sel.handlers:
            self.assertIn(sys.stdin, sel.handlers[action])
        sel.remove(sys.stdin)
        for action in sel.handlers:
            self.assertNotIn(sys.stdin, sel.handlers[action])

    def test_remove_nonexistant(self):
        selectz.Selector().remove(None)

if __name__ == '__main__':
    unittest.main()
