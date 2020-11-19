import inspect
import rlcompleter


class Klass:
    name = 'klass'
    value = 2

    def __getitem__(self, key):
        return self.name[key]

    def foo(self):
        # return self[self.value]
        namespace = inspect.currentframe().f_locals
        completer = rlcompleter.Completer(namespace)
        print(completer.complete('self[ self.', 0))
        print(completer.complete('self[self.', 0))
        print(completer.complete('self[se', 0))
        print(completer.complete('sel', 0))
        print(completer.complete('self.', 0))


if __name__ == '__main__':
    Klass().foo()
