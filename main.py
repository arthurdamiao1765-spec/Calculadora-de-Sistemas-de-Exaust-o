# -*- coding: utf-8 -*-
# main.py

"""
Programa Principal - Calculadora de Sistemas de Exaustão Industrial
Guia o usuário na montagem do sistema e apresenta os resultados finais.
"""

import dados_ventilacao as dados
import calculos_engenharia as calc

def imprimir_cabecalho(texto):
    print("\n" + "=" * 60)
    print(f" {texto.center(58)} ")
    print("=" * 60)

def main():
    imprimir_cabecalho("BEM-VINDO À CALCULADORA DE SISTEMAS DE EXAUSTÃO")
    
    sistema = []
    vazao_total = 0
    perda_carga_total = 0
    peso_total = 0
    
    # 1. Adicionar Captores (fontes de pó)
    imprimir_cabecalho("Passo 1: Adicionar Captores (Fontes de Pó)")
    while True:
        print("\nMáquinas e Processos Disponíveis:")
        for i, maquina in enumerate(dados.MAQUINAS_E_PROCESSOS.keys(), 1):
            print(f"  {i}. {maquina}")
        
        escolha = input("\nEscolha um captor pelo número (ou 'fim' para continuar): ")
        if escolha.lower() == 'fim':
            break
            
        try:
            maquina_escolhida = list(dados.MAQUINAS_E_PROCESSOS.keys())[int(escolha) - 1]
            vazao_padrao = dados.MAQUINAS_E_PROCESSOS[maquina_escolhida]
            
            print(f"  > Máquina: {maquina_escolhida}")
            print(f"  > Vazão Padrão: {vazao_padrao} m³/h")
            
            vazao_str = input("  > Deseja alterar a vazão? (deixe em branco para usar o padrão): ")
            vazao = float(vazao_str) if vazao_str else vazao_padrao
            
            sistema.append({'tipo': 'Captor', 'nome': maquina_escolhida, 'vazao': vazao})
            vazao_total += vazao
            print(f"--- Captor '{maquina_escolhida}' adicionado com vazão de {vazao} m³/h ---")
        except (ValueError, IndexError):
            print("!!! Escolha inválida. Tente novamente. !!!")

    # 2. Adicionar Componentes da Tubulação
    imprimir_cabecalho("Passo 2: Montar a Tubulação (do captor mais distante ao filtro)")
    diametro_atual_mm = 400 # Diâmetro inicial de exemplo
    material_padrao = "Aço Carbono"
    espessura_padrao = 2.0 # em mm
    
    while True:
        print("\nAdicionar componente à tubulação:")
        print("  1. Duto Reto")
        print("  2. Curva 90 graus")
        print("  3. Curva 45 graus")
        print("  4. Ramal (Junção 45 graus)")
        
        escolha = input("\nEscolha um componente (ou 'fim' para continuar): ")
        if escolha.lower() == 'fim':
            break
            
        try:
            if escolha == '1':
                comprimento = float(input("  > Comprimento do duto (m): "))
                pd_duto = calc.calcular_perda_carga_duto_reto(vazao_total, diametro_atual_mm, comprimento)
                peso_duto = calc.calcular_peso_tubulacao(diametro_atual_mm, comprimento, espessura_padrao, material_padrao)
                perda_carga_total += pd_duto
                peso_total += peso_duto
                print(f"--- Duto Reto adicionado. Perda de Carga: {pd_duto:.2f} mmH2O | Peso: {peso_duto:.2f} kg ---")

            elif escolha in ['2', '3']:
                tipo_curva = "Curva 90 graus (raio/D = 1.5)" if escolha == '2' else "Curva 45 graus (raio/D = 1.5)"
                fator_k = dados.FATORES_K[tipo_curva]
                pd_comp = calc.calcular_perda_carga_componente(vazao_total, diametro_atual_mm, fator_k)
                # Peso da curva é aproximado como um duto reto de comprimento igual a 1.5x o diâmetro
                peso_comp = calc.calcular_peso_tubulacao(diametro_atual_mm, 1.5 * (diametro_atual_mm/1000), espessura_padrao, material_padrao)
                perda_carga_total += pd_comp
                peso_total += peso_comp
                print(f"--- {tipo_curva} adicionada. Perda de Carga: {pd_comp:.2f} mmH2O | Peso: {peso_comp:.2f} kg ---")

            elif escolha == '4':
                print("  > (A vazão do ramal já foi somada no Passo 1)")
                fator_k = dados.FATORES_K["Entrada de duto em linha principal (junção 45 graus)"]
                pd_comp = calc.calcular_perda_carga_componente(vazao_total, diametro_atual_mm, fator_k)
                perda_carga_total += pd_comp
                print(f"--- Ramal adicionado. Perda de Carga: {pd_comp:.2f} mmH2O ---")

        except ValueError:
            print("!!! Entrada inválida. Tente novamente. !!!")
            
    # 3. Adicionar Equipamentos (Filtro, Ciclone)
    imprimir_cabecalho("Passo 3: Adicionar Equipamentos de Despoeiramento")
    
    while True:
        print("\nEscolha o equipamento principal:")
        print("  1. Filtro de Mangas/Cartuchos")
        print("  2. Ciclone")
        escolha = input("\nEscolha uma opção (ou 'fim' para pular): ")
        
        if escolha.lower() == 'fim':
            break

        if escolha == '1':
            print("\nTipos de poeira disponíveis:", ", ".join(dados.RELACAO_AR_PANO.keys()))
            tipo_poeira = input("  > Digite o tipo de poeira: ")
            try:
                area_f, pd_f, peso_f = calc.calcular_filtro(vazao_total, tipo_poeira)
                perda_carga_total += pd_f
                peso_total += peso_f
                print(f"--- Filtro Adicionado. Área: {area_f:.2f} m² | Perda de Carga: {pd_f:.2f} mmH2O | Peso: {peso_f:.2f} kg ---")
                break
            except ValueError as e:
                print(f"!!! Erro: {e} !!!")
        
        elif escolha == '2':
            diam_c, pd_c, peso_c = calc.calcular_ciclone(vazao_total)
            perda_carga_total += pd_c
            peso_total += peso_c
            print(f"--- Ciclone Adicionado. Diâmetro: {diam_c:.2f} m | Perda de Carga: {pd_c:.2f} mmH2O | Peso: {peso_c:.2f} kg ---")
            break
        else:
            print("!!! Opção inválida. !!!")
            
    # 4. Chaminé e Ventilador
    imprimir_cabecalho("Passo 4: Ventilador e Chaminé")
    comprimento_chamine = float(input("  > Digite o comprimento da chaminé (m): "))
    pd_chamine = calc.calcular_perda_carga_duto_reto(vazao_total, diametro_atual_mm, comprimento_chamine)
    pd_saida = calc.calcular_perda_carga_componente(vazao_total, diametro_atual_mm, dados.FATORES_K["Chaminé (saída livre)"])
    perda_carga_total += pd_chamine + pd_saida
    
    peso_chamine = calc.calcular_peso_tubulacao(diametro_atual_mm, comprimento_chamine, espessura_padrao, material_padrao)
    peso_total += peso_chamine
    
    potencia_cv, tipo_rotor, peso_vent = calc.selecionar_ventilador(vazao_total, perda_carga_total)
    peso_total += peso_vent

    # 5. Resultados Finais e Custo
    imprimir_cabecalho("RELATÓRIO FINAL DO SISTEMA")
    print(f"  Vazão Total do Sistema: {vazao_total:.2f} m³/h")
    print(f"  Perda de Carga Total Calculada: {perda_carga_total:.2f} mmH2O")
    print("-" * 60)
    print("  Ventilador Recomendado:")
    print(f"    Tipo de Rotor: {tipo_rotor}")
    print(f"    Potência do Motor: {potencia_cv} CV")
    print(f"    Peso Estimado do Ventilador: {peso_vent:.2f} kg")
    print("-" * 60)
    print(f"  Peso Total Estimado do Sistema (Tubos, Filtro, Vent., etc.): {peso_total:.2f} kg")
    print("-" * 60)

    try:
        custo_kg = float(input("\nPara estimar o custo, digite o valor do material beneficiado (R$/kg): "))
        custo_total = calc.calcular_custo(peso_total, custo_kg)
        print(f"\n  > Custo de Fabricação Estimado: R$ {custo_total:,.2f}")
        margem = float(input("  > Digite a margem de lucro desejada (%): "))
        preco_venda = custo_total * (1 + margem / 100)
        print(f"  > Preço de Venda Sugerido: R$ {preco_venda:,.2f}")
    except ValueError:
        print("\nCálculo de custo pulado.")
        
    imprimir_cabecalho("FIM DO PROGRAMA")


if __name__ == "__main__":
    main()
