from django import forms

class QuestionnaireForm(forms.Form):
    SEMESTRE_CHOICES = [
        ('1er - 3er', '1°-3° (Primeros semestres)'),
        ('4to - 6to', '4°-6° (Semestres intermedios)'),
        ('7mo o más', '7° o más (Últimos semestres)'),
    ]
    semestre_ord = forms.ChoiceField(
        choices=SEMESTRE_CHOICES, 
        widget=forms.RadioSelect, 
        label="¿En qué semestre te encuentras actualmente?"
    )

    BINARY_CHOICES = [
        ('Sí', 'Sí'),
        ('No', 'No'),
    ]
    desmotivacion_bin = forms.ChoiceField(
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect,
        label="¿Te has sentido desmotivado(a) para continuar tus estudios en el ITD en los últimos 6 meses?"
    )

    considerado_abandonar_bin = forms.ChoiceField(
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect,
        label="¿Alguna vez has considerado abandonar la carrera?"
    )

    dificultades_economicas_bin = forms.ChoiceField(
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect,
        label="¿Presentas dificultades económicas para cubrir tus gastos escolares?"
    )

    EMPLEO_CHOICES = [
        ('No', 'No'),
        ('Sí, medio tiempo', 'Sí, medio tiempo'),
        ('Sí, tiempo completo', 'Sí, tiempo completo'),
    ]
    empleo_ord = forms.ChoiceField(
        choices=EMPLEO_CHOICES,
        widget=forms.RadioSelect,
        label="¿Tienes un empleo además de estudiar?"
    )

    IMPACTO_LABORAL_CHOICES = [
        ('No afecta/No trabajo', 'No afecta / No trabajo'),
        ('Algo', 'Algo'),
        ('Sí, mucho', 'Sí, mucho'),
    ]
    impacto_laboral_ord = forms.ChoiceField(
        choices=IMPACTO_LABORAL_CHOICES,
        widget=forms.RadioSelect,
        label="¿Consideras que tus responsabilidades laborales afectan tu rendimiento académico?"
    )

    reprobo_materias_bin = forms.ChoiceField(
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect,
        label="¿Has reprobado alguna materia en el último semestre escolar?"
    )

    APOYO_CHOICES = [
        ('Nunca', 'Nunca'),
        ('Algunas veces', 'Algunas veces'),
        ('Siempre', 'Siempre'),
    ]
    apoyo_institucional_ord = forms.ChoiceField(
        choices=APOYO_CHOICES,
        widget=forms.RadioSelect,
        label="¿Te sientes apoyado/a por el personal docente y administrativo del ITD?"
    )

    SATISFACCION_CHOICES = [
        ('Muy insatisfecho/a', 'Muy insatisfecho/a'),
        ('Insatisfecho/a', 'Insatisfecho/a'),
        ('Satisfecho/a', 'Satisfecho/a'),
        ('Muy satisfecho/a', 'Muy satisfecho/a'),
    ]
    satisfaccion_servicios_ord = forms.ChoiceField(
        choices=SATISFACCION_CHOICES,
        widget=forms.RadioSelect,
        label="¿Cómo calificarías tu satisfacción con los servicios del ITD?"
    )

    ACTIVIDADES_CHOICES = [
        ('Nunca', 'Nunca'),
        ('Algunas veces', 'Algunas veces'),
        ('Sí, frecuentemente', 'Sí, frecuentemente'),
    ]
    actividades_extracurriculares_ord = forms.ChoiceField(
        choices=ACTIVIDADES_CHOICES,
        widget=forms.RadioSelect,
        label="¿Participas en actividades extracurriculares dentro del ITD?"
    )
