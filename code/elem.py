from pynput import mouse
import Quartz
import datetime

def get_element_under_cursor():
    # Get the location of the cursor
    location = Quartz.CGEventGetLocation(Quartz.CGEventCreate(None))
    x, y = int(location.x), int(location.y)

    # Get the UI element under the cursor
    system_element = Quartz.AXUIElementCreateSystemWide()
    result, ax_element = Quartz.AXUIElementCopyElementAtPosition(system_element, x, y)

    if result == Quartz.kAXErrorSuccess:
        # Get the description of the UI element
        result, description = Quartz.AXUIElementCopyAttributeValue(ax_element, Quartz.kAXDescriptionAttribute, None)
        if result == Quartz.kAXErrorSuccess and description is not None:
            return description
        else:
            # Fallback to title or value if description is not available
            result, title = Quartz.AXUIElementCopyAttributeValue(ax_element, Quartz.kAXTitleAttribute, None)
            if result == Quartz.kAXErrorSuccess and title is not None:
                return title

            result, value = Quartz.AXUIElementCopyAttributeValue(ax_element, Quartz.kAXValueAttribute, None)
            if result == Quartz.kAXErrorSuccess and value is not None:
                return value

    return None

def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at ({x}, {y}) with {button}")
        element_text = get_element_under_cursor()
        if element_text:
            print(f"Text under cursor: {element_text}")

# Create a listener
with mouse.Listener(on_click=on_click) as listener:
    listener.join()
