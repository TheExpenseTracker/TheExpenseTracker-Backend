import joblib
from sklearn.linear_model import LinearRegression
import numpy as np

class LinearRegressionPredictor:
    def __init__(self, model_path):
        self.model = self.load_model(model_path)

    def load_model(self, model_path):
        try:
            model = joblib.load(model_path)
            return model
        except Exception as e:
            raise Exception(f"Error loading the model from {model_path}: {e}")


    def predict(self, input_data):
        input_data = np.array(input_data).reshape(1, -1)
        predictions = self.model.predict(input_data)
        return predictions[0]