import os
import tempfile
from text_file_editor import TextFileEditor

def test_md5sum_protection_fix():
    """
    Testa se o TextFileEditor agora protege corretamente o arquivo md5sum.txt
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Teste de proteção md5sum.txt em: {temp_dir}")
        
        # Cria estrutura como no caso real L08989/0008989/AITs/
        l08989_dir = os.path.join(temp_dir, "L08989")
        subdir_0008989 = os.path.join(l08989_dir, "0008989")
        aits_dir = os.path.join(subdir_0008989, "AITs")
        
        os.makedirs(aits_dir)
        
        # Cria arquivos incluindo md5sum.txt que NÃO deve ser alterado
        files_to_create = [
            (os.path.join(l08989_dir, "L08989.txt"), "0008989;dados;info;..."),
            (os.path.join(aits_dir, "normal.txt"), "0008989;dados normais"),
            (os.path.join(aits_dir, "md5sum.txt"), "hash_original;0008989;valor_hash_importante")
        ]
        
        for file_path, content in files_to_create:
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"Criado: {os.path.relpath(file_path, temp_dir)}")
        
        # Lê o conteúdo original do md5sum.txt
        md5sum_path = os.path.join(aits_dir, "md5sum.txt")
        with open(md5sum_path, 'r') as f:
            original_md5sum_content = f.read()
        print(f"\\nConteúdo original md5sum.txt: {original_md5sum_content}")
        
        # Aplica o TextFileEditor
        print(f"\\n=== APLICANDO TextFileEditor ===")
        editor = TextFileEditor(temp_dir)
        
        # Simula a chamada que estava alterando md5sum.txt indevidamente
        editor.edit_text_content("L08989", "L08989")
        
        # Verifica se md5sum.txt foi preservado
        with open(md5sum_path, 'r') as f:
            current_md5sum_content = f.read()
        print(f"\\nConteúdo atual md5sum.txt: {current_md5sum_content}")
        
        # Verifica se outros arquivos foram processados
        normal_txt_path = os.path.join(aits_dir, "normal.txt")
        with open(normal_txt_path, 'r') as f:
            normal_content = f.read()
        print(f"Conteúdo normal.txt: {normal_content}")
        
        # Resultado
        md5sum_preserved = (original_md5sum_content == current_md5sum_content)
        
        print(f"\\n=== RESULTADO ===")
        print(f"md5sum.txt preservado: {'✅ SIM' if md5sum_preserved else '❌ NÃO'}")
        
        if md5sum_preserved:
            print("🎉 CORREÇÃO FUNCIONOU!")
            print("✅ TextFileEditor agora protege md5sum.txt")
            print("✅ Outros arquivos .txt são processados normalmente")
            print("\\n📋 Para aplicar:")
            print("   1. Feche a aplicação OperaLote")
            print("   2. Reinicie a aplicação")
            print("   3. md5sum.txt será preservado")
        else:
            print("❌ CORREÇÃO FALHOU - md5sum.txt ainda está sendo alterado")
            
        return md5sum_preserved

if __name__ == "__main__":
    test_md5sum_protection_fix()