months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]


def phone_parse(x) -> str:
    s = str(x)
    phone = ''
    for i in s:
        if i.isdigit():
            phone += i
    phone = phone[-10:]
    return phone


def month_to_date(month) -> int or bool:
    if month in months:
        if months.index(month) == 0:
            return 1
        elif months.index(month) == 11:
            return 12
        else:
            return months.index(month) + 1
    return False
