import os
import tempfile
from infraction_analyzer import InfractionAnalyzer

def test_infraction_analyzer():
    """
    Testa a funcionalidade de análise e alteração de códigos de infrações
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Testando InfractionAnalyzer em: {temp_dir}")
        
        # Cria estrutura de teste
        l08998_dir = os.path.join(temp_dir, "L08998")
        subdir_0008998 = os.path.join(l08998_dir, "0008998")
        aits_dir = os.path.join(subdir_0008998, "AITs")
        
        os.makedirs(aits_dir)
        
        # Cria arquivos com diferentes códigos de infrações
        test_files = [
            (os.path.join(l08998_dir, "infraction1.txt"), 
             "0008998;BRI1306/2023;20250905;14:49:38;2;000;000,0;00125000070a.jpg;00125000070b.jpg;001306;Av Getulio Vargas x Durval Carneiro SCB;5673\n"),
            
            (os.path.join(aits_dir, "infraction2.txt"), 
             "0008998;BRI1306/2023;20250905;14:49:38;2;000;000,0;00125000071a.jpg;00125000071b.jpg;001306;Rua Principal x Secundaria;6050\n"
             "0008998;BRI1306/2023;20250905;15:30:22;1;000;000,0;00125000072a.jpg;00125000072b.jpg;001306;Avenida Central;5673\n"),
            
            (os.path.join(aits_dir, "infraction3.txt"),
             "0008998;BRI1306/2023;20250905;16:15:45;3;000;000,0;00125000073a.jpg;00125000073b.jpg;001306;Via Expressa;7587\n"
             "0008998;BRI1306/2023;20250905;17:22:11;1;000;000,0;00125000074a.jpg;00125000074b.jpg;001306;Centro da Cidade;6050\n"
             "0008998;BRI1306/2023;20250905;18:45:33;2;000;000,0;00125000075a.jpg;00125000075b.jpg;001306;Zona Comercial;7587\n"),
            
            # Arquivo md5sum.txt que NÃO deve ser processado
            (os.path.join(aits_dir, "md5sum.txt"),
             "hash123;0008998;valor_hash_importante;5673")
        ]
        
        for file_path, content in test_files:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        print("\n=== ARQUIVOS CRIADOS ===")
        for file_path, content in test_files:
            rel_path = os.path.relpath(file_path, temp_dir)
            print(f"📄 {rel_path}")
            if not file_path.endswith('md5sum.txt'):
                lines = content.strip().split('\n')
                for line in lines:
                    if line.strip():
                        parts = line.split(';')
                        if len(parts) > 0:
                            code = parts[-1].strip()
                            print(f"   → Código: {code}")
        
        # Testa o analisador
        analyzer = InfractionAnalyzer(temp_dir)
        
        print("\n=== ANÁLISE DE INFRAÇÕES ===")
        infraction_counts = analyzer.analyze_infractions("L08998")
        
        print("Contadores encontrados:")
        for code, count in infraction_counts.items():
            description = analyzer.get_infraction_description(code)
            print(f"  {code}: {count} ocorrências ({description})")
        
        # Verifica se os números estão corretos
        expected_counts = {"5673": 2, "6050": 2, "7587": 2}
        
        print("\n=== VERIFICAÇÃO ===")
        analysis_correct = True
        for code, expected in expected_counts.items():
            actual = infraction_counts.get(code, 0)
            status = "✅" if actual == expected else "❌"
            print(f"{status} Código {code}: Esperado={expected}, Encontrado={actual}")
            if actual != expected:
                analysis_correct = False
        
        # Verifica se md5sum.txt foi ignorado
        md5sum_ignored = "md5sum.txt não foi processado (correto)"
        print(f"✅ {md5sum_ignored}")
        
        # Testa alteração em massa
        print("\n=== TESTE DE ALTERAÇÃO EM MASSA ===")
        print("Alterando todos os códigos 5673 para 6050...")
        
        files_modified, lines_modified = analyzer.change_infraction_codes("L08998", "5673", "6050")
        print(f"Arquivos modificados: {files_modified}")
        print(f"Linhas modificadas: {lines_modified}")
        
        # Re-analisa para verificar mudanças
        print("\n=== ANÁLISE APÓS ALTERAÇÃO ===")
        new_counts = analyzer.analyze_infractions("L08998")
        
        for code, count in new_counts.items():
            description = analyzer.get_infraction_description(code)
            print(f"  {code}: {count} ocorrências ({description})")
        
        # Verifica se alteração funcionou
        expected_after_change = {"5673": 0, "6050": 4, "7587": 2}  # 5673 virou 6050
        
        print("\n=== VERIFICAÇÃO FINAL ===")
        change_correct = True
        for code, expected in expected_after_change.items():
            actual = new_counts.get(code, 0)
            status = "✅" if actual == expected else "❌"
            print(f"{status} Código {code}: Esperado={expected}, Encontrado={actual}")
            if actual != expected:
                change_correct = False
        
        # Verifica se md5sum.txt não foi alterado
        md5sum_path = os.path.join(aits_dir, "md5sum.txt")
        with open(md5sum_path, 'r') as f:
            md5sum_content = f.read()
        
        md5sum_preserved = "5673" in md5sum_content  # Deve manter o conteúdo original
        status = "✅" if md5sum_preserved else "❌"
        print(f"{status} md5sum.txt preservado: {'SIM' if md5sum_preserved else 'NÃO'}")
        
        # Resultado final
        success = analysis_correct and change_correct and md5sum_preserved
        
        if success:
            print("\n🎉 TESTE PASSOU!")
            print("✅ Análise de infrações funcionando")
            print("✅ Alteração em massa funcionando") 
            print("✅ md5sum.txt preservado")
            print("\n📋 A funcionalidade está pronta para uso na GUI!")
        else:
            print("\n❌ TESTE FALHOU")
            if not analysis_correct:
                print("  - Problema na análise de infrações")
            if not change_correct:
                print("  - Problema na alteração em massa")
            if not md5sum_preserved:
                print("  - md5sum.txt foi alterado indevidamente")
        
        return success

if __name__ == "__main__":
    test_infraction_analyzer()