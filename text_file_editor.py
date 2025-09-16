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
        # Guarda o conteúdo original
        original_content = filename
        
        # Remove prefixo '00' se existir
        if filename.startswith('00'):
            filename = filename[2:]
        
        # Aplica a lógica de substituição para nomes de arquivos JPG
        # Procura por sequências de 5 ou mais dígitos
        digit_sequences = re.findall(r'\d{5,}', filename)
        
        # Para cada sequência encontrada, verifica se corresponde ao padrão antigo
        for seq in sorted(digit_sequences, key=len, reverse=True):
            # Verifica se a sequência contém o número antigo
            old_number_trimmed = old_name_number.lstrip('0')
            seq_trimmed = seq.lstrip('0')
            
            if seq_trimmed.startswith(old_number_trimmed):
                # Substitui apenas a parte que corresponde ao número do lote
                # Garantindo que o novo número tenha exatamente 7 dígitos
                correct_new_number = self._create_padded_number(new_name_number)
                # Calcula a parte restante após o número do lote
                # A parte restante é o que vem depois do número do lote na sequência
                rest_part = seq[len(old_number_trimmed):]
                # Cria o novo padrão: novo número com 7 dígitos + parte restante
                new_seq = correct_new_number + rest_part
                filename = filename.replace(seq, new_seq)
                break  # Processa apenas a primeira sequência encontrada
            # Verifica também se a sequência inteira corresponde ao número do lote
            elif seq == old_name_number or seq_trimmed == old_number_trimmed:
                # Substitui a sequência inteira pelo novo número padronizado
                correct_new_number = self._create_padded_number(new_name_number)
                filename = filename.replace(seq, correct_new_number)
                break  # Processa apenas a primeira sequência encontrada
        
        return filename

    def edit_text_content(self, old_name, new_name):
        old_name_number = self._extract_numbers_from_name(old_name)
        new_name_number = self._extract_numbers_from_name(new_name)

        # Padroniza o novo número com 7 dígitos
        new_name_number = self._create_padded_number(new_name_number)
        print(f'Text Content: {new_name_number} ')
        print(f'Text Old Number: {old_name_number}')

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
                                        line_split[i] = self._update_jpg_filename(
                                            line_split[i], old_name_number, new_name_number)
                                    else:
                                        # Para outros campos, aplica a substituição simples
                                        # mas apenas se o campo contém o número antigo
                                        if old_name_number in line_split[i]:
                                            line_split[i] = line_split[i].replace(
                                                old_name_number, self._create_padded_number(new_name_number))
                        else:
                            # Para linhas que não contém o número antigo, apenas atualiza o primeiro campo
                            if len(line_split) > 0:
                                line_split[0] = self._create_padded_number(new_name_number)

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