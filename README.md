<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora de Engenharia de Exaustão (Profissional)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; scroll-behavior: smooth; }
        .card { background-color: white; border-radius: 0.75rem; padding: 1.5rem; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1); }
        .input-group { margin-bottom: 1rem; }
        .input-label { display: block; margin-bottom: 0.5rem; font-weight: 500; color: #374151; }
        .input-field { width: 100%; padding: 0.75rem; border: 1px solid #D1D5DB; border-radius: 0.5rem; transition: border-color 0.2s; background-color: #F9FAFB; }
        .input-field:focus { outline: none; border-color: #3B82F6; box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.4); background-color: white; }
        .btn { padding: 0.75rem 1.5rem; border-radius: 0.5rem; font-weight: 600; cursor: pointer; transition: background-color 0.2s; text-align: center; }
        .btn-primary { background-color: #2563EB; color: white; }
        .btn-primary:hover { background-color: #1D4ED8; }
        .btn-secondary { background-color: #6B7280; color: white; }
        .btn-secondary:hover { background-color: #4B5563; }
        .btn-tertiary { background-color: #f3f4f6; color: #374151; border: 1px solid #d1d5db; }
        .btn-tertiary:hover { background-color: #e5e7eb; }
        .result-table th, .result-table td { padding: 0.75rem; text-align: left; border-bottom: 1px solid #E5E7EB; }
        .result-table th { font-weight: 600; color: #111827; }
        .result-table td { color: #374151; }
        .result-table tr:last-child th, .result-table tr:last-child td { border-bottom: none; }
        .grid-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; }
        .hidden-section { display: none; }
        .component-item { display: flex; align-items: center; justify-content: space-between; gap: 0.5rem; margin-bottom: 0.5rem; font-size: 0.875rem; }
        .warning { color: #D97706; font-weight: bold; }

        /* Print-specific styles */
        @media print {
            body.printing * { visibility: hidden; }
            #relatorio-impressao, #relatorio-impressao * { visibility: visible; }
            #relatorio-impressao {
                position: absolute; left: 0; top: 0; width: 100%;
                font-family: 'Times New Roman', Times, serif; color: black;
            }
            .no-print { display: none !important; }
            @page { size: A4; margin: 2cm; }
        }
    </style>
</head>
<body class="bg-gray-100 text-gray-800">

    <div class="container mx-auto p-4 md:p-8 no-print">
        <header class="text-center mb-8">
            <h1 class="text-3xl md:text-4xl font-bold text-gray-900">Calculadora de Engenharia de Exaustão</h1>
            <p class="mt-2 text-lg text-gray-600">Ferramenta modular para dimensionamento de sistemas industriais.</p>
        </header>

        <main class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div class="lg:col-span-1 space-y-6">
                <div class="card">
                    <h2 class="text-xl font-bold mb-4 border-b pb-2">Configuração do Sistema</h2>
                    <div class="input-group">
                        <label for="modoCalculo" class="input-label">Modo de Cálculo</label>
                        <select id="modoCalculo" class="input-field">
                            <option value="completo">Projeto Completo</option>
                            <option value="tubulacao">Apenas Tubulação e Perda de Carga</option>
                            <option value="filtro">Apenas Filtro de Mangas</option>
                            <option value="ventilador">Apenas Ventilador</option>
                        </select>
                    </div>
                    <div class="input-group">
                        <label class="flex items-center"><input type="checkbox" id="incluirCiclone" class="mr-2 h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500">Incluir Ciclone como Pré-Filtro</label>
                    </div>
                </div>

                <div id="card-condicoes-gerais" class="card">
                    <h2 class="text-xl font-bold mb-4 border-b pb-2">1. Condições Gerais</h2>
                    <div class="grid grid-cols-2 gap-4">
                        <div class="input-group"><label for="estado" class="input-label">Estado</label><select id="estado" class="input-field"></select></div>
                        <div class="input-group"><label for="cidade" class="input-label">Cidade</label><select id="cidade" class="input-field"></select></div>
                    </div>
                    <div class="input-group"><label for="altitude" class="input-label">Altitude (m)</label><input type="number" id="altitude" class="input-field" readonly></div>
                    <div class="input-group"><label for="materialDuto" class="input-label">Material do Duto</label><select id="materialDuto" class="input-field"></select></div>
                    <div class="input-group"><label for="velocidadeProjeto" class="input-label">Velocidade de Projeto (m/s)</label><input type="number" id="velocidadeProjeto" class="input-field" value="20"></div>
                </div>

                <div id="card-dados-processo" class="card">
                    <h2 class="text-xl font-bold mb-4 border-b pb-2">2. Dados do Processo e do Pó</h2>
                    <div class="input-group"><label for="particulado" class="input-label">Tipo de Particulado</label><select id="particulado" class="input-field"></select></div>
                    <div class="input-group"><label for="temperatura" class="input-label">Temperatura do Gás (°C)</label><input type="number" id="temperatura" class="input-field" value="25"></div>
                    <h3 class="text-lg font-semibold mt-6 mb-2">Fatores de Correção (Renner)</h3>
                    <div class="grid grid-cols-2 gap-4">
                        <div class="input-group"><label for="fatorB" class="input-label">B: Aplicação</label><select id="fatorB" class="input-field"></select></div>
                        <div class="input-group"><label for="fatorC" class="input-label">C: Granulometria</label><select id="fatorC" class="input-field"></select></div>
                        <div class="input-group"><label for="fatorD" class="input-label">D: Carga de Pó</label><select id="fatorD" class="input-field"></select></div>
                        <div class="input-group"><label for="fatorE" class="input-label">E: Temperatura</label><select id="fatorE" class="input-field"></select></div>
                        <div class="input-group"><label for="fatorF" class="input-label">F: Fluidização</label><select id="fatorF" class="input-field"></select></div>
                        <div class="input-group"><label for="fatorG" class="input-label">G: Fluxo</label><select id="fatorG" class="input-field"></select></div>
                    </div>
                     <div class="input-group mt-4">
                        <label class="flex items-center"><input type="checkbox" id="fatorH" class="mr-2 h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500">H: Condições Tropicais (Úmidas)</label>
                    </div>
                </div>
                
                <div id="card-dados-manuais" class="card hidden-section">
                     <h2 class="text-xl font-bold mb-4 border-b pb-2">Dados Manuais para Cálculo</h2>
                     <div id="input-manual-vazao" class="input-group hidden-section"><label for="vazaoManual" class="input-label">Vazão Total (m³/h)</label><input type="number" id="vazaoManual" class="input-field" value="15000"></div>
                    <div id="input-manual-perda" class="input-group hidden-section"><label for="perdaManual" class="input-label">Perda de Carga Total (Pa)</label><input type="number" id="perdaManual" class="input-field" value="2500"></div>
                </div>

                <div id="card-pontos-captacao" class="card">
                    <h2 class="text-xl font-bold mb-4 border-b pb-2">3. Pontos de Captação</h2>
                    <div id="pontos-captacao-container" class="space-y-6"></div>
                    <button id="add-ponto" class="btn btn-secondary mt-4 w-full">Adicionar Ponto de Captação</button>
                </div>

                <div id="card-dim-filtro" class="card">
                    <h2 class="text-xl font-bold mb-4 border-b pb-2">4. Dimensionamento do Filtro</h2>
                    <div class="input-group"><label for="sistemaLimpeza" class="input-label">Sistema de Limpeza (Fator An)</label><select id="sistemaLimpeza" class="input-field"></select></div>
                    <div class="input-group"><label for="numFileiras" class="input-label">Número de Fileiras (Válvulas)</label><select id="numFileiras" class="input-field"><option value="2">2</option><option value="4">4</option><option value="6">6</option><option value="8">8</option><option value="10" selected>10</option><option value="12">12</option><option value="14">14</option><option value="16">16</option></select></div>
                    <div class="grid-container">
                        <div class="input-group"><label for="diametroElemento" class="input-label">Ø Manga (mm)</label><input type="number" id="diametroElemento" class="input-field" value="152"></div>
                        <div class="input-group"><label for="comprimentoElemento" class="input-label">Comp. Manga (m)</label><input type="number" id="comprimentoElemento" class="input-field" value="3.0"></div>
                        <div class="input-group"><label for="espacamentoMangas" class="input-label">Espacejamento (mm)</label><input type="number" id="espacamentoMangas" class="input-field" value="220"></div>
                        <div class="input-group"><label for="distanciaBorda" class="input-label">Dist. Borda (mm)</label><input type="number" id="distanciaBorda" class="input-field" value="100"></div>
                    </div>
                </div>

                <button id="calcular" class="btn btn-primary w-full text-lg shadow-lg">CALCULAR PROJETO</button>
            </div>

            <div id="resultados-container" class="lg:col-span-2 space-y-6 hidden">
                 <div class="flex justify-end"><button id="emitir-relatorio" class="btn btn-secondary">Emitir Relatório</button></div>
                 <div id="res-card-geral" class="card">
                    <h2 class="text-xl font-bold mb-4">Resultados Gerais</h2>
                    <div class="overflow-x-auto"><table class="w-full result-table"><tbody>
                        <tr><th>Densidade do Ar (ρ)</th><td id="res-densidade"></td></tr>
                        <tr><th>Velocidade de Projeto (Vt)</th><td id="res-velocidade-transporte"></td></tr>
                        <tr><th>Vazão Total do Sistema (Q)</th><td id="res-vazao-total"></td></tr>
                        <tr class="bg-blue-50"><th>Perda de Carga Total (ΔPt) c/ 15% de Margem</th><td id="res-perda-carga-total" class="font-bold"></td></tr>
                    </tbody></table></div>
                </div>
                
                <div id="res-card-tubulacao" class="card">
                    <h2 class="text-xl font-bold mb-4">Detalhamento da Tubulação</h2>
                    <div class="overflow-x-auto"><table class="w-full result-table"><thead><tr class="bg-gray-50">
                        <th>Trecho</th><th>Ø Ideal (mm)</th><th>Ø Padrão (mm)</th><th>Veloc. Real (m/s)</th><th>Perda Carga (Pa)</th>
                    </tr></thead><tbody id="res-trechos-table"></tbody></table></div>
                </div>

                <div id="res-card-filtro" class="card">
                    <h2 class="text-xl font-bold mb-4">Dimensionamento do Filtro de Mangas</h2>
                     <div class="overflow-x-auto"><table class="w-full result-table"><tbody>
                        <tr><th>Relação Ar/Pano (A/C) Calculada</th><td id="res-relacao-ac" class="font-bold"></td></tr>
                        <tr><th>Área Filtrante Necessária</th><td id="res-area-filtrante"></td></tr>
                        <tr class="bg-blue-50"><th>Quantidade Total de Mangas (Corrigido)</th><td id="res-qtde-elementos" class="font-bold"></td></tr>
                        <tr><th>Arranjo das Mangas</th><td id="res-arranjo-mangas"></td></tr>
                        <tr class="bg-blue-50"><th>Dimensões da Carcaça (L x C)</th><td id="res-dimensoes-carcaca" class="font-bold"></td></tr>
                    </tbody></table></div>
                </div>

                <div id="res-card-ventilador" class="card">
                    <h2 class="text-xl font-bold mb-4">Análise e Seleção do Ventilador</h2>
                    <canvas id="ventiladorChart"></canvas>
                    <h3 class="text-lg font-semibold mt-6 mb-2">Opções de Ventiladores</h3>
                    <div class="overflow-x-auto">
                        <table class="w-full result-table">
                            <thead><tr class="bg-gray-50"><th>Selecionar</th><th>Modelo</th><th>Rendimento</th><th>Rotor (mm)</th><th>RPM Req.</th><th>Motor Padrão (CV)</th></tr></thead>
                            <tbody id="ventiladores-table"></tbody>
                        </table>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <div id="relatorio-impressao"></div>

    <script>
        // --- START OF INTEGRATED SCRIPT ---
        
        // --- CITIES MODULE (FULL) ---
        const CIDADES_BRASIL = {
            "Acre": {"Acrelândia": 174, "Assis Brasil": 331, "Brasiléia": 249, "Bujari": 174, "Capixaba": 174, "Cruzeiro do Sul": 182, "Epitaciolândia": 174, "Feijó": 174, "Jordão": 174, "Mâncio Lima": 190, "Manoel Urbano": 174, "Marechal Thaumaturgo": 174, "Plácido de Castro": 174, "Porto Acre": 174, "Porto Walter": 174, "Rio Branco": 153, "Rodrigues Alves": 174, "Santa Rosa do Purus": 174, "Sena Madureira": 145, "Senador Guiomard": 174, "Tarauacá": 167, "Xapuri": 174},
            "Alagoas": {"Água Branca": 570, "Anadia": 165, "Arapiraca": 264, "Atalaia": 39, "Barra de Santo Antônio": 14, "Barra de São Miguel": 13, "Batalha": 30, "Belém": 120, "Belo Monte": 60, "Boca da Mata": 105, "Branquinha": 85, "Cacimbinhas": 440, "Cajueiro": 100, "Campestre": 120, "Campo Alegre": 104, "Campo Grande": 150, "Canapi": 480, "Capela": 80, "Carneiros": 300, "Chã Preta": 450, "Coité do Nóia": 250, "Colônia Leopoldina": 150, "Coqueiro Seco": 20, "Coruripe": 16, "Craíbas": 200, "Delmiro Gouveia": 256, "Dois Riachos": 200, "Estrela de Alagoas": 300, "Feira Grande": 200, "Feliz Deserto": 25, "Flexeiras": 100, "Girau do Ponciano": 250, "Ibateguara": 300, "Igaci": 200, "Igreja Nova": 20, "Inhapi": 500, "Jacaré dos Homens": 150, "Jacuípe": 80, "Japaratinga": 5, "Jaramataia": 150, "Jequiá da Praia": 10, "Joaquim Gomes": 100, "Jundiá": 100, "Junqueiro": 150, "Lagoa da Canoa": 200, "Limoeiro de Anadia": 250, "Maceió": 7, "Major Isidoro": 200, "Mar Vermelho": 500, "Maragogi": 5, "Maravilha": 250, "Marechal Deodoro": 15, "Maribondo": 150, "Mata Grande": 500, "Matriz de Camaragibe": 50, "Messias": 100, "Minador do Negrão": 300, "Monteirópolis": 150, "Murici": 80, "Novo Lino": 100, "Olho d'Água das Flores": 200, "Olho d'Água do Casado": 250, "Olho d'Água Grande": 100, "Olivença": 250, "Ouro Branco": 400, "Palestina": 200, "Palmeira dos Índios": 290, "Pão de Açúcar": 20, "Pariconha": 400, "Paripueira": 10, "Passo de Camaragibe": 10, "Paulo Jacinto": 200, "Penedo": 27, "Piaçabuçu": 10, "Pilar": 13, "Pindoba": 200, "Piranhas": 199, "Poço das Trincheiras": 300, "Porto Calvo": 50, "Porto de Pedras": 10, "Porto Real do Colégio": 20, "Quebrangulo": 300, "Rio Largo": 123, "Roteiro": 10, "Santa Luzia do Norte": 20, "Santana do Ipanema": 250, "Santana do Mundaú": 200, "São Brás": 25, "São José da Laje": 150, "São José da Tapera": 250, "São Luís do Quitunde": 50, "São Miguel dos Campos": 49, "São Miguel dos Milagres": 10, "São Sebastião": 150, "Satuba": 50, "Senador Rui Palmeira": 300, "Tanque d'Arca": 200, "Taquarana": 250, "Teotônio Vilela": 150, "Traipu": 50, "União dos Palmares": 150, "Viçosa": 279},
            "Amapá": {"Amapá": 11, "Calçoene": 12, "Cutias": 10, "Ferreira Gomes": 56, "Itaubal": 13, "Laranjal do Jari": 43, "Macapá": 14, "Mazagão": 14, "Oiapoque": 10, "Pedra Branca do Amapari": 120, "Porto Grande": 46, "Pracuúba": 12, "Santana": 15, "Serra do Navio": 138, "Tartarugalzinho": 20, "Vitória do Jari": 15},
            "Amazonas": {"Alvarães": 45, "Amaturá": 60, "Anamã": 30, "Anori": 35, "Apuí": 150, "Atalaia do Norte": 70, "Autazes": 35, "Barcelos": 34, "Barreirinha": 30, "Benjamin Constant": 65, "Beruri": 30, "Boa Vista do Ramos": 25, "Boca do Acre": 100, "Borba": 45, "Caapiranga": 30, "Canutama": 50, "Carauari": 80, "Careiro": 30, "Careiro da Várzea": 30, "Coari": 45, "Codajás": 40, "Eirunepé": 125, "Envira": 130, "Fonte Boa": 65, "Guajará": 100, "Humaitá": 90, "Ipixuna": 120, "Iranduba": 25, "Itacoatiara": 40, "Itamarati": 100, "Itapiranga": 40, "Japurá": 50, "Juruá": 80, "Jutaí": 70, "Lábrea": 60, "Manacapuru": 30, "Manaquiri": 30, "Manaus": 92, "Manicoré": 55, "Maraã": 50, "Maués": 20, "Nhamundá": 20, "Nova Olinda do Norte": 40, "Novo Airão": 40, "Novo Aripuanã": 50, "Parintins": 25, "Pauini": 100, "Presidente Figueiredo": 123, "Rio Preto da Eva": 80, "Santa Isabel do Rio Negro": 60, "Santo Antônio do Içá": 65, "São Gabriel da Cachoeira": 80, "São Paulo de Olivença": 60, "São Sebastião do Uatumã": 30, "Silves": 30, "Tabatinga": 60, "Tapauá": 70, "Tefé": 55, "Tonantins": 60, "Uarini": 50, "Urucará": 35, "Urucurituba": 30},
            "Bahia": {"Salvador": 8, "Feira de Santana": 234, "Vitória da Conquista": 923, "Camaçari": 36, "Itabuna": 54, "Ilhéus": 52},
            "Ceará": {"Fortaleza": 21, "Juazeiro do Norte": 377, "Caucaia": 29, "Maracanaú": 42, "Sobral": 70},
            "Distrito Federal": {"Brasília": 1172},
            "Espírito Santo": {"Vitória": 12, "Vila Velha": 4, "Serra": 301, "Cariacica": 22},
            "Goiás": {"Goiânia": 749, "Anápolis": 1017, "Aparecida de Goiânia": 808, "Rio Verde": 748},
            "Maranhão": {"São Luís": 4, "Imperatriz": 95, "São José de Ribamar": 3},
            "Mato Grosso": {"Cuiabá": 165, "Várzea Grande": 185, "Rondonópolis": 227},
            "Mato Grosso do Sul": {"Campo Grande": 546, "Dourados": 430, "Três Lagoas": 313},
            "Minas Gerais": {"Belo Horizonte": 852, "Uberlândia": 863, "Juiz de Fora": 678, "Poços de Caldas": 1186, "Contagem": 858},
            "Pará": {"Belém": 10, "Ananindeua": 20, "Santarém": 51},
            "Paraíba": {"João Pessoa": 40, "Campina Grande": 560, "Santa Rita": 16},
            "Paraná": {"Curitiba": 935, "Londrina": 576, "Maringá": 555, "Ponta Grossa": 975},
            "Pernambuco": {"Recife": 4, "Caruaru": 554, "Jaboatão dos Guararapes": 10},
            "Piauí": {"Teresina": 72, "Parnaíba": 5},
            "Rio de Janeiro": {"Rio de Janeiro": 2, "Nova Friburgo": 846, "São Gonçalo": 19, "Duque de Caxias": 7},
            "Rio Grande do Norte": {"Natal": 30, "Mossoró": 20},
            "Rio Grande do Sul": {"Porto Alegre": 10, "Caxias do Sul": 760, "Gramado": 830, "Pelotas": 7},
            "Rondônia": {"Porto Velho": 87, "Ji-Paraná": 170},
            "Roraima": {"Boa Vista": 85},
            "Santa Catarina": {"Florianópolis": 2, "Joinville": 4, "Lages": 916, "São Joaquim": 1353, "Blumenau": 21},
            "São Paulo": {"São Paulo": 760, "Campinas": 685, "São José dos Campos": 660, "Ribeirão Preto": 546, "Campos do Jordão": 1628, "São José do Rio Preto": 489, "Guarulhos": 759},
            "Sergipe": {"Aracaju": 4, "Nossa Senhora do Socorro": 16},
            "Tocantins": {"Palmas": 230, "Araguaína": 227}
        };

        // --- DATA MODULE ---
        const DADOS_TECNICOS = {
            particulados: {
                "Abrasivos cerâmicos": { vt: 22, A: 1.8, tipo: 'abrasivo', gran: '10-50 micron' }, "Ácido tereftálico": { vt: 18, A: 3.0, tipo: 'quimico', gran: '5-10 micron' },
                "Adubos fosfáticos": { vt: 18, A: 2.4, tipo: 'quimico', gran: '10-50 micron' }, "Algodão": { vt: 18, A: 4.0, tipo: 'fibroso', gran: '50-100 micron' },
                "Alumina": { vt: 20, A: 2.7, tipo: 'abrasivo', gran: '10-50 micron' }, "Alumínio (pó)": { vt: 20, A: 3.2, tipo: 'metalico', gran: '10-50 micron' },
                "Amido de milho": { vt: 18, A: 2.4, tipo: 'po_fino_organico', gran: '5-10 micron' }, "Areia de Fundição": { vt: 23, A: 3.0, tipo: 'abrasivo', gran: '50-100 micron' },
                "Argila (pó)": { vt: 18, A: 2.5, tipo: 'inerte', gran: '10-50 micron' }, "Asbesto": { vt: 18, A: 2.7, tipo: 'fibroso_perigoso', gran: '2-5 micron' },
                "Açúcar": { vt: 18, A: 3.0, tipo: 'po_fino_organico', gran: '10-50 micron' }, "Baquelite (pó)": { vt: 18, A: 3.8, tipo: 'plastico', gran: '10-50 micron' },
                "Borracha (pó)": { vt: 20, A: 3.5, tipo: 'elastômero', gran: '50-100 micron' }, "Cacau (pó)": { vt: 18, A: 3.3, tipo: 'po_fino_organico', gran: '5-10 micron' },
                "Café (pó)": { vt: 18, A: 2.6, tipo: 'po_fino_organico', gran: '10-50 micron' }, "Cal (pó)": { vt: 18, A: 2.7, tipo: 'quimico_alcalino', gran: '5-10 micron' },
                "Carvão Ativado": { vt: 18, A: 2.6, tipo: 'po_fino_organico', gran: '2-5 micron' }, "Carvão Fino (pó)": { vt: 20, A: 3.2, tipo: 'abrasivo', gran: '10-50 micron' },
                "Cimento (pó)": { vt: 18, A: 2.2, tipo: 'quimico_alcalino', gran: '5-10 micron' }, "Cinzas Volantes": { vt: 18, A: 2.8, tipo: 'abrasivo', gran: '2-5 micron' },
                "Coque (pó)": { vt: 22, A: 1.6, tipo: 'abrasivo', gran: '10-50 micron' }, "Couro (pó de lixagem)": { vt: 20, A: 3.2, tipo: 'fibroso', gran: '50-100 micron' },
                "Detergente em pó": { vt: 15, A: 2.2, tipo: 'quimico', gran: '10-50 micron' }, "Dolomita em pó": { vt: 18, A: 3.0, tipo: 'inerte', gran: '10-50 micron' },
                "Enxofre (pó)": { vt: 18, A: 2.8, tipo: 'quimico', gran: '5-10 micron' }, "Epóxi (resina em pó)": { vt: 18, A: 3.2, tipo: 'plastico', gran: '10-50 micron' },
                "Escória de alto forno": { vt: 22, A: 2.0, tipo: 'abrasivo', gran: '10-50 micron' }, "Estearatos": { vt: 15, A: 2.7, tipo: 'quimico', gran: '5-10 micron' },
                "Farelo": { vt: 18, A: 3.7, tipo: 'po_fino_organico', gran: '50-100 micron' }, "Farinha de carne": { vt: 18, A: 2.2, tipo: 'po_fino_organico', gran: '10-50 micron' },
                "Farinha de osso": { vt: 18, A: 2.0, tipo: 'po_fino_organico', gran: '10-50 micron' }, "Farinha de peixe": { vt: 18, A: 2.5, tipo: 'po_fino_organico', gran: '10-50 micron' },
                "Farinha de rocha": { vt: 20, A: 2.6, tipo: 'inerte', gran: '10-50 micron' }, "Farinha de sangue": { vt: 18, A: 3.8, tipo: 'po_fino_organico', gran: '10-50 micron' },
                "Farinha de Trigo": { vt: 18, A: 3.0, tipo: 'po_fino_organico', gran: '10-50 micron' }, "Feldspato": { vt: 20, A: 2.2, tipo: 'inerte', gran: '10-50 micron' },
                "Fermento seco": { vt: 15, A: 2.7, tipo: 'po_fino_organico', gran: '5-10 micron' }, "Ferro (óxido, fumos)": { vt: 15, A: 1.7, tipo: 'fumo', gran: '< 2 micron' },
                "Ferro fundido (rebarbação)": { vt: 23, A: 3.3, tipo: 'metalico', gran: '50-100 micron' }, "Ferromanganes": { vt: 20, A: 1.5, tipo: 'metalico', gran: '5-10 micron' },
                "Ferrosilicio": { vt: 20, A: 1.3, tipo: 'metalico', gran: '2-5 micron' }, "Fibra de vidro": { vt: 18, A: 4.5, tipo: 'fibroso', gran: '50-100 micron' },
                "Fosfato bruto": { vt: 18, A: 1.5, tipo: 'quimico', gran: '10-50 micron' }, "Freios (revestimento)": { vt: 20, A: 3.3, tipo: 'abrasivo', gran: '2-5 micron' },
                "Frutas em pó": { vt: 15, A: 1.5, tipo: 'po_fino_organico', gran: '5-10 micron' }, "Fuligem": { vt: 15, A: 1.6, tipo: 'po_fino_carbonaceo', gran: '< 2 micron' },
                "Fumo (pó de)": { vt: 18, A: 2.7, tipo: 'po_fino_organico', gran: '10-50 micron' }, "Fumos de Solda": { vt: 15, A: 1.5, tipo: 'fumo', gran: '< 2 micron' },
                "Fundição (pó geral)": { vt: 22, A: 2.7, tipo: 'inerte', gran: '10-50 micron' }, "Gesso (pó)": { vt: 18, A: 2.3, tipo: 'quimico', gran: '10-50 micron' },
                "Grafite": { vt: 18, A: 2.0, tipo: 'po_fino_carbonaceo', gran: '5-10 micron' }, "Leite em pó": { vt: 15, A: 2.0, tipo: 'po_fino_organico', gran: '5-10 micron' },
                "Madeira (pó de lixa com cola)": { vt: 20, A: 2.3, tipo: 'fibroso_pegajoso', gran: '10-50 micron' }, "Madeira (serragem fina)": { vt: 20, A: 4.0, tipo: 'fibroso', gran: '50-100 micron' },
                "Mármore (farinha)": { vt: 18, A: 3.3, tipo: 'inerte', gran: '10-50 micron' }, "Negro de fumo": { vt: 15, A: 2.3, tipo: 'po_fino_carbonaceo', gran: '< 2 micron' },
                "PVC (pó)": { vt: 18, A: 2.4, tipo: 'plastico', gran: '10-50 micron' }, "Pigmentos (geral)": { vt: 15, A: 2.6, tipo: 'po_fino_quimico', gran: '2-5 micron' },
                "Plástico granulado": { vt: 20, A: 2.5, tipo: 'plastico', gran: '> 100 micron' }, "Quartzo (farinha)": { vt: 22, A: 2.0, tipo: 'abrasivo_perigoso', gran: '2-5 micron' },
                "Ração balanceada": { vt: 18, A: 2.4, tipo: 'po_fino_organico', gran: '50-100 micron' }, "Sabão em pó": { vt: 15, A: 2.0, tipo: 'quimico', gran: '10-50 micron' },
                "Sal de cozinha": { vt: 18, A: 2.0, tipo: 'quimico', gran: '10-50 micron' }, "Sílica": { vt: 22, A: 2.5, tipo: 'abrasivo_perigoso', gran: '2-5 micron' },
                "Soja (farelo)": { vt: 18, A: 2.0, tipo: 'po_fino_organico', gran: '10-50 micron' }, "Talco": { vt: 15, A: 2.6, tipo: 'po_fino_quimico', gran: '2-5 micron' },
                "Tinta em pó": { vt: 15, A: 2.0, tipo: 'plastico', gran: '10-50 micron' }, "Trigo (moagem)": { vt: 18, A: 3.2, tipo: 'po_fino_organico', gran: '10-50 micron' },
                "Vidro (pó)": { vt: 22, A: 2.3, tipo: 'abrasivo', gran: '10-50 micron' }, "Zinco (óxido)": { vt: 15, A: 2.3, tipo: 'fumo', gran: '< 2 micron' },
            },
            maquinas: {
                "Forno (Coifa Circular Quente)": { vazao_m3h: 0, captor: "Coifa Circular", calculoEspecial: 'forno' },
                "Lixadeira de cinta (leve)": { vazao_m3h: 1200, captor: "Bocal Retangular Flangeado"},
                "Lixadeira de disco (pesado)": { vazao_m3h: 1800, captor: "Bocal Retangular Flangeado"},
                "Serra de fita (madeira)": { vazao_m3h: 1500, captor: "Bocal Retangular Flangeado"},
                "Aplainadora (madeira)": { vazao_m3h: 2000, captor: "Coifa de Cabine (Booth Hood)"},
                "Soldagem (eletrodo manual)": { vazao_m3h: 1000, captor: "Braço Extrator"},
                "Rebarbação / Esmeril (até Ø10\")": { vazao_m3h: 1400, captor: "Coifa para Esmeril"},
                "Transporte de cimento (ponto)": { vazao_m3h: 2500, captor: "Coifa de Cabine (Booth Hood)"},
                "Jateamento de areia (cabine)": { vazao_m3h: 3000, captor: "Coifa de Cabine (Booth Hood)"},
                "Cabine de pintura (pequena)": { vazao_m3h: 4000, captor: "Coifa de Cabine (Booth Hood)"},
                "Silo de Cimento": { vazao_m3h: 1700, captor: "Coifa de Cabine (Booth Hood)" },
                "Moinho de Martelos": { vazao_m3h: 4000, captor: "Coifa de Cabine (Booth Hood)" },
                "Transportador de Correia (Ponto de Queda)": { vazao_m3h: 2500, captor: "Coifa de Cabine (Booth Hood)" },
                "Bancada de Solda": { vazao_m3h: 1500, captor: "Coifa de Tanque Retangular (Slot Hood)" },
                "Forno de Indução (pequeno)": { vazao_m3h: 5000, captor: "Coifa de Cabine (Booth Hood)" },
                "Forno Cubilô": { vazao_m3h: 15000, captor: "Coifa de Cabine (Booth Hood)" },
                "Sistema de Areia (Misturador)": { vazao_m3h: 3400, captor: "Coifa de Cabine (Booth Hood)" },
                "Desmoldagem / Shakeout": { vazao_m3h: 6800, captor: "Mesa com Exaustão Inferior (Downdraft)" },
                "Outro (Vazão Manual)": { vazao_m3h: 1000, captor: "Abertura de Duto Simples" }
            },
            captores: {
                "Abertura de Duto Simples": { K: 1.0 }, "Bocal Retangular Flangeado": { K: 0.25 },
                "Bocal Cônico Flangeado (45°)": { K: 0.15 }, "Coifa de Cabine (Booth Hood)": { K: 0.50 },
                "Coifa de Tanque Retangular (Slot Hood)": { K: 1.78 }, "Coifa para Esmeril": { K: 0.75 },
                "Mesa com Exaustão Inferior (Downdraft)": { K: 2.5 }, "Coifa Circular": { K: 0.5 },
                "Braço Extrator": { K: 1.2 }
            },
            acessorios: { // Fatores de perda de carga (K) para componentes
                "duto_reto": { K_por_metro: 0.02 }, // Fator de atrito, usado de forma diferente
                "curva_90_raio_longo": { K: 0.27 },
                "curva_45": { K: 0.15 },
                "juncao_t_90_graus": { K: 1.2 },
                "expansao_gradual_30": { K: 0.15 },
                "reducao_gradual_30": { K: 0.05 }
            },
            materiaisDuto: {
                "Aço Galvanizado (novo)": { rugosidade: 0.00015 }, "Aço Carbono (comercial)": { rugosidade: 0.000045 },
                "PVC Liso": { rugosidade: 0.0000015 },
            },
            diametrosPadrao: [76.2, 101.6, 127, 152.4, 203.2, 254, 304.8, 355.6, 406.4, 457.2, 508, 558.8, 609.6, 660.4, 711.2, 762, 812.8, 863.6, 914.4, 965.2, 1016], // Em mm
            sistemasLimpeza: {
                "Pulse-jet com Venturi (mangas)": { An: 1.0 }, "Pulse-jet direto (mangas isoladas)": { An: 1.3 },
                "Pulse-jet direto (fileira de mangas)": { An: 1.5 }, "Sacudimento mecânico (mangas)": { An: 0.65 },
                "Fluxo Reverso (mangas)": { An: 0.45 },
            },
            fatores: {
                B: { "Aspiração Simples": 1.0, "Recuperação de Produto": 0.9, "Filtro de Processo": 0.8 },
                C: { "> 100 micron": 1.2, "50-100 micron": 1.1, "10-50 micron": 1.0, "5-10 micron": 0.9, "2-5 micron": 0.8, "< 2 micron": 0.7 },
                D: { "Até 10 g/m³": 1.3, "Até 35 g/m³": 1.1, "Até 60 g/m³": 1.0, "Até 150 g/m³": 0.85, "Acima de 150 g/m³": 0.8 },
                E: { "Até 50°C": 1.0, "Até 85°C": 0.8, "Até 150°C": 0.7, "Acima de 150°C": 0.6 },
                F: { "Densidade > 0.6 g/cm³": 1.0, "Densidade 0.4-0.6 g/cm³": 0.95, "Densidade 0.2-0.4 g/cm³": 0.85, "Densidade < 0.2 g/cm³": 0.65 },
                G: { "A/C Base < 1.8 m/min": 1.0, "A/C Base < 2.2 m/min": 0.9, "A/C Base < 3.0 m/min": 0.8, "A/C Base > 3.0 m/min": 0.7 }
            },
            modelosVentiladores: [
                { modelo: "V-STD-AP (Alta Pressão)", rotor_mm: 630, base_RPM: 1750, base_Q: 2.5, base_P: 3000, efficiency: 0.72, curveCoeffs: [3500, 100, 40] },
                { modelo: "V-STD-AV (Alta Vazão)", rotor_mm: 800, base_RPM: 1150, base_Q: 4.0, base_P: 2000, efficiency: 0.78, curveCoeffs: [2200, 50, 20] },
                { modelo: "V-STD-EQ (Equilibrado)", rotor_mm: 710, base_RPM: 1450, base_Q: 3.0, base_P: 2500, efficiency: 0.75, curveCoeffs: [2800, 80, 30] },
            ]
        };

        // --- MAIN SCRIPT LOGIC ---
        let fanChart = null;
        let finalResults = {};
        let pontoIdCounter = 0;

        document.addEventListener('DOMContentLoaded', () => {
            populateUI();
            addEventListeners();
            addPontoCaptacao();
            updateUIVisibility();
        });

        function populateUI() {
            const populateSelect = (id, data, sort = true) => {
                const select = document.getElementById(id);
                if (!select) {
                    console.error(`Element with ID '${id}' not found.`);
                    return;
                }
                select.innerHTML = '';
                let keys = Object.keys(data);
                if (sort) keys.sort((a, b) => a.localeCompare(b));
                keys.forEach(key => {
                    select.innerHTML += `<option value="${key}">${key}</option>`;
                });
            };
            
            populateSelect('particulado', DADOS_TECNICOS.particulados);
            populateSelect('materialDuto', DADOS_TECNICOS.materiaisDuto, false);
            populateSelect('sistemaLimpeza', DADOS_TECNICOS.sistemasLimpeza, false);
            populateSelect('fatorB', DADOS_TECNICOS.fatores.B, false);
            populateSelect('fatorC', DADOS_TECNICOS.fatores.C, false);
            populateSelect('fatorD', DADOS_TECNICOS.fatores.D, false);
            populateSelect('fatorE', DADOS_TECNICOS.fatores.E, false);
            populateSelect('fatorF', DADOS_TECNICOS.fatores.F, false);
            populateSelect('fatorG', DADOS_TECNICOS.fatores.G, false);

            const estadoSelect = document.getElementById('estado');
            Object.keys(CIDADES_BRASIL).sort().forEach(estado => {
                estadoSelect.innerHTML += `<option value="${estado}">${estado}</option>`;
            });
            updateCidades();
        }

        function addEventListeners() {
            document.getElementById('add-ponto').addEventListener('click', addPontoCaptacao);
            document.getElementById('calcular').addEventListener('click', executarProjeto);
            document.getElementById('particulado').addEventListener('change', updatePoeiraData);
            document.getElementById('modoCalculo').addEventListener('change', updateUIVisibility);
            document.getElementById('estado').addEventListener('change', updateCidades);
            document.getElementById('cidade').addEventListener('change', updateAltitude);
            document.getElementById('emitir-relatorio').addEventListener('click', gerarRelatorio);
        }
        
        function updateCidades() {
            const estado = document.getElementById('estado').value;
            const cidadeSelect = document.getElementById('cidade');
            cidadeSelect.innerHTML = '';
            if (CIDADES_BRASIL[estado]) {
                Object.keys(CIDADES_BRASIL[estado]).sort().forEach(cidade => {
                    cidadeSelect.innerHTML += `<option value="${cidade}">${cidade}</option>`;
                });
            }
            updateAltitude();
        }

        function updateAltitude() {
            const estado = document.getElementById('estado').value;
            const cidade = document.getElementById('cidade').value;
            const altitudeInput = document.getElementById('altitude');
            if (CIDADES_BRASIL[estado] && CIDADES_BRASIL[estado][cidade]) {
                altitudeInput.value = CIDADES_BRASIL[estado][cidade];
            }
        }

        function updatePoeiraData() {
            const particuladoKey = document.getElementById('particulado').value;
            const particuladoData = DADOS_TECNICOS.particulados[particuladoKey];
            if (particuladoData) {
                document.getElementById('fatorC').value = particuladoData.gran;
                document.getElementById('temperatura').value = particuladoData.temp_padrao || 25;
            }
        }

        function updateUIVisibility() {
            const modo = document.getElementById('modoCalculo').value;
            const sections = {
                'card-condicoes-gerais': ['completo', 'tubulacao', 'filtro', 'ventilador'],
                'card-dados-processo': ['completo', 'tubulacao', 'filtro'],
                'card-pontos-captacao': ['completo', 'tubulacao'],
                'card-dim-filtro': ['completo', 'filtro'],
                'card-dados-manuais': ['filtro', 'ventilador'],
                'input-manual-vazao': ['filtro', 'ventilador'],
                'input-manual-perda': ['ventilador'],
                'res-card-geral': ['completo', 'tubulacao', 'filtro', 'ventilador'],
                'res-card-tubulacao': ['completo', 'tubulacao'],
                'res-card-filtro': ['completo', 'filtro'],
                'res-card-ventilador': ['completo', 'ventilador'],
            };

            for (const [sectionId, modes] of Object.entries(sections)) {
                const element = document.getElementById(sectionId);
                if (modes.includes(modo)) {
                    element.classList.remove('hidden-section');
                } else {
                    element.classList.add('hidden-section');
                }
            }
        }
        
        function addPontoCaptacao() {
            pontoIdCounter++;
            const container = document.getElementById('pontos-captacao-container');
            const div = document.createElement('div');
            div.className = 'border p-4 rounded-lg bg-gray-50';
            div.id = `ponto-${pontoIdCounter}`;
            let maquinaOptions = Object.keys(DADOS_TECNICOS.maquinas).sort().map(k => `<option value="${k}">${k}</option>`).join('');
            
            div.innerHTML = `
                <div class="flex justify-between items-center mb-2">
                    <h3 class="font-bold text-lg">Ponto ${pontoIdCounter}</h3>
                    <button class="text-red-500 hover:text-red-700 font-semibold text-sm" onclick="removerPonto(${pontoIdCounter})">REMOVER</button>
                </div>
                <div class="input-group">
                    <label class="input-label">Máquina / Processo</label>
                    <select class="input-field tipo-maquina">${maquinaOptions}</select>
                </div>
                
                <div class="forno-params hidden-section space-y-4">
                     <div class="grid grid-cols-2 gap-4">
                        <div class="input-group"><label class="input-label">Ø Fonte Calor (Ds) [m]</label><input type="number" class="input-field forno-ds" value="1"></div>
                        <div class="input-group"><label class="input-label">Dist. Coifa (Y) [m]</label><input type="number" class="input-field forno-y" value="1"></div>
                     </div>
                     <div class="input-group">
                        <label class="input-label">Temp. Fonte Quente (Tq) [°C]</label>
                        <input type="number" class="input-field forno-tq" value="200">
                     </div>
                </div>

                <div class="input-group vazao-group"><label class="input-label">Vazão (m³/h)</label><input type="number" class="input-field vazao"></div>
                <input type="hidden" class="tipo-captor">
                
                <h4 class="font-semibold mt-4 mb-2">Componentes da Tubulação</h4>
                <div class="componentes-container border-t pt-2"></div>
                <div class="grid grid-cols-3 gap-2 mt-2">
                    <select class="input-field col-span-2 tipo-componente">
                        <option value="duto_reto">Duto Reto</option>
                        <option value="curva_90_raio_longo">Curva 90°</option>
                        <option value="curva_45">Curva 45°</option>
                        <option value="juncao_t_90_graus">Junção T 90°</option>
                        <option value="expansao_gradual_30">Expansão Gradual</option>
                        <option value="reducao_gradual_30">Redução Gradual</option>
                    </select>
                    <button class="btn btn-tertiary add-componente">Add</button>
                </div>
            `;
            container.appendChild(div);
            
            const maquinaSelect = div.querySelector('.tipo-maquina');
            maquinaSelect.addEventListener('change', (e) => updatePontoData(e.target));
            updatePontoData(maquinaSelect);

            div.querySelector('.add-componente').addEventListener('click', (e) => {
                const pontoDiv = e.target.closest('.border');
                const tipo = pontoDiv.querySelector('.tipo-componente').value;
                addComponente(pontoDiv, tipo);
            });
        }

        function addComponente(pontoDiv, tipo) {
            const desc = tipo.replace(/_/g, ' ');
            const unit = tipo === 'duto_reto' ? 'm' : 'unid';
            const valor = prompt(`Insira o valor para ${desc} (${unit}):`, '1');
            if (valor && !isNaN(parseFloat(valor))) {
                const container = pontoDiv.querySelector('.componentes-container');
                const item = document.createElement('div');
                item.className = 'component-item';
                item.dataset.tipo = tipo;
                item.dataset.valor = valor;
                item.innerHTML = `<span>${desc}: ${valor} ${unit}</span><button class="text-red-500 text-xs font-bold" onclick="this.parentElement.remove()">X</button>`;
                container.appendChild(item);
            }
        }
        
        function updatePontoData(selectElement) {
            const pontoDiv = selectElement.closest('.border');
            const maquinaKey = selectElement.value;
            const maquinaData = DADOS_TECNICOS.maquinas[maquinaKey];

            const fornoParamsDiv = pontoDiv.querySelector('.forno-params');
            const vazaoGroupDiv = pontoDiv.querySelector('.vazao-group');

            if (maquinaData) {
                pontoDiv.querySelector('.tipo-captor').value = maquinaData.captor;

                if(maquinaData.calculoEspecial === 'forno') {
                    fornoParamsDiv.classList.remove('hidden-section');
                    vazaoGroupDiv.classList.add('hidden-section');
                    pontoDiv.querySelector('.vazao').value = 0; // Reset vazão
                } else {
                    fornoParamsDiv.classList.add('hidden-section');
                    vazaoGroupDiv.classList.remove('hidden-section');
                    pontoDiv.querySelector('.vazao').value = maquinaData.vazao_m3h;
                }
            }
        }

        function removerPonto(id) { document.getElementById(`ponto-${id}`).remove(); }

        function executarProjeto() {
            try {
                // Primeiro, calcular vazão dos fornos, se houver
                document.querySelectorAll('#pontos-captacao-container > div').forEach(pontoDiv => {
                    const maquinaKey = pontoDiv.querySelector('.tipo-maquina').value;
                    if(DADOS_TECNICOS.maquinas[maquinaKey].calculoEspecial === 'forno') {
                        calcularVazaoForno(pontoDiv);
                    }
                });

                const modo = document.getElementById('modoCalculo').value;
                const { densidadeAr, particulado } = getCommonData();
                let vazaoTotal_m3_s = 0, perdaCargaTubulacao = 0, trechosResultados = [];

                if (['completo', 'tubulacao'].includes(modo)) {
                    const ductingResult = calculateDucting(densidadeAr, particulado);
                    vazaoTotal_m3_s = ductingResult.vazaoTotal_m3_s;
                    perdaCargaTubulacao = ductingResult.perdaCargaTubulacao;
                    trechosResultados = ductingResult.trechosResultados;
                } else {
                    vazaoTotal_m3_s = parseFloat(document.getElementById('vazaoManual').value) / 3600;
                }

                let filtroResultados = {};
                if (['completo', 'filtro'].includes(modo)) {
                    filtroResultados = calculateFilter(vazaoTotal_m3_s, particulado);
                }

                let perdaCargaTotalSistema = calculateTotalPressureDrop(modo, perdaCargaTubulacao, filtroResultados);
                let ventiladorResultados = {};
                if (['completo', 'ventilador'].includes(modo)) {
                    ventiladorResultados = calculateFan(vazaoTotal_m3_s, perdaCargaTotalSistema, particulado);
                }

                finalResults = {
                    inputs: getInputsForReport(),
                    modo, densidadeAr, Vt: particulado.vt, vazaoTotal_m3_s, perdaCargaTotalSistema,
                    trechosResultados, perdaCargaTubulacao, filtroResultados, ventiladorResultados
                };
                apresentarResultados(finalResults);

            } catch (error) {
                console.error("Calculation Error:", error);
                alert("Ocorreu um erro durante o cálculo. Verifique os valores de entrada. Detalhe: " + error.message);
            }
        }
        
        function getCommonData() {
            const altitude = parseFloat(document.getElementById('altitude').value);
            const temperaturaC = parseFloat(document.getElementById('temperatura').value);
            const particuladoKey = document.getElementById('particulado').value;
            const particulado = DADOS_TECNICOS.particulados[particuladoKey];
            
            const T_kelvin = temperaturaC + 273.15;
            const P_atm = 101325 * Math.exp(-altitude / 8200);
            const densidadeAr = P_atm / (287.05 * T_kelvin);
            return { densidadeAr, particulado };
        }
        
        function findStandardDiameter(vazao_m3_s, targetVelocity) {
            const standardDiameters = DADOS_TECNICOS.diametrosPadrao;
            let bestFit = null;
            let smallestError = Infinity;
            const idealDiameter_m = Math.sqrt((4 * vazao_m3_s) / (Math.PI * targetVelocity));

            for (const d_mm of standardDiameters) {
                const d_m = d_mm / 1000;
                const area = Math.PI * Math.pow(d_m, 2) / 4;
                const realVelocity = vazao_m3_s / area;
                const error = Math.abs(realVelocity - targetVelocity);

                if (error <= 1.5) {
                    if (bestFit === null || error < smallestError) {
                        bestFit = d_mm;
                        smallestError = error;
                    }
                }
            }
            
            if (bestFit === null) {
                 const closestDiameter = standardDiameters.reduce((prev, curr) => 
                    Math.abs(curr - (idealDiameter_m * 1000)) < Math.abs(prev - (idealDiameter_m * 1000)) ? curr : prev
                );
                return { diameter: closestDiameter, warning: true };
            }
            
            return { diameter: bestFit, warning: false };
        }

        function calculateDucting(densidadeAr, particulado) {
            let vazaoTotal_m3_s = 0, perdaCargaMaisCritica = 0, trechosResultados = [];
            const targetVelocity = parseFloat(document.getElementById('velocidadeProjeto').value);
            
            document.querySelectorAll('#pontos-captacao-container > div').forEach(pontoDiv => {
                const vazao_m3_h = parseFloat(pontoDiv.querySelector('.vazao').value);
                if (isNaN(vazao_m3_h) || vazao_m3_h === 0) return;
                const vazao_m3_s = vazao_m3_h / 3600;
                vazaoTotal_m3_s += vazao_m3_s;
                
                const { diameter: diametroPadrao_mm, warning } = findStandardDiameter(vazao_m3_s, targetVelocity);
                const diametroPadrao_m = diametroPadrao_mm / 1000;
                const diametroIdeal_m = Math.sqrt((4 * vazao_m3_s) / (Math.PI * targetVelocity));

                const velocidadeReal = (4 * vazao_m3_s) / (Math.PI * Math.pow(diametroPadrao_m, 2));
                const Pd = 0.5 * densidadeAr * Math.pow(velocidadeReal, 2);
                
                const captorKey = pontoDiv.querySelector('.tipo-captor').value;
                const K_captor = DADOS_TECNICOS.captores[captorKey].K;
                let perdaTotalTrecho = K_captor * Pd; // Perda de carga da entrada

                pontoDiv.querySelectorAll('.component-item').forEach(comp => {
                    const tipo = comp.dataset.tipo;
                    const valor = parseFloat(comp.dataset.valor);
                    const acessorio = DADOS_TECNICOS.acessorios[tipo];
                    
                    if (tipo === 'duto_reto') {
                        perdaTotalTrecho += (1 / diametroPadrao_m) * 0.023 * valor * Pd;
                    } else if (acessorio && acessorio.K) {
                        perdaTotalTrecho += acessorio.K * valor * Pd;
                    }
                });

                if (perdaTotalTrecho > perdaCargaMaisCritica) perdaCargaMaisCritica = perdaTotalTrecho;
                
                let warningText = warning ? '<span class="warning">⚠ Vel. fora da faixa ideal</span>' : '';

                trechosResultados.push({ 
                    id: pontoDiv.id.replace('ponto-', 'Ramal '), 
                    diametroIdeal: (diametroIdeal_m * 1000).toFixed(1),
                    diametroPadrao: diametroPadrao_mm,
                    velocidade: `${velocidadeReal.toFixed(2)} ${warningText}`,
                    perda: perdaTotalTrecho
                });
            });

            // Adiciona o trecho principal (tronco)
            if (vazaoTotal_m3_s > 0) {
                 const { diameter: diametroPadrao_mm, warning } = findStandardDiameter(vazaoTotal_m3_s, targetVelocity);
                 const diametroPadrao_m = diametroPadrao_mm / 1000;
                 const diametroIdeal_m = Math.sqrt((4 * vazaoTotal_m3_s) / (Math.PI * targetVelocity));
                 const velocidadeReal = (4 * vazaoTotal_m3_s) / (Math.PI * Math.pow(diametroPadrao_m, 2));
                 let warningText = warning ? '<span class="warning">⚠ Vel. fora da faixa ideal</span>' : '';

                 trechosResultados.push({
                     id: '<b>Trecho Principal</b>',
                     diametroIdeal: (diametroIdeal_m * 1000).toFixed(1),
                     diametroPadrao: diametroPadrao_mm,
                     velocidade: `${velocidadeReal.toFixed(2)} ${warningText}`,
                     perda: 0 // A perda do trecho principal é a do ramal mais crítico
                 });
            }

            return { vazaoTotal_m3_s, perdaCargaTubulacao: perdaCargaMaisCritica, trechosResultados };
        }

        function calculateFilter(vazaoTotal_m3_s, particulado) {
            const A = particulado.A;
            const An = DADOS_TECNICOS.sistemasLimpeza[document.getElementById('sistemaLimpeza').value].An;
            const B = DADOS_TECNICOS.fatores.B[document.getElementById('fatorB').value];
            const C = DADOS_TECNICOS.fatores.C[document.getElementById('fatorC').value];
            const D = DADOS_TECNICOS.fatores.D[document.getElementById('fatorD').value];
            const E = DADOS_TECNICOS.fatores.E[document.getElementById('fatorE').value];
            const F = DADOS_TECNICOS.fatores.F[document.getElementById('fatorF').value];
            const G = DADOS_TECNICOS.fatores.G[document.getElementById('fatorG').value];
            const H = document.getElementById('fatorH').checked ? 0.8 : 1.0;
            
            let relacaoAC_m_min = A * An * B * C * D * E * F * G * H;
            
            if (relacaoAC_m_min < 1.1) relacaoAC_m_min = 1.1;
            else if (relacaoAC_m_min > 2.2) relacaoAC_m_min = 2.2;

            const relacaoAC_m_s = relacaoAC_m_min / 60;

            const areaFiltrante = vazaoTotal_m3_s / relacaoAC_m_s;
            const diametroElemento = parseFloat(document.getElementById('diametroElemento').value) / 1000;
            const comprimentoElemento = parseFloat(document.getElementById('comprimentoElemento').value);
            const areaPorElemento = Math.PI * diametroElemento * comprimentoElemento;
            const qtdeElementosInicial = Math.ceil(areaFiltrante / areaPorElemento);

            const numFileiras = parseInt(document.getElementById('numFileiras').value);
            let mangasPorFileira = Math.ceil(qtdeElementosInicial / numFileiras);
            if (mangasPorFileira % 2 !== 0 && mangasPorFileira > 1) mangasPorFileira++;
            const qtdeElementosCorrigido = mangasPorFileira * numFileiras;
            
            const espacamento = parseFloat(document.getElementById('espacamentoMangas').value) / 1000;
            const distBorda = parseFloat(document.getElementById('distanciaBorda').value) / 1000;
            const larguraCarcaça = (mangasPorFileira - 1) * espacamento + diametroElemento + 2 * distBorda;
            const comprimentoCarcaça = (numFileiras - 1) * espacamento + diametroElemento + 2 * distBorda;
            
            return {
                relacaoAC_m_min, areaFiltrante, areaPorElemento, qtdeElementos: qtdeElementosCorrigido,
                mangasPorFileira, numFileiras, larguraCarcaça, comprimentoCarcaça, 
                totalSolenoides: numFileiras, perdaFiltroEstimada: 1471 // 150 mmca
            };
        }
        
        function calculateTotalPressureDrop(modo, perdaTubulacao, filtroResultados) {
            let pressaoCalculada = 0;
            const comCiclone = document.getElementById('incluirCiclone').checked;

            if (modo === 'completo') {
                pressaoCalculada = perdaTubulacao + (filtroResultados.perdaFiltroEstimada || 0) + (comCiclone ? 785 : 0);
            } else if (modo === 'tubulacao') {
                pressaoCalculada = perdaTubulacao + (comCiclone ? 785 : 0);
            } else if (modo === 'ventilador') {
                pressaoCalculada = parseFloat(document.getElementById('perdaManual').value);
            } else if (modo === 'filtro') {
                pressaoCalculada = (filtroResultados.perdaFiltroEstimada || 0) + (comCiclone ? 785 : 0);
            }
            
            return pressaoCalculada * 1.15; // Adiciona 15% de margem de segurança
        }
        
        function selectStandardMotor(cv) {
            const standardCVs = [0.5, 1, 1.5, 2, 3, 5, 7.5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 100, 125, 150, 200];
            for (const standard of standardCVs) {
                if (standard >= cv) return standard;
            }
            return Math.ceil(cv);
        }

        function calculateFan(vazao_m3_s, pressao_pa_com_margem, particulado) {
            const fanOptions = [];
            const systemK = pressao_pa_com_margem / Math.pow(vazao_m3_s, 2);

            DADOS_TECNICOS.modelosVentiladores.forEach(fan => {
                const RPM_req = fan.base_RPM * Math.sqrt(pressao_pa_com_margem / fan.base_P);
                const potencia_W = (vazao_m3_s * pressao_pa_com_margem) / fan.efficiency;
                const potencia_CV_req = potencia_W / 735.5;
                const motor_CV_std = selectStandardMotor(potencia_CV_req);

                fanOptions.push({
                    modelo: fan.modelo,
                    rendimento: fan.efficiency,
                    rotor: fan.rotor_mm,
                    rpm: RPM_req,
                    motor_cv: motor_CV_std,
                    curveData: fan.curveCoeffs
                });
            });
            
            let rotorSugerido = "Pás radiais (material abrasivo)";
            if (particulado && ['fumo', 'po_fino_organico', 'plastico'].includes(particulado.tipo)) {
                rotorSugerido = "Limit-Load ou Airfoil (alta eficiência)";
            }
            
            return { fanOptions, systemK, rotorSugerido };
        }

        function apresentarResultados(res) {
            document.getElementById('resultados-container').classList.remove('hidden');
            
            document.getElementById('res-densidade').textContent = `${res.densidadeAr.toFixed(4)} kg/m³`;
            document.getElementById('res-velocidade-transporte').textContent = document.getElementById('velocidadeProjeto').value + ' m/s';
            document.getElementById('res-vazao-total').textContent = `${(res.vazaoTotal_m3_s * 3600).toFixed(2)} m³/h (${res.vazaoTotal_m3_s.toFixed(2)} m³/s)`;
            document.getElementById('res-perda-carga-total').textContent = `${res.perdaCargaTotalSistema.toFixed(2)} Pa (~${(res.perdaCargaTotalSistema / 9.80665).toFixed(2)} mmH₂O)`;

            const trechosTable = document.getElementById('res-trechos-table');
            trechosTable.innerHTML = '';
            if(res.trechosResultados && res.trechosResultados.length > 0) {
                res.trechosResultados.forEach(t => {
                    trechosTable.innerHTML += `<tr><td>${t.id}</td><td>${t.diametroIdeal}</td><td>${t.diametroPadrao}</td><td>${t.velocidade}</td><td>${t.perda.toFixed(2)}</td></tr>`;
                });
                trechosTable.innerHTML += `<tr class="bg-gray-100 font-bold"><td colspan="4">Perda de Carga Máxima na Tubulação</td><td>${res.perdaCargaTubulacao.toFixed(2)}</td></tr>`;
            }

            const f = res.filtroResultados;
            if (f && f.qtdeElementos) {
                document.getElementById('res-relacao-ac').textContent = `${f.relacaoAC_m_min.toFixed(2)} m/min`;
                document.getElementById('res-area-filtrante').textContent = `${f.areaFiltrante.toFixed(2)} m²`;
                document.getElementById('res-qtde-elementos').textContent = `${f.qtdeElementos} mangas`;
                document.getElementById('res-arranjo-mangas').textContent = `${f.mangasPorFileira} mangas/fileira x ${f.numFileiras} fileiras`;
                document.getElementById('res-dimensoes-carcaca').textContent = `${f.larguraCarcaça.toFixed(2)} m x ${f.comprimentoCarcaça.toFixed(2)} m`;
            }

            const v = res.ventiladorResultados;
            if (v && v.fanOptions) {
                const fanTable = document.getElementById('ventiladores-table');
                fanTable.innerHTML = '';
                v.fanOptions.forEach((fan, index) => {
                    fanTable.innerHTML += `<tr><td><input type="radio" name="fan-select" value="${index}" class="input-field h-5"></td><td>${fan.modelo}</td><td>${(fan.rendimento * 100).toFixed(1)}%</td><td>${fan.rotor}</td><td>${fan.rpm.toFixed(0)}</td><td>${fan.motor_cv}</td></tr>`;
                });
                fanTable.querySelector('input').checked = true;
                desenharGraficoVentiladores(res.vazaoTotal_m3_s, v.systemK, v.fanOptions);
            }
            window.scrollTo({ top: document.getElementById('resultados-container').offsetTop, behavior: 'smooth' });
        }

        function desenharGraficoVentiladores(operatingQ, systemK, fanOptions) {
            const ctx = document.getElementById('ventiladorChart').getContext('2d');
            if (fanChart) fanChart.destroy();

            const maxQ = operatingQ * 2;
            const systemCurveData = Array.from({length: 20}, (_, i) => {
                const q = (maxQ / 19) * i;
                return { x: q * 3600, y: systemK * q * q };
            });

            const datasets = [{
                label: 'Curva do Sistema', data: systemCurveData, borderColor: '#ef4444',
                borderWidth: 3, fill: false, tension: 0.4, pointRadius: 0
            }];

            const colors = ['#3b82f6', '#10b981', '#8b5cf6'];
            fanOptions.forEach((fan, index) => {
                const [a, b, c] = fan.curveData;
                const fanCurveData = Array.from({length: 20}, (_, i) => {
                    const q = (maxQ / 19) * i;
                    const p = a - b * q - c * q * q;
                    return { x: q * 3600, y: p > 0 ? p : 0 };
                });
                datasets.push({
                    label: fan.modelo, data: fanCurveData, borderColor: colors[index % colors.length],
                    borderWidth: 2, fill: false, borderDash: [5, 5], pointRadius: 0
                });
            });

            fanChart = new Chart(ctx, {
                type: 'line', data: { datasets },
                options: {
                    responsive: true,
                    scales: { x: { title: { display: true, text: 'Vazão (m³/h)' } }, y: { title: { display: true, text: 'Pressão Estática (Pa)' } } },
                    plugins: { title: { display: true, text: 'Curvas de Desempenho: Ventilador vs. Sistema' } }
                }
            });
        }
        
        function getInputsForReport() {
            const pontos = [];
            document.querySelectorAll('#pontos-captacao-container > div').forEach(pontoDiv => {
                const maquina = pontoDiv.querySelector('.tipo-maquina').value;
                const vazao = pontoDiv.querySelector('.vazao').value;
                const isForno = DADOS_TECNICOS.maquinas[maquina]?.calculoEspecial === 'forno';
                const pontoData = {
                    id: pontoDiv.id.replace('ponto-','Ponto '),
                    maquina,
                    vazao,
                    isForno,
                    fornoCalcs: isForno ? JSON.parse(pontoDiv.dataset.fornoCalcs || '{}') : null
                };
                pontos.push(pontoData);
            });

            return {
                cidade: document.getElementById('cidade').value,
                estado: document.getElementById('estado').value,
                altitude: document.getElementById('altitude').value,
                particulado: document.getElementById('particulado').value,
                temperatura: document.getElementById('temperatura').value,
                fatorB: document.getElementById('fatorB').selectedOptions[0].text,
                fatorC: document.getElementById('fatorC').selectedOptions[0].text,
                fatorD: document.getElementById('fatorD').selectedOptions[0].text,
                fatorE: document.getElementById('fatorE').selectedOptions[0].text,
                sistemaLimpeza: document.getElementById('sistemaLimpeza').selectedOptions[0].text,
                diametroManga: document.getElementById('diametroElemento').value,
                comprimentoManga: document.getElementById('comprimentoElemento').value,
                incluirCiclone: document.getElementById('incluirCiclone').checked,
                pontos: pontos,
            };
        }

        function gerarRelatorio() {
            if (Object.keys(finalResults).length === 0) {
                alert("Por favor, execute o cálculo primeiro.");
                return;
            }
            const reportContainer = document.getElementById('relatorio-impressao');
            const i = finalResults.inputs;
            const f = finalResults.filtroResultados;
            const v = finalResults.ventiladorResultados;
            const selectedFanIndex = document.querySelector('input[name="fan-select"]:checked')?.value;
            const selectedFan = (selectedFanIndex && v.fanOptions) ? v.fanOptions[selectedFanIndex] : null;

            const today = new Date();
            const dateStr = today.toLocaleDateString('pt-BR', { day: '2-digit', month: 'long', year: 'numeric' });

            // Gerar HTML para os pontos de captação, incluindo detalhes do forno
            const pontosHTML = i.pontos.map(p => {
                if(p.isForno && p.fornoCalcs) {
                    const c = p.fornoCalcs;
                    return `
                    <h3 style="font-size: 12px; font-weight: bold; margin-top:15px">Memorial de Cálculo - Coifa Quente (${p.id})</h3>
                    <table class="report-table">
                        <tr><th>Parâmetro</th><th>Valor</th><th>Unidade</th><th>Descrição</th></tr>
                        <tr><td>Ds</td><td>${c.Ds.toFixed(2)}</td><td>m</td><td>Diâmetro da Fonte de Calor</td></tr>
                        <tr><td>Y</td><td>${c.Y.toFixed(2)}</td><td>m</td><td>Distância da Fonte à Coifa</td></tr>
                        <tr><td>Tq</td><td>${c.Tq.toFixed(2)}</td><td>°C</td><td>Temperatura da Fonte Quente</td></tr>
                        <tr><td>Ta</td><td>${c.Ta.toFixed(2)}</td><td>°C</td><td>Temperatura Ambiente</td></tr>
                        <tr style="background-color: #f2f2f2;"><td><b>Dc</b></td><td><b>${c.Dc.toFixed(2)}</b></td><td>m</td><td><b>Diâmetro da Pluma de Ar Quente</b></td></tr>
                        <tr style="background-color: #f2f2f2;"><td><b>Vf</b></td><td><b>${c.Vf.toFixed(2)}</b></td><td>m/s</td><td><b>Velocidade da Pluma de Ar Quente</b></td></tr>
                        <tr style="background-color: #f2f2f2;"><td><b>Dcoifa</b></td><td><b>${c.Dcoifa.toFixed(2)}</b></td><td>m</td><td><b>Diâmetro Ideal da Coifa</b></td></tr>
                        <tr style="background-color: #f2f2f2;"><td><b>Qconv</b></td><td><b>${(c.Q_conv_m3s * 3600).toFixed(2)}</b></td><td>m³/h</td><td><b>Vazão da Pluma de Convecção</b></td></tr>
                        <tr style="background-color: #e6e6e6;"><td><b>Qtotal</b></td><td><b>${(c.Q_total_m3s * 3600).toFixed(2)}</b></td><td>m³/h</td><td><b>VAZÃO TOTAL RECOMENDADA</b></td></tr>
                    </table>`;
                }
                return '';
            }).join('');


            const reportHTML = `
                <style>
                    .report-body { font-family: Arial, sans-serif; font-size: 11px; line-height: 1.5; }
                    .report-header { text-align: center; margin-bottom: 30px; }
                    .report-header h1 { font-size: 18px; font-weight: bold; margin: 0; }
                    .report-header p { font-size: 12px; margin: 0; }
                    .report-h1 { font-size: 16px; font-weight: bold; text-align: center; margin-bottom: 25px; border-bottom: 2px solid #000; padding-bottom: 10px; }
                    .report-h2 { font-size: 13px; font-weight: bold; margin-top: 25px; margin-bottom: 10px; border-bottom: 1px solid #888; padding-bottom: 5px; }
                    .report-table { width: 100%; border-collapse: collapse; margin-bottom: 15px; }
                    .report-table th, .report-table td { border: 1px solid #ccc; padding: 5px; text-align: left; }
                    .report-table th { background-color: #e9ecef; font-weight: bold; }
                    .report-footer { text-align: center; font-size: 9px; margin-top: 40px; border-top: 1px solid #ccc; padding-top: 10px; }
                </style>
                <div class="report-body">
                    <div class="report-header">
                        <h1>ATMO Sistemas, Consultoria e Serviços LTDA.</h1>
                        <p>Soluções em Engenharia Ambiental e Controle de Poluição</p>
                    </div>
                    <h1 class="report-h1">MEMORIAL DE CÁLCULO E ESPECIFICAÇÕES TÉCNICAS</h1>
                    <p style="text-align: right;">Data: ${dateStr}</p>
                    
                    <h2 class="report-h2">1. DADOS DE PROJETO</h2>
                    <table class="report-table">
                        <tr><th>Local</th><td>${i.cidade}, ${i.estado}</td><th>Altitude</th><td>${i.altitude} m</td></tr>
                        <tr><th>Particulado</th><td>${i.particulado}</td><th>Temperatura de Operação</th><td>${i.temperatura} °C</td></tr>
                    </table>

                    ${pontosHTML}

                    <h2 class="report-h2">2. RESUMO DO DIMENSIONAMENTO</h2>
                    <table class="report-table">
                        <tr><th>Densidade do Ar (ρ)</th><td>${finalResults.densidadeAr.toFixed(4)} kg/m³</td></tr>
                        <tr><th>Velocidade de Projeto (Vt)</th><td>${document.getElementById('velocidadeProjeto').value} m/s</td></tr>
                        <tr><th>Vazão Total do Sistema (Q)</th><td><b>${(finalResults.vazaoTotal_m3_s * 3600).toFixed(2)} m³/h</b></td></tr>
                        <tr><th>Relação Ar/Pano (A/C)</th><td>${f.relacaoAC_m_min ? f.relacaoAC_m_min.toFixed(2) : 'N/A'} m/min</td></tr>
                        <tr><th>Perda de Carga na Tubulação</th><td>${finalResults.perdaCargaTubulacao.toFixed(2)} Pa</td></tr>
                        ${i.incluirCiclone ? `<tr><th>Perda de Carga no Ciclone</th><td>785.00 Pa (Estimado)</td></tr>` : ''}
                        ${finalResults.modo !== 'tubulacao' ? `<tr><th>Perda de Carga no Filtro (Estimada)</th><td>${f.perdaFiltroEstimada ? f.perdaFiltroEstimada.toFixed(2) : 'N/A'} Pa</td></tr>` : ''}
                        <tr><th>Perda de Carga Total (c/ margem de 15%)</th><td><b>${finalResults.perdaCargaTotalSistema.toFixed(2)} Pa (~${(finalResults.perdaCargaTotalSistema / 9.80665).toFixed(2)} mmH₂O)</b></td></tr>
                    </table>

                    <h2 class="report-h2">3. ESPECIFICAÇÕES TÉCNICAS</h2>
                    
                    ${f.qtdeElementos ? `
                    <h3>3.1. Filtro de Mangas</h3>
                    <table class="report-table">
                        <tr><th>Tipo</th><td>Filtro de Mangas com limpeza por Jato Pulsante</td></tr>
                        <tr><th>Área Filtrante</th><td>${f.areaFiltrante.toFixed(2)} m²</td></tr>
                        <tr><th>Quantidade de Mangas</th><td>${f.qtdeElementos}</td></tr>
                        <tr><th>Dimensões da Manga</th><td>Ø ${i.diametroManga} mm x ${i.comprimentoManga * 1000} mm (Comp.)</td></tr>
                        <tr><th>Arranjo</th><td>${f.mangasPorFileira} mangas por fileira x ${f.numFileiras} fileiras</td></tr>
                        <tr><th>Dimensões da Carcaça (aprox.)</th><td>${f.larguraCarcaça.toFixed(2)} m (L) x ${f.comprimentoCarcaça.toFixed(2)} m (C)</td></tr>
                        <tr><th>Sistema de Limpeza</th><td>${i.sistemaLimpeza} com ${f.totalSolenoides} válvulas</td></tr>
                    </table>` : '<p><i>Filtro não calculado neste modo.</i></p>'}

                    ${selectedFan ? `
                    <h3>3.2. Ventilador Centrífugo</h3>
                    <table class="report-table">
                        <tr><th>Modelo Sugerido</th><td>${selectedFan.modelo}</td></tr>
                        <tr><th>Diâmetro do Rotor</th><td>${selectedFan.rotor} mm</td></tr>
                        <tr><th>Rotação de Operação</th><td>${selectedFan.rpm.toFixed(0)} RPM</td></tr>
                        <tr><th>Potência de Motor Padrão</th><td>${selectedFan.motor_cv} CV</td></tr>
                        <tr><th>Rendimento do Ventilador</th><td>${(selectedFan.rendimento * 100).toFixed(1)}%</td></tr>
                        <tr><th>Tipo de Rotor Sugerido</th><td>${v.rotorSugerido}</td></tr>
                    </table>
                    ` : '<p><i>Ventilador não calculado neste modo.</i></p>'}

                    ${finalResults.trechosResultados.length > 0 ? `
                    <h3>3.3. Tubulação</h3>
                    <table class="report-table">
                        <thead><tr><th>Trecho</th><th>Ø Ideal (mm)</th><th>Ø Padrão (mm)</th><th>Veloc. Real (m/s)</th><th>Perda Carga (Pa)</th></tr></thead>
                        <tbody>
                            ${finalResults.trechosResultados.map(t => `
                                <tr><td>${t.id}</td><td>${t.diametroIdeal}</td><td>${t.diametroPadrao}</td><td>${t.velocidade}</td><td>${t.perda.toFixed(2)}</td></tr>
                            `).join('')}
                        </tbody>
                    </table>` : '<p><i>Tubulação não calculada neste modo.</i></p>'}
                    
                    <div class="report-footer">
                        Relatório gerado por ATMO Sistemas, Consultoria e Serviços LTDA. Os resultados devem ser verificados por um engenheiro qualificado.
                    </div>
                </div>
            `;
            reportContainer.innerHTML = reportHTML;
            document.body.classList.add('printing');
            window.print();
            document.body.classList.remove('printing');
        }

    </script>
</body>
</html>
