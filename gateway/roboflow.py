import asyncio
import cv2
import random
from inference_sdk import InferenceHTTPClient


def resize_image(image, max_width, max_height):
    height, width = image.shape[:2]
    if width > max_width or height > max_height:
        scaling_factor = min(max_width / width, max_height / height)
        new_width = int(width * scaling_factor)
        new_height = int(height * scaling_factor)
        resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        return resized_image
    return image


def get_random_contrast_color():
    # Generate a random color that is contrasting with white by limiting the maximum value of each component
    return (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))


def draw_bounding_boxes(image, boxes):
    class_colors = {}
    for box in boxes:
        x, y, w, h = int(box['x'] - box['width'] / 2), int(box['y'] - box['height'] / 2), int(box['width']), int(
            box['height'])
        confidence = box['confidence']

        # Get a color for the class, generate a new one if it doesn't exist
        label = box['class']
        if label not in class_colors:
            class_colors[label] = get_random_contrast_color()
        color = class_colors[label]

        # Draw the bounding box with a thinner line
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 1)  # Changed line: thickness set to 1

        # Draw the class id and confidence
        text = f"{label} {int(confidence * 100)}%"
        (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_TRIPLEX, 0.4, 1)
        # Ensure the text is always on top by using a thicker rectangle and then overlaying the text
        cv2.rectangle(image, (x, y - text_height - 5), (x + text_width, y), color, -1)
        cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1)


# Load the image
image_file = "../original.jpg"
image = cv2.imread(image_file)

# Resize the image to a smaller resolution if necessary
max_width = 1000
max_height = 1000
image = resize_image(image, max_width, max_height)

# Initialize the client
client = InferenceHTTPClient(
    api_url="https://upm.penki.tech",
    api_key="DkNxM1dr7CMBhEo90xrB"
)

# Run inference
loop = asyncio.get_event_loop()
result = loop.run_until_complete(
    client.infer_async(image, model_id="samolet-init/1")
)

# Print textual results
print(result)

# Draw bounding boxes on the image if predictions are present in the result
if 'predictions' in result:
    draw_bounding_boxes(image, result['predictions'])
    # Save or display the image with bounding boxes
    output_file = "../img_with_boxes.png"
    cv2.imwrite(output_file, image)
    print(f"Image with bounding boxes saved to {output_file}")
else:
    print("No predictions found in the result.")
