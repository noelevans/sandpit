def identity_decorator(fn):
    def wrapper(*args):
        return fn(*args)
    return wrapper


@identity_decorator
def stringify(obj):
    return str(obj)


print(stringify(78))


def uppercase(fn):
    def wrapper(*args):
        result = fn(*args)
        return result.upper()
    return wrapper


@uppercase
def stringify(obj):
    return str(obj)


print(stringify('Hello'))


def cache(fn):
    c = {}
    def wrapper(*args):
        if args in c:
            return c[args]
        result = fn(*args)
        c[args] = result
        return result
    return wrapper


@cache
def fibonacci(n):
    print('Calculating fibonacci({})'.format(n))
    if n == 1:
        return 1
    return n * fibonacci(n - 1)


print(fibonacci(4))
print(fibonacci(5))
