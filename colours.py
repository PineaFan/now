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

    def rgb(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"
