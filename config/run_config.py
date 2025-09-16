"""
Configuração de execução do OperaLote 4.3
"""

import sys
import os

def setup_path():
    """Configura o path do Python para incluir o diretório src"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    src_path = os.path.join(project_root, 'src')
    
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
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
