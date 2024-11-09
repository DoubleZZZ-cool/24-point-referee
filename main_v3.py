import cv2
import pytesseract
from PIL import Image

def preprocess_image(image_path):
    # Read the image using OpenCV
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use adaptive thresholding to create a binary image
    binary = cv2.adaptiveThreshold(
        blurred, 255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )

    # Save the preprocessed image for reference
    cv2.imwrite('preprocessed_image.png', binary)

    return binary

def recognize_card_numbers(image_path):
    # Preprocess the image
    preprocessed_image = preprocess_image(image_path)

    # Convert the preprocessed image to PIL format
    pil_image = Image.fromarray(preprocessed_image)

    # Use pytesseract to detect the bounding boxes of the characters
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
    detected_boxes = pytesseract.image_to_boxes(pil_image, config=custom_config)

    # Store recognized numbers and their positions
    recognized_numbers = []

    # Parse detected boxes
    for line in detected_boxes.splitlines():
        char, x, y, w, h, _ = line.split()
        if char.isdigit():
            recognized_numbers.append((char, int(x)))

    # Sort recognized numbers by their x-position (left to right)
    recognized_numbers = sorted(recognized_numbers, key=lambda x: x[1])

    # Extract only the digits from the sorted list
    recognized_digits = [num[0] for num in recognized_numbers]

    # Return the first 4 recognized digits, or as many as are available
    return recognized_digits[:4]

# Example usage
if __name__ == "__main__":
    image_path = 'test2.png'  # Replace with your image file path
    card_numbers = recognize_card_numbers(image_path)
    print(f"Recognized Card Numbers: {card_numbers}")
