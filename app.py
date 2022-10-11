#!/usr/bin/env python3

from datetime import datetime, timedelta, timezone
from flask import Flask, render_template, request
from zoneinfo import ZoneInfo  # Requires Python 3.9
import yaml


app = Flask(__name__)

with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)


@app.route("/")
def show_index_page():
    return render_template("index.html", data=calculate_windows())


def calculate_windows():
    now = datetime.now(timezone.utc)

    data = {
        'utc_time_now': now.strftime(config['time_format_utc']),
        'eastern_time_now': now.astimezone(ZoneInfo(config['time_zones']['nyc'])).strftime(config['time_format']),
        'regions': []
    }

    for region, time_zone in config['time_zones'].items():
        local_time_now = now.astimezone(ZoneInfo(config['time_zones'][region]))

        # Notify at least one week in advance.

        start_time = local_time_now + timedelta(weeks=1)

        # Round forward if not already midnight local time.

        if start_time.strftime('%H:%M') != '00:00':
            plus_one_day = start_time + timedelta(days=1)
            start_time = datetime(plus_one_day.year, plus_one_day.month, plus_one_day.day, tzinfo=start_time.tzinfo)

        # Forward until the start time is a desired weekday:

        while start_time.weekday() in config['weekdays_to_exclude']:
            start_time += timedelta(days=1)

        # Calculate other times, as well as how close to the deadline (state
        # time) we are.

        state_time = start_time - timedelta(weeks=1)
        end_time = start_time + timedelta(hours=8)

        if state_time - local_time_now < timedelta(hours=4):
            urgency = 'sooner'
        elif state_time - local_time_now < timedelta(hours=8):
            urgency = 'soon'
        else:
            urgency = 'none'

        # Print the results.

        this_region = {
            'name': region,
            'urgency': urgency,
            'utc_time': {
                'state': state_time.astimezone(ZoneInfo('Etc/UTC')).strftime(config['time_format_utc']),
                'start': start_time.astimezone(ZoneInfo('Etc/UTC')).strftime(config['time_format_utc']),
                'end': end_time.astimezone(ZoneInfo('Etc/UTC')).strftime(config['time_format_utc'])
            },
            'local_time': {
                'now': local_time_now.strftime(config['time_format']),
                'state': state_time.strftime(config['time_format']),
                'start': start_time.strftime(config['time_format']),
                'end': end_time.strftime(config['time_format'])
            }
        }

        data['regions'].append(this_region)

    return data
