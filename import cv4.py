import cv2
import numpy as np
import matplotlib.pyplot as plt
def display_image(title, image):
    """Utility function to display an image."""
    plt.figure(figsize=(8, 8))
    if len(image.shape) == 2:
        plt.imshow(image, cmap='gray')
    else:
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.show()

def interactive_edge_detection(image_path):
    """Interactive activity for edge detection and filtering."""
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found!")
        return

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    display_image("Original Grayscale Image", gray_image)