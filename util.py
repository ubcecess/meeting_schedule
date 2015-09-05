import os


def get_ical_files(sched_dir):
    return {fname[:-4].split("_")[0]: os.path.join(sched_dir, fname) for fname in filter(
        lambda x: x.endswith(".ics"),
        os.listdir(sched_dir)
    )}


# Write your own shitty Time class because who needs datetime/arrow amirite??? *cry*
class Time(object):
    def __init__(self, hour=None, mins=None, s=None):
        if s:
            s = s.replace(":", "")
            self.hour = int(s[:-2])
            self.mins = int(s[-2:])
        else:
            assert all(i is not None for i in (hour, mins))
            self.hour = hour
            self.mins = mins

    def step(self):
        if self.mins >= 30:
            self.hour = (self.hour + 1) % 24
            self.mins = 0
        else:
            self.mins = 30

    def back(self):
        if self.mins == 0:
            self.mins = 30
            self.hour = (self.hour - 1) % 24
        elif self.mins <= 30:
            self.mins = 0
        else:
            self.mins = 30

    def __str__(self):
        return "{}:{}".format(
            str(self.hour).zfill(2),
            str(self.mins).zfill(2)
        )

    def __repr__(self):
        # return "{}({})".format(
        #    self.__class__.__name__,
        #    ", ".join(["{}={}".format(attr, getattr(self, attr)) for attr in ("hour", "mins")])
        # )
        return "{}:{}".format(*[str(i).zfill(2) for i in (self.hour, self.mins)])

    def __eq__(self, other):
        return other.hour == self.hour and other.mins == self.mins

    def __lt__(self, other):
        if self.__eq__(other):
            return False
        if other.hour > self.hour:
            return True
        elif other.hour < self.hour:
            return False
        else:
            return other.mins > self.mins

    def __gt__(self, other):
        return not (self.__eq__(other) or self.__lt__(other))

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other


def get_rounded(time, type):
    """
    Aww yiss doctests?
    >>> str(get_rounded(937, "start"))
    '1000'
    >>> str(get_rounded(900, "start"))
    '0900'
    >>> str(get_rounded(923, "start"))
    '0930'
    >>> str(get_rounded(937, "end"))
    '0930'
    >>> str(get_rounded(900, "end"))
    '0900'
    >>> str(get_rounded(923, "end"))
    '0900'
    """
    t = Time(s=str(time))
    if t.mins not in [0, 30]:
        if type == "start":
            t.step()
        elif type == "end":
            t.back()
        else:
            raise ValueError
    return t


def yield_intervals(start, end, duration):
    start, end = get_rounded(start, "start"), get_rounded(end, "end")
    counter = Time(s=str(start))
    while counter <= end:
        s = Time(s=str(counter))
        e = Time(s=str(counter))
        counter.step()
        for i in range(duration):
            e.step()
        yield s, e


def check_conflict(i1, i2):
    s1, e1 = i1
    s2, e2 = i2
    return all([
        s1 < e2,
        e1 > s2
    ])
