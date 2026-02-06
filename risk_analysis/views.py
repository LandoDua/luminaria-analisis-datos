from django.shortcuts import render, redirect
from .forms import QuestionnaireForm
from .services import RiskPredictor

def landing(request):
    return render(request, 'risk_analysis/landing.html')

def index(request):
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                predictor = RiskPredictor()
                result = predictor.predict(data)
                
                # PRG Pattern: Store result in session and redirect
                request.session['risk_result'] = result
                return redirect('result')
            except Exception as e:
                # En producción manejaríamos esto mejor
                return render(request, 'risk_analysis/error.html', {'error': str(e)})
    else:
        form = QuestionnaireForm()

    return render(request, 'risk_analysis/index.html', {'form': form})

def result(request):
    """
    Vista para mostrar el resultado recuperándolo de la sesión.
    Evita el reenvío del formulario al refrescar.
    """
    result = request.session.get('risk_result')
    
    if not result:
        # Si no hay resultado en sesión, redirigir al cuestionario
        return redirect('questionnaire')
        
    # Opcional: Limpiar la sesión si queremos que el resultado sea efímero
    # del request.session['risk_result'] 
    
    return render(request, 'risk_analysis/result.html', {'result': result})
