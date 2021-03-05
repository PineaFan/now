import datetime
import psutil
import humanize
import time
import os


class C:
    c = '\033[0m'
    White = '\033[1m'
    Italics = '\033[3m'
    Underline = '\033[4m'
    BlinkItalics = '\033[5m'
    BlinkInverted = '\033[7m'
    Strike = '\033[28m'
    Invisible = '\033[30m'
    RedDark = '\033[31m'
    GreenDark = '\033[32m'
    YellowDark = '\033[33m'
    BlueDark = '\033[34m'
    PinkDark = '\033[35m'
    CyanDark = '\033[36m'
    RedDarkInverted = '\033[41m'
    GreenDarkInverted = '\033[42m'
    YellowDarkInverted = '\033[43m'
    BlueDarkInverted = '\033[44m'
    PinkDarkInverted = '\033[45m'
    CyanDarkInverted = '\033[46m'
    WhiteDarkInverted = '\033[47m'
    Grey = '\033[90m'
    Red = '\033[91m'
    Green = '\033[92m'
    Yellow = '\033[93m'
    Blue = '\033[94m'
    Pink = '\033[95m'
    Cyan = '\033[96m'
    RedInverted = '\033[101m'
    GreenInverted = '\033[102m'
    YellowInverted = '\033[103m'
    BlueInverted = '\033[104m'
    PinkInverted = '\033[105m'
    CyanInverted = '\033[106m'
    WhiteInverted = '\033[107m'


def colgen(percent, ranges):
    if percent < ranges[0]:
        return C.Green
    if percent < ranges[1]:
        return C.Yellow
    return C.Red


def clamp(string, length):
    string = str(string)
    if len(string) < length:
        spaces = " " * (length - len(string))
        return spaces + string
    if len(string) > length:
        return string[length:]
    return string


def clampfields(fields: list, length):
    string = []
    length -= 1
    for field in fields:
        if len("   ".join(string)) + len(field) + 3 <= length:
            string.append(field)
    incomplete = False
    if len(string) < len(fields):
        incomplete = True
    string = " • ".join(string)
    pad = ""
    if len(string) < length:
        pad = "=" * (length - len(string) - 1)
        pad = " " + pad
    return string + pad + (">" if incomplete else "=")


def highlight(string, percent, colour):
    string = colour + string
    characters = round((percent / 100) * len(string))
    string = string[:characters] + C.c + string[characters:]
    return string


while True:
    _, th = os.popen('stty size', 'r').read().split()
    posswidth = int(th)

    cpupercent = psutil.getloadavg()[0]*10
    mempercent = round((psutil.virtual_memory().used/psutil.virtual_memory().total)*100, 2)
    diskpercent = psutil.disk_usage('/').percent

    temps = 0
    for sensor in psutil.sensors_temperatures()["coretemp"]:
        temps += sensor.current
    coreav = temps / len(psutil.sensors_temperatures()["coretemp"])
    tempcol = C.Blue if coreav < 50 else C.Yellow if coreav < 75 else C.Red
    wifi = psutil.sensors_temperatures()["iwlwifi_1"][0].current
    pch = psutil.sensors_temperatures()["pch_cannonlake"][0].current

    strings = [
        highlight(
            clampfields(
                fields=[
                    f"{clamp(psutil.cpu_count(), 1)} Cores",
                    f"{clamp(round(psutil.cpu_freq().max/1000, 1), 3)}GHz",
                    f"{clamp(round(cpupercent), 3)}% Load"
                ],
                length=posswidth-11
            ),
            percent=cpupercent,
            colour=colgen(cpupercent, [33, 66])
        ),
        highlight(
            clampfields(
                fields=[
                    f"{clamp(mempercent, 5)}%",
                    f"{clamp(humanize.naturalsize(psutil.virtual_memory().total, False, True), 4)} Total",
                    f"{clamp(humanize.naturalsize(psutil.virtual_memory().used, False, True), 4)} Used"
                ],
                length=posswidth-11
            ),
            percent=mempercent,
            colour=colgen(mempercent, [33, 66])
        ),
        highlight(
            clampfields(
                fields=[
                    f"{clamp(psutil.disk_usage('/').percent, 4)}% Used",
                    f"{clamp(len([d.mountpoint for d in psutil.disk_partitions()]), 1)} Mounts"
                ] + [d.mountpoint for d in psutil.disk_partitions()],
                length=posswidth-11
            ),
            percent=diskpercent,
            colour=colgen(diskpercent, [33, 66])
        ),
        highlight(
            clampfields(
                fields=[
                    f"Cores {round(coreav)}°c",
                    f"Network {round(wifi)}°c",
                    f"PCH {round(pch)}°c"
                ],
                length=posswidth-11
            ),
            percent=(coreav),
            colour=tempcol
        ),
        highlight(
            clampfields(
                fields=[
                    f"{clamp(round(psutil.swap_memory().percent, 2), 4)}% Used",
                    f"{clamp(humanize.naturalsize(psutil.swap_memory().used), 8)} Used",
                    f"{clamp(humanize.naturalsize(psutil.swap_memory().total), 6)} Total"
                ],
                length=posswidth-11
            ),
            percent=max(psutil.swap_memory().percent, 7),
            colour=colgen(psutil.swap_memory().percent, [33, 66])
        ),
        highlight(
            clampfields(
                fields=[
                    f"{len(psutil.pids())} Processes"
                ],
                length=posswidth-11
            ),
            percent=((len(psutil.pids())/500)*100),
            colour=colgen(((len(psutil.pids())/500)*100), [33, 66])
        ),
        highlight(
            clampfields(
                fields=[
                    f"{datetime.datetime.now().strftime('%H:%M:%S')}",
                    f"{datetime.datetime.now().strftime('%y-%m-%d')}"
                ],
                length=posswidth-11
            ),
            percent=(int(datetime.datetime.now().strftime('%S')))/60*100,
            colour=colgen(int(datetime.datetime.now().strftime('%M')), [20, 40])
        ),
    ]
    os.system("clear")
    print(f"{C.c}[ {C.c          }TIME {C.c}| " + strings[6] + f"{C.c} ]")
    print(f"{C.c}[ {C.Red        }PROC {C.c}| " + strings[5] + f"{C.c} ]")
    print(f"{C.c}[ {C.Blue       }CPU  {C.c}| " + strings[0] + f"{C.c} ]")
    print(f"{C.c}[ {C.PinkDark   }MEM  {C.c}| " + strings[1] + f"{C.c} ]")
    print(f"{C.c}[ {C.YellowDark }SWAP {C.c}| " + strings[4] + f"{C.c} ]")
    print(f"{C.c}[ {C.Yellow     }DISK {C.c}| " + strings[2] + f"{C.c} ]")
    print(f"{C.c}[ {C.Green      }TEMP {C.c}| " + strings[3] + f"{C.c} ]", end="\r")

    time.sleep(0.5)
