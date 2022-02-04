import datetime, json, os

def convert_tztodate(tz):
    year = int(tz[0:4]) 
    month = int(tz[4:6])
    day = int(tz[6:8])
    hour = int(tz[9:11])
    mi = int(tz[11:13])
    sec = int(tz[13:15])
    delta = datetime.timedelta(hours=9)
    time = datetime.datetime(year, month, day, hour, mi, sec, tzinfo=datetime.timezone(delta)) + delta 
    return time

def event2dict(event):
    description = event.split('\n')
    event_dict = dict()
    for d in description:
        dl = d.split(':')
        if len(dl) == 1:
            continue
        key, value = d.split(':')
        if key in {'SUMMARY', 'DTEND', 'CATEGORIES'}:
            if key == 'DTEND':
                event_dict[key] = convert_tztodate(value).isoformat()
            else:
                event_dict[key] = value
    return event_dict

def convert():
    print('[FUNCTION] convert')
    ret_dict = dict()
    with open('./tmpcalendar.ics') as fi:
        print('[MIS] read tmpcalendar.ics')
        rawstr = fi.read()
        rawdata = rawstr.split('BEGIN:')[2:]
        for i, event in enumerate(rawdata):
            ret_dict[i] = event2dict(event)
    with open('./calendar.json', 'w') as fo:
        print('[MIS] write calendar.json')
        fo.write(json.dumps(ret_dict, indent=4))
#    os.remove('./tmpcalendar.ics')    
    print('[MIS] delete tmpcalendar.ics')
    print('[FUNCTION] end convert')

