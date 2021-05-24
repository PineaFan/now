import datetime
import time
import os
import sys
import subprocess
import platform
from typing import ValuesView

# Use a temperature of *C*elcius, *F*ahrenheit, *K*elvin, or *R*ankine
temperature = "c"
# How long to wait before updating stats (seconds)
refreshRate = 0.5

try:
    import humanize
except ModuleNotFoundError:
    x = input("Module humanize not found - Install it? [Y/n] ")
    if x == "" or x.lower() == "y":
        os.system(f"{sys} -m install humanize --user")

try:
    import psutil
except ModuleNotFoundError:
    x = input("Module psutil not found - Install it? [Y/n] ")
    if x == "" or x.lower() == "y":
        os.system(f"{sys} -m install psutil --user")


def convertTemp(temperature, unit=temperature):
    temperature = int(temperature)
    unit = unit.lower()
    if unit == "c":
        return temperature, "°C"
    elif unit == "f":
        return (temperature * (9/5)) + 32, "°F"
    elif unit == "k":
        return temperature + 273.15, "K"
    elif unit == "r":
        return (temperature * (9/5)) + 32 + 459.67, "°R"


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


clearCommand = "clear"
if platform.system() == "Windows":
    clearCommand = "cls"
    x = input(f"{C.Red}Is this text in red?{C.c} [y/N] ")
    if x == "" or x.lower() == "n":
        for n in [i for i in C.__dict__.keys() if i[:1] != '_']:
            setattr(C, n, "")


def transformCPU(value):
    if platform.system == "Darwin":
        return value / psutil.cpu_count()
    return value


def getTemps():
    if platform.system() == "Darwin":
        temp = float(subprocess.check_output(["osx-cpu-temp"]).decode()[:-3])
        tempcol = C.Blue if temp < 50 else C.Yellow if temp < 75 else C.Red
        return temp, [("Cores", temp)], tempcol
    sensorNames = {
        "acpitz": "Sockets",
        "pch_cannonlake": "PCH",
        "coretemp": "Cores",
        "iwlwifi_1": "WIFI"
    }
    temp, count = 0, 0
    try:
        sensors = psutil.sensors_temperatures()
    except AttributeError:
        sensors = []
    tempsens = []
    for sensor in sensors:
        s = [0, 0]
        for each in sensors[sensor]:
            temp += each.current
            s[0] += each.current
            count += 1
            s[1] += 1
        if sensor in sensorNames:
            sensor = sensorNames[sensor]
        tempsens.append((sensor, s[0]/s[1]))
    try:
        tempav = temp/count
        tempcol = C.Blue if tempav < 50 else C.Yellow if tempav < 75 else C.Red
    except ZeroDivisionError:
        tempav = convertTemp(100)[0]
        tempsens = [("No temperature sensors found", -1)]
        tempcol = C.Blue

    for item in range(len(tempsens)):
        if tempsens[item][0] == "Cores":
            t = tempsens.pop(item)
            tempsens = [t] + tempsens

    return tempav, tempsens, tempcol

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
        return string[:length]
    return string


def clampfields(fields: list, length, warning=None, level=False):
    if level:
        fields.append(warning)
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


def highlight(string, percent, colour, warning=False):
    characters = round((percent / 100) * len(string))
    return colour + string[:characters] + C.c + string[characters:]


def warning(string, warning, cycle, param):
    if param and cycle % 2:
        return warning
    else:
        return string


cycle = 0
minProcs = 10000
topProcs = 1
while True:
    skipMI = False
    if not cycle:
        try:
            th = os.get_terminal_size().columns
            posswidth = int(th) - 11
        except OSError:
            _, th = os.popen('stty size', 'r').read().split()
            posswidth = int(th) - 11

    cycle = (cycle + 1) % 4

    procs = list()
    try:
        for proc in psutil.process_iter(attrs=None, ad_value=None):
            procInfo = proc.as_dict(attrs=['name', 'cpu_percent', 'memory_percent'])
            procs.append(procInfo)
        mostCPU = procs[0]
        mostRAM = procs[0]
        for p in procs:
            if p["cpu_percent"] > mostCPU["cpu_percent"]:
                mostCPU = p
            if p["memory_percent"] > mostRAM["memory_percent"]:
                mostRAM = p
    except (psutil.NoSuchProcess, TypeError, psutil.ProcessLookupError):
        skipMI = True

    minProcs = min(minProcs, len(psutil.pids()))
    topProcs = max(topProcs, len(psutil.pids()))
    procs = len(psutil.pids())
    pidpercent = abs((((topProcs-procs)-(topProcs-minProcs)) / topProcs) * 100)

    cpupercent = psutil.getloadavg()
    cpupercent = transformCPU((sum(cpupercent)/len(cpupercent))*10)
    mempercent = round((psutil.virtual_memory().used/psutil.virtual_memory().total)*100, 2)
    diskpercent = psutil.disk_usage('/').percent

    tempav, tempsens, tempcol = getTemps()

    swapfields = [
        f"{clamp(round(psutil.swap_memory().percent, 2), 5)}% Used",
        f"{humanize.naturalsize(psutil.swap_memory().used)} Used",
        f"{humanize.naturalsize(psutil.swap_memory().total)} Total"
    ]
    swappercent = psutil.swap_memory().percent
    if not psutil.swap_memory().total:
        swapfields = [
            "Swap is not avaliable"
        ]
        swappercent = -1

    strings = [
        highlight(
            clampfields(
                fields=[
                    f"{datetime.datetime.now().strftime('%H:%M:%S')}",
                    f"{datetime.datetime.now().strftime('%y-%m-%d')}"
                ],
                length=posswidth
            ),
            percent=(int(datetime.datetime.now().strftime('%S')))/60*100,
            colour=colgen(int(datetime.datetime.now().strftime('%M')), [20, 40])
        ),
        highlight(
            clampfields(
                fields=[
                    f"{len(psutil.pids())} Processes",
                    f"Lowest: {minProcs}",
                    f"Highest: {topProcs}"
                ],
                length=posswidth
            ),
            percent=(pidpercent),
            colour=colgen(pidpercent, [33, 66])
        ),
        highlight(
            clampfields(
                fields=[
                    f"{clamp(str(round(cpupercent, 3)), 5)}% Load",
                    f"{psutil.cpu_count()} Cores",
                    f"{round(psutil.cpu_freq().max/1000, 1)}GHz"
                ],
                length=posswidth,
                warning=f"{mostCPU['name']}: {round(mostCPU['cpu_percent']/psutil.cpu_count(), 2)}% CPU" if not skipMI else "High CPU Usage",
                level=(cpupercent > 80)
            ),
            percent=cpupercent,
            colour=C.RedInverted if (cpupercent > 80 and cycle % 2) else colgen(cpupercent, [33, 66]),
        ),
        highlight(
            clampfields(
                fields=[
                    f"{clamp(mempercent, 5)}% Used",
                    f"{humanize.naturalsize(psutil.virtual_memory().used, False, True)} Used",
                    f"{humanize.naturalsize(psutil.virtual_memory().total, False, True)} Total"
                ],
                length=posswidth,
                warning=f"{mostRAM['name']}: {round(mostRAM['memory_percent'], 2)}% RAM" if not skipMI else "High RAM Usage",
                level=(mempercent > 80)
            ),
            percent=mempercent,
            colour=C.RedInverted if (mempercent > 80 and cycle % 2) else colgen(mempercent, [33, 66])
        ),
        highlight(
            clampfields(
                fields=swapfields,
                length=posswidth,
                warning="High Swap Usage",
                level=(0 > psutil.swap_memory().percent > 80)
            ),
            percent=swappercent if swappercent >= 0 else 100,
            colour=C.RedInverted if (0 > psutil.swap_memory().percent > 80 and cycle % 2) else colgen(psutil.swap_memory().percent, [33, 66])
        ),
        highlight(
            clampfields(
                fields=[
                    f"{clamp(psutil.disk_usage('/').percent, 5)}% Used",
                    f"{len([d.mountpoint for d in psutil.disk_partitions()])} Mounts"
                ] + [d.mountpoint for d in psutil.disk_partitions()],
                length=posswidth
            ),
            percent=diskpercent,
            colour=colgen(diskpercent, [33, 66])
        ),
        highlight(
            clampfields(
                fields=[f"{t[0]}: {round(convertTemp(t[1])[0])}{convertTemp(0)[1]}" for t in tempsens],
                length=posswidth,
                warning="High temperature",
                level=(0 > tempav > convertTemp(75)[0])
            ),
            percent=convertTemp(tempav, "c")[0],
            colour=C.RedInverted if (0 > tempav > convertTemp(75)[0] and cycle % 2) else tempcol
        ),
    ]
    os.system(clearCommand)
    print(f"{C.c}[ {C.c          }TIME {C.c}| " + strings[0] + f"{C.c} ]")
    print(f"{C.c}[ {C.Red        }PROC {C.c}| " + strings[1] + f"{C.c} ]")
    print(f"{C.c}[ {C.Blue       }CPU  {C.c}| " + strings[2] + f"{C.c} ]")
    print(f"{C.c}[ {C.PinkDark   }MEM  {C.c}| " + strings[3] + f"{C.c} ]")
    print(f"{C.c}[ {C.YellowDark }SWAP {C.c}| " + strings[4] + f"{C.c} ]")
    print(f"{C.c}[ {C.Yellow     }DISK {C.c}| " + strings[5] + f"{C.c} ]")
    print(f"{C.c}[ {C.Green      }TEMP {C.c}| " + strings[6] + f"{C.c} ]", end="\r")

    time.sleep(refreshRate)
