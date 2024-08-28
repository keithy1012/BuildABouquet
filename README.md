# Build A Bouquet

## Overview

"Build A Bouquet" is a comprehensive application designed to streamline the process of selecting and visualizing flowers based on user preferences.

### Technologies Used

- **BeautifulSoup & Requests**: Retrieve flowers by month from online sources.
- **DynamoDB & S3**: Store flower names and images efficiently.
- **NTLK**: Processes user input to be processed.
- **Tensorflow & Keras**: Developed a Neural Network to predict a list of adjectives given a HSV value.
- **numpy & Pandas**: Used to compute various intermediary values and data transformation.
- **PIL & OpenCV**: Works on various flower image computations, such as contour definition.
- **PyTorch, Transformers & Open3D**: Converts a 2D Image into a 3D mesh (point cloud processing)

## Process

### Pre-requisite: Installing Dependencies

- `pip install -r requirements.txt`

### Step 1: Fetching the Data

- `python fetch_data.py` fetches and stores data in AWS S3 and DynamoDB using `db/s3.py` and `db/dynamodb.py`

### Step 2: Filtering and finding the best flowers given a user input

- `python main.py`

#### a. User Input and Processing

- `utils/userInputProcessor.py` uses NLTK punkt and averaged_perceptron_tagger to break up user inputs.

#### b. Filtering Flowers Based on User Selection

- `utils/filterUtil.py` filters all flowers based on months and adjectives gathered from user processing.
- `utils/flowerUtil.py` contains methods to compuete the main colors of flowers.
- ` utils/model.py` contains a Neural Network that converts colors from `utils/flowerUtil.py` into a list of adjectives used in `utils/filterUtil.py`

#### c. Display Filtered Flowers

- `FlowerCanvas.py` displays the filtered flowers with id's for users to select from.

### Step 3: Generate 3D Models from 2D Images

- `3dmodel.py`

### TODO: Implement AR capability
