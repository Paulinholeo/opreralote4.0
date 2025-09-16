import os
import glob
from collections import defaultdict

class InfractionAnalyzer:
    """
    Classe para análise e modificação de códigos de infrações em arquivos de texto
    """
    
    def __init__(self, directory):
        self.directory = directory
        self.infraction_types = {
            "5673": "PARADO SOBRE A FAIXA DE PEDESTRE",
            "6050": "AVANÇO DE SINAL VERMELHO", 
            "7587": "TRANSITAR EM FAIXA EXCLUSIVA"
        }
        
    def analyze_infractions(self, lote_name):
        """
        Analisa todos os arquivos .txt do lote e conta infrações por tipo
        Retorna: dict com contadores de infrações
        """
        infraction_counts = defaultdict(int)
        
        # Define os diretórios onde procurar arquivos
        search_directories = self._get_search_directories(lote_name)
        
        for search_dir in search_directories:
            if not os.path.exists(search_dir):
                continue
                
            for filename in glob.glob(os.path.join(search_dir, '*.txt')):
                # Pula md5sum.txt
                if os.path.basename(filename).lower() == 'md5sum.txt':
                    continue
                    
                try:
                    with open(filename, 'r', encoding='utf-8') as file:
                        for line in file:
                            line = line.strip()
                            if not line:
                                continue
                                
                            # Split da linha por ';'
                            parts = line.split(';')
                            
                            # O código de infração está na última posição
                            if len(parts) > 0:
                                infraction_code = parts[-1].strip()
                                if infraction_code and infraction_code.isdigit():
                                    infraction_counts[infraction_code] += 1
                                    
                except Exception as e:
                    print(f"Erro ao analisar arquivo {filename}: {e}")
                    
        return dict(infraction_counts)
    
    def change_infraction_codes(self, lote_name, old_code, new_code):
        """
        Altera todas as ocorrências de old_code para new_code nos arquivos do lote
        """
        files_modified = 0
        lines_modified = 0
        
        # Define os diretórios onde procurar arquivos
        search_directories = self._get_search_directories(lote_name)
        
        for search_dir in search_directories:
            if not os.path.exists(search_dir):
                continue
                
            for filename in glob.glob(os.path.join(search_dir, '*.txt')):
                # Pula md5sum.txt - NUNCA alterar
                if os.path.basename(filename).lower() == 'md5sum.txt':
                    continue
                    
                try:
                    # Lê o arquivo
                    with open(filename, 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                    
                    new_lines = []
                    file_changed = False
                    
                    for line in lines:
                        original_line = line
                        line_stripped = line.strip()
                        
                        if not line_stripped:
                            new_lines.append(line)
                            continue
                            
                        # Split da linha por ';'
                        parts = line_stripped.split(';')
                        
                        # Verifica se o código de infração (última posição) é o que queremos alterar
                        if len(parts) > 0:
                            current_code = parts[-1].strip()
                            if current_code == old_code:
                                parts[-1] = new_code
                                new_line = ';'.join(parts) + '\n'
                                new_lines.append(new_line)
                                file_changed = True
                                lines_modified += 1
                                print(f"Alterado: {current_code} -> {new_code} em {os.path.basename(filename)}")
                            else:
                                new_lines.append(original_line)
                        else:
                            new_lines.append(original_line)
                    
                    # Salva o arquivo se houver mudanças
                    if file_changed:
                        with open(filename, 'w', encoding='utf-8') as file:
                            file.writelines(new_lines)
                        files_modified += 1
                        print(f"Arquivo modificado: {filename}")
                        
                except Exception as e:
                    print(f"Erro ao modificar arquivo {filename}: {e}")
                    
        return files_modified, lines_modified
    
    def _get_search_directories(self, lote_name):
        """
        Retorna lista de diretórios onde procurar arquivos de texto
        """
        search_directories = []
        
        # Diretório principal do lote
        main_dir = os.path.join(self.directory, lote_name)
        if os.path.exists(main_dir):
            search_directories.append(main_dir)
            
            # Busca subdiretórios
            for item in os.listdir(main_dir):
                item_path = os.path.join(main_dir, item)
                if os.path.isdir(item_path):
                    search_directories.append(item_path)
                    
                    # Adiciona subdiretórios AITs se existirem
                    aits_path = os.path.join(item_path, 'AITs')
                    if os.path.exists(aits_path):
                        search_directories.append(aits_path)
        
        return search_directories
    
    def get_infraction_description(self, code):
        """
        Retorna a descrição da infração pelo código
        """
        return self.infraction_types.get(code, f"Código {code}")