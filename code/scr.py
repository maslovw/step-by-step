from pynput import mouse
from PIL import ImageGrab, ImageDraw, Image
import datetime
import Quartz

def get_display_resolution():
    main_display = Quartz.CGDisplayBounds(Quartz.CGMainDisplayID())
    width = int(main_display.size.width)
    height = int(main_display.size.height)
    return width, height

def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at ({x}, {y}) with {button}")
        take_screenshot(int(x), int(y))

def take_screenshot(x, y, region_w=1000, region_h=500):
    # Get the current display resolution
    screen_width, screen_height = get_display_resolution()

    # Define the region around the cursor
    left = max(0, x - region_w // 2)
    top = max(0, y - region_h // 2)
    right = min(screen_width, x + region_w // 2)
    bottom = min(screen_height, y + region_h // 2)

    # Capture the screenshot
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))

    # Create a new image for the circle
    circle_diameter = 60
    circle_radius = circle_diameter // 2
    circle_image = Image.new("RGBA", (circle_diameter, circle_diameter), (0, 0, 0, 0))
    draw = ImageDraw.Draw(circle_image)
    draw.ellipse((0, 0, circle_diameter, circle_diameter), fill=(0, 255, 0, 128))  # Green with 50% transparency

    # Composite the circle image onto the screenshot
    circle_position = (x - left - circle_radius, y - top - circle_radius)
    screenshot.paste(circle_image, circle_position, circle_image)

    # Save the screenshot with a timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot.save(f"screenshot_{timestamp}.png")

# Create a listener
with mouse.Listener(on_click=on_click) as listener:
    listener.join()
