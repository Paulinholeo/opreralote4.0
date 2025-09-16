import os
import glob
import re

class TextFileEditor:
    def __init__(self, directory):
        self.directory = directory

    def _extract_numbers_from_name(self, name):
        """
        Extrai o número do nome do lote, removendo o prefixo 'L' se existir.
        
        Args:
            name (str): Nome do lote (ex: "L0544" ou "0544")
            
        Returns:
            str: Número do lote sem prefixo (ex: "0544")
        """
        return name[1:] if name.startswith('L') else name

    def _create_padded_number(self, number, padding=7):
        """
        Cria um número com padding específico de zeros à esquerda.
        
        Args:
            number (str): Número a ser padronizado
            padding (int): Quantidade de dígitos desejada (padrão: 7)
            
        Returns:
            str: Número padronizado com zeros à esquerda
        """
        return str(number).zfill(padding)

    def _get_search_directories(self):
        """
        Obtém todos os diretórios onde devemos procurar por arquivos de texto.
        
        Returns:
            list: Lista de caminhos de diretórios
        """
        search_directories = [self.directory]
        
        # Se há estrutura com AITs, adiciona os subdiretórios à busca
        main_dir = self.directory
        if os.path.exists(main_dir):
            for item in os.listdir(main_dir):
                item_path = os.path.join(main_dir, item)
                if os.path.isdir(item_path):
                    search_directories.append(item_path)
                    # Adiciona também subdiretórios de AITs se existirem
                    aits_path = os.path.join(item_path, 'AITs')
                    if os.path.exists(aits_path):
                        search_directories.append(aits_path)
        
        return search_directories

    def _update_jpg_filename(self, filename, old_name_number, new_name_number):
        """
        Atualiza nomes de arquivos JPG em uma linha de texto.
        
        Args:
            filename (str): Nome do arquivo JPG a ser atualizado
            old_name_number (str): Número antigo do lote
            new_name_number (str): Número novo do lote
            
        Returns:
            str: Nome do arquivo atualizado
        """
        # Padroniza os números
        old_number_trimmed = old_name_number.lstrip('0')
        new_number_padded = self._create_padded_number(new_name_number)
        
        # Procura pelo padrão específico: 00 + número_do_lote
        pattern = r'00' + re.escape(old_number_trimmed)
        match = re.search(pattern, filename)
        
        if match:
            # Substitui o padrão encontrado pelo novo número
            # Mas também remove o número sequencial que vem depois
            start_pos = match.end()
            remaining = filename[start_pos:]
            
            # Procura por um número sequencial (2 dígitos, não 00) seguido de zeros
            seq_match = re.match(r'([1-9]\d)0+', remaining)
            if seq_match:
                # Remove o número sequencial e mantém apenas os zeros
                seq_number = seq_match.group(1)
                zeros_part = remaining[len(seq_number):]
                new_remaining = zeros_part
            else:
                # Se não há número sequencial, mantém o resto como está
                new_remaining = remaining
            
            filename = new_number_padded + new_remaining
        else:
            # Fallback: procura por qualquer ocorrência do número antigo
            if old_name_number in filename:
                filename = filename.replace(old_name_number, new_number_padded)
            elif old_number_trimmed in filename:
                filename = filename.replace(old_number_trimmed, new_number_padded)
        
        return filename

    def edit_text_content(self, old_name, new_name):
        old_name_number = self._extract_numbers_from_name(old_name)
        new_name_number = self._extract_numbers_from_name(new_name)

        # Padroniza o novo número com 7 dígitos
        new_name_number = self._create_padded_number(new_name_number)
        print(f'Text Content: {new_name_number} ')
        print(f'Text Old Number: {old_name_number}')
        print(f'Processando arquivos de texto para renomeação de {old_name} para {new_name}')

        # Define os diretórios onde procurar arquivos de texto
        search_directories = self._get_search_directories()
        
        # Processa arquivos .txt em todos os diretórios relevantes
        for search_dir in search_directories:
            if not os.path.exists(search_dir):
                continue
                
            for filename in glob.glob(os.path.join(search_dir, '*.txt')):
                # IMPORTANTE: Nunca alterar o conteúdo do arquivo md5sum.txt
                if os.path.basename(filename).lower() == 'md5sum.txt':
                    print(f"Pulando md5sum.txt (conteúdo preservado): {filename}")
                    continue
                    
                try:
                    with open(filename, 'r', encoding='utf-8') as file:
                        filedata = file.readlines()

                    new_filedata = []
                    for line in filedata:
                        line_split = line.strip().split(';')
                        
                        # Verifica se a linha contém o número antigo
                        line_contains_old_number = old_name_number in line
                        
                        if line_contains_old_number and len(line_split) > 0:
                            # Atualiza o primeiro campo (número do lote)
                            line_split[0] = self._create_padded_number(new_name_number)
                            
                            # Verifica se já não tem '/2023' antes de adicionar
                            if len(line_split) > 1 and not line_split[1].endswith('/2023'):
                                line_split[1] = line_split[1] + '/2023'
                            
                            # Processa todos os campos da linha para atualizar nomes de arquivos
                            for i in range(1, len(line_split)):
                                if line_split[i]:
                                    # Verifica se o campo contém um nome de arquivo JPG
                                    if line_split[i].endswith('.jpg'):
                                        original_jpg = line_split[i]
                                        line_split[i] = self._update_jpg_filename(
                                            line_split[i], old_name_number, new_name_number)
                                        if original_jpg != line_split[i]:
                                            print(f"  JPG atualizado: {original_jpg} -> {line_split[i]}")
                                    else:
                                        # Para outros campos, aplica a substituição simples
                                        # mas apenas se o campo contém o número antigo
                                        if old_name_number in line_split[i]:
                                            line_split[i] = line_split[i].replace(
                                                old_name_number, self._create_padded_number(new_name_number))
                        else:
                            # Para linhas que não contém o número antigo, atualiza o primeiro campo
                            # e verifica se há arquivos JPG que precisam ser atualizados
                            if len(line_split) > 0:
                                line_split[0] = self._create_padded_number(new_name_number)
                                
                                # Verifica se há arquivos JPG nos outros campos que precisam ser atualizados
                                for i in range(1, len(line_split)):
                                    if line_split[i] and line_split[i].endswith('.jpg'):
                                        # Verifica se o arquivo JPG contém o número antigo
                                        if old_name_number in line_split[i]:
                                            original_jpg = line_split[i]
                                            line_split[i] = self._update_jpg_filename(
                                                line_split[i], old_name_number, new_name_number)
                                            if original_jpg != line_split[i]:
                                                print(f"  JPG atualizado (linha sem número antigo): {original_jpg} -> {line_split[i]}")

                        new_line = ';'.join(line_split) + '\n'
                        print(f"Linha processada: {new_line.strip()}")
                        new_filedata.append(new_line)
                        
                    # Salva o arquivo atualizado
                    with open(filename, 'w', encoding='utf-8') as file:
                        file.writelines(new_filedata)
                        
                    print(f"Arquivo atualizado: {filename}")
                    
                except Exception as e:
                    print(f"Erro ao processar arquivo {filename}: {e}")
                    import traceback
                    traceback.print_exc()