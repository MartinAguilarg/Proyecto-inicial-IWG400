import calendar
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, F
from django.db.models.functions import Abs

from .models import Equipo, Partido, Desafio, Perfil
from .forms import RegistroCapitanForm, CrearEquipoForm

def registro(request):
    if request.method == 'POST':
        form = RegistroCapitanForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            telefono = form.cleaned_data.get('telefono')
            comuna = form.cleaned_data.get('comuna')
            Perfil.objects.create(usuario=usuario, telefono=telefono, comuna=comuna)
            messages.success(request, "Cuenta creada exitosamente. Ahora puedes iniciar sesión.")
            return redirect('login')
    else:
        form = RegistroCapitanForm()
    return render(request, 'registration/registro.html', {'form': form})

def calcular_elo(elo_a, elo_b, goles_a, goles_b):
    K = 32 # cantidad max de puntos base
    
    # calculo matematico para probabilidad
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

def inicio(request):
    es_capitan = False
    partidos_activos = None
    
    if request.user.is_authenticated:
        equipo_qs = Equipo.objects.filter(capitan=request.user)
        if equipo_qs.exists():
            es_capitan = True
            mi_equipo = equipo_qs.first()
            partidos_activos = Partido.objects.filter(
                Q(equipo_1=mi_equipo) | Q(equipo_2=mi_equipo)
            ).exclude(estado='confirmado')
            
    return render(request, 'registration/inicio.html', {
        'es_capitan': es_capitan,
        'partidos_activos': partidos_activos
    })

def ranking(request):
    equipos = Equipo.objects.all().order_by('-elo')
    return render(request, 'registration/ranking.html', {'equipos': equipos})

@login_required
def crear_equipo(request):
    if Equipo.objects.filter(capitan=request.user).exists():
        messages.info(request, "Ya tienes un equipo registrado.")
        return redirect('inicio')
        
    if request.method == 'POST':
        form = CrearEquipoForm(request.POST)
        if form.is_valid():
            equipo = form.save(commit=False)
            equipo.capitan = request.user
            equipo.elo = 1000
            equipo.save()
            messages.success(request, "¡Tu equipo ha sido creado exitosamente!")
            return redirect('inicio')
    else:
        form = CrearEquipoForm()
        
    return render(request, 'registration/crear_equipo.html', {'form': form})

@login_required
def mi_perfil(request):
    mi_equipo = get_object_or_404(Equipo, capitan=request.user)
    return redirect('perfil_equipo', equipo_id=mi_equipo.id)

def perfil_equipo(request, equipo_id):
    equipo = get_object_or_404(Equipo, id=equipo_id)
    capitan = equipo.capitan
    
    telefono = capitan.perfil.telefono if hasattr(capitan, 'perfil') else "Sin teléfono registrado"
    
    historial = Partido.objects.filter(
        (Q(equipo_1=equipo) | Q(equipo_2=equipo)) & Q(estado='confirmado')
    ).order_by('-id')

    victorias, derrotas, empates = 0, 0, 0
    goles_a_favor, goles_en_contra = 0, 0

    for partido in historial:
        if partido.equipo_1 == equipo:
            goles_a_favor += partido.goles_equipo_1
            goles_en_contra += partido.goles_equipo_2
            if partido.goles_equipo_1 > partido.goles_equipo_2: victorias += 1
            elif partido.goles_equipo_1 < partido.goles_equipo_2: derrotas += 1
            else: empates += 1
        else:
            goles_a_favor += partido.goles_equipo_2
            goles_en_contra += partido.goles_equipo_1
            if partido.goles_equipo_2 > partido.goles_equipo_1: victorias += 1
            elif partido.goles_equipo_2 < partido.goles_equipo_1: derrotas += 1
            else: empates += 1

    contexto = {
        'equipo': equipo,
        'capitan': capitan,
        'telefono': telefono,
        'historial': historial,
        'partidos_jugados': historial.count(),
        'victorias': victorias,
        'derrotas': derrotas,
        'empates': empates,
        'goles_a_favor': goles_a_favor,
        'goles_en_contra': goles_en_contra,
    }
    
    return render(request, 'registration/perfil.html', contexto)

@login_required
def reportar_partido(request, partido_id):
    partido = get_object_or_404(Partido, id=partido_id)
    usuario_actual = request.user

    es_capitan_1 = partido.equipo_1.capitan == usuario_actual
    es_capitan_2 = partido.equipo_2.capitan == usuario_actual

    if not es_capitan_1 and not es_capitan_2 and not usuario_actual.is_staff:
        messages.error(request, "No tienes permiso para reportar este partido.")
        return redirect('inicio')

    if request.method == 'POST':
        goles_1 = int(request.POST.get('goles_1', 0))
        goles_2 = int(request.POST.get('goles_2', 0))

        if es_capitan_1 and partido.estado in ['pendiente', 'disputa']:
            partido.goles_1_c1 = goles_1
            partido.goles_2_c1 = goles_2
            partido.estado = 'esperando_c2'
            partido.save()
            messages.info(request, "Resultado enviado. Esperando confirmación del rival.")

        elif es_capitan_2 and partido.estado == 'esperando_c2':
            partido.goles_1_c2 = goles_1
            partido.goles_2_c2 = goles_2

            if partido.goles_1_c1 == goles_1 and partido.goles_2_c1 == goles_2:
                partido.goles_equipo_1 = goles_1
                partido.goles_equipo_2 = goles_2
                partido.estado = 'confirmado'
                partido.save()
                
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
                messages.success(request, "El resultado coincide. ¡Partido finalizado y ranking actualizado!")
            else:
                partido.estado = 'disputa'
                partido.save()
                messages.warning(request, "Los resultados no coinciden. El partido está en disputa.")

        return redirect('inicio')

    return render(request, 'registration/reportar_partido.html', {
        'partido': partido, 
        'es_capitan_1': es_capitan_1, 
        'es_capitan_2': es_capitan_2
    })

@login_required
def radar_desafios(request):
    mi_equipo = get_object_or_404(Equipo, capitan=request.user)
    otros_equipos = Equipo.objects.exclude(id=mi_equipo.id)

    duelo_justo = otros_equipos.annotate(
        diferencia=Abs(F('elo') - mi_equipo.elo)
    ).order_by('diferencia').first()

    underdog = otros_equipos.filter(elo__lt=mi_equipo.elo).order_by('-elo').first()
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
        
        Desafio.objects.create(retador=mi_equipo, retado=equipo_retado)
        messages.success(request, "¡Desafío enviado con éxito!")
        
    return redirect('radar')

@login_required
def bandeja_desafios(request):
    mi_equipo = get_object_or_404(Equipo, capitan=request.user)
    desafios_pendientes = Desafio.objects.filter(retado=mi_equipo, estado='pendiente')
    
    return render(request, 'registration/bandeja.html', {
        'mi_equipo': mi_equipo,
        'desafios': desafios_pendientes
    })

@login_required
def responder_desafio(request, desafio_id, accion):
    desafio = get_object_or_404(Desafio, id=desafio_id, retado__capitan=request.user)
    
    if request.method == 'POST' or request.method == 'GET':
        if accion == 'aceptar':
            desafio.estado = 'aceptado'
            desafio.save()
            Partido.objects.create(
                equipo_1=desafio.retador, 
                equipo_2=desafio.retado, 
                estado='pendiente'
            )
            messages.success(request, "Desafío aceptado. ¡Ahora propón un horario y lugar!")
            return redirect('coordinacion')
        elif accion == 'rechazar':
            desafio.estado = 'rechazado'
            desafio.save()
            messages.warning(request, "Has rechazado el desafío.")
            return redirect('bandeja_desafios')
            
    return redirect('bandeja_desafios')

@login_required
def calendario(request):
    mi_equipo = get_object_or_404(Equipo, capitan=request.user)
    partidos_confirmados = Partido.objects.filter(
        (Q(equipo_1=mi_equipo) | Q(equipo_2=mi_equipo)),
        estado_coordinacion='aceptado'
    ).order_by('fecha_programada')
    
    return render(request, 'registration/calendario.html', {'partidos': partidos_confirmados})

@login_required
def coordinacion(request):
    mi_equipo = get_object_or_404(Equipo, capitan=request.user)
    partidos = Partido.objects.filter(
        (Q(equipo_1=mi_equipo) | Q(equipo_2=mi_equipo))
    ).exclude(estado_coordinacion='aceptado')
    
    return render(request, 'registration/coordinacion.html', {'partidos': partidos})

@login_required
def proponer_horario(request, partido_id):
    partido = get_object_or_404(Partido, id=partido_id)
    if request.method == 'POST':
        if 'aceptar' in request.POST:
            partido.estado_coordinacion = 'aceptado'
            messages.success(request, "¡Partido confirmado! Ya pueden prepararse para jugar.")
        elif 'rechazar' in request.POST:
            partido.fecha_programada = None
            partido.hora_programada = None
            partido.lugar_acordado = None
            partido.color_equipo_1 = None
            partido.color_equipo_2 = None
            partido.proponente = None  
            partido.estado_coordinacion = 'sin_fecha'
            messages.warning(request, "Propuesta rechazada. Rellena el formulario para enviar tu contraoferta.")
        else:
            partido.fecha_programada = request.POST.get('fecha')
            partido.hora_programada = request.POST.get('hora')
            partido.lugar_acordado = request.POST.get('lugar')
            partido.color_equipo_1 = request.POST.get('color_1')
            partido.color_equipo_2 = request.POST.get('color_2')
            partido.proponente = request.user  
            partido.estado_coordinacion = 'propuesto'
            messages.info(request, "Propuesta de coordinación enviada al rival.")
        partido.save()
    return redirect('coordinacion')