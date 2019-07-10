import functools
import inspect


class Plugin(object):

    def __init__(self):
        self.execution_count = 0

    @functools.lru_cache()
    def first_name(self):
        self.execution_count += 1
        return 'Brian'

    def last_name(self):
        return 'Messiah'


def main():
    p = Plugin()
    print(p.first_name())
    print(p.first_name())
    print(p.execution_count)
    props = dict(inspect.getmembers(p))

    print(dir(props['first_name']))
    print(type(props['first_name']))
    print('Func: ' + str(props['first_name'].__func__))
    print(props['first_name'].__qualname__)
    print(props['first_name'].__module__)
    print(props['first_name'].__name__)
    print(props['first_name'].__annotations__)
    print(props['first_name'].__wrapped__)
    print('.')

    print(dir(props['last_name']))
    print(type(props['last_name']))
    print('Func: ' + str(props['last_name'].__func__))
    print('.')

    print(
            set(dir(props['first_name'])) - 
            set(dir(props['last_name']))
        )


if __name__ == '__main__':
    main()

