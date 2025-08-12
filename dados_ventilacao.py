# -*- coding: utf-8 -*-
# dados_ventilacao.py

"""
Este arquivo armazena todos os dados de referência para o sistema de cálculo,
incluindo vazões recomendadas, dados de materiais e fatores de perda de carga.
"""

# Dicionário de máquinas e processos com vazão recomendada em m³/h
# As vazões podem ser alteradas pelo usuário no programa principal.
MAQUINAS_E_PROCESSOS = {
    # Lixadeiras
    "Lixadeira de cinta (até 15cm larg.)": 850,
    "Lixadeira de cinta (15-25cm larg.)": 1360,
    "Lixadeira de disco (até 75cm diâm.)": 1020,
    "Lixadeira de tambor": 1700,
    # Serras
    "Serra de fita": 850,
    "Serra circular": 850,
    # Esmerilhamento
    "Esmeril/Rebarbadora (até 40cm diâm.)": 1020,
    "Esmeril/Rebarbadora (40-75cm diâm.)": 1700,
    # Jateamento
    "Cabine de Jateamento (pequena)": 3400,
    "Sala de Jateamento (por m² de grade)": 2040,
    # Soldagem
    "Bancada de Solda (pequena)": 1700,
    "Solda Robotizada (braço de extração)": 500,
    # Manuseio de Materiais
    "Ensacamento (manual)": 2550,
    "Peneira vibratória (coifa)": 3400,
    "Moega de recepção": 3400,
    "Elevador de canecas": 2040,
    # Fornos (valores base, refinar com cálculo de coifa quente)
    "Forno de cadinho (pequeno)": 3000,
    "Forno elétrico a arco (porta)": 8500,
}

# Densidade dos materiais em kg/m³ para cálculo de peso
DENSIDADE_MATERIAIS = {
    "Aço Carbono": 7850,
    "Aço Inox 304": 7900,
    "Aço Galvanizado": 7850, # A camada de zinco tem impacto mínimo no peso total
    "Alumínio": 2700,
}

# Fatores de perda de carga (K) para componentes comuns
# Baseado em dados do manual ACGIH
FATORES_K = {
    "Curva 90 graus (raio/D = 1.5)": 0.22,
    "Curva 45 graus (raio/D = 1.5)": 0.12,
    "Entrada de duto em linha principal (junção 30 graus)": 0.18,
    "Entrada de duto em linha principal (junção 45 graus)": 0.30,
    "Expansão gradual (30 graus total)": 0.15,
    "Redução gradual (30 graus total)": 0.05,
    "Chaminé (saída livre)": 1.0, # Perda de saída na pressão dinâmica
}

# Relação Ar/Pano (m/min) recomendada por tipo de poeira para Filtros de Mangas
RELACAO_AR_PANO = {
    "Poeira de cimento": 1.2,
    "Pó de madeira (fino)": 1.5,
    "Pó metálico (fumos de solda)": 0.9,
    "Grãos e cereais": 1.8,
    "Poeira de carvão": 1.3,
    "Poeira genérica (baixa carga)": 2.0,
}
