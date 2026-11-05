# WebTK - GTK Alternatives UI Engine

# İnstall:
```bash
pip install -e .
```

## Example:
```python
from webtk import Button, Window

win = Window()
win.set_default_size(640, 480)

btn = Button(label="Tıkla", x=50, y=50, width=180, height=45)
btn.connect("clicked", lambda: print("Butona tıklandı!"))

win.add(btn)
win.show()
```
### I Thanks for Gemini
