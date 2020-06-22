import pdb
import rlcompleter

# These do not tab complete
# instance[self.
# instance[sel


class Person:
    name = "Noel"
    idx = 2

    def __getitem__(self, key):
        return self.name[key]

    def do_something(self):
        p1 = Person()
        print(p1[self.idx % len(self.name)])
        # Test with
        # p1[self.
        pdb.set_trace()


pn = Person()
pn.do_something()

