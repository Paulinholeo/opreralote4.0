"""
Utilitários comuns para o sistema OperaLote.
Contém funções compartilhadas entre FileRenamer e TextFileEditor.
"""

import os
import re
from typing import List, Tuple, Optional
from config import (
    DEFAULT_PADDING, MIN_DIRECTORY_LENGTH, JPG_EXTENSION, TXT_EXTENSION,
    MD5SUM_FILENAME, L_PREFIX_PATTERN, L00125_PATTERN, AITS_DIRECTORY,
    TEXT_SEPARATOR, YEAR_SUFFIX, LOG_MESSAGES
)


class LotNumberUtils:
    """Utilitários para manipulação de números de lote."""
    
    @staticmethod
    def extract_numbers_from_name(name: str) -> str:
        """
        Extrai o número do nome do lote, removendo o prefixo 'L' se existir.
        
        Args:
            name (str): Nome do lote (ex: "L0544" ou "0544")
            
        Returns:
            str: Número do lote sem prefixo (ex: "0544")
        """
        return name[1:] if name.startswith('L') else name
    
    @staticmethod
    def create_padded_number(number: str, padding: int = DEFAULT_PADDING) -> str:
        """
        Cria um número com padding específico de zeros à esquerda.
        
        Args:
            number (str): Número a ser padronizado
            padding (int): Quantidade de dígitos desejada (padrão: 7)
            
        Returns:
            str: Número padronizado com zeros à esquerda
        """
        return str(number).zfill(padding)
    
    @staticmethod
    def get_trimmed_number(number: str) -> str:
        """
        Remove zeros à esquerda de um número.
        
        Args:
            number (str): Número com zeros à esquerda
            
        Returns:
            str: Número sem zeros à esquerda
        """
        return number.lstrip('0')


class DirectoryUtils:
    """Utilitários para manipulação de diretórios."""
    
    @staticmethod
    def get_search_directories(directory: str) -> List[str]:
        """
        Obtém todos os diretórios onde devemos procurar por arquivos.
        
        Args:
            directory (str): Diretório base
            
        Returns:
            List[str]: Lista de caminhos de diretórios
        """
        search_directories = [directory]
        
        # Percorre todos os subdiretórios recursivamente
        for root, dirs, files in os.walk(directory):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                if dir_path not in search_directories:
                    search_directories.append(dir_path)
                    
        return search_directories
    
    @staticmethod
    def get_text_search_directories(directory: str) -> List[str]:
        """
        Obtém diretórios específicos para busca de arquivos de texto.
        Inclui subdiretórios AITs se existirem.
        
        Args:
            directory (str): Diretório base
            
        Returns:
            List[str]: Lista de caminhos de diretórios
        """
        search_directories = [directory]
        
        if os.path.exists(directory):
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isdir(item_path):
                    search_directories.append(item_path)
                    # Adiciona também subdiretórios de AITs se existirem
                    aits_path = os.path.join(item_path, AITS_DIRECTORY)
                    if os.path.exists(aits_path):
                        search_directories.append(aits_path)
        
        return search_directories


class JpgFilenameProcessor:
    """Processador especializado para nomes de arquivos JPG."""
    
    @staticmethod
    def update_jpg_filename(filename: str, old_name_number: str, new_name_number: str) -> str:
        """
        Atualiza nomes de arquivos JPG aplicando regras específicas.
        
        Args:
            filename (str): Nome do arquivo JPG a ser atualizado
            old_name_number (str): Número antigo do lote
            new_name_number (str): Número novo do lote
            
        Returns:
            str: Nome do arquivo atualizado
        """
        # Padroniza os números
        old_number_padded = LotNumberUtils.create_padded_number(old_name_number)
        new_number_padded = LotNumberUtils.create_padded_number(new_name_number)
        
        # Remove extensão para processamento
        if filename.endswith(JPG_EXTENSION):
            name_without_ext = filename[:-4]
            file_ext = JPG_EXTENSION
        else:
            name_without_ext = filename
            file_ext = ''
        
        # Verifica se o arquivo começa com o número do lote
        if name_without_ext.startswith(old_number_padded):
            rest_part = name_without_ext[len(old_number_padded):]
            old_number_trimmed = LotNumberUtils.get_trimmed_number(old_name_number)
            
            # Verifica se há duplicação no rest_part
            corrected_rest = JpgFilenameProcessor._check_and_fix_duplication(
                rest_part, old_number_trimmed
            )
            
            return new_number_padded + corrected_rest + file_ext
        
        # Fallback: substituição direta se o número antigo estiver em qualquer lugar
        if old_number_padded in name_without_ext:
            corrected_name = name_without_ext.replace(old_number_padded, new_number_padded, 1)
            return corrected_name + file_ext
        
        return filename
    
    @staticmethod
    def _check_and_fix_duplication(rest_part: str, old_number_trimmed: str) -> str:
        """
        Verifica e corrige duplicação de dígitos no rest_part.
        
        Args:
            rest_part (str): Parte restante do nome do arquivo
            old_number_trimmed (str): Número do lote sem zeros à esquerda
            
        Returns:
            str: Parte restante corrigida
        """
        # Padrão: 000017070000060a -> 0000170 + 70 + 000060a
        # Onde 70 são os últimos 2 dígitos do lote (170 -> 70)
        if len(rest_part) >= 2 and len(old_number_trimmed) >= 2:
            last_two_digits = old_number_trimmed[-2:]
            first_two_rest = rest_part[:2]
            
            if first_two_rest == last_two_digits:
                # Remove a duplicação (primeiros 2 dígitos do rest_part)
                return rest_part[2:]
        
        # Sem duplicação, mantém o rest_part como está
        return rest_part


class FileValidationUtils:
    """Utilitários para validação de arquivos."""
    
    @staticmethod
    def should_rename_file(filename: str, old_name_number: str) -> bool:
        """
        Verifica se um arquivo deve ser renomeado com base no número antigo.
        
        Args:
            filename (str): Nome do arquivo
            old_name_number (str): Número antigo do lote
            
        Returns:
            bool: True se o arquivo deve ser renomeado, False caso contrário
        """
        base_filename = os.path.basename(filename)
        file_name_without_ext = os.path.splitext(base_filename)[0]
        file_ext = os.path.splitext(base_filename)[1]
        
        # Verifica se o arquivo contém o número antigo
        if old_name_number in file_name_without_ext:
            return True
        
        # Verifica padrões numéricos equivalentes
        old_number_trimmed = LotNumberUtils.get_trimmed_number(old_name_number)
        if old_number_trimmed in file_name_without_ext:
            return FileValidationUtils._check_numeric_patterns(
                file_name_without_ext, old_number_trimmed
            )
        
        # Verifica padrões especiais
        if FileValidationUtils._check_special_patterns(
            base_filename, file_name_without_ext, file_ext, old_name_number
        ):
            return True
        
        # Caso especial para arquivos JPG
        if file_ext.lower() == JPG_EXTENSION:
            return FileValidationUtils._check_jpg_patterns(
                file_name_without_ext, old_name_number
            )
        
        return False
    
    @staticmethod
    def _check_numeric_patterns(file_name_without_ext: str, old_number_trimmed: str) -> bool:
        """Verifica padrões numéricos no nome do arquivo."""
        found_sequences = re.findall(r'\d+', file_name_without_ext)
        for seq in found_sequences:
            seq_trimmed = seq.lstrip('0')
            if seq_trimmed.startswith(old_number_trimmed) and len(seq) >= 5:
                return True
        return False
    
    @staticmethod
    def _check_special_patterns(
        base_filename: str, 
        file_name_without_ext: str, 
        file_ext: str, 
        old_name_number: str
    ) -> bool:
        """Verifica padrões especiais de arquivos."""
        # Verifica padrões como "L00125" quando old_name_number é "0000125"
        if len(old_name_number) >= MIN_DIRECTORY_LENGTH and old_name_number.startswith('00'):
            old_number_trimmed = LotNumberUtils.get_trimmed_number(old_name_number)
            if (f"L{old_number_trimmed.zfill(5)}" in base_filename or 
                f"L00{old_number_trimmed}" in base_filename):
                return True
        
        # Verifica padrão reverso: se old_name contém "L" e arquivo contém número
        if old_name_number.startswith('L'):
            return any(part in base_filename for part in [old_name_number, old_name_number.lstrip('0')])
        
        # Caso especial: arquivo L00125.txt que sempre deve ser renomeado
        if file_name_without_ext == L00125_PATTERN and file_ext.lower() == TXT_EXTENSION:
            return True
        
        return False
    
    @staticmethod
    def _check_jpg_patterns(file_name_without_ext: str, old_name_number: str) -> bool:
        """Verifica padrões específicos para arquivos JPG."""
        digit_sequences = re.findall(r'\d{5,}', file_name_without_ext)
        old_number_trimmed = LotNumberUtils.get_trimmed_number(old_name_number)
        
        for seq in digit_sequences:
            seq_trimmed = seq.lstrip('0')
            if seq_trimmed.startswith(old_number_trimmed) or old_number_trimmed in seq_trimmed:
                return True
        
        return False


class TextLineProcessor:
    """Processador para linhas de texto em arquivos."""
    
    @staticmethod
    def process_text_line(
        line: str, 
        old_name_number: str, 
        new_name_number: str
    ) -> str:
        """
        Processa uma linha de texto, atualizando números de lote e nomes JPG.
        
        Args:
            line (str): Linha de texto a ser processada
            old_name_number (str): Número antigo do lote
            new_name_number (str): Número novo do lote
            
        Returns:
            str: Linha processada
        """
        line_split = line.strip().split(TEXT_SEPARATOR)
        
        # Verifica se a linha contém o número antigo
        line_contains_old_number = old_name_number in line
        
        if line_contains_old_number and len(line_split) > 0:
            return TextLineProcessor._process_line_with_old_number(
                line_split, old_name_number, new_name_number
            )
        else:
            return TextLineProcessor._process_line_without_old_number(
                line_split, old_name_number, new_name_number
            )
    
    @staticmethod
    def _process_line_with_old_number(
        line_split: List[str], 
        old_name_number: str, 
        new_name_number: str
    ) -> str:
        """Processa linha que contém o número antigo."""
        # Atualiza o primeiro campo (número do lote)
        line_split[0] = LotNumberUtils.create_padded_number(new_name_number)
        
        # Verifica se já não tem '/2023' antes de adicionar
        if len(line_split) > 1 and not line_split[1].endswith(YEAR_SUFFIX):
            line_split[1] = line_split[1] + YEAR_SUFFIX
        
        # Processa todos os campos da linha
        for i in range(1, len(line_split)):
            if line_split[i]:
                line_split[i] = TextLineProcessor._process_field(
                    line_split[i], old_name_number, new_name_number
                )
        
        return TEXT_SEPARATOR.join(line_split) + '\n'
    
    @staticmethod
    def _process_line_without_old_number(
        line_split: List[str], 
        old_name_number: str, 
        new_name_number: str
    ) -> str:
        """Processa linha que não contém o número antigo."""
        if len(line_split) > 0:
            line_split[0] = LotNumberUtils.create_padded_number(new_name_number)
            
            # Verifica se há arquivos JPG nos outros campos
            for i in range(1, len(line_split)):
                if line_split[i] and line_split[i].endswith(JPG_EXTENSION):
                    if old_name_number in line_split[i]:
                        line_split[i] = JpgFilenameProcessor.update_jpg_filename(
                            line_split[i], old_name_number, new_name_number
                        )
        
        return TEXT_SEPARATOR.join(line_split) + '\n'
    
    @staticmethod
    def _process_field(field: str, old_name_number: str, new_name_number: str) -> str:
        """Processa um campo individual da linha."""
        if field.endswith(JPG_EXTENSION):
            return JpgFilenameProcessor.update_jpg_filename(
                field, old_name_number, new_name_number
            )
        elif old_name_number in field:
            return field.replace(
                old_name_number, 
                LotNumberUtils.create_padded_number(new_name_number)
            )
        return field


class LoggingUtils:
    """Utilitários para logging e mensagens."""
    
    @staticmethod
    def log_file_rename(old_filename: str, new_filename: str, success: bool) -> None:
        """Log de renomeação de arquivo."""
        if success:
            print(f"    {LOG_MESSAGES['file_renamed'].format(old_filename, new_filename)}")
        else:
            print(f"    {LOG_MESSAGES['file_rename_error'].format(old_filename, '')}")
    
    @staticmethod
    def log_jpg_update(original: str, updated: str) -> None:
        """Log de atualização de JPG."""
        if original != updated:
            print(f"  {LOG_MESSAGES['jpg_updated'].format(original, updated)}")
    
    @staticmethod
    def log_text_file_update(filename: str) -> None:
        """Log de atualização de arquivo de texto."""
        print(LOG_MESSAGES['text_file_updated'].format(filename))
    
    @staticmethod
    def log_skip_md5sum(filename: str) -> None:
        """Log de pulo do arquivo md5sum."""
        print(LOG_MESSAGES['skip_md5sum'].format(filename))
