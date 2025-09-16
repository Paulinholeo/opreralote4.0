import os
import glob
import zipfile
import rarfile
import shutil
import re


class FileRenamer:
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
        """
        Obtém todos os diretórios onde devemos procurar por arquivos.
        
        Returns:
            list: Lista de caminhos de diretórios
        """
        search_directories = [self.directory]
        
        # Percorre todos os subdiretórios recursivamente
        for root, dirs, files in os.walk(self.directory):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                if dir_path not in search_directories:
                    search_directories.append(dir_path)
                    
        return search_directories
    
    def _should_rename_file(self, filename, old_name_number):
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
        old_number_trimmed = old_name_number.lstrip('0')
        if old_number_trimmed in file_name_without_ext:
            # Verifica se a sequência encontrada representa o mesmo número
            found_sequences = re.findall(r'\d+', file_name_without_ext)
            for seq in found_sequences:
                seq_trimmed = seq.lstrip('0')
                # Verifica se o número antigo está no início da sequência encontrada
                if seq_trimmed.startswith(old_number_trimmed) and len(seq) >= 5:
                    return True
        
        # Verifica padrões como "L00125" quando old_name_number é "0000125"
        if len(old_name_number) >= 6 and old_name_number.startswith('00'):
            old_number_trimmed = old_name_number.lstrip('0')
            if f"L{old_number_trimmed.zfill(5)}" in base_filename or f"L00{old_number_trimmed}" in base_filename:
                return True
                
        # Verifica padrão reverso: se old_name contém "L" e arquivo contém número
        if old_name_number.startswith('L') and any(part in base_filename for part in [old_name_number, old_name_number.lstrip('0')]):
            return True
            
        # Caso especial: arquivo .txt sem prefixo L quando new_name tem L
        # (Esta lógica será tratada separadamente na função de renomeação)
        
        # Caso especial: arquivo L00125.txt que sempre deve ser renomeado para o lote atual
        if file_name_without_ext == 'L00125' and file_ext.lower() == '.txt':
            return True
            
        # Caso especial para arquivos JPG - verifica padrões mais complexos
        if file_ext.lower() == '.jpg':
            # Procura por sequências numéricas no nome do arquivo
            digit_sequences = re.findall(r'\d{5,}', file_name_without_ext)
            old_number_trimmed = old_name_number.lstrip('0')
            
            # Verifica se alguma sequência começa com o número antigo
            for seq in digit_sequences:
                seq_trimmed = seq.lstrip('0')
                if seq_trimmed.startswith(old_number_trimmed):
                    return True
                    
                # Verifica se o número antigo está contido na sequência
                if old_number_trimmed in seq_trimmed:
                    return True
        
        return False
    
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
            file_name_without_ext = os.path.splitext(base_filename)[0]
            file_ext = os.path.splitext(base_filename)[1]
            
            if file_ext.lower() != '.jpg':
                return False
            
            # Para arquivos JPG, garante que o novo número tenha exatamente 7 dígitos
            new_number_padded = self._create_padded_number(new_name_number)
            old_number_padded = self._create_padded_number(old_name_number)
            
            # Caso especial: quando old_name == new_name, mas precisamos padronizar o formato
            if old_name_number == new_name_number:
                # Procura por sequências que comecem com o número do lote
                digit_sequences = re.findall(r'\d{5,}', file_name_without_ext)
                
                # Processa as sequências em ordem de comprimento decrescente
                for seq in sorted(digit_sequences, key=len, reverse=True):
                    # Verifica se a sequência começa com o número do lote
                    if seq.startswith(old_number_padded):
                        # Verifica se após o número do lote temos uma continuação que também contém 
                        # parte do número do lote (caso do problema L03889)
                        rest_part = seq[len(old_number_padded):]
                        old_number_trimmed = old_name_number.lstrip('0')
                        
                        # Verifica se o restante começa com parte do número do lote
                        # Isso detecta casos como 0003889889 onde 889 é parte do número 03889
                        # Precisamos verificar se o início do rest_part corresponde ao início do número do lote
                        condition = False
                        if len(rest_part) >= 3:  # Precisamos de pelo menos 3 dígitos para comparar
                            # Verifica se os primeiros 3 dígitos do rest_part correspondem aos últimos 3 do número do lote
                            if len(old_number_trimmed) >= 3:
                                last_three_digits = old_number_trimmed[-3:]
                                first_three_rest = rest_part[:3]
                                condition = last_three_digits == first_three_rest
                        
                        if condition:
                            # Substitui toda a parte que corresponde ao número do lote duplicado
                            # por apenas uma ocorrência do número padronizado
                            # Mas precisamos ser mais precisos aqui
                            # O que queremos remover é a parte duplicada
                            # No caso de 0003889889, queremos remover o 889 extra
                            new_seq = new_number_padded + rest_part[3:]  # Remove os 3 dígitos duplicados
                            new_file_name_without_ext = file_name_without_ext.replace(seq, new_seq, 1)
                            return self._perform_file_rename(filename, new_file_name_without_ext + file_ext)
                        else:
                            # Caso normal: substitui o prefixo que corresponde ao número do lote
                            new_seq = new_number_padded + rest_part
                            new_file_name_without_ext = file_name_without_ext.replace(seq, new_seq, 1)
                            return self._perform_file_rename(filename, new_file_name_without_ext + file_ext)
                
                # Se não encontrou padrões complexos, tenta substituição direta
                if old_number_padded in file_name_without_ext and old_number_padded != new_number_padded:
                    new_file_name_without_ext = file_name_without_ext.replace(old_number_padded, new_number_padded, 1)
                    return self._perform_file_rename(filename, new_file_name_without_ext + file_ext)
            
            return False
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
                print(f"    ✅ Arquivo renomeado com sucesso: {old_filename} -> {full_new_filename}")
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
                        
                        # Verifica se já não tem '/2023' antes de adicionar
                        if len(line_split) > 1 and not line_split[1].endswith('/2023'):
                            line_split[1] = line_split[1] + '/2023'
                        
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
        """
        Atualiza nomes de arquivos JPG em uma linha de texto.
        Esta função unifica a lógica de processamento de nomes JPG entre FileRenamer e TextFileEditor.
        
        Args:
            filename (str): Nome do arquivo JPG a ser atualizado
            old_name_number (str): Número antigo do lote
            new_name_number (str): Número novo do lote
            
        Returns:
            str: Nome do arquivo atualizado
        """
        # Remove prefixo '00' se existir
        if filename.startswith('00'):
            filename = filename[2:]
        
        # Aplica a lógica de substituição para nomes de arquivos JPG
        # Procura por sequências numéricas no nome do arquivo
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
    
    def _fix_jpg_filename_pattern(self, filename_part, lot_number):
        """
        Corrige padrões incorretos em nomes de arquivos JPG.
        
        Exemplo: '000017070000060a.jpg' -> '00001700000060a.jpg'
                 '0000170' + '70000060a.jpg' -> '0000170' + '0000060a.jpg'
        
        Args:
            filename_part (str): Parte do nome do arquivo JPG
            lot_number (str): Número do lote atual
            
        Returns:
            str: Nome do arquivo corrigido
        """
        try:
            # Verifica se é um arquivo JPG
            if not filename_part.lower().endswith('.jpg'):
                return filename_part
                
            # Extrai o nome do arquivo sem extensão
            file_name_without_ext = os.path.splitext(filename_part)[0]
            file_ext = os.path.splitext(filename_part)[1]
            
            # Número do lote com padding
            lot_number_padded = self._create_padded_number(lot_number)
            lot_number_trimmed = lot_number.lstrip('0')
            
            # Verifica se o número do lote está no nome do arquivo
            if lot_number_padded in file_name_without_ext:
                # Encontra a posição do número do lote
                lot_pos = file_name_without_ext.find(lot_number_padded)
                if lot_pos != -1:
                    # Pega o restante do nome após o número do lote
                    rest_part = file_name_without_ext[lot_pos + len(lot_number_padded):]
                    
                    # Verifica se o restante começa com o último dígito do número do lote completo
                    # Isso indica que houve uma duplicação do último dígito
                    if (len(rest_part) > 0 and len(lot_number_padded) > 0 and 
                        rest_part[0] == lot_number_padded[-1]):
                        # Remove o primeiro caractere do restante (que é duplicado)
                        corrected_rest = rest_part[1:] if len(rest_part) > 1 else ""
                        # Reconstrói o nome do arquivo
                        corrected_name = lot_number_padded + corrected_rest
                        return corrected_name + file_ext
            
            # Retorna o nome original se não encontrou padrões incorretos
            return filename_part
        except Exception as e:
            print(f"Erro ao corrigir padrão de nome de arquivo JPG: {e}")
            return filename_part