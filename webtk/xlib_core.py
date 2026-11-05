import ctypes
import ctypes.util

xlib_path = ctypes.util.find_library("X11")
if not xlib_path:
  raise RuntimeError("Sistemde libX11 bulunamadı.")

xlib = ctypes.CDLL(xlib_path)

Display = ctypes.c_void_p
Window = ctypes.c_ulong
GC = ctypes.c_void_p


class XAnyEvent(ctypes.Structure):
  _fields_ = [
      ("type", ctypes.c_int),
      ("serial", ctypes.c_ulong),
      ("send_event", ctypes.c_int),
      ("display", Display),
      ("window", Window),
  ]


class XButtonPressedEvent(ctypes.Structure):
  _fields_ = [
      ("type", ctypes.c_int),
      ("serial", ctypes.c_ulong),
      ("send_event", ctypes.c_int),
      ("display", Display),
      ("window", Window),
      ("subwindow", Window),
      ("time", ctypes.c_ulong),
      ("x", ctypes.c_int),
      ("y", ctypes.c_int),
      ("x_root", ctypes.c_int),
      ("y_root", ctypes.c_int),
      ("state", ctypes.c_uint),
      ("button", ctypes.c_uint),
      ("same_screen", ctypes.c_int),
  ]


class XEvent(ctypes.Union):
  _fields_ = [
      ("type", ctypes.c_int),
      ("xbutton", XButtonPressedEvent),
      ("pad", ctypes.c_byte * 192),
  ]


# Xlib Fonksiyonları
xlib.XOpenDisplay.argtypes = [ctypes.c_char_p]
xlib.XOpenDisplay.restype = Display

xlib.XDefaultScreen.argtypes = [Display]
xlib.XDefaultScreen.restype = ctypes.c_int

xlib.XRootWindow.argtypes = [Display, ctypes.c_int]
xlib.XRootWindow.restype = Window

xlib.XCreateSimpleWindow.argtypes = [
    Display,
    Window,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_uint,
    ctypes.c_uint,
    ctypes.c_uint,
    ctypes.c_ulong,
    ctypes.c_ulong,
]
xlib.XCreateSimpleWindow.restype = Window

xlib.XMapWindow.argtypes = [Display, Window]
xlib.XMapWindow.restype = ctypes.c_int

xlib.XStoreName.argtypes = [Display, Window, ctypes.c_char_p]
xlib.XStoreName.restype = ctypes.c_int

xlib.XSelectInput.argtypes = [Display, Window, ctypes.c_long]
xlib.XSelectInput.restype = ctypes.c_int

xlib.XFlush.argtypes = [Display]
xlib.XFlush.restype = ctypes.c_int

xlib.XNextEvent.argtypes = [Display, ctypes.POINTER(XEvent)]
xlib.XNextEvent.restype = ctypes.c_int

xlib.XCreateGC.argtypes = [Display, Window, ctypes.c_ulong, ctypes.c_void_p]
xlib.XCreateGC.restype = GC

xlib.XSetForeground.argtypes = [Display, GC, ctypes.c_ulong]
xlib.XSetForeground.restype = ctypes.c_int

xlib.XDrawString.argtypes = [
    Display,
    Window,
    GC,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_char_p,
    ctypes.c_int,
]
xlib.XDrawString.restype = ctypes.c_int

xlib.XFillRectangle.argtypes = [
    Display,
    Window,
    GC,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_uint,
    ctypes.c_uint,
]
xlib.XFillRectangle.restype = ctypes.c_int

xlib.XDrawRectangle.argtypes = [
    Display,
    Window,
    GC,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_uint,
    ctypes.c_uint,
]
xlib.XDrawRectangle.restype = ctypes.c_int

ExposeMask = 1 << 15
ButtonPressMask = 1 << 2
Expose = 12
ButtonPress = 4
