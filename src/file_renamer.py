import os
import glob
import zipfile
import rarfile
import shutil
import re
from utils import (
    LotNumberUtils, 
    DirectoryUtils, 
    JpgFilenameProcessor, 
    FileValidationUtils,
    LoggingUtils
)


class FileRenamer:
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
    
    def _move_directory_content(self, source_path, target_path):
        """
        Move o conteúdo de um diretório para outro, substituindo arquivos existentes.
        
        Args:
            source_path (str): Caminho do diretório de origem
            target_path (str): Caminho do diretório de destino
        """
        if not os.path.exists(source_path):
            return
            
        os.makedirs(target_path, exist_ok=True)
        
        for item in os.listdir(source_path):
            source = os.path.join(source_path, item)
            target = os.path.join(target_path, item)
            
            # Remove o destino se já existir
            if os.path.exists(target):
                if os.path.isdir(target):
                    shutil.rmtree(target)
                else:
                    os.remove(target)
            
            # Move o item
            if os.path.exists(source):
                shutil.move(source, target)
    
    def _get_search_directories(self):
        """Delega para DirectoryUtils."""
        return DirectoryUtils.get_search_directories(self.directory)
    
    def _should_rename_file(self, filename, old_name_number):
        """Delega para FileValidationUtils."""
        return FileValidationUtils.should_rename_file(filename, old_name_number)
    
    def _rename_jpg_file(self, filename, old_name_number, new_name_number):
        """
        Renomeia um arquivo JPG aplicando as regras específicas para imagens.
        
        Args:
            filename (str): Caminho completo do arquivo JPG
            old_name_number (str): Número antigo do lote
            new_name_number (str): Número novo do lote
            
        Returns:
            bool: True se o arquivo foi renomeado com sucesso, False caso contrário
        """
        try:
            base_filename = os.path.basename(filename)
            file_ext = os.path.splitext(base_filename)[1]
            
            if file_ext.lower() != '.jpg':
                return False
            
            # Usa o processador de JPG para obter o novo nome
            new_filename = JpgFilenameProcessor.update_jpg_filename(
                base_filename, old_name_number, new_name_number
            )
            
            # Realiza a renomeação
            return self._perform_file_rename(filename, new_filename)
            
        except Exception as e:
            print(f"Erro ao renomear arquivo JPG {filename}: {e}")
            return False
    
    def _perform_file_rename(self, old_filename, new_filename):
        """
        Realiza a renomeação de um arquivo, criando diretórios necessários.
        
        Args:
            old_filename (str): Caminho completo do arquivo original
            new_filename (str): Nome do novo arquivo (com extensão)
            
        Returns:
            bool: True se a renomeação foi bem-sucedida, False caso contrário
        """
        dir_name = os.path.dirname(old_filename)
        full_new_filename = os.path.join(dir_name, new_filename)
        
        # Verifica se o diretório de destino existe
        dest_dir = os.path.dirname(full_new_filename)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir, exist_ok=True)
        
        if os.path.exists(old_filename) and old_filename != full_new_filename:
            # Verifica se o arquivo de destino já existe
            if os.path.exists(full_new_filename):
                print(f"    ⚠️  Arquivo de destino já existe: {full_new_filename}")
                print(f"    ℹ️  Arquivo de destino já existe, não fazendo nada")
                return False
            
            try:
                os.rename(old_filename, full_new_filename)
                LoggingUtils.log_file_rename(old_filename, full_new_filename, True)
                return True
            except Exception as e:
                print(f"    ❌ Erro ao renomear {old_filename}: {e}")
                return False
        else:
            print(f"    ℹ️  Não renomeando: old_filename={old_filename}, full_new_filename={full_new_filename}")
            return False
    
    def _fix_subdirectories(self, main_dir_path, new_name, old_name_number, new_name_number):
        """
        Corrige subdiretórios que precisam ser atualizados após renomeação.
        
        Args:
            main_dir_path (str): Caminho do diretório principal
            new_name (str): Novo nome do diretório
            old_name_number (str): Número antigo do lote
            new_name_number (str): Número novo do lote
            
        Returns:
            bool: True se a correção foi bem-sucedida, False caso contrário
        """
        if not os.path.exists(main_dir_path):
            return False
            
        print(f"Verificação OBRIGATÓRIA: corrigindo subdiretórios em {main_dir_path}...")
        
        # Lista todos os subdiretórios para verificar se precisam ser corrigidos
        subdirs_to_fix = []
        for item in os.listdir(main_dir_path):
            item_path = os.path.join(main_dir_path, item)
            if os.path.isdir(item_path) and item.isdigit() and len(item) >= 6:
                expected_number = self._create_padded_number(new_name_number)
                if item != expected_number:
                    subdirs_to_fix.append((item, expected_number))
                    print(f"DETECTADO: Subdiretório {item} precisa ser renomeado para {expected_number}")
        
        # Força a correção de TODOS os subdiretórios encontrados
        for old_subdir, new_subdir in subdirs_to_fix:
            print(f"CORRIGINDO AGORA: {old_subdir} -> {new_subdir}")
            old_subdir_path = os.path.join(main_dir_path, old_subdir)
            new_subdir_path = os.path.join(main_dir_path, new_subdir)
            
            try:
                if os.path.exists(new_subdir_path):
                    # Se destino existe, move conteúdo
                    self._move_directory_content(old_subdir_path, new_subdir_path)
                    if os.path.exists(old_subdir_path):
                        os.rmdir(old_subdir_path)
                    print(f"SUCESSO: Conteúdo movido de {old_subdir} para {new_subdir}")
                else:
                    # Renomeia diretamente
                    if os.path.exists(old_subdir_path):
                        os.rename(old_subdir_path, new_subdir_path)
                    print(f"SUCESSO: Subdiretório renomeado {old_subdir} -> {new_subdir}")
            except Exception as e:
                print(f"ERRO ao corrigir subdiretório {old_subdir}: {e}")
                return False
                
        if subdirs_to_fix:
            print(f"✅ CORREÇÃO CONCLUÍDA: {len(subdirs_to_fix)} subdiretório(s) corrigido(s)")
        else:
            print(f"✅ VERIFICAÇÃO OK: Nenhum subdiretório precisa de correção")
            
        return True
    
    def rename_internal_directories_with_aits(self, directory_path, old_name, new_name):
        """
        Renomeia diretórios internos quando há subdiretório AITs
        Cria a estrutura: diretorio_pai/novo_nome/novo_nome/AITs
        """
        try:
            old_name_number = self._extract_numbers_from_name(old_name)
            new_name_number = self._extract_numbers_from_name(new_name)
            
            # Verifica se há diretório AITs diretamente no diretório principal
            aits_direct_path = os.path.join(directory_path, 'AITs')
            if os.path.exists(aits_direct_path):
                # Caso: diretorio/AITs -> diretorio/novo_nome/AITs
                new_subdir_path = os.path.join(directory_path, new_name_number)
                os.makedirs(new_subdir_path, exist_ok=True)
                
                new_aits_path = os.path.join(new_subdir_path, 'AITs')
                print(f"Movendo AITs: {aits_direct_path} -> {new_aits_path}")
                # VERIFICAÇÃO ADICIONAL: Verifica se o diretório AITs ainda existe antes de mover
                if os.path.exists(aits_direct_path):
                    shutil.move(aits_direct_path, new_aits_path)
                
                # Move outros arquivos que possam estar no diretório principal
                for item in os.listdir(directory_path):
                    item_path = os.path.join(directory_path, item)
                    if os.path.isfile(item_path) and item != new_name_number:
                        target_path = os.path.join(new_subdir_path, item)
                        print(f"Movendo arquivo: {item_path} -> {target_path}")
                        # VERIFICAÇÃO ADICIONAL: Verifica se o arquivo ainda existe antes de mover
                        if os.path.exists(item_path):
                            shutil.move(item_path, target_path)
                
                return True
            
            # Caso: procura por subdiretórios que precisam ser renomeados
            # Exemplo: L0544/0000125/AITs -> L0544/02544/AITs
            subdir_renamed = False
            for item in os.listdir(directory_path):
                item_path = os.path.join(directory_path, item)
                if os.path.isdir(item_path):
                    # Se o item contém o número do lote antigo, precisa ser renomeado
                    should_rename = False
                    
                    # Verifica se o nome do subdiretório contém partes do nome antigo
                    if old_name_number in item:
                        should_rename = True
                    elif item == old_name_number:
                        should_rename = True
                    # Verifica padrões como "0000125" quando old_name é "L0544"
                    elif len(item) >= 6 and item.isdigit():
                        # Pode ser um subdiretório numérico que precisa ser atualizado
                        should_rename = True
                        
                    if should_rename:
                        new_item_path = os.path.join(directory_path, new_name_number)
                        print(f"Renomeando diretório interno: {item_path} -> {new_item_path}")
                        
                        # Se o destino já existe, move o conteúdo
                        if os.path.exists(new_item_path):
                            self._move_directory_content(item_path, new_item_path)
                            # Remove o diretório de origem, se ainda existir
                            if os.path.exists(item_path):
                                os.rmdir(item_path)
                        else:
                            # VERIFICAÇÃO ADICIONAL: Verifica se o diretório ainda existe antes de renomear
                            if os.path.exists(item_path):
                                os.rename(item_path, new_item_path)
                        
                        subdir_renamed = True
                        break
            
            # Após renomear o diretório principal, renomeia recursivamente 
            # todos os subdiretórios internos com o mesmo nome
            if subdir_renamed:
                print(f"Aplicando renomeação recursiva de subdiretórios...")
                self.rename_directories_recursively(directory_path, old_name, new_name)
                        
            return True
                        
        except Exception as e:
            print(f"Erro ao renomear diretórios internos: {e}")
            return False
    
    def update_internal_structure(self, directory_name, old_internal_name, new_internal_name):
        """
        Atualiza a estrutura interna de um diretório sem renomear o diretório principal.
        Útil quando L08786 permanece L08786, mas 0000125 deve virar 0008786.
        
        Args:
            directory_name: Nome do diretório principal (ex: "L08786")
            old_internal_name: Nome antigo do subdiretório interno (ex: "0000125")
            new_internal_name: Nome novo do subdiretório interno (ex: "0008786")
        """
        try:
            main_dir_path = os.path.join(self.directory, directory_name)
            
            if not os.path.exists(main_dir_path):
                print(f"Diretório principal {directory_name} não encontrado")
                return False
            
            print(f"Atualizando estrutura interna de {directory_name}: {old_internal_name} -> {new_internal_name}")
            
            # Para atualizar a estrutura interna corretamente, precisamos:
            # 1. Procurar por subdiretórios com o nome antigo (formato com zeros à esquerda)
            # 2. Renomeá-los para o novo nome (também com zeros à esquerda)
            
            old_padded = self._create_padded_number(old_internal_name)
            new_padded = self._create_padded_number(new_internal_name)
            
            print(f"Procurando subdiretório {old_padded} para renomear para {new_padded}")
            
            # Procura pelo subdiretório antigo
            old_subdir_path = os.path.join(main_dir_path, old_padded)
            new_subdir_path = os.path.join(main_dir_path, new_padded)
            
            if os.path.exists(old_subdir_path):
                print(f"Encontrado subdiretório {old_padded}, renomeando para {new_padded}")
                # Se o destino já existe, move o conteúdo
                if os.path.exists(new_subdir_path):
                    print(f"Destino {new_padded} já existe, movendo conteúdo")
                    self._move_directory_content(old_subdir_path, new_subdir_path)
                    # Remove o diretório de origem, se ainda existir
                    if os.path.exists(old_subdir_path):
                        os.rmdir(old_subdir_path)
                else:
                    # Renomeia diretamente
                    os.rename(old_subdir_path, new_subdir_path)
                    print(f"Subdiretório renomeado com sucesso")
                
                # Aplica renomeação recursiva nos subdiretórios internos
                # success = self.rename_directories_recursively(main_dir_path, old_padded, new_padded)
                print(f"Estrutura interna atualizada com sucesso")
                return True
            else:
                print(f"Subdiretório {old_padded} não encontrado")
                # Tenta encontrar qualquer subdiretório numérico que precise ser atualizado
                for item in os.listdir(main_dir_path):
                    item_path = os.path.join(main_dir_path, item)
                    if os.path.isdir(item_path) and item.isdigit() and len(item) >= 6:
                        # Verifica se este subdiretório precisa ser atualizado
                        expected_old = self._create_padded_number(old_internal_name)
                        if item == expected_old:
                            new_item_path = os.path.join(main_dir_path, new_padded)
                            print(f"Encontrado subdiretório {item} que deve ser atualizado para {new_padded}")
                            
                            # Se o destino já existe, move o conteúdo
                            if os.path.exists(new_item_path):
                                print(f"Destino {new_padded} já existe, movendo conteúdo")
                                self._move_directory_content(item_path, new_item_path)
                                # Remove o diretório de origem, se ainda existir
                                if os.path.exists(item_path):
                                    os.rmdir(item_path)
                            else:
                                # Renomeia diretamente
                                os.rename(item_path, new_item_path)
                                print(f"Subdiretório renomeado com sucesso")
                            return True
                
                print(f"Nenhuma atualização necessária para a estrutura interna")
                return True
                
        except Exception as e:
            print(f"Erro ao atualizar estrutura interna: {e}")
            return False
    
    def rename_subdirectory_and_files(self, parent_directory, old_subdir_name, new_subdir_name):
        """
        Renomeia um subdiretório e todos os arquivos dentro dele.
        Útil para casos como L08685/0000125 -> L08685/0008685
        """
        try:
            # Primeiro renomeia o subdiretório
            success = self.rename_internal_directories_with_aits(parent_directory, old_subdir_name, new_subdir_name)
            
            if success:
                # Depois renomeia os arquivos dentro do subdiretório
                # Temporariamente ajusta o diretório base para o parent_directory
                original_dir = self.directory
                self.directory = parent_directory
                
                # Renomeia arquivos
                self.rename_files(old_subdir_name, new_subdir_name)
                
                # Renomeia conteúdo dos arquivos de texto
                self.rename_text_content(old_subdir_name, new_subdir_name)
                
                # Restaura o diretório original
                self.directory = original_dir
                
                return True
            
            return False
            
        except Exception as e:
            print(f"Erro ao renomear subdiretório e arquivos: {e}")
            return False
    
    def rename_directories_recursively(self, directory_path, old_name, new_name):
        """
        Renomeia recursivamente todos os diretórios que tenham o nome antigo.
        Não altera arquivos, apenas diretórios.
        
        Args:
            directory_path: Caminho do diretório pai onde buscar
            old_name: Nome antigo do diretório (ex: "0000125")
            new_name: Nome novo do diretório (ex: "0005654")
        """
        try:
            old_name_number = self._extract_numbers_from_name(old_name)
            new_name_number = self._extract_numbers_from_name(new_name)
            
            print(f"Renomeando diretórios recursivamente: {old_name_number} -> {new_name_number}")
            
            # Lista todos os itens no diretório atual
            if not os.path.exists(directory_path):
                return False
                
            items_to_process = []
            for item in os.listdir(directory_path):
                item_path = os.path.join(directory_path, item)
                if os.path.isdir(item_path):
                    items_to_process.append((item, item_path))
            
            # Processa diretórios que precisam ser renomeados
            for item_name, item_path in items_to_process:
                # Verifica se este diretório tem o nome que deve ser alterado
                if item_name == old_name_number:
                    new_item_path = os.path.join(directory_path, new_name_number)
                    print(f"Renomeando diretório: {item_path} -> {new_item_path}")
                    
                    # Se o destino já existe, move o conteúdo
                    if os.path.exists(new_item_path):
                        self._move_directory_content(item_path, new_item_path)
                        # Remove o diretório de origem, se ainda existir
                        if os.path.exists(item_path):
                            os.rmdir(item_path)
                        # Agora processa recursivamente o diretório destino
                        self.rename_directories_recursively(new_item_path, old_name, new_name)
                    else:
                        # Renomeia o diretório
                        os.rename(item_path, new_item_path)
                        # Processa recursivamente o diretório renomeado
                        self.rename_directories_recursively(new_item_path, old_name, new_name)
                else:
                    # Para diretórios que não precisam ser renomeados, 
                    # ainda processa recursivamente em busca de subdiretórios
                    self.rename_directories_recursively(item_path, old_name, new_name)
            
            return True
            
        except Exception as e:
            print(f"Erro ao renomear diretórios recursivamente: {e}")
            return False

    def rename_directory(self, old_name, new_name):
        old_dir_path = os.path.join(self.directory, old_name)
        new_dir_path = os.path.join(self.directory, new_name)
        home_dir = self.directory
        
        # Caso especial: mesmo nome de diretório, mas precisa atualizar estrutura interna
        if old_name == new_name:
            print(f"Mesmo nome de diretório ({old_name}). Verificando se precisa atualizar estrutura interna...")
            
            # Extrai números para verificar se são diferentes
            old_name_number = self._extract_numbers_from_name(old_name)
            new_name_number = self._extract_numbers_from_name(new_name)
            
            # Procura por subdiretórios que possam precisar ser atualizados
            if os.path.exists(old_dir_path):
                for item in os.listdir(old_dir_path):
                    item_path = os.path.join(old_dir_path, item)
                    if os.path.isdir(item_path) and item.isdigit() and len(item) >= 6:
                        # Encontrou subdiretório numérico que pode precisar ser atualizado
                        # Ex: encontrou "0000125" quando new_name é "L08786"
                        expected_number = self._create_padded_number(new_name_number)  # Ex: "0008786"
                        if item != expected_number:
                            print(f"Encontrado subdiretório {item} que deve ser atualizado para {expected_number}")
                            return self.update_internal_structure(old_name, item, expected_number)
                
                print(f"Nenhuma atualização de estrutura interna necessária para {old_name}")
                return True
            else:
                print(f"Diretório {old_name} não encontrado")
                return False
        
        # Fluxo normal: nomes diferentes
        if os.path.exists(new_dir_path):
            print("Erro: O diretório já existe.")
            return False

        if not new_dir_path:
            print("Erro: O novo nome do diretório não pode estar vazio.")
            return False

        try:
            if old_dir_path.endswith('.zip'):
                with zipfile.ZipFile(old_dir_path, 'r') as zip_ref:
                    zip_ref.extractall(new_dir_path)
                    extracted_dir = os.path.splitext(old_dir_path)[0]
                    
                    if os.path.exists(extracted_dir):
                        if len((old_dir_path.split('/')[-1])) == len(old_name):
                            os.rename(extracted_dir, new_name)
                        else:
                            os.rename(extracted_dir, new_dir_path)
            elif old_dir_path.endswith('.rar'):
                with rarfile.RarFile(old_dir_path, 'r') as rar_ref:
                    rar_ref.extractall(new_dir_path)
                    extracted_dir = os.path.splitext(old_dir_path)[0]
                    if os.path.exists(extracted_dir):
                        if old_dir_path.split('/')[-1] == old_name:
                            os.rename(extracted_dir, new_name)
                        else:
                            os.rename(extracted_dir, new_dir_path)
            else:
                if os.path.exists(old_dir_path):
                    # Renomeia o diretório principal
                    os.rename(old_dir_path, new_dir_path)
                    
                    # Após renomear o diretório principal, atualiza a estrutura interna
                    # Extrai números para atualizar subdiretórios
                    old_name_number = self._extract_numbers_from_name(old_name)
                    new_name_number = self._extract_numbers_from_name(new_name)
                    
                    # Aplica atualização de estrutura interna nos subdiretórios
                    print(f"Atualizando estrutura interna de {new_name}: {old_name_number} -> {new_name_number}")
                    self.update_internal_structure(new_name, old_name_number, new_name_number)
                    
                    print(f"Renomeação de diretórios concluída. Estrutura pronta para processamento de arquivos.")
                        
        except Exception as e:
            print(f"Erro ao renomear o diretório: {e}")
            return False

        return True

    def rename_files(self, old_name, new_name):
        old_name_number = self._extract_numbers_from_name(old_name)
        new_name_number = self._extract_numbers_from_name(new_name)
        
        # Extrai os números para comparação
        old_number_trimmed = old_name_number.lstrip('0')
        new_number_trimmed = new_name_number.lstrip('0')
        
        # CORREÇÃO: Verifica se os números são realmente diferentes
        numbers_are_different = old_number_trimmed != new_number_trimmed or old_name_number != new_name_number
        
        # Só impede a renomeação se os nomes E os números forem iguais
        # MAS permite renomeação para arquivos JPG que precisam de padronização de dígitos
        if old_name == new_name and not numbers_are_different:
            print(f"Mesmo nome de lote ({old_name}) e mesmo número ({old_name_number}). Verificando necessidade de padronização de arquivos.")
            # Continua o processamento para verificar se há arquivos JPG que precisam ser padronizados
            
        # Se old_name == new_name mas os números são diferentes, continua o processamento para padronizar os números
        if old_name == new_name and numbers_are_different:
            print(f"Mesmo nome de lote ({old_name}) mas números diferentes ({old_name_number} -> {new_name_number}). Processando padronização de arquivos.")
        elif old_name != new_name:
            print(f"Nomes diferentes ({old_name} -> {new_name}). Processando renomeação completa.")
        
        print(f"=== INICIANDO rename_files({old_name} -> {new_name}) ===")
        
        # CRÍTICO: SEMPRE verifica e corrige subdiretórios ANTES de processar arquivos
        # Isso resolve definitivamente o problema onde arquivos são processados em caminhos antigos
        main_dir_path = os.path.join(self.directory, new_name if os.path.exists(os.path.join(self.directory, new_name)) else old_name)
        self._fix_subdirectories(main_dir_path, new_name, old_name_number, new_name_number)
        
        # SEMPRE reconstrói a lista de diretórios após qualquer correção
        # Define os diretórios onde procurar arquivos
        search_directories = self._get_search_directories()
        
        print(f"Diretórios de busca para arquivos: {search_directories}")
        
        # Processa arquivos em todos os diretórios relevantes
        for search_dir in search_directories:
            if not os.path.exists(search_dir):
                continue
                
            for filename in glob.glob(os.path.join(search_dir, '*')):
                base_filename = os.path.basename(filename)
                
                # Pula diretórios
                if os.path.isdir(filename):
                    continue
                
                # Verifica se o arquivo deve ser renomeado
                if self._should_rename_file(filename, old_name_number):
                    # Calcula o novo nome do arquivo
                    file_ext = os.path.splitext(base_filename)[1]
                    file_name_without_ext = os.path.splitext(base_filename)[0]
                    
                    # Lógica de renomeação mais robusta
                    new_file_name_without_ext = file_name_without_ext
                    
                    print(f"  Iniciando renomeação de: {file_name_without_ext}")
                    
                    # Casos especiais para arquivos com padrão "L00125"
                    if file_name_without_ext.startswith('L00') and len(file_name_without_ext) >= 6:
                        # Substitui L00125 por L + novo_numero
                        new_file_name_without_ext = f"L{new_name_number}"
                        print(f"    Aplicado caso especial L00xxx: {new_file_name_without_ext}")
                    # Caso especial específico: L00125.txt sempre vira L + número do lote
                    elif file_name_without_ext == 'L00125' and file_ext == '.txt':
                        new_file_name_without_ext = f"L{new_name_number}"
                        print(f"    Aplicado caso especial L00125.txt: {new_file_name_without_ext}")
                    # Caso especial: arquivo sem L que deveria ter L
                    elif (file_ext == '.txt' and new_name.startswith('L') and 
                          not file_name_without_ext.startswith('L') and
                          file_name_without_ext == new_name[1:]):
                        new_file_name_without_ext = new_name
                        print(f"    Aplicado caso especial .txt sem L: {new_file_name_without_ext}")
                    # Caso especial para arquivos JPG - garante 7 dígitos
                    elif file_ext.lower() == '.jpg':
                        # Para arquivos JPG, delega para a função especializada
                        self._rename_jpg_file(filename, old_name_number, new_name_number)
                        continue  # Já foi processado, pula para o próximo arquivo
                    # Caso padrão
                    elif old_name_number in file_name_without_ext:
                        # Sempre garante que o novo número tenha exatamente 7 dígitos
                        new_number_padded = self._create_padded_number(new_name_number)
                        new_file_name_without_ext = file_name_without_ext.replace(old_name_number, new_number_padded)
                        print(f"    Aplicado caso padrão com 7 dígitos: {new_file_name_without_ext}")
                    # Tenta substituir versão sem zeros à esquerda
                    else:
                        old_trimmed = old_name_number.lstrip('0')
                        if old_trimmed in file_name_without_ext:
                            new_trimmed = new_name_number.lstrip('0')
                            new_file_name_without_ext = file_name_without_ext.replace(old_trimmed, new_trimmed)
                            print(f"    Substituído versão sem zeros: {new_file_name_without_ext}")
                    
                    # Verificação especial para arquivos .txt sem prefixo L (fallback)
                    if (file_ext == '.txt' and new_name.startswith('L') and 
                        not new_file_name_without_ext.startswith('L') and 
                        file_name_without_ext == new_file_name_without_ext):
                        new_file_name_without_ext = new_name  # Usa o nome completo com L
                        print(f"    Aplicado fallback para .txt: {new_file_name_without_ext}")
                    
                    # Realiza a renomeação do arquivo
                    self._perform_file_rename(filename, new_file_name_without_ext + file_ext)
                
                # Processa arquivos compactados
                if filename.endswith('.zip'):
                    with zipfile.ZipFile(filename, 'r') as zip_ref:
                        zip_ref.extractall(search_dir)
                        extracted_dir = os.path.splitext(filename)[0]
                        if os.path.exists(extracted_dir):
                            # Verifica se o diretório de destino já existe
                            target_dir = extracted_dir.replace(old_name, new_name)
                            if os.path.exists(target_dir):
                                print(f"Destino {target_dir} já existe. Movendo conteúdo...")
                                # Move o conteúdo do diretório extraído para o diretório existente
                                self._move_directory_content(extracted_dir, target_dir)
                                # Remove o diretório extraído vazio, se ainda existir
                                if os.path.exists(extracted_dir):
                                    os.rmdir(extracted_dir)
                            else:
                                # Se o destino não existe, renomeia normalmente
                                os.rename(extracted_dir, target_dir)
                elif filename.endswith('.rar'):
                    with rarfile.RarFile(filename, 'r') as rar_ref:
                        rar_ref.extractall(search_dir)
                        extracted_dir = os.path.splitext(filename)[0]
                        if os.path.exists(extracted_dir):
                            if extracted_dir == old_name:
                                os.rename(extracted_dir, new_name)
                            else:
                                os.rename(extracted_dir, extracted_dir.replace(old_name, new_name))

    def rename_text_content(self, old_name, new_name):
        old_name_number = self._extract_numbers_from_name(old_name)
        new_name_number = self._extract_numbers_from_name(new_name)

        # Define os diretórios onde procurar arquivos de texto usando a mesma lógica melhorada
        search_directories = self._get_search_directories()
        
        # Processa arquivos .txt em todos os diretórios relevantes
        for search_dir in search_directories:
            if not os.path.exists(search_dir):
                continue
                
            for filename in glob.glob(os.path.join(search_dir, '*.txt')):
                if os.path.basename(filename).lower() == 'md5sum.txt':
                    continue
                    
                # Lê o conteúdo do arquivo
                with open(filename, 'r', encoding='utf-8') as file:
                    filedata = file.readlines()

                # Processa cada linha
                new_filedata = []
                for line in filedata:
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
                        
                        # Processa todos os campos da linha para atualizar nomes de arquivos
                        for i in range(1, len(line_split)):
                            if line_split[i]:
                                # Verifica se o campo contém um nome de arquivo JPG
                                if line_split[i].endswith('.jpg'):
                                    # Atualiza nomes de arquivos JPG na linha
                                    line_split[i] = self._update_jpg_filename_in_text(
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
                    new_filedata.append(new_line)
                
                # Salva o arquivo atualizado
                with open(filename, 'w', encoding='utf-8') as file:
                    file.writelines(new_filedata)
                    
                print(f"Arquivo de texto atualizado: {filename}")
    
    def _update_jpg_filename_in_text(self, filename, old_name_number, new_name_number):
        """Delega para JpgFilenameProcessor."""
        return JpgFilenameProcessor.update_jpg_filename(filename, old_name_number, new_name_number)
    
    def _fix_jpg_filename_pattern(self, filename_part, lot_number):
        """Delega para JpgFilenameProcessor."""
        return JpgFilenameProcessor.update_jpg_filename(filename_part, lot_number, lot_number)
    
    def set_year_config(self, add_year, year):
        """
        Configura se deve adicionar ano e qual ano usar.
        
        Args:
            add_year (bool): Se deve adicionar ano ao código de infração
            year (str): Ano a ser adicionado (ex: "2023")
        """
        self.add_year = add_year
        self.year = year if add_year else None