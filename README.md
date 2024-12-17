
# **Cyclist Detection Playground Database**

This repository provides a flexible and efficient application to interact with an **image database** for cyclist detection. The application supports querying, fetching, previewing, and downloading image data annotated in **YOLO format**. It is ideal for developers working on object detection projects who need organized and filtered data to train and validate their machine learning models.

---

## **1. Introduction**

The Cyclist Detection Playground allows developers to:
- Access and download cyclist images with bounding box annotations.
- Preview and filter data interactively.
- Retrieve specific subsets of the data (e.g., for train, validation, and test splits).

We designed the application to maximize **storage efficiency** and **flexibility** using a **PostgreSQL database** for metadata and an **Amazon S3-like storage** for image files.

---

## **2. Features**

### **Current Features**
1. **Fetch and Download Data**  
   Retrieve any number of images and labels in YOLO format with options to:
   - Filter data by class (default: cyclist, class `0`).
   - Split data into train/val/test sets with customizable ratios.

2. **Generate Statistics**  
   View key statistics about the database:
   - Total number of images.
   - Class distribution with bounding box counts.  
   Example:
   ```
   Total Images: 32,028
   Class Distribution:
     Class '0': 49,657 bounding boxes
   ```

3. **Preview Data**  
   - **Random Image Preview**: View a random image with all bounding boxes drawn.
   - **Preview by Class**: View images containing a specific class.

### **Future Features (Planned)**
1. **Data Filtering and Querying**  
   - Filter images by resolution, bounding box count, or other criteria.
2. **Data Augmentations**  
   - On-the-fly augmentations like flipping, rotation, cropping, etc.
3. **Dataset Versioning**  
   - Save snapshots of datasets with applied filters for reproducible experiments.
4. **Annotation Validation Tools**  
   - Detect invalid or zero-sized bounding boxes.
5. **Multi-Format Export**  
   - Support exporting data in COCO JSON, Pascal VOC XML, and CSV formats.
6. **Streamlit UI**  
   - A visual interface for browsing, filtering, and downloading the data.

---

## **3. Data Sources**

The dataset has been curated from the following publicly available resources:
1. [Roboflow: Bike Detection Dataset](https://universe.roboflow.com/bicycle-detection/bike-detect-ct/dataset/5#)
2. [Kaggle: Cyclist Dataset](https://www.kaggle.com/datasets/semiemptyglass/cyclist-dataset)

---

## **4. Database Design**

The database consists of two primary tables in PostgreSQL: `images` and `annotations`.

### **Table: `images`**
Stores metadata for each image, including file path and dimensions.

```sql
CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    width INT NOT NULL,
    height INT NOT NULL,
    split VARCHAR(10) CHECK (split IN ('train', 'val', 'test'))
);
```

### **Table: `annotations`**
Stores bounding box annotations in **YOLO format**.

```sql
CREATE TABLE annotations (
    id SERIAL PRIMARY KEY,
    image_id INT REFERENCES images(id) ON DELETE CASCADE,
    x_center FLOAT NOT NULL, -- Bounding box center X (relative)
    y_center FLOAT NOT NULL, -- Bounding box center Y (relative)
    width FLOAT NOT NULL,    -- Bounding box width (relative)
    height FLOAT NOT NULL,   -- Bounding box height (relative)
    class_name TEXT NOT NULL -- Class label (default: 0 for cyclists)
);
```

### **Why This Design?**
- **Storage Efficiency**: Storing relative bounding box coordinates is compact and scalable.
- **Flexibility**: Images and annotations are decoupled, making it easier to query, filter, and update.

### **Storage Strategy**
- Images are stored as folders in an **Amazon S3-like storage system** for cost-effective and scalable access.
- Metadata and annotations are managed through PostgreSQL for fast querying and filtering.

---

## **5. How to Use**

### **Setup**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/cyclist-database-playground.git
   cd cyclist-database-playground
   ```
2. Set up PostgreSQL and create the database schema using the SQL commands provided above.

3. Install required Python libraries:
   ```bash
   pip install psycopg2 pillow
   ```

4. Configure database settings in the script:
   ```python
   db_config = {
       "host": "localhost",
       "database": "your_database_name",
       "user": "your_username",
       "password": "your_password",
       "port": 5432
   }
   ```

---

### **Usage Examples**

#### **Fetch and Download Data**
Fetch 1000 images and labels split into train/val/test folders:
```python
fetch_and_download_data(db_config, output_folder="output_data", num_images=1000)
```

#### **Generate Statistics**
View statistics about the dataset:
```python
generate_statistics(db_config)
```

#### **Preview a Random Image**
Preview an image with bounding boxes drawn:
```python
preview_random_image(db_config)
```

#### **Preview Images by Class**
View images containing the specified class (e.g., cyclists):
```python
preview_image_by_class(db_config, class_name='0')
```

---

## **6. Future Applications**

In addition to the current features, we envision expanding the application with the following functionalities. These additions will make the Cyclist Detection Playground even more versatile and powerful for data scientists, ML engineers, and developers.

---

### **1. On-the-Fly Data Augmentations**

Provide developers with augmented data to test model robustness and improve generalization during training.

- **Supported Augmentations**: Flipping, Rotation, Cropping, Color Adjustments, and more.
- Save augmented images alongside the original data into structured folders.

**Example Use Case**: A developer can request augmented data during fetching.

```python
fetch_and_download_data(num_images=500, augment=True, augment_types=["flip", "rotate"])
```

**Output**: Augmented data is saved into structured folders:
```
output_data/
├── train/
│   ├── images/
│   ├── labels/
├── train_aug/
│   ├── images/
│   ├── labels/
```

---

### **2. Versioning and Dataset Snapshots**

Allow users to **version datasets** or take snapshots of their data during experiments.

- Store metadata such as applied filters and splits (e.g., "500 images, class=0 only").
- Maintain a **dataset history log** for reproducibility.

**Example**:

```python
create_dataset_version("v1.0", filters={"classes": ["0"], "image_count": 500})
```

**Output**:
- Metadata and filters are stored in the database.
- Users can download specific versions of the dataset.

---

### **3. Annotation Validation Tools**

Provide built-in tools to **validate YOLO annotations** for quality control.

- **Features**:
  - Check for invalid bounding boxes (e.g., coordinates exceeding image bounds).
  - Detect zero-sized bounding boxes.
  - Highlight overlapping or redundant bounding boxes.
- Generate a **validation report**.

**Example**:

```python
validate_annotations()
```

**Output**:
```yaml
Invalid Bounding Boxes:
  - image_0005.txt: x_max > image width

Zero-Sized Boxes:
  - image_0012.txt: width = 0
```

---

### **4. Real-Time Data Exploration with Streamlit**

Build a **Streamlit-based UI** to enable real-time data exploration and visualization.

- Browse images with bounding boxes interactively.
- Apply filters (e.g., filter by class, resolution, or dataset splits).
- Download filtered data directly from the UI.

**Benefits**:
- A visual playground for non-technical team members.
- Easy interaction without modifying code.

---

### **5. Monitoring Data Usage**

Track and analyze how developers are interacting with the database.

- **Log Statistics**:
  - Most downloaded classes.
  - Popular data splits (train/val/test ratios).
- Use these insights to identify underrepresented classes or trends.

**Example Query**:

```sql
SELECT COUNT(*) AS download_count, class_name
FROM annotations
GROUP BY class_name;
```

**Use Case**:  
If "class 0" (cyclist) is downloaded most often, we can prioritize adding data for underrepresented classes.

---

### **6. Integration with Model Training Pipelines**

Streamline the workflow by preparing data for popular training frameworks.

- Automatically generate preformatted **train/val/test splits** for YOLO, TensorFlow, and PyTorch.
- Create **data configuration files** needed for training.

**Example for YOLO**:

**Generated Config**:
```yaml
train: /path/to/train/images
val: /path/to/val/images
test: /path/to/test/images
nc: 1
names: ['cyclist']
```

**Feature**:

```python
generate_training_config(format="yolo")
```

---

### **7. Export Data in Multiple Formats**

Support exporting data in different annotation formats for compatibility across frameworks.

- **Supported Formats**:
  - YOLO: Default format.
  - Pascal VOC (XML).
  - COCO JSON.
  - CSV.

**Example**:

```python
fetch_and_download_data(output_format="coco")
```

**Benefit**: Developers can seamlessly switch between frameworks like YOLO, Faster R-CNN, or SSD without reformatting their annotations.

---

### **Why These Features?**

The proposed features aim to:
- **Improve Usability**: Simplify interactions with the database and data.
- **Enhance Flexibility**: Support multiple ML frameworks, formats, and use cases.
- **Optimize Workflow**: Reduce manual overhead for dataset preparation and validation.
- **Ensure Data Quality**: Provide tools for validation and augmentation.

---

By implementing these features, the Cyclist Detection Playground will become a complete, end-to-end solution for managing, preparing, and deploying cyclist detection datasets.

Contributions and suggestions for these future features are welcome! 🚀


---

## **7. Contributing**

Contributions are welcome! Please open an issue or submit a pull request if you'd like to:
- Add new features.
- Improve the codebase.
- Report bugs.

---

## **8. License**

This project is licensed under the MIT License.
