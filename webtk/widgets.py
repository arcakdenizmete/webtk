import ctypes
from .xlib_core import (
    ButtonPress,
    ButtonPressMask,
    Expose,
    ExposeMask,
    XEvent,
    xlib,
)


class Widget:

  def __init__(self):
    self.x = 0
    self.y = 0
    self.width = 100
    self.height = 40


class Window(Widget):

  def __init__(self):
    super().__init__()
    self.title = None  # Varsayılan olarak başlık yok (Title olmasın desteği)
    self.display = None
    self.win_id = None
    self.gc = None
    self.widgets = []

  def set_title(self, title):
    self.title = title

  def setWindowTitle(self, title):
    self.title = title

  def set_default_size(self, w, h):
    self.width, self.height = w, h

  def resize(self, w, h):
    self.width, self.height = w, h

  def add(self, widget):
    self.widgets.append(widget)

  def addWidget(self, widget):
    self.widgets.append(widget)

  def show_all(self):
    self.show()

  def show(self):
    self.display = xlib.XOpenDisplay(None)
    if not self.display:
      raise ConnectionError("X Display açılamadı.")

    screen = xlib.XDefaultScreen(self.display)
    root = xlib.XRootWindow(self.display, screen)

    black_pixel = 0x000000
    white_pixel = 0xFFFFFF

    self.win_id = xlib.XCreateSimpleWindow(
        self.display,
        root,
        100,
        100,
        self.width,
        self.height,
        2,
        black_pixel,
        black_pixel,
    )

    # Eğer başlık atanmışsa isimlendir, atanmamışsa başlıksız/çerçevesiz kalır
    if self.title:
      xlib.XStoreName(self.display, self.win_id, self.title.encode("utf-8"))

    xlib.XSelectInput(self.display, self.win_id, ExposeMask | ButtonPressMask)
    xlib.XMapWindow(self.display, self.win_id)
    xlib.XFlush(self.display)

    self.gc = xlib.XCreateGC(self.display, self.win_id, 0, None)

    # X11 Olay Döngüsü
    event = XEvent()
    while True:
      xlib.XNextEvent(self.display, ctypes.byref(event))

      if event.type == Expose:
        for w in self.widgets:
          if isinstance(w, Button):
            # Buton Çizimi
            xlib.XSetForeground(self.display, self.gc, 0x3E3E5F)
            xlib.XFillRectangle(
                self.display, self.win_id, self.gc, w.x, w.y, w.width, w.height
            )
            xlib.XSetForeground(self.display, self.gc, white_pixel)
            xlib.XDrawString(
                self.display,
                self.win_id,
                self.gc,
                w.x + 15,
                w.y + 25,
                w.label.encode("utf-8"),
                len(w.label),
            )

          elif isinstance(w, Card):
            # Kart Arka Planı ve Çerçevesi
            xlib.XSetForeground(self.display, self.gc, 0x1E1E2F)
            xlib.XFillRectangle(
                self.display, self.win_id, self.gc, w.x, w.y, w.width, w.height
            )
            xlib.XSetForeground(self.display, self.gc, 0x5E5E8F)
            xlib.XDrawRectangle(
                self.display, self.win_id, self.gc, w.x, w.y, w.width, w.height
            )
            # Kart Başlığı
            xlib.XSetForeground(self.display, self.gc, white_pixel)
            xlib.XDrawString(
                self.display,
                self.win_id,
                self.gc,
                w.x + 15,
                w.y + 25,
                w.title.encode("utf-8"),
                len(w.title),
            )

          elif isinstance(w, Image):
            # Resim Konteyneri (X11 Alanı)
            xlib.XSetForeground(self.display, self.gc, 0x2A2A3A)
            xlib.XFillRectangle(
                self.display, self.win_id, self.gc, w.x, w.y, w.width, w.height
            )
            xlib.XSetForeground(self.display, self.gc, white_pixel)
            placeholder = f"[Resim: {w.path}]"
            xlib.XDrawString(
                self.display,
                self.win_id,
                self.gc,
                w.x + 10,
                w.y + (w.height // 2),
                placeholder.encode("utf-8"),
                len(placeholder),
            )

      elif event.type == ButtonPress:
        bx = event.xbutton.x
        by = event.xbutton.y
        for w in self.widgets:
          if isinstance(w, Button):
            if w.x <= bx <= w.x + w.width and w.y <= by <= w.y + w.height:
              if "clicked" in w.signals:
                w.signals["clicked"]()


class Button(Widget):

  def __init__(self, label="", x=50, y=50, width=180, height=45):
    super().__init__()
    self.label = label
    self.x, self.y, self.width, self.height = x, y, width, height
    self.signals = {}

  def connect(self, signal_name, callback):
    self.signals[signal_name] = callback


class Card(Widget):

  def __init__(self, title="", x=50, y=110, width=300, height=150):
    super().__init__()
    self.title = title
    self.x, self.y, self.width, self.height = x, y, width, height


class Image(Widget):

  def __init__(self, path="", x=370, y=110, width=200, height=150):
    super().__init__()
    self.path = path
    self.x, self.y, self.width, self.height = x, y, width, height


class GtkNamespace:
  Window = Window
  Button = Button
  Card = Card
  Image = Image


Gtk = GtkNamespace()
