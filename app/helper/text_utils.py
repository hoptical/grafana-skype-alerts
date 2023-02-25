
class TextUtils(object):
    @staticmethod
    def add_thousand_seperator(number):
        # this function adds ',' after every 3 digits from right to ease the read
        # 1000-->1,000
        s = '%d' % number
        groups = []
        while s and s[-1].isdigit():
            groups.append(s[-3:])
            s = s[:-3]
        return s + ','.join(reversed(groups))
