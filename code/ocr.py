from pynput import mouse
from PIL import ImageGrab, ImageDraw, Image
import datetime
import Quartz
import Vision
import io

def get_display_resolution():
    main_display = Quartz.CGDisplayBounds(Quartz.CGMainDisplayID())
    width = int(main_display.size.width)
    height = int(main_display.size.height)
    return width, height

def perform_ocr(image):
    # Convert PIL image to bytes
    with io.BytesIO() as output:
        image.save(output, format="PNG")
        image_data = output.getvalue()

    # Create a VNImageRequestHandler with the image data
    request_handler = Vision.VNImageRequestHandler.alloc().initWithData_options_(image_data, None)

    # Create a VNRecognizeTextRequest
    request = Vision.VNRecognizeTextRequest.alloc().init()

    # Perform the request
    success, error = request_handler.performRequests_error_([request], None)

    if not success:
        print(f"OCR Error: {error}")
        return None

    # Extract text from the request results
    observations = request.results()
    recognized_text = []
    for observation in observations:
        recognized_text.append(observation.topCandidates_(1)[0].string())

    return "\n".join(recognized_text)

def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at ({x}, {y}) with {button}")
        take_screenshot_and_ocr(int(x), int(y))

def take_screenshot_and_ocr(x, y, region_size=1000):
    # Get the current display resolution
    screen_width, screen_height = get_display_resolution()

    # Define the region around the cursor
    left = max(0, x - region_size // 2)
    top = max(0, y - region_size // 2)
    right = min(screen_width, x + region_size // 2)
    bottom = min(screen_height, y + region_size // 2)

    # Capture the screenshot
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))

    # Draw a semi-transparent green circle
    circle_diameter = 100
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

    # Perform OCR on the screenshot
    text = perform_ocr(screenshot)
    if text:
        print(f"Recognized text: {text}")

# Create a listener
with mouse.Listener(on_click=on_click) as listener:
    listener.join()
