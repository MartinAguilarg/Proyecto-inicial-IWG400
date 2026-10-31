from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})
from .models import Equipo, Partido

def calcular_elo(elo_a, elo_b, goles_a, goles_b):
    K = 32 #cantidad max de puntos base
    
    #calculo matematico para probabilidad, para que si un equipo de harto elo pierde con uno de bajo haya mas castigo
    prob_a = 1 / (1 + 10 ** ((elo_b - elo_a) / 400))
    prob_b = 1 / (1 + 10 ** ((elo_a - elo_b) / 400))
    
    # asignacion de resultados
    if goles_a > goles_b:
        res_a, res_b = 1, 0
    elif goles_a < goles_b:
        res_a, res_b = 0, 1
    else:
        res_a, res_b = 0.5, 0.5
        
    # bonus por los goles
    diferencia = abs(goles_a - goles_b)
    bonus = diferencia * 2  # 2 puntos por cada gol extra
    
    # formula elo final
    nuevo_elo_a = elo_a + K * (res_a - prob_a)
    nuevo_elo_b = elo_b + K * (res_b - prob_b)
    
    # aplicacion de bonus al equipo ganador
    if goles_a > goles_b:
        nuevo_elo_a += bonus
        nuevo_elo_b -= bonus
    elif goles_b > goles_a:
        nuevo_elo_b += bonus
        nuevo_elo_a -= bonus
        
    return int(nuevo_elo_a), int(nuevo_elo_b)