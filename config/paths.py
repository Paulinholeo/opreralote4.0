"""
Configuração de paths para o OperaLote 4.3
"""

import sys
import os

def setup_environment():
    """
    Configura o ambiente Python com todos os paths necessários
    """
    # Obtém o diretório raiz do projeto
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    # Paths necessários
    paths = [
        os.path.join(project_root, 'src'),      # Código fonte
        os.path.join(project_root, 'assets'),   # Assets e módulos customizados
        os.path.join(project_root, 'assets', 'CTkScrollableDropdown'),  # CTkScrollableDropdown
        os.path.join(project_root, 'assets', 'CTkListbox'),  # CTkListbox
    ]
    
    # Adiciona cada path ao sys.path se não estiver presente
    for path in paths:
        if os.path.exists(path) and path not in sys.path:
            sys.path.insert(0, path)
    
    return project_root

def get_assets_path():
    """Retorna o caminho para os assets"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    return os.path.join(project_root, 'assets')

def get_logs_path():
    """Retorna o caminho para os logs"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    return os.path.join(project_root, 'logs')

def get_src_path():
    """Retorna o caminho para o código fonte"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    return os.path.join(project_root, 'src')
