from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.cluster import KMeans
import cv2

# Directory containing your dataset
dataset_dir = '/home/trg1/alok/model/croppedimages'

# Directory to save the segmented images
segmented_dir = '/home/trg1/alok/model/segmentedimages'

# Ensure the output directories exist
os.makedirs(segmented_dir, exist_ok=True)

# Iterate over all images in the dataset directory
for filename in os.listdir(dataset_dir):
    # Check if the file is an image
    if filename.endswith('.png') or filename.endswith('.jpg'):
        # Construct the full file path
        filepath = os.path.join(dataset_dir, filename)
        
        # Load the image
        img = cv2.imread(filepath, 0)

        # Apply the median filter
        median_filtered_img = cv2.medianBlur(img, ksize=3)

        # Normalize the image
        normalized_img = cv2.normalize(median_filtered_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

        # Reshape the image to be a list of pixel intensities
        pixels = normalized_img.reshape(-1, 1)

        adaptive_thresh_img = cv2.adaptiveThreshold(normalized_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

        # Perform K-means clustering
        kmeans = KMeans(n_clusters=7, random_state=0).fit(pixels)

        # Replace each pixel with its cluster center
        segmented_img = kmeans.cluster_centers_[kmeans.labels_].reshape(normalized_img.shape).astype(np.uint8)

        # Save the segmented image
        cv2.imwrite(os.path.join(segmented_dir, 'segmented_' + filename), segmented_img)