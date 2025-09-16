#!/usr/bin/env python3
"""
OperaLote 4.3 - Sistema de Análise de Infrações
Ponto de entrada principal da aplicação
"""

import sys
import os

# Adiciona o diretório src ao path do Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Importa e executa a aplicação
from main import main

if __name__ == "__main__":
    main()
