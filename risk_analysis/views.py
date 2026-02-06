from django.shortcuts import render, redirect
from .forms import QuestionnaireForm
from .services import RiskPredictor

def landing(request):
    return render(request, 'risk_analysis/landing.html')

def index(request):
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            # Extraer datos limpios
            data = form.cleaned_data
            
            try:
                # Instanciar servicio y predecir
                predictor = RiskPredictor()
                result = predictor.predict(data)
                
                # Mapear resultado a texto legible si es necesario
                # Asumiendo que result es el string de la clase (e.g. 'Alto Riesgo', 'Bajo Riesgo')
                # Si el modelo devuelve números, habría que mapear aquí.
                
                return render(request, 'risk_analysis/result.html', {'result': result})
            except Exception as e:
                # En producción manejaríamos esto mejor
                return render(request, 'risk_analysis/error.html', {'error': str(e)})
    else:
        form = QuestionnaireForm()

    return render(request, 'risk_analysis/index.html', {'form': form})
