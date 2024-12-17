
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

This application can be extended to include:
- **Data Filtering**: Retrieve specific subsets of images based on resolution, bounding box count, etc.
- **Data Augmentations**: Generate augmented data for improving model robustness.
- **Multi-Format Export**: Convert the dataset to COCO, Pascal VOC, or CSV formats.
- **Annotation Validation**: Detect and report issues in labels.
- **Streamlit UI**: A visual playground to browse, filter, and download the dataset.
- **Usage Monitoring**: Track download counts and popular classes for analysis.

---

## **7. Contributing**

Contributions are welcome! Please open an issue or submit a pull request if you'd like to:
- Add new features.
- Improve the codebase.
- Report bugs.

---

## **8. License**

This project is licensed under the MIT License.
