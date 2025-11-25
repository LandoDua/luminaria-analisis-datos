# Como el pipeline fue contruido en base a un DataFrame
# y en base a un BaseEstimator personalizado, es necesario
# replicar esas partes aquí para poder usar el pipeline

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder

binarias = ['dificultades_economicas_bin', 'reprobo_materias_bin']
ordinales = {
    'semestre_ord': ['1er - 3er', '4to - 6to', '7mo o más'],
    'apoyo_institucional_ord': ['Nunca', 'Algunas veces', 'Siempre'],
    'satisfaccion_servicios_ord': ['Muy insatisfecho/a', 'Insatisfecho/a', 'Satisfecho/a', 'Muy satisfecho/a'],
    'actividades_extracurriculares_ord': ['Nunca', 'Algunas veces', 'Sí, frecuentemente']
}
onehot = ['empleo_ord', 'impacto_laboral_ord']


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

preprocessor = ColumnTransformer(
    transformers=[
        # Binarias
        ('bin', BinarioMapper(), binarias),
        # Ordinales
        ('ord', OrdinalEncoder(categories=[ordinales[k] for k in ordinales], dtype=int),
         list(ordinales.keys())),
        # One-hot
        ('onehot', OneHotEncoder(drop='first', sparse_output=False, dtype=int), onehot)
    ]
)

if __name__ == '__main__':
    pipeline = Pipeline([
        ('pre', preprocessor),
        ('scaler', StandardScaler())
    ])