import os
import glob
import re
from utils import (
    LotNumberUtils, 
    DirectoryUtils, 
    JpgFilenameProcessor, 
    TextLineProcessor,
    LoggingUtils
)

class TextFileEditor:
    def __init__(self, directory):
        self.directory = directory
        self.add_year = True  # Default: adicionar ano
        self.year = "2023"    # Default: ano 2023

    def _extract_numbers_from_name(self, name):
        """Delega para LotNumberUtils."""
        return LotNumberUtils.extract_numbers_from_name(name)

    def _create_padded_number(self, number, padding=7):
        """Delega para LotNumberUtils."""
        return LotNumberUtils.create_padded_number(number, padding)

    def _get_search_directories(self):
        """Delega para DirectoryUtils."""
        return DirectoryUtils.get_text_search_directories(self.directory)

    def _update_jpg_filename(self, filename, old_name_number, new_name_number):
        """Delega para JpgFilenameProcessor."""
        return JpgFilenameProcessor.update_jpg_filename(filename, old_name_number, new_name_number)
    
    def set_year_config(self, add_year, year):
        """
        Configura se deve adicionar ano e qual ano usar.
        
        Args:
            add_year (bool): Se deve adicionar ano ao código de infração
            year (str): Ano a ser adicionado (ex: "2023")
        """
        self.add_year = add_year
        self.year = year if add_year else None
    
    def _process_text_line_with_year_config(self, line, old_name_number, new_name_number):
        """
        Processa uma linha de texto com configuração personalizada de ano.
        
        Args:
            line (str): Linha de texto a ser processada
            old_name_number (str): Número antigo do lote
            new_name_number (str): Número novo do lote
            
        Returns:
            str: Linha processada
        """
        line_split = line.strip().split(';')
        
        # Verifica se a linha contém o número antigo
        line_contains_old_number = old_name_number in line
        
        if line_contains_old_number and len(line_split) > 0:
            # Atualiza o primeiro campo (número do lote)
            line_split[0] = self._create_padded_number(new_name_number)
            
            # Verifica se deve adicionar ano e se já não tem ano
            if (self.add_year and self.year and 
                len(line_split) > 1 and 
                not line_split[1].endswith(f'/{self.year}')):
                line_split[1] = line_split[1] + f'/{self.year}'
            
            # Processa todos os campos da linha
            for i in range(1, len(line_split)):
                if line_split[i]:
                    line_split[i] = self._process_field_with_year_config(
                        line_split[i], old_name_number, new_name_number
                    )
        else:
            # Para linhas que não contém o número antigo
            if len(line_split) > 0:
                line_split[0] = self._create_padded_number(new_name_number)
                
                # Verifica se há arquivos JPG nos outros campos
                for i in range(1, len(line_split)):
                    if line_split[i] and line_split[i].endswith('.jpg'):
                        if old_name_number in line_split[i]:
                            line_split[i] = self._update_jpg_filename(
                                line_split[i], old_name_number, new_name_number
                            )
        
        return ';'.join(line_split) + '\n'
    
    def _process_field_with_year_config(self, field, old_name_number, new_name_number):
        """
        Processa um campo individual da linha com configuração de ano.
        
        Args:
            field (str): Campo a ser processado
            old_name_number (str): Número antigo do lote
            new_name_number (str): Número novo do lote
            
        Returns:
            str: Campo processado
        """
        if field.endswith('.jpg'):
            return self._update_jpg_filename(field, old_name_number, new_name_number)
        elif old_name_number in field:
            return field.replace(
                old_name_number, 
                self._create_padded_number(new_name_number)
            )
        return field

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
                    LoggingUtils.log_skip_md5sum(filename)
                    continue
                    
                try:
                    with open(filename, 'r', encoding='utf-8') as file:
                        filedata = file.readlines()

                    new_filedata = []
                    for line in filedata:
                        # Usa o processador de linha customizado com configuração de ano
                        processed_line = self._process_text_line_with_year_config(
                            line, old_name_number, new_name_number
                        )
                        
                        # Log da linha processada
                        print(f"Linha processada: {processed_line.strip()}")
                        new_filedata.append(processed_line)
                        
                    # Salva o arquivo atualizado
                    with open(filename, 'w', encoding='utf-8') as file:
                        file.writelines(new_filedata)
                        
                    LoggingUtils.log_text_file_update(filename)
                    
                except Exception as e:
                    print(f"Erro ao processar arquivo {filename}: {e}")
                    import traceback
                    traceback.print_exc()