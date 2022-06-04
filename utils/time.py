def end_time_calculator(end_time):
    import datetime
    now_time_str = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    now_time = datetime.datetime.strptime(now_time_str, "%m/%d/%Y %H:%M:%S")
    end_time_str = end_time.strftime("%m/%d/%Y %H:%M:%S")
    end_time = end_time.strptime(end_time_str, "%m/%d/%Y %H:%M:%S")
    if now_time >= end_time:
        return True
    else:
        return False


def end_time_reaming(end_time):
    import datetime
    now_time_str = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    now_time = datetime.datetime.strptime(now_time_str, "%m/%d/%Y %H:%M:%S")
    end_time_str = end_time.strftime("%m/%d/%Y %H:%M:%S")
    end_time = end_time.strptime(end_time_str, "%m/%d/%Y %H:%M:%S")
    reaming_time = end_time - now_time
    reaming_time_str = str(reaming_time)
    reaming_time_farsi = reaming_time_str.replace('days', 'روز')
    reaming_time_farsi = reaming_time_farsi.replace('day', 'روز')
    return reaming_time_farsi
