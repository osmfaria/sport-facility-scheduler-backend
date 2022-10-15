def set_new_hour(str_datetime, hour):
    date_str = str_datetime.split()
    date_str[1] = str(hour).zfill(2)
    return ' '.join(date_str)