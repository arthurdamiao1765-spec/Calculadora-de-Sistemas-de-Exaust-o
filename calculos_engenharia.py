# -*- coding: utf-8 -*-
# calculos_engenharia.py

"""
Este arquivo contém todas as funções de cálculo de engenharia para o sistema:
- Perda de carga em dutos e componentes
- Dimensionamento e perda de carga de filtros e ciclones
- Seleção de ventilador e cálculo de potência
- Cálculo de peso e custo
"""

import math
from dados_ventilacao import DENSIDADE_MATERIAIS, FATORES_K, RELACAO_AR_PANO

PI = math.pi

def calcular_perda_carga_duto_reto(vazao_m3h, diametro_mm, comprimento_m):
    """Calcula a perda de carga em um duto reto usando a Equação de Darcy-Weisbach."""
    if diametro_mm == 0: return 0
    vazao_m3s = vazao_m3h / 3600
    diametro_m = diametro_mm / 1000
    area = PI * (diametro_m ** 2) / 4
    velocidade_ms = vazao_m3s / area
    
    # Fator de atrito (f) - simplificação usando um valor comum para dutos de aço (0.02)
    fator_atrito = 0.02
    
    # Perda de carga em mmH2O (rho * g ~ 9.8, rho ar ~ 1.2 kg/m³)
    perda_carga_pa = fator_atrito * (comprimento_m / diametro_m) * (1.2 * velocidade_ms**2 / 2)
    return perda_carga_pa / 9.81

def calcular_perda_carga_componente(vazao_m3h, diametro_mm, fator_k):
    """Calcula a perda de carga em um componente (curva, junção, etc.)."""
    if diametro_mm == 0: return 0
    vazao_m3s = vazao_m3h / 3600
    diametro_m = diametro_mm / 1000
    area = PI * (diametro_m ** 2) / 4
    velocidade_ms = vazao_m3s / area
    
    # Perda de carga em mmH2O
    pressao_dinamica_pa = (1.2 * velocidade_ms**2) / 2
    perda_carga_pa = fator_k * pressao_dinamica_pa
    return perda_carga_pa / 9.81

def calcular_peso_tubulacao(diametro_mm, comprimento_m, espessura_mm, material):
    """Calcula o peso de um componente de tubulação."""
    if material not in DENSIDADE_MATERIAIS:
        raise ValueError(f"Material '{material}' não encontrado.")
        
    diametro_m = diametro_mm / 1000
    espessura_m = espessura_mm / 1000
    densidade = DENSIDADE_MATERIAIS[material]
    
    # Área da seção transversal do material do duto
    area_material = PI * ((diametro_m / 2)**2 - ((diametro_m / 2) - espessura_m)**2)
    volume = area_material * comprimento_m
    peso_kg = volume * densidade
    return peso_kg

def calcular_filtro(vazao_total_m3h, tipo_poeira):
    """Dimensiona um filtro de mangas e calcula sua perda de carga."""
    if tipo_poeira not in RELACAO_AR_PANO:
        raise ValueError(f"Tipo de poeira '{tipo_poeira}' não encontrado.")
    
    vazao_m3min = vazao_total_m3h / 60
    relacao = RELACAO_AR_PANO[tipo_poeira]
    
    area_filtrante_m2 = vazao_m3min / relacao
    
    # Estimativa de perda de carga (inicial + limpeza) em mmH2O
    perda_carga_filtro = 120 # Valor típico médio para filtros com sistema de limpeza
    
    # Estimativa de peso da carcaça e estrutura (simplificado)
    # 15 kg por m² de área filtrante é uma estimativa razoável para um pré-projeto
    peso_filtro_kg = area_filtrante_m2 * 20
    
    return area_filtrante_m2, perda_carga_filtro, peso_filtro_kg

def calcular_ciclone(vazao_total_m3h):
    """Dimensiona um ciclone e calcula sua perda de carga e peso (simplificado)."""
    # Dimensionamento baseado em velocidade de entrada ótima (aprox. 15-20 m/s)
    vazao_m3s = vazao_total_m3h / 3600
    velocidade_entrada_ms = 18
    area_entrada_m2 = vazao_m3s / velocidade_entrada_ms
    
    # Proporções de ciclone padrão (Lapple)
    a = math.sqrt(area_entrada_m2 / 2)
    b = a / 2
    diametro_corpo_m = 4 * a
    
    # Perda de carga em mmH2O - aprox. 8x a pressão dinâmica na entrada
    pressao_dinamica_pa = (1.2 * velocidade_entrada_ms**2) / 2
    perda_carga_ciclone = (8 * pressao_dinamica_pa) / 9.81
    
    # Cálculo de peso simplificado (chapa de 3mm)
    altura_total = 8 * a
    area_superficie_m2 = (PI * diametro_corpo_m * altura_total) + (PI * diametro_corpo_m**2 / 4) # Corpo + cone
    peso_ciclone_kg = area_superficie_m2 * 3 * 7.85 # Aço Carbono 3mm
    
    return diametro_corpo_m, perda_carga_ciclone, peso_ciclone_kg
    
def selecionar_ventilador(vazao_total_m3h, perda_carga_total_mmh2o):
    """Calcula a potência do ventilador e sugere um tipo."""
    vazao_m3s = vazao_total_m3h / 3600
    perda_carga_pa = perda_carga_total_mmh2o * 9.81
    
    # Eficiência típica do ventilador (incluindo perdas de transmissão)
    eficiencia = 0.65
    
    potencia_eixo_watts = (vazao_m3s * perda_carga_pa) / eficiencia
    potencia_eixo_cv = potencia_eixo_watts / 735.5
    
    # Seleção do motor comercial imediatamente superior
    motores_cv = [1, 2, 3, 5, 7.5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 100]
    potencia_motor_cv = next((p for p in motores_cv if p >= potencia_eixo_cv), 100)

    # Sugestão do tipo de rotor
    if perda_carga_total_mmh2o > 250:
        tipo_rotor = "Centrífugo com pás radiais (alta pressão, ideal para material)"
    else:
        tipo_rotor = "Centrífugo com pás sirocco ou limit-load (média pressão, ar limpo)"

    # Estimativa de peso (simplificado)
    peso_ventilador_kg = potencia_motor_cv * 20

    return potencia_motor_cv, tipo_rotor, peso_ventilador_kg

def calcular_custo(peso_total_kg, custo_por_kg):
    """Calcula o custo de fabricação."""
    return peso_total_kg * custo_por_kg
