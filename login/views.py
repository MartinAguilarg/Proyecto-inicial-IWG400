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
from django.shortcuts import render, redirect, get_object_or_404
from .models import Partido

def reportar_partido(request, partido_id):
    # Busca el partido dentro de la base de datos
    partido = get_object_or_404(Partido, id=partido_id)
    
    if request.method == 'POST':
        # Anota los goles del formulario
        goles_1 = int(request.POST.get('goles_1', 0))
        goles_2 = int(request.POST.get('goles_2', 0))
        
        # Guarda los goles y cambia el estado del partido
        partido.goles_equipo_1 = goles_1
        partido.goles_equipo_2 = goles_2
        partido.estado = 'Confirmado'
        partido.save()
        
        # Usa la funcion del calculo de elo
        nuevo_elo_1, nuevo_elo_2 = calcular_elo(
            partido.equipo_1.elo, 
            partido.equipo_2.elo, 
            goles_1, 
            goles_2
        )
        
        # Actualiza y guarda los nuevos puntajes de los equipos
        partido.equipo_1.elo = nuevo_elo_1
        partido.equipo_2.elo = nuevo_elo_2
        partido.equipo_1.save()
        partido.equipo_2.save()
        
        return redirect('login') 
        
    return render(request, 'registration/reportar_partido.html', {'partido': partido})