from nicegui import events, ui


class RectDrawer:
    def __init__(self) -> None:
        self.mouse_down = False
        self.x0 = 0
        self.y0 = 0
        self.bounding_boxes = []
        self.new_rect = ""

    def mouse_handler(self, e: events.MouseEventArguments):
        color = "SkyBlue"
        if e.type == "mousedown":
            self.mouse_down = True
            self.x0 = e.image_x
            self.y0 = e.image_y

            x1 = e.image_x
            y1 = e.image_y

        elif e.type == "mouseup":
            self.mouse_down = False
            self.bounding_boxes += [self.new_rect]
            print(self.bounding_boxes)
            return
        elif e.type == "mousemove":
            x1 = e.image_x
            y1 = e.image_y
            if not self.mouse_down:
                return
        # ii.content = ii.content[: -(self.prev_len + 1)]

        width = abs(x1 - self.x0)
        height = abs(y1 - self.y0)
        self.new_rect = f'<rect x="{self.x0}" y="{self.y0}" width="{width}" height="{height}" fill="none" stroke="{color}" stroke-width="4" />'

        ii.content = " ".join(self.bounding_boxes) + self.new_rect
        # print(ii.content)

        # if e.type == "mousedown" else "SteelBlue"
        # width = 30
        # height = 20
        # x = e.image_x - width / 2
        # y = e.image_y - height / 2
        # ui.notify(f"{e.type} at ({e.image_x:.1f}, {e.image_y:.1f})")


drawer = RectDrawer()

src = "https://picsum.photos/id/565/640/360"
ii = ui.interactive_image(
    src,
    on_mouse=drawer.mouse_handler,
    events=["mousedown", "mouseup", "mousemove"],
    cross=True,
)


ui.run()
