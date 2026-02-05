import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from django.conf import settings
from sklearn.base import BaseEstimator, TransformerMixin

# Definición de la clase necesaria para cargar el pipeline
# Se replica exactamente como fue definida en el entrenamiento
class BinarioMapper(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.maps = {
            'dificultades_economicas_bin': {'Sí': 1, 'No': 0},
            'reprobo_materias_bin': {'Sí': 1, 'No': 0}
        }
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        X_ = X.copy()
        for col, mapping in self.maps.items():
            X_[col + '_bin'] = X_[col].map(mapping)
        return X_[[col + '_bin' for col in self.maps]]

# Hack para que joblib encuentre la clase si fue guardada en __main__
import sys
if '__main__' in sys.modules:
    setattr(sys.modules['__main__'], 'BinarioMapper', BinarioMapper)

class RiskPredictor:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RiskPredictor, cls).__new__(cls)
            cls._instance._load_models()
        return cls._instance

    def _load_models(self):
        # Rutas relativas a la raíz del proyecto (donde está manage.py o un nivel arriba)
        # Asumiendo estructura: /project/modelos y /project/luminaria_web
        # BASE_DIR en settings suele apuntar a /project/luminaria_web/ (donde está settings) o /project/
        # En settings.py: BASE_DIR = Path(__file__).resolve().parent.parent 
        # Si settings está en luminaria_web/settings.py, parent.parent es la raíz del repo.
        self.base_dir = settings.BASE_DIR
        self.models_dir = self.base_dir / 'modelos'
        
        try:
            self.pipeline = joblib.load(self.models_dir / 'svm_preprocessor.joblib')
            self.model = joblib.load(self.models_dir / 'svm_optimized.joblib')
        except FileNotFoundError as e:
            print(f"Error loading models: {e}")
            raise e
        except Exception as e:
            print(f"Error loading pickle: {e}")
            # Intento de corrección si falla por namespace
            import __main__
            __main__.BinarioMapper = BinarioMapper
            self.pipeline = joblib.load(self.models_dir / 'svm_preprocessor.joblib')
            self.model = joblib.load(self.models_dir / 'svm_optimized.joblib')


    def predict(self, data_dict):
        """
        Recibe un diccionario con las respuestas y devuelve la predicción.
        """
        # Crear DataFrame con una sola fila
        df = pd.DataFrame([data_dict])
        
        # Transformar
        try:
            X_encoded = self.pipeline.transform(df)
            
            # El pipeline devuelve un array numpy o dataframe?
            # En el notebook: pipeline.transform(X_test) -> array si tiene steps finales, 
            # pero aquí 'pipeline' es el preprocessor (ColumnTransformer) probablemente?
            # El notebook dice: preprocessor = ColumnTransformer(...) 
            # pipeline (variable) = Pipeline([('pre', preprocessor), ('scaler', ...)])
            # Pero el archivo se llama 'svm_preprocessor.joblib'. 
            # Es posible que contenga solo el preprocessor o el pipeline completo sin el estimador.
            # Verificaremos si tiene predict.
            
            # Si 'svm_preprocessor.joblib' es solo el preprocesamiento:
            # X_encoded = self.pipeline.transform(df)
            # prediction = self.model.predict(X_encoded)
            
            # En el notebook, svm_optimized.joblib podria ser el modelo (SVC) o el Pipeline completo?
            # Normalmente se guarda el pipeline completo como 'model.joblib'.
            # Pero los nombres sugieren separación.
            
            prediction_code = self.model.predict(X_encoded)[0]
            
            return prediction_code
        except Exception as e:
            print(f"Prediction error: {e}")
            raise e

