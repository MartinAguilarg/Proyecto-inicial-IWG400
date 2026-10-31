from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.db.models import F
from django.db.models.functions import Abs
from .models import Desafio
from .models import Equipo, Partido, Desafio
from django.db.models import Q
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
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Partido

@login_required
def reportar_partido(request, partido_id):
    partido = get_object_or_404(Partido, id=partido_id)
    usuario_actual = request.user

    # Verificar si el usuario es capitán de alguno de los dos equipos
    es_capitan_1 = partido.equipo_1.capitan == usuario_actual
    es_capitan_2 = partido.equipo_2.capitan == usuario_actual

    if not es_capitan_1 and not es_capitan_2 and not usuario_actual.is_staff:
        return redirect('login') # O una vista de error/prohibido

    if request.method == 'POST':
        goles_1 = int(request.POST.get('goles_1', 0))
        goles_2 = int(request.POST.get('goles_2', 0))

        # caso 1: El capitan 1 reporta por primera vez
        if es_capitan_1 and partido.estado in ['pendiente', 'disputa']:
            partido.goles_1_c1 = goles_1
            partido.goles_2_c1 = goles_2
            partido.estado = 'esperando_c2'
            partido.save()

        # caso 2: El capitan 2 responde al reporte
        elif es_capitan_2 and partido.estado == 'esperando_c2':
            partido.goles_1_c2 = goles_1
            partido.goles_2_c2 = goles_2

            # Verificamos si los resultados coinciden
            if partido.goles_1_c1 == goles_1 and partido.goles_2_c1 == goles_2:
                # coinciden, se oficializa el resultado
                partido.goles_equipo_1 = goles_1
                partido.goles_equipo_2 = goles_2
                partido.estado = 'confirmado'
                partido.save()

                # hacer calculo de elo
                nuevo_elo_1, nuevo_elo_2 = calcular_elo(
                    partido.equipo_1.elo, 
                    partido.equipo_2.elo, 
                    goles_1, 
                    goles_2
                )
                partido.equipo_1.elo = nuevo_elo_1
                partido.equipo_2.elo = nuevo_elo_2
                partido.equipo_1.save()
                partido.equipo_2.save()
            else:
                # No coinciden, Disputa abierta
                partido.estado = 'disputa'
                partido.save()

        return redirect('login')

    return render(request, 'registration/reportar_partido.html', {
        'partido': partido, 
        'es_capitan_1': es_capitan_1, 
        'es_capitan_2': es_capitan_2
    })
@login_required
def radar_desafios(request):
    # Identificamos el equipo del usuario conectado
    mi_equipo = get_object_or_404(Equipo, capitan=request.user)
    
    # excluimos a nuestro propio equipo de la busqueda
    otros_equipos = Equipo.objects.exclude(id=mi_equipo.id)

    #  duelo justo
    duelo_justo = otros_equipos.annotate(
        diferencia=Abs(F('elo') - mi_equipo.elo)
    ).order_by('diferencia').first()

    # el equipo mas cercano por debajo del elo
    underdog = otros_equipos.filter(elo__lt=mi_equipo.elo).order_by('-elo').first()

    # 3. el jefe con mas elo en toda la plataforma
    jefe = otros_equipos.filter(elo__gt=mi_equipo.elo).order_by('-elo').first()

    contexto = {
        'mi_equipo': mi_equipo,
        'duelo_justo': duelo_justo,
        'underdog': underdog,
        'jefe': jefe,
    }
    
    return render(request, 'registration/radar.html', contexto)
@login_required
def enviar_desafio(request, retado_id):
    if request.method == 'POST':
        mi_equipo = get_object_or_404(Equipo, capitan=request.user)
        equipo_retado = get_object_or_404(Equipo, id=retado_id)
        
        # Genera el registro del reto en la base de datos
        Desafio.objects.create(retador=mi_equipo, retado=equipo_retado)
        
    return redirect('radar')
@login_required
def bandeja_desafios(request):
    mi_equipo = get_object_or_404(Equipo, capitan=request.user)
    # Filtra solo los desafíos que nos han enviado y no se han respondido
    desafios_pendientes = Desafio.objects.filter(retado=mi_equipo, estado='pendiente')
    
    return render(request, 'registration/bandeja.html', {
        'mi_equipo': mi_equipo,
        'desafios': desafios_pendientes
    })

@login_required
def responder_desafio(request, desafio_id, accion):
    desafio = get_object_or_404(Desafio, id=desafio_id, retado__capitan=request.user)
    
    if request.method == 'POST':
        if accion == 'aceptar':
            desafio.estado = 'aceptado'
            desafio.save()
            # Al aceptar, se crea el partido
            Partido.objects.create(
                equipo_1=desafio.retador, 
                equipo_2=desafio.retado, 
                estado='pendiente'
            )
        elif accion == 'rechazar':
            desafio.estado = 'rechazado'
            desafio.save()
            
    return redirect('bandeja_desafios')
def inicio(request):
    equipos = Equipo.objects.all().order_by('-elo')
    es_capitan = False
    partidos_activos = None
    
    if request.user.is_authenticated:
        equipo_qs = Equipo.objects.filter(capitan=request.user)
        if equipo_qs.exists():
            es_capitan = True
            mi_equipo = equipo_qs.first()
            # Busca partidos de este equipo que aún no estén confirmados
            partidos_activos = Partido.objects.filter(
                Q(equipo_1=mi_equipo) | Q(equipo_2=mi_equipo)
            ).exclude(estado='confirmado')
    
    return render(request, 'registration/inicio.html', {
        'equipos': equipos,
        'es_capitan': es_capitan,
        'partidos_activos': partidos_activos
    })