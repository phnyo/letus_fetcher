import datetime, json, os, re

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
        if len(dl) != 2:
            continue
        key, value = d.split(':')
        print(key, value)
        if key in {'SUMMARY', 'DTEND', 'CATEGORIES', 'DESCRIPTION'}:
            if key == 'CATEGORIES':
                course_number = re.split('\(|（', value)
                if course_number[1].rstrip(')').rstrip('）').isdigit() == False:
                    return {}
                event_dict[key] = course_number[0].rstrip('　')

            elif key == 'DTEND':
                event_dict[key] = convert_tztodate(value).isoformat()
            else:
                event_dict[key] = value
    summary_flg = not 'SUMMARY' in event_dict or event_dict['SUMMARY'] == ''
    desc_flg = not 'DESCRIPTION' in event_dict or event_dict['DESCRIPTION'] == ''
    if summary_flg and desc_flg:
        return {}
    return event_dict

def convert():
    print('[FUNCTION] convert')
    ret_dict = dict()
    with open('./tmpcalendar.ics') as fi:
        print('[MIS] read tmpcalendar.ics')
        rawstr = fi.read()
        rawdata = rawstr.split('BEGIN:')[2:]
        ind = 0
        for event in rawdata:
            tmp_dict= event2dict(event)
            if tmp_dict:
                ret_dict[ind] = tmp_dict
            ind += 1
    for event in ret_dict:
        print(ret_dict[event])

    with open('./calendar.json', 'w') as fo:
        print('[MIS] write calendar.json')
        fo.write(json.dumps(ret_dict, indent=4))
#    os.remove('./tmpcalendar.ics')    
    print('[MIS] delete tmpcalendar.ics')
    print('[FUNCTION] end convert')

if __name__ == "__main__":
    convert()
