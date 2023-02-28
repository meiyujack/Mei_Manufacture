from uuid import uuid4
from datetime import datetime


class HumanBeing:
    TIAN_GAN = "甲乙丙丁戊己庚辛壬癸"
    DI_ZHI = "子丑寅卯辰巳午未申酉戌亥"
    INIT = 1984
    DAYS = {1: 31, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    SIGN = {
        ("0321 0721", "0420 1817"): {"星宫": "白羊", "拉丁": "Aries"},
        ("0420 1817", "0521 1721"): {"星宫": "金牛", "拉丁": "Taurus"},
        ("0521 1721", "0622 0116"): {"星宫": "双子", "拉丁": "Gemini"},
        ("0622 0116", "0723 1212"): {"星宫": "巨蟹", "拉丁": "Cancer"},
        ("0723 1212", "0823 1921"): {"星宫": "狮子", "拉丁": "Leo"},
        ("0823 1921", "0923 1705"): {"星宫": "室女", "拉丁": "Virgo"},
        ("0923 1705", "1024 0230"): {"星宫": "天秤", "拉丁": "Libra"},
        ("1024 0230", "1123 0008"): {"星宫": "天蝎", "拉丁": "Scorpio"},
        ("1123 0008", "1222 1330"): {"星宫": "射手", "拉丁": "Sagittarius"},
        ("1222 1330", "0121 0010"): {"星宫": "摩羯", "拉丁": "Capricorn"},
        ("0121 0010", "0219 1418"): {"星宫": "宝瓶", "拉丁": "Aquarius"},
        ("0219 1418", "0320 1314"): {"星宫": "双鱼", "拉丁": "Pisces"},
    }

    def __init__(self, birth: str):
        self.id = uuid4()
        self.birth = datetime.strptime(birth, "%Y%m%d")
        self.gan_zhi = ''.join(HumanBeing.TIAN_GAN)[(self.birth.year - HumanBeing.INIT) % 10] + \
                       ''.join(HumanBeing.DI_ZHI)[(self.birth.year - HumanBeing.INIT) % 12]
        self.sign = self.get_sign()

    def get_sign(self):
        for s, v in HumanBeing.SIGN.items():
            if datetime.strptime(s[0].split(' ')[0], "%m%d") <= datetime.strptime(f"{self.birth.month}{self.birth.day}",
                                                                                  "%m%d") < datetime.strptime(
                    s[1].split(' ')[0], "%m%d"):
                return v

    @staticmethod
    def is_leap_year(year):
        if year % 100 == 0:
            if year % 400 == 0:
                return True
        if year % 4 == 0:
            return True
        return False

    @staticmethod
    def update_feb(year):
        HumanBeing.DAYS.update({2: 29}) if HumanBeing.is_leap_year(year) else HumanBeing.DAYS.update({2: 28})

    def get_days(self):
        _sum = 0
        r = [HumanBeing.is_leap_year(y) for y in range(self.birth.year + 1, datetime.now().year)]
        days = r.count(True) * 366 + r.count(False) * 365
        HumanBeing.update_feb(self.birth.year)
        for m in list(HumanBeing.DAYS.keys())[:self.birth.month]:
            _sum += HumanBeing.DAYS[m]
        _sum += self.birth.day
        HumanBeing.update_feb(datetime.now().year)
        for m in list(HumanBeing.DAYS.keys())[:datetime.now().month - 1]:
            _sum += HumanBeing.DAYS[m]
        _sum += datetime.now().day
        return days + _sum

    @staticmethod
    def alive_in_year(year):
        months = (datetime.now().year - year) * 12 + datetime.now().month
        print(f"这是{year}年第{months}月")

    def leave_message(self):
        print(f"{self.sign['星宫']}({self.sign['拉丁']})的我于{self.gan_zhi}{self.birth.year}年来到人间，至今已模已样存在{self.get_days()}天。")
