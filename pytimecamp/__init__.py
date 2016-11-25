__author__ = 'agiletekengineering'
__version__ = '0.1.4'
import datetime as dt

import dateutil.relativedelta as rdelta
from dateutil.rrule import DAILY, rrule
from dateutil.parser import parse
import requests as http

URL_START = "https://www.timecamp.com/third_party/api"
TC_ITEM_TYPES = ['users', 'tasks', 'entries', 'timer_running',
                 'entries_changes', 'activity', 'application',
                 'window_title', 'client', 'invoice', 'attendance',
                 'away_time']
TODAY = dt.date.today()
DATE_FORMAT = "%Y-%m-%d"
HEADERS = {'user-agent': 'pytimecamp/{}'.format(__version__)}


def convert_day_name(day_name):
    """
    :param day_name:
    :return:

    see: http://stackoverflow.com/a/15835012/3271558
    """
    days_full = 'monday tuesday wednesday thursday friday saturday sunday'.split()
    if day_name.lower() not in days_full:
        raise KeyError("{} is not a day of the week.".format(day_name))
    days_2char = 'MO TU WE TH FR SA SU'.split()
    day_of_week = dict(zip(days_full, (getattr(rdelta, d) for d in days_2char)))
    return day_of_week[day_name.lower()]


def string_from_date_type(date):
    """
    :param date: a str, datetime.date or datetime.datetime date
    :return: string formatted as per DATE_FORMAT
    """
    if isinstance(date, (dt.date, dt.datetime)):
        return date.strftime(DATE_FORMAT)
    elif isinstance(date, str):
        return parse(date, default=TODAY).strftime(DATE_FORMAT)
    else:
        msg = ("date types can be:"
               " str, datetime.date or datetime.datetime [got {}]")
        raise TypeError(msg.format(date))


class TimecampError(Exception):
    """branded errors."""
    pass

class TCItem:
    def __init__(self, item_type, item_data):
        self.item_type = item_type
        self._data = item_data
        for attr, value in item_data.items():
            setattr(self, attr, value)

    def __repr__(self):
        s = "\n<" + self.item_type + ">"
        for k, v in self._data.items():
            s += "\n{}: {}".format(k, v)
        return s


class Timecamp:
    def __init__(self, api_token, **kwargs):
        """
        a new Timecamp API client

        :param api_token:
        :param kwargs:
        :return:
        """
        self.api_token = api_token
        self.format = 'json'
        self.start_week = convert_day_name(kwargs.get('week_starts',
                                                      'monday'))
        self.check_ssl = kwargs.get('check_ssl', True)

    def _request(self, item_type, method='get', data=None, **kwargs):
        if item_type not in TC_ITEM_TYPES:
            raise TimecampError("{} is not a valid API item.".format(item_type))
        if data:
            HEADERS['Content-Type'] = 'application/x-www-form-urlencoded'
        base_url = "{}/{}/format/json/api_token/{}".format(URL_START, item_type,
                                                           self.api_token)
        from_date = kwargs.get('from_date')
        to_date = kwargs.get('to_date')
        base_url += self._parse_dates(from_date, to_date)
        ids = [(k, v) for k, v in kwargs.items() if k.endswith("_ids")]
        for id_type, values in ids:
            if values:
                csv = ','.join([str(v) for v in values])
                base_url += "/{}/{}".format(id_type, csv)
        if kwargs.get('with_subtasks'):
            base_url += "/with_subtasks/1"
        if kwargs.get('task_id'):
            base_url += "/task_id/" + str(kwargs.get('task_id'))
        if kwargs.get('date'):
            base_url += "/date/" + string_from_date_type(kwargs.get('date'))
        self.last_request_url = base_url
        r = http.request(method.upper(), base_url,
                         headers=HEADERS, verify=self.check_ssl,
                         data=data)
        if not r.ok:
            m = "[{}] {}".format(r.status_code, r.text)
            raise TimecampError(m)
        return r.json()

    def _parse_dates(self, from_date, to_date):

        if from_date is None:
            from_date = string_from_date_type(dt.date(2000, 1, 1))
        else:
            from_date = string_from_date_type(from_date)
        if to_date is None:
            to_date = string_from_date_type(TODAY)
        else:
            to_date = string_from_date_type(to_date)

        return "/from/{}/to/{}".format(from_date, to_date)

    def _one_item(self, item_type, item_data, method="post"):
        item = self._request(item_type, method, data=item_data)
        return list(item.items())[0]

    @property
    def users(self):
        for item_data in self._request('users'):
            yield TCItem('User ' + item_data['user_id'], item_data)

    def user_by_id(self, user_id):
        for user in self._request('users'):
            if user['user_id'] == user_id:
                return TCItem("User {}".format(user['user_id']), user)
        else:
            m = "No user found with id {}."
            raise TimecampError(m.format(user_id))

    def user_by_name(self, name):
        for user in self._request('users'):
            if user['display_name'] == name:
                return TCItem("User {}".format(user['user_id']), user)
        else:
            err = "No user named {} found.".format(name)
            raise TimecampError(err)

    def _embedded_users(self, user_ids):
        return [self.user_by_id(uid) for uid in user_ids]

    def tasks(self, embed_users=False, ):
        for task_id, task_data in self._request('tasks').items():
            if task_data['users'] and embed_users:
                task_data['users'] = self._embedded_users(task_data['users'].keys())
            yield TCItem('Task {}'.format(task_id),
                         task_data)

    def task_by_id(self, task_id, embed_users=False):
        task_data = self._request('tasks', task_id=task_id)
        if not task_data:
            raise TimecampError("No task with id " + str(task_id))
        else:
            task_data = list(task_data.values())[0]
        if task_data['users'] and embed_users:
            task_data['users'] = self._embedded_users(task_data['users'].keys())
        return TCItem('Task {}'.format(task_id), task_data)

    def add_task(self, task_data):
        task_id, task_data = self._one_item('tasks', task_data)
        return TCItem('Task {}'.format(task_id), task_data)

    def update_task(self, task_data):
        task_id, task_data = self._one_item('tasks', task_data, 'put')
        return task_id, task_data

    def entries(self, from_date=None, to_date=None, task_ids=None, user_ids=None,
                embed_user=False, with_subtasks=False):
        if (task_ids is not None) and (not isinstance(task_ids, (tuple, list))):
            raise TimecampError("task_ids needs to be None, list or tuple.")
        if (user_ids is not None) and (not isinstance(user_ids, (tuple, list))):
            raise TimecampError("user_ids needs to be None, list or tuple.")
        entries = self._request("entries", from_date=from_date, to_date=to_date,
                                task_ids=task_ids, user_ids=user_ids,
                                with_subtasks=with_subtasks)
        for entry in entries:
            if embed_user:
                entry['user_id'] = self.user_by_id(entry['user_id'])
            yield TCItem("Entry {}".format(entry['id']), entry)

    def add_entry(self, entry_data):
        entry_id, entry_data = self._one_item('entries', entry_data)
        return TCItem('Entry {}'.format(entry_id), entry_data)

    def update_entry(self, entry_data):
        entry_id, entry_data = self._one_item('tasks', entry_data, 'put')
        return TCItem('Entry {}'.format(entry_id), entry_data)

    def activities_by_day(self, date=TODAY, user_id=None):
        for activity in self._request("activity", date=date,
                                      user_id=user_id):
            yield TCItem("Activity", activity)

    def past_days_activity(self, days, user_id=None):
        _start_date = TODAY - rdelta.relativedelta(days=days)
        days = rrule(DAILY, count=days, dtstart=_start_date)
        for day in days:
            yield self.activities_by_day(day, user_id)

    def applications(self, application_ids=None):
        if (application_ids is not None) and \
                (not isinstance(application_ids, (tuple, list))):
            m = "application_ids needs to be None, list or tuple."
            raise TimecampError(m)
        apps = self._request("application", application_ids=application_ids)
        for app_id, app_data in apps.items():
            yield TCItem("Application " + app_id, app_data)

    def window_titles(self, window_title_ids=None):
        if (window_title_ids is not None) and \
                (not isinstance(window_title_ids, (tuple, list))):
            m = "window_title_ids needs to be None, list or tuple."
            raise TimecampError(m)
        windows = self._request("window_title", window_title_ids=window_title_ids)
        for window_id, window_data in windows.items():
            yield TCItem("Window " + window_id, window_data)


