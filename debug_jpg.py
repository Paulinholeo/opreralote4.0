import os
import tempfile
from file_renamer import FileRenamer

def debug_jpg_rename():
    """
    Debug específico para entender porque os JPGs não estão sendo renomeados
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Debug JPG em: {temp_dir}")
        
        # Cria estrutura já corrigida (L08987/0008987/AITs/)
        l08987_dir = os.path.join(temp_dir, "L08987")
        subdir_0008987 = os.path.join(l08987_dir, "0008987") 
        aits_dir = os.path.join(subdir_0008987, "AITs")
        
        os.makedirs(aits_dir)
        
        # Cria apenas arquivos JPG para debug
        jpg_files = [
            os.path.join(aits_dir, "0000125000001a.jpg"),
            os.path.join(aits_dir, "0000125000001b.jpg"),
        ]
        
        for jpg_file in jpg_files:
            with open(jpg_file, 'w') as f:
                f.write("fake jpg data")
        
        print("\n=== ESTRUTURA INICIAL (após correção subdir) ===")
        for root, dirs, files in os.walk(l08987_dir):
            level = root.replace(l08987_dir, '').count(os.sep)
            indent = '  ' * level
            print(f"{indent}📁 {os.path.basename(root)}/")
            sub_indent = '  ' * (level + 1)
            for file in files:
                print(f"{sub_indent}📄 {file}")
        
        # Simula apenas a parte de JPG da função rename_files
        renamer = FileRenamer(temp_dir)
        old_name = "L08987"
        new_name = "L08987"
        
        old_name_number = old_name[1:] if old_name[0].isalpha() else old_name
        new_name_number = new_name[1:] if new_name[0].isalpha() else new_name
        
        print(f"\\nValores de controle:")
        print(f"old_name: {old_name}")
        print(f"new_name: {new_name}")
        print(f"old_name_number: {old_name_number}")
        print(f"new_name_number: {new_name_number}")
        
        # Busca diretórios como na função original
        search_directories = []
        
        main_dir_new = os.path.join(temp_dir, new_name)
        if os.path.exists(main_dir_new):
            search_directories.append(main_dir_new)
            print(f"Adicionado diretório principal: {main_dir_new}")
        
        # Expande para subdiretórios
        expanded_search_dirs = []
        for search_dir in search_directories:
            expanded_search_dirs.append(search_dir)
            if os.path.exists(search_dir):
                for item in os.listdir(search_dir):
                    item_path = os.path.join(search_dir, item)
                    if os.path.isdir(item_path):
                        expanded_search_dirs.append(item_path)
                        aits_path = os.path.join(item_path, 'AITs')
                        if os.path.exists(aits_path):
                            expanded_search_dirs.append(aits_path)
                            print(f"Adicionado AITs: {aits_path}")
        
        search_directories = expanded_search_dirs
        
        print(f"\\n=== DIRETÓRIOS DE BUSCA ===")
        for search_dir in search_directories:
            print(f"🔍 {search_dir}")
        
        # Simula a lógica de JPG
        print(f"\\n=== PROCESSANDO JPGs ===")
        import glob
        
        for search_dir in search_directories:
            if not os.path.exists(search_dir):
                continue
            
            print(f"\\nProcurando JPGs em: {search_dir}")
            jpg_pattern = os.path.join(search_dir, '*.jpg')
            print(f"Padrão: {jpg_pattern}")
            
            jpg_files_found = glob.glob(jpg_pattern)
            print(f"JPGs encontrados: {len(jpg_files_found)}")
            
            for filename in jpg_files_found:
                print(f"\\nProcessando: {filename}")
                
                old_name_number_jpg = old_name[1:].split('.')[0] if old_name[0].isalpha() else old_name.split('.')[0]
                print(f"old_name_number_jpg: {old_name_number_jpg}")
                
                base_filename = os.path.basename(filename)
                print(f"base_filename: {base_filename}")
                
                if old_name_number_jpg in base_filename:
                    print(f"✅ Contém {old_name_number_jpg}")
                    
                    file_name_without_ext = os.path.splitext(base_filename)[0]
                    print(f"file_name_without_ext: {file_name_without_ext}")
                    
                    new_base_name_without_ext = file_name_without_ext.replace(old_name_number_jpg, '00' + new_name_number)
                    print(f"new_base_name_without_ext: {new_base_name_without_ext}")
                    
                    new_base_name = new_base_name_without_ext + '.jpg'
                    new_filename = os.path.join(os.path.dirname(filename), new_base_name)
                    
                    print(f"Tentando renomear:")
                    print(f"  De: {filename}")
                    print(f"  Para: {new_filename}")
                    
                    if os.path.exists(filename) and filename != new_filename:
                        try:
                            os.rename(filename, new_filename)
                            print(f"✅ SUCESSO!")
                        except Exception as e:
                            print(f"❌ ERRO: {e}")
                    else:
                        print(f"⚠️ Arquivo não existe ou nomes são iguais")
                else:
                    print(f"❌ NÃO contém {old_name_number_jpg}")

if __name__ == "__main__":
    debug_jpg_rename()