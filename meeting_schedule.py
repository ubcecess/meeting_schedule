#!/usr/bin/env python2.7

import datetime
from calendar_parser import CalendarParser
from util import get_ical_files, yield_intervals, Time, check_conflict


SCHED_DIR = 'class_schedules'  # Directory with .ics files of everyone's class schedule
ALLOWED_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
ALLOWED_TIME_RANGE = (900, 1900, 2)  # (start, end, duration_in_half_hours)
YEAR = 2015


def main():
    icals = get_ical_files(SCHED_DIR)
    calendars = {k: CalendarParser(ics_file=v) for k, v in icals.items()}
    parsed_cals = {k: v.parse_calendar(force_list=True) for k, v in calendars.items()}

    # # Somik is special
    # parsed_cals["Somik"].append(
    #     {'end_time': datetime.datetime(2014, 9, 5, 21, 0),
    #      'location': u'idk',
    #      'name': u'Work',
    #      'repeat_day': u'FR',
    #      'repeat_freq': u'WEEKLY',
    #      'repeats': True,
    #      'start_time': datetime.datetime(2014, 9, 5, 14, 30)}
    # )

    # Scheduling algorithms? lawwwwwl
    d = {}
    for day in ALLOWED_DAYS:
        print("{}\n{}".format(day, len(day)*"-"))
        d[day] = {}
        for interval in yield_intervals(*ALLOWED_TIME_RANGE):
            l = set()
            for name, cal in parsed_cals.items():
                for event in cal:
                    if event.get("repeat_day") == day[:2].upper():
                        stime = event.get("start_time")
                        etime = event.get("end_time")
                        until = event.get("repeat_until")
                        if (
                            stime.year == YEAR or
                            getattr(until, "year", None) == YEAR
                        ):
                            if check_conflict(interval, (
                                Time(hour=stime.hour, mins=stime.minute),
                                Time(hour=etime.hour, mins=etime.minute),
                            )):
                                l.add("{}({})".format(name, event.get("name")))
                                # l.add(name)
            d[day][interval] = (
                (", ".join(l) if l else "EVERYBODY IS FREEEEEEEEEEEEE!!!!!!")
                if len(l) < 6 else len(l)
            )
            if len(l) < 5:
                print("    {}: {}".format(interval, d[day][interval]))


if __name__ == '__main__':
    main()
