import fileinput
import re
import datetime
from collections import defaultdict

r = re.compile(r'^\[(\d+-\d+-\d+ \d+:\d+)](?: Guard #(\d+))? (falls asleep|wakes up|begins shift)$')

def parse(line):
    d, id, event = r.match(line).groups()
    return datetime.datetime.strptime(d, '%Y-%m-%d %H:%M'), event, id and int(id)

def part1():
    guards_total = defaultdict(int)
    guards = defaultdict(lambda: defaultdict(int))
    parsed = sorted(parse(line) for line in fileinput.input())

    id = None
    sleepy_time = None
    for date, event, newid in parsed:
        if event == 'begins shift':
            id = newid
        if event == 'falls asleep':
            sleepy_time = date

        if event == 'wakes up':
            for m in range(sleepy_time.minute, date.minute):
                guards[id][m] += 1
                guards_total[id] += 1

    most_sleepy_guard_id = max(guards_total, key=guards_total.get)
    most_sleepy_minute_of_most_sleepy_guard = max(guards[most_sleepy_guard_id], key=guards[most_sleepy_guard_id].get)
    print(most_sleepy_guard_id * most_sleepy_minute_of_most_sleepy_guard)

def part2():
    guards = defaultdict(int)
    parsed = sorted(parse(line) for line in fileinput.input())

    id = None
    sleepy_time = None
    for date, event, newid in parsed:
        if event == 'begins shift':
            id = newid
        if event == 'falls asleep':
            sleepy_time = date

        if event == 'wakes up':
            for m in range(sleepy_time.minute, date.minute):
                guards[(id, m)] += 1

    most_sleepy_guard_id, most_sleepy_minute = max(guards, key=guards.get)
    print(most_sleepy_guard_id * most_sleepy_minute)

part2()
