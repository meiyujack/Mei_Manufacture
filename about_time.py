from uuid import uuid4
from datetime import datetime
import datetime as DT


class HumanBeing:
    TIAN_GAN = "甲乙丙丁戊己庚辛壬癸"
    DI_ZHI = "子丑寅卯辰巳午未申酉戌亥"
    INIT = 1984
    DAYS = {
        1: 31,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31
    }
    SIGN = {
        ("0321 0721", "0420 1817"): [{
            "星宫": "白羊",
            "拉丁": "Aries",
            "角度": (0, 30)
        }, {
            "春分": 0,
            "清明": 15
        }],
        ("0420 1817", "0521 1721"): [{
            "星宫": "金牛",
            "拉丁": "Taurus",
            "角度": (30, 60)
        }, {
            "谷雨": 30,
            "立夏": 45
        }],
        ("0521 1721", "0622 0116"): [{
            "星宫": "双子",
            "拉丁": "Gemini",
            "角度": (60, 90)
        }, {
            "小满": 60,
            "芒种": 75
        }],
        ("0622 0116", "0723 1212"): [{
            "星宫": "巨蟹",
            "拉丁": "Cancer",
            "角度": (90, 120)
        }, {
            "夏至": 90,
            "小暑": 105
        }],
        ("0723 1212", "0823 1921"): [{
            "星宫": "狮子",
            "拉丁": "Leo",
            "角度": (120, 150)
        }, {
            "大暑": 120,
            "立秋": 135
        }],
        ("0823 1921", "0923 1705"): [{
            "星宫": "室女",
            "拉丁": "Virgo",
            "角度": (150, 180)
        }, {
            "处属": 150,
            "白露": 165
        }],
        ("0923 1705", "1024 0230"): [{
            "星宫": "天秤",
            "拉丁": "Libra",
            "角度": (180, 210)
        }, {
            "秋分": 180,
            "寒露": 195
        }],
        ("1024 0230", "1123 0008"): [{
            "星宫": "天蝎",
            "拉丁": "Scorpio",
            "角度": (210, 240)
        }, {
            "霜降": 210,
            "立冬": 225
        }],
        ("1123 0008", "1222 1330"): [{
            "星宫": "射手",
            "拉丁": "Sagittarius",
            "角度": (240, 270)
        }, {
            "小雪": 240,
            "大雪": 255
        }],
        ("1222 1330", "0121 0010"): [{
            "星宫": "摩羯",
            "拉丁": "Capricorn",
            "角度": (270, 300)
        }, {
            "冬至": 270,
            "小寒": 285
        }],
        ("0121 0010", "0219 1418"): [{
            "星宫": "宝瓶",
            "拉丁": "Aquarius",
            "角度": (300, 330)
        }, {
            "大寒": 300,
            "立春": 315
        }],
        ("0219 1418", "0320 1314"): [{
            "星宫": "双鱼",
            "拉丁": "Pisces",
            "角度": (330, 0)
        }, {
            "雨水": 330,
            "惊蛰": 345
        }],
    }
    CENTURY_21_C = {
        "春分": 20.646,
        "清明": 4.81,
        "谷雨": 20.1,
        "立夏": 5.52,
        "小满": 21.04,
        "芒种": 5.678,
        "夏至": 21.37,
        "小暑": 7.108,
        "大暑": 22.83,
        "立秋": 7.5,
        "处暑": 23.13,
        "白露": 7.646,
        "秋分": 23.042,
        "寒露": 8.318,
        "霜降": 23.438,
        "立冬": 7.438,
        "小雪": 22.36,
        "大雪": 7.18,
        "冬至": 21.94,
        "小寒": 5.4055,
        "大寒": 20.12,
        "立春": 3.87,
        "雨水": 18.73,
        "惊蛰": 5.63
    }

    def get_JIE_QI(self):
        near_jieqi = list(HumanBeing.get_sign(datetime.now())[1].keys())
        y = int(datetime.now().strftime("%y"))
        d = [
            int(y * 0.2422 + HumanBeing.CENTURY_21_C[k] - int(y / 4))
            for k in near_jieqi
        ]

        near_jieqi = list(
            HumanBeing.get_sign(datetime.now() +
                                DT.timedelta(days=15))[1].keys())
        d = [
            int(y * 0.2422 + HumanBeing.CENTURY_21_C[k] - int(y / 4))
            for k in near_jieqi
        ]
        r = dict(zip(near_jieqi, d))
        if int(datetime.now().strftime("%d")) > 15:
            print(
                f'即将来临的节气是{list(r.keys())[1]},为{int(datetime.now().strftime("%m"))+1}月{list(r.values())[1]}号'
            )
        else:
            print(
                f'即将来临的节气是{list(r.keys())[0]},为{int(datetime.now().strftime("%m"))}月{list(r.values())[0]}号'
            )
        #return dict(zip(near_jieqi, d))

    def __init__(self, birth: str):
        self.id = uuid4()
        try:
            self.birth = datetime.strptime(birth, "%Y%m%d")
        except ValueError:
            raise "格式错误"
        self.gan_zhi = ''.join(HumanBeing.TIAN_GAN)[(self.birth.year - HumanBeing.INIT) % 10] + \
                       ''.join(HumanBeing.DI_ZHI)[(self.birth.year - HumanBeing.INIT) % 12]
        self.sign = HumanBeing.get_sign(self.birth)

    @staticmethod
    def get_sign(dt: datetime):
        for s, v in HumanBeing.SIGN.items():
            if s[0].split(' ')[0] <= dt.strftime("%m%d") < s[1].split(' ')[0]:
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
        HumanBeing.DAYS.update({2: 29}) if HumanBeing.is_leap_year(
            year) else HumanBeing.DAYS.update({2: 28})
        HumanBeing.DAYS = {
            k: HumanBeing.DAYS[k]
            for k in sorted(HumanBeing.DAYS)
        }

    def get_days(self):
        _sum = 0
        r = [
            HumanBeing.is_leap_year(y) for y in range(self.birth.year + 1,
                                                      datetime.now().year)
        ]
        days = r.count(True) * 366 + r.count(False) * 365
        for m in list(HumanBeing.DAYS.keys())[self.birth.month - 1:12 + 1]:
            _sum += HumanBeing.DAYS[m]
        _sum += HumanBeing.DAYS[self.birth.month] - self.birth.day
        HumanBeing.update_feb(datetime.now().year)
        for m in list(HumanBeing.DAYS.keys())[0:datetime.now().month - 1]:
            _sum += HumanBeing.DAYS[m]
        _sum += datetime.now().day
        return days + _sum

    @staticmethod
    def alive_in_year(year):
        months = (datetime.now().year - year) * 12 + datetime.now().month
        print(f"这是{year}年{months}月")

    def leave_message(self):
        print(
            f"{self.sign[0]['星宫']}({self.sign[0]['拉丁']})的我于{self.gan_zhi}{self.birth.year}年来到人间，至今已模已样存在{self.get_days()}天。"
        )


if __name__ == '__main__':
    birth = input("请输入您的出生年月日(YYYYmmdd)：")
    my = HumanBeing(birth)
    my.leave_message()
    my.get_JIE_QI()
    year = input("您最想回到哪一年？")
    my.alive_in_year(int(year))
