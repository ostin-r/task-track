#!/usr/bin/env python3
import sys
import json
import time
import os
import argparse
from tabulate import tabulate


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = CURRENT_DIR + '/tasks_14kl31i.json'

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
    task['duration'] += last_interval['end'] - last_interval['start']
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
        duration = tasks[name]['duration']
        minutes_spent = str(round(duration / 60))
        if duration == 0:
            minutes_spent = 'In progress'  # todo: calculate total time spent on task so far
        display_data.append([name, minutes_spent])
        max_len = max(max_len, len(name), len(minutes_spent))
    print(tabulate(display_data, headers=['Task Name', 'Time Spent (min)']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A dead simple time tracker')
    parser.add_argument('-s', help='start tracking a task: track -s <task_name>')
    parser.add_argument('-x', help='stop tracking a task: track -x <task_name>')
    parser.add_argument('-l', action='store_true', help='list all tasks: track -l')
    args = parser.parse_args()
    if args.s:
        start_task(args.s)
    elif args.x:
        stop_task(args.x)
    elif args.l:
        list_tasks()
    else:
        print('failed')

