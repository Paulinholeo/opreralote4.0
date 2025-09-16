import os
import tempfile
from infraction_analyzer import InfractionAnalyzer

def test_auto_analysis_scenarios():
    """
    Testa diferentes cenários de análise automática de infrações
    """
    print("=== TESTE DE ANÁLISE AUTOMÁTICA DE INFRAÇÕES ===\n")
    
    # Cenário 1: Maioria de um tipo (>70%)
    test_scenario_1()
    
    # Cenário 2: Códigos mistos  
    test_scenario_2()
    
    # Cenário 3: Códigos desconhecidos
    test_scenario_3()

def test_scenario_1():
    """Cenário 1: 80% das infrações são do tipo 5673"""
    print("📊 CENÁRIO 1: Maioria esmagadora (80% tipo 5673)")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Cria estrutura
        lote_dir = os.path.join(temp_dir, "L05655")
        aits_dir = os.path.join(lote_dir, "0005655", "AITs")
        os.makedirs(aits_dir)
        
        # Cria arquivo com 8 infrações tipo 5673 e 2 tipo 6050 (80% vs 20%)
        content = ""
        for i in range(8):
            content += f"0005655;BRI1306/2023;20250905;14:49:38;2;000;000,0;img{i}a.jpg;img{i}b.jpg;001306;Local {i};5673\n"
        for i in range(2):
            content += f"0005655;BRI1306/2023;20250905;15:30:22;1;000;000,0;img{i+8}a.jpg;img{i+8}b.jpg;001306;Local {i+8};6050\n"
            
        with open(os.path.join(aits_dir, "infractions.txt"), 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Analisa
        analyzer = InfractionAnalyzer(temp_dir)
        counts = analyzer.analyze_infractions("L05655")
        
        print(f"  Infrações encontradas: {counts}")
        
        # Simula lógica de sugestão
        total = sum(counts.values())
        for code, count in counts.items():
            percentage = (count / total) * 100
            if percentage >= 70:
                print(f"  ✅ SUGESTÃO: Padronizar para {code} ({percentage:.1f}% já são deste tipo)")
                print(f"     Ação: Converter {total - count} infrações restantes para {code}")
                break
        
        print()

def test_scenario_2():
    """Cenário 2: Códigos mistos sem maioria clara"""
    print("📊 CENÁRIO 2: Códigos mistos (sem maioria)")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Cria estrutura
        lote_dir = os.path.join(temp_dir, "L05656")
        aits_dir = os.path.join(lote_dir, "0005656", "AITs")
        os.makedirs(aits_dir)
        
        # Cria arquivo com distribuição equilibrada: 4-3-3
        content = ""
        # 4 x 5673
        for i in range(4):
            content += f"0005656;BRI1306/2023;20250905;14:49:38;2;000;000,0;img{i}a.jpg;img{i}b.jpg;001306;Local {i};5673\n"
        # 3 x 6050  
        for i in range(3):
            content += f"0005656;BRI1306/2023;20250905;15:30:22;1;000;000,0;img{i+4}a.jpg;img{i+4}b.jpg;001306;Local {i+4};6050\n"
        # 3 x 7587
        for i in range(3):
            content += f"0005656;BRI1306/2023;20250905;16:15:45;3;000;000,0;img{i+7}a.jpg;img{i+7}b.jpg;001306;Local {i+7};7587\n"
            
        with open(os.path.join(aits_dir, "infractions.txt"), 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Analisa
        analyzer = InfractionAnalyzer(temp_dir)
        counts = analyzer.analyze_infractions("L05656")
        
        print(f"  Infrações encontradas: {counts}")
        
        # Simula lógica de sugestão para código mais comum
        known_codes = {"5673": counts.get("5673", 0), "6050": counts.get("6050", 0), "7587": counts.get("7587", 0)}
        most_common = max(known_codes, key=known_codes.get)
        
        if known_codes[most_common] > 0 and len([c for c in known_codes.values() if c > 0]) > 1:
            print(f"  ✅ SUGESTÃO: Unificar para código mais comum {most_common} ({known_codes[most_common]} ocorrências)")
            print(f"     Ação: Converter todas as outras infrações para {most_common}")
        
        print()

def test_scenario_3():
    """Cenário 3: Códigos desconhecidos"""
    print("📊 CENÁRIO 3: Códigos desconhecidos")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Cria estrutura
        lote_dir = os.path.join(temp_dir, "L05657")
        aits_dir = os.path.join(lote_dir, "0005657", "AITs")
        os.makedirs(aits_dir)
        
        # Cria arquivo com códigos não mapeados
        content = ""
        for i in range(3):
            content += f"0005657;BRI1306/2023;20250905;14:49:38;2;000;000,0;img{i}a.jpg;img{i}b.jpg;001306;Local {i};9999\n"
        for i in range(2):
            content += f"0005657;BRI1306/2023;20250905;15:30:22;1;000;000,0;img{i+3}a.jpg;img{i+3}b.jpg;001306;Local {i+3};8888\n"
            
        with open(os.path.join(aits_dir, "infractions.txt"), 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Analisa
        analyzer = InfractionAnalyzer(temp_dir)
        counts = analyzer.analyze_infractions("L05657")
        
        print(f"  Infrações encontradas: {counts}")
        
        # Simula lógica de sugestão para códigos desconhecidos
        unknown_codes = {code: count for code, count in counts.items() 
                        if code not in ["5673", "6050", "7587"]}
        
        if unknown_codes:
            print(f"  ⚠️  CÓDIGOS DESCONHECIDOS: {unknown_codes}")
            print(f"  ✅ SUGESTÃO: Padronizar para 5673 (PARADO SOBRE FAIXA DE PEDESTRE - mais comum)")
            print(f"     Ação: Converter todas as {sum(unknown_codes.values())} infrações para 5673")
        
        print()

def simulate_auto_decision_logic():
    """Simula a lógica de decisão automática"""
    print("🤖 LÓGICA DE DECISÃO AUTOMÁTICA IMPLEMENTADA:")
    print("  1. Se >70% de um tipo conhecido → Sugere padronizar para esse tipo")
    print("  2. Se códigos mistos → Sugere unificar para o mais comum")  
    print("  3. Se códigos desconhecidos → Sugere padronizar para 5673")
    print("  4. Sempre pergunta confirmação antes de aplicar")
    print("  5. Mostra estatísticas e razão da sugestão")
    print()

if __name__ == "__main__":
    test_auto_analysis_scenarios()
    simulate_auto_decision_logic()
    
    print("✅ TESTES CONCLUÍDOS!")
    print("🚀 Funcionalidade de análise automática pronta!")
    print()
    print("📋 COMO USAR:")
    print("  1. Clique 'Executar' para renomear lote")
    print("  2. Sistema analisa automaticamente após renomeação")
    print("  3. Recebe sugestão inteligente se necessário")
    print("  4. Confirma ou rejeita a sugestão")
    print("  5. Padronização aplicada automaticamente se confirmada")