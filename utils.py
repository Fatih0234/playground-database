import os
import random
import psycopg2
import shutil
from PIL import Image, ImageDraw

# TODO: Annotations also need to be fetched with images, has to be done

def fetch_and_download_data(db_config, output_folder, num_images, split_data=True, 
                            train_ratio=0.8, val_ratio=0.1, test_ratio=0.1, filter_classes=None):
    """
    Fetches a specified number of images and labels (YOLO format) from the database, splits them, 
    filters by class (if specified), and downloads the data.
    """
    # Connect to the database
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # Define SQL query with class filtering
    if filter_classes is None:
        filter_classes = ['0']  # Default to class 0 (cyclists)

    format_classes = tuple(filter_classes)
    class_filter_query = """
        SELECT i.file_path, a.x_center, a.y_center, a.width, a.height, a.class_name
        FROM images i
        JOIN annotations a ON i.id = a.image_id
        WHERE a.class_name IN %s
        LIMIT %s;
    """

    # Fetch filtered records
    cursor.execute(class_filter_query, (format_classes, num_images))
    records = cursor.fetchall()
    random.shuffle(records)  # Shuffle for randomness

    # Define output paths
    train_images = os.path.join(output_folder, "train", "images")
    train_labels = os.path.join(output_folder, "train", "labels")
    val_images = os.path.join(output_folder, "val", "images")
    val_labels = os.path.join(output_folder, "val", "labels")
    test_images = os.path.join(output_folder, "test", "images")
    test_labels = os.path.join(output_folder, "test", "labels")

    # Create folders
    folders = [train_images, train_labels, val_images, val_labels, test_images, test_labels]
    if not split_data:  # Single output folder
        folders = [os.path.join(output_folder, "images"), os.path.join(output_folder, "labels")]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

    # Split data
    total_records = len(records)
    train_count = int(total_records * train_ratio)
    val_count = int(total_records * val_ratio)

    splits = {
        "train": records[:train_count],
        "val": records[train_count:train_count + val_count],
        "test": records[train_count + val_count:]
    }

    if not split_data:
        splits = {"all": records}

    # Copy files and write YOLO labels
    label_data = {}
    for split_name, data in splits.items():
        image_folder = os.path.join(output_folder, split_name, "images") if split_data else folders[0]
        label_folder = os.path.join(output_folder, split_name, "labels") if split_data else folders[1]

        for file_path, x_center, y_center, width, height, class_name in data:
            file_name = os.path.basename(file_path)

            # Copy image
            shutil.copy(file_path, os.path.join(image_folder, file_name))

            # Prepare label content in YOLO format
            if file_name not in label_data:
                label_data[file_name] = []
            label_data[file_name].append(f"{class_name} {x_center} {y_center} {width} {height}")

            # Write label file
            label_file = os.path.splitext(file_name)[0] + ".txt"
            with open(os.path.join(label_folder, label_file), "w") as f:
                f.write("\n".join(label_data[file_name]))

    print(f"Data ({num_images} images) exported successfully to {output_folder}.")

    cursor.close()
    conn.close()


def generate_statistics(db_config):
    """
    Generates statistics for the dataset, including class distribution and image count.
    """
    # Connect to the database
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # Count total images
    cursor.execute("SELECT COUNT(*) FROM images;")
    total_images = cursor.fetchone()[0]

    # Class distribution
    cursor.execute("""
        SELECT class_name, COUNT(*) 
        FROM annotations 
        GROUP BY class_name;
    """)
    class_counts = cursor.fetchall()

    # Print statistics
    print(f"Total Images: {total_images}")
    print("Class Distribution:")
    for class_name, count in class_counts:
        print(f"  Class '{class_name}': {count} bounding boxes")

    cursor.close()
    conn.close()


def preview_random_image(db_config):
    """
    Displays a random image with all bounding boxes drawn.
    """
    # Connect to the database
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # Fetch a random image and all its annotations
    cursor.execute("""
        SELECT i.file_path, a.x_center, a.y_center, a.width, a.height, a.class_name
        FROM images i
        JOIN annotations a ON i.id = a.image_id
        WHERE i.id = (
            SELECT id FROM images ORDER BY RANDOM() LIMIT 1
        );
    """)
    records = cursor.fetchall()

    if not records:
        print("No data available.")
        return

    # Load image
    file_path = records[0][0]
    image = Image.open(file_path)
    draw = ImageDraw.Draw(image)

    # Draw all bounding boxes for this image
    for _, x_center, y_center, width, height, class_name in records:
        img_width, img_height = image.size
        x_min = int((x_center - width / 2) * img_width)
        y_min = int((y_center - height / 2) * img_height)
        x_max = int((x_center + width / 2) * img_width)
        y_max = int((y_center + height / 2) * img_height)

        # Draw bounding box
        draw.rectangle([x_min, y_min, x_max, y_max], outline="red", width=2)
        draw.text((x_min, y_min - 10), f"{class_name}", fill="red")

    # Display the image with all bounding boxes
    image.show()
    cursor.close()
    conn.close()
    print(f"Displayed image with bounding boxes from: {file_path}")
