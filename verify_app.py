import os
import django
from django.test import RequestFactory
from django.urls import reverse

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luminaria_web.settings')
django.setup()

from risk_analysis.views import index
from risk_analysis.services import RiskPredictor

def verify_setup():
    print("1. Verifying ML Service...")
    predictor = RiskPredictor()
    # Test valid data
    test_data = {
        'semestre_ord': '1er - 3er',
        'desmotivacion_bin': 'Sí',
        'considerado_abandonar_bin': 'Sí',
        'dificultades_economicas_bin': 'Sí',
        'empleo_ord': 'Sí, medio tiempo',
        'impacto_laboral_ord': 'No afecta/No trabajo',
        'reprobo_materias_bin': 'Sí',
        'apoyo_institucional_ord': 'Algunas veces',
        'satisfaccion_servicios_ord': 'Insatisfecho/a',
        'actividades_extracurriculares_ord': 'Nunca'
    }
    
    try:
        result = predictor.predict(test_data)
        print(f"   Prediction success! Result: {result}")
    except Exception as e:
        print(f"   Prediction FAILED: {e}")
        return False

    print("\n2. Verifying Views...")
    factory = RequestFactory()
    
    # Test GET
    request_get = factory.get('/')
    response_get = index(request_get)
    if response_get.status_code == 200:
        print("   GET / (Index) - OK")
    else:
        print(f"   GET / (Index) - FAILED {response_get.status_code}")
        return False

    # Test POST
    request_post = factory.post('/', test_data)
    response_post = index(request_post)
    if response_post.status_code == 200:
        print("   POST / (Prediction) - OK")
        # Check if result is in content (basic check)
        if b'An\xc3\xa1lisis Completado' in response_post.content or b'class="result-badge' in response_post.content:
             print("   Result template rendered.")
        else:
             print("   WARNING: content might be missing result.")
    else:
        print(f"   POST / (Prediction) - FAILED {response_post.status_code}")
        return False
        
    return True

if __name__ == "__main__":
    success = verify_setup()
    if success:
        print("\nVerification PASSED.")
    else:
        print("\nVerification FAILED.")
