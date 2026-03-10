from enum import Enum


class CursorShape(str, Enum):
    bar = "bar"
    vintage = "vintage"
    underscore = "underscore"
    filledBox = "filledBox"
    emptyBox = "emptyBox"
    doubleUnderscore = "doubleUnderscore"


class BellStyle(str, Enum):
    audible = "audible"
    visual = "visual"
    none = "none"
    window_title = "window title"


class BackgroundStretchMode(str, Enum):
    fill = "fill"
    none = "none"
    uniform = "uniform"
    uniformToFill = "uniformToFill"


class BackgroundAlignment(str, Enum):
    center = "center"
    left = "left"
    top = "top"
    right = "right"
    bottom = "bottom"
    topLeft = "topLeft"
    topRight = "topRight"
    bottomLeft = "bottomLeft"
    bottomRight = "bottomRight"


class IntenseTextStyle(str, Enum):
    bold = "bold"
    bright = "bright"
    all = "all"
    none = "none"


class ScrollbarState(str, Enum):
    visible = "visible"
    hidden = "hidden"
    always = "always"


class AntialiasingMode(str, Enum):
    grayscale = "grayscale"
    cleartype = "cleartype"
    aliased = "aliased"


class CloseOnExit(str, Enum):
    always = "always"
    graceful = "graceful"
    never = "never"


class PathTranslationStyle(str, Enum):
    none = "none"
    wsl = "wsl"
    cygwin = "cygwin"
