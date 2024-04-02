#!/usr/bin/env python3
import sys
import json
import time
import os
from tabulate import tabulate

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = CURRENT_DIR + '/tasks.json'

def _write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)


def start_task(task_name):
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({}, f)
    with open(DATA_FILE, 'r') as f:
        tasks = json.load(f)
    if task_name not in tasks:
        tasks[task_name] = {
            'name': task_name,
            'time_intervals': [{'start': time.time(), 'end': None}],
            'duration': 0
        }
    else:
        task = tasks[task_name]
        if task['time_intervals'][-1]['end'] is None:
            print(f'Task {task_name} has already been started.  Run \'track stop <task_name>\' to complete the task first.')
            return -1
        task['time_intervals'].append({
            'start': time.time(),
            'end': None
        })
    print(f'Task {task_name} has been successfully started')
    _write_data(tasks)


def stop_task(task_name):
    with open(DATA_FILE, 'r') as f:
        tasks = json.load(f)
    if task_name not in tasks:
        print(f'Task {task_name} could not be found in the current task list, try \'track ls\' to see active tasks.')
        return -1
    task = tasks[task_name]
    last_interval = task['time_intervals'][-1]
    last_interval['end'] = time.time()
    duration = 0
    for interval in task['time_intervals']:
        duration += interval['end'] - interval['start']
    task['duration'] = duration
    _write_data(tasks)

    minutes_spent = task['duration'] / 60
    print(f'Task {task_name} successfully stopped. Session time: {minutes_spent} minutes.')
    print('To view time spent on tasks, use \'track ls -a\'')


def list_tasks(show_all=None):
    try:
        with open(DATA_FILE, 'r') as f:
            tasks = json.load(f)
    except:
        tasks = {}
    if len(tasks) == 0:
        print('No tasks have been started, run \'track start <task_name>\' to get started')
        return -1
    display_data, max_len = [], 0
    for name in tasks:
        if show_all or tasks[name]['time_intervals'][-1]['end'] is None:
            duration = tasks[name]['duration']
            minutes_spent = str(round(duration / 60))
            if duration == 0:
                minutes_spent = 'In progress'  # todo: calculate total time spent on task so far
            display_data.append([name, minutes_spent])
            max_len = max(max_len, len(name), len(minutes_spent))
    print(tabulate(display_data, headers=['Task Name', 'Time Spent (min)']))


if __name__ == '__main__':
    if sys.argv[1] == 'start':
        if len(sys.argv) == 3 and isinstance(sys.argv[1], str):
            start_task(sys.argv[2])
        else:
            print('Incorrect usage of \'start\' command. Try \'task start <unique_task_name>\'')
    elif sys.argv[1] == 'stop':
        if len(sys.argv) == 3 and isinstance(sys.argv[1], str):
            stop_task(sys.argv[2])
        else:
            print('Incorrect usage of \'stop\' command. Try \'task stop <unique_task_name>\'')
    elif sys.argv[1] == 'ls':
        if len(sys.argv) == 2:
            list_tasks()
        elif len(sys.argv) == 3:
            list_tasks(sys.argv[2])
        else:
            print('Incorrect usage of \'ls\' command.  Use \'track ls\' or \'track ls -a\'')
    else:
        print('unkown arguments given')

