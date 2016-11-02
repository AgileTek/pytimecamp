# PyTimeCamp

A python interface to the [TimeCamp API](https://github.com/timecamp2/timecamp-api).

Currently supports interface to:

* Users
* Tasks
* Entries
* Activities

## External dependencies

Only tested on Python 3.4 at present

[requests](http://docs.python-requests.org/en/latest/) (like almost any python library 
involving http)

[dateutil](https://dateutil.readthedocs.org/en/latest/) (to deal with filtering by dates)

## Installing

`python setup.py install`

## API Summary

TimeCamp:  

* users
* user_by_id(id)
* user_by_name(name)
* tasks(embed_users=False) - embedded users on lots of tasks is currently 
very expensive due to lack of caching
* task_by_id(task_id, embed_users=False)
* add_task(task_data)
* update_task(task_data)
* entries(from_date=None, to_date=None, task_ids=None, user_ids=None,
                embed_user=False,with_subtasks=False) - no "to_date" or "from_date" dates assumes all time to now
* add_entry(entry_data)
* update_entry(entry_data)
* activities_by_day(date=TODAY, user_id=None)
* applications(application_ids=None)
* window_titles(window_title_ids=None)

Methods return TCItem object (or lists or generators) where the top level keys are mapped to 
object attributes.  


## Example Usage

    from pytimecamp import Timecamp
    
    tc = Timecamp("s0met0k3nap1k3ystr1ng")
    for u in tc.users:
        print(u)
        # <User 444444>
        # login_time: 2015-06-01 08:27:14
        # email: nospamthanks@agil3tek.co.mk
        # display_name: Steven Rossiter
        # user_id: 444444
        # synch_time: 2015-06-04 15:08:37
        # login_count: 98
    
    
    # Get my entries since 23rd May
    me = list(tc.users)[0] # Timecamp.users is a generator
    
    # You pass dates as strings written like a normal person! (almost any date format 
    # will work - dateutil rocks - but try not confuse it with DDMMYY vs. MMDDYY)
    for entry in tc.entries(from_date="23rd May 2015", user_ids=[me.user_id]):
        print(entry)
        # <Entry 44444444>
        # duration: 1374
        # user_name: Steven Rossiter
        # locked: 0
        # start_time: 10:09:13
        # billable: 0
        # description:
        # name: CRM, Sales & Marketing
        # id: 44444444
        # last_modify: 2015-05-26 11:38:24
        # end_time: 10:32:11
        # user_id: 444444
        # task_id: 4444444
        # invoiceId: 0
        # date: 2015-05-26
    
    # get the task with ID 4444444 with the users embedded
    task = tc.task_by_id(4444444,True)
    print(task)
    # <Task 4444444>
    # tags: CRM, Sales, Marketing, INT002
    # user_access_type: 3
    # archived: 0
    # users: [
    # <User 444445>
    # display_name: Hugh Martindale
    # email: nospamthanks@agiletek.co.mk
    # synch_time: 2015-06-03 21:04:14
    # login_time: 2015-06-02 14:23:02
    # user_id: 49192
    # login_count: 26,
    # <User 444444>
    # display_name: Steven Rossiter
    # email: nospamthanks@agiletek.co.mk
    # synch_time: 2015-06-04 15:13:42
    # login_time: 2015-06-01 08:27:14
    # user_id: 49191
    # login_count: 98,
    # <User 444446>
    # display_name: Truan Willis
    # email: nospamthanks@agiletek.co.mk
    # synch_time: 2015-06-04 15:17:58
    # login_time: 2015-06-03 11:32:22
    # user_id: 444446
    # login_count: 81,
    # <User 444447>
    # display_name: Richard Langdon
    # email: richard@agiletek.co.uk
    # synch_time: 2015-06-04 15:14:36
    # login_time: 2015-06-03 20:01:52
    # user_id: 444447
    # login_count: 103]
    # external_parent_id: None
    # name: CRM, Sales & Marketing
    # billable: 0
    # parent_id: 3333333
    # task_id: 4444444
    # perms: {'5': 3, '6': 3, '7': 3, '1': 3, '3': 3, '2': 3}
    # color: #34C644
    # root_group_id: 27055
    # level: 2
    # budgeted: 0

    
## Licence

MIT (c) 2016 AgileTek Engineering Limited

## TODO

1. Unit tests!




