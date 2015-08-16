import time


def safety_wrapper(func):
    
    def wrapper(x, y):
        if isinstance(x, int) and isinstance(y, int):
            return func(x, y)
        else:
            return 'Bad args!'

    return wrapper


@safety_wrapper
def add(x,y):
    return x + y

#######

def time_it(func):

    def wrapper(*arg):
        t = time.clock()
        res = func(*arg)
        print func.func_name, time.clock() - t
        return res

    return wrapper


@time_it
def slow_code(n):
    total = 0
    for i in range(n):
        total = total + i

    return total


@time_it
def highspeed_code(n):
    return sum(i for i in xrange(n))


@time_it
def very_highspeed_code(n):
    return sum(xrange(n))

#######

def accepts(types):

    def wrapper(func):

        def wrapped_f(arg):
            if any((isinstance(arg, t) for t in types)):
                return func(arg)
            else:
                return 'Bad arg - wrong type for argument: ' + str(arg)

        return wrapped_f

    return wrapper


@accepts([float])
def half(val):
    return 'The accurate value of %f / 2 = %f' % (val, val / 2)

#######

def main():

    # Add which has been wrapped to have a safety test
    print add(2, 2)
    print add('a', 2)
    print

    n = 10000000
    print slow_code(n)
    print highspeed_code(n)
    print very_highspeed_code(n)
    print

    print half(5.0)
    print half(5)


if __name__ == '__main__':
    main()