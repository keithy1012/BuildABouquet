import numpy as np
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

current_directory = os.path.dirname(__file__)
FILE_PATH = os.path.join(current_directory, 'hsv_desc.csv')

# A Neural Network trained to convert HSV values into a list of adjective descriptions. 
class HSVAdjectiveNN:
    def __init__(self, epochs=50, batch_size=32, random_state=42):
        """
        Initializes and trains the neural network model for predicting adjectives based on HSV values.
        
        :param epochs: Number of epochs for training the model.
        :param batch_size: Batch size for training.
        :param random_state: Random seed for reproducibility.
        """
        df = pd.read_csv(FILE_PATH, sep=',')

        hsv_values = df[['hue', 'saturation', 'value']].values
        adjectives = df['adjective_list'].apply(lambda x: eval(x) if pd.notnull(x) else [])


        self.epochs = epochs
        self.batch_size = batch_size
        self.random_state = random_state
        self.mlb = MultiLabelBinarizer()
        self.mlb.fit_transform(adjectives)
        print(self.mlb.classes_)
        self.model = self._build_model(self.mlb.classes_)

        self.X, self.y = self._preprocess_data(hsv_values, adjectives)
        self._train()

    # Builds and compiles a Keras neural network model. 
    def _build_model(self, classes):
        model = Sequential([
            Dense(64, input_dim=3, activation='relu'),
            Dense(32, activation='relu'),
            Dense(len(classes), activation='sigmoid')
        ])
        
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model

    # Preprocesses the input data (hue, saturation, value, adjectives)
    def _preprocess_data(self, hsv_values, adjectives):
        X = np.array(hsv_values)
        y = self.mlb.fit_transform(adjectives)
        return X, y

    # Training the neural network on the input data. 
    def _train(self):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=self.random_state)

        history = self.model.fit(X_train, y_train, epochs=self.epochs, batch_size=self.batch_size, validation_split=0.1)
        
        loss, accuracy = self.model.evaluate(X_test, y_test)
        #print(f"Test Loss: {loss:.4f}, Test Accuracy: {accuracy:.4f}")

    # Predicts the list of adjectives given a HSV value. 
    def predict(self, hsv):
        hsv = np.array(hsv).reshape(-1, 3) 
        prediction = self.model.predict(hsv)
        if prediction is None or prediction.size == 0:
            raise ValueError("Model prediction returned None or empty result.")
        predicted_classes = (prediction > 0.5).astype(int)
        adjectives = self.mlb.inverse_transform(predicted_classes)
        print("Predicted adjectives for HSV values", hsv, ":", adjectives)
        return adjectives

    # Predicts the list of adjectives for a weighted list of HSV values in a picture. 
    def predict_weighted(self, top_colors):
        total_count = sum(count for _, count in top_colors)
        weighted_hsv = np.zeros(3)
        
        for (hsv_color, count) in top_colors:
            weighted_hsv += np.array(hsv_color) * count
        
        weighted_hsv /= total_count
        
        weighted_hsv = weighted_hsv.reshape(1, -1)
        return self.predict(weighted_hsv)