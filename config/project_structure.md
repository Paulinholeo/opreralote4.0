# Estrutura do Projeto OperaLote 4.3

## 📁 Organização de Diretórios

### Estrutura Principal:
```
OperaLote_3.0/
├── src/                    # Código fonte principal
│   ├── main.py            # Ponto de entrada da aplicação
│   ├── gui.py             # Interface gráfica (CustomTkinter)
│   ├── file_renamer.py    # Lógica de renomeação de arquivos
│   ├── text_file_editor.py # Editor de arquivos de texto
│   ├── utils.py           # Utilitários e classes auxiliares
│   ├── infraction_analyzer.py # Analisador de infrações
│   └── config.py          # Configurações do sistema
├── docs/                  # Documentação
│   ├── REFATORACAO_CLEAN_CODE.md
│   ├── IMPLEMENTACAO_ANO.md
│   └── SOLUCAO_WINDOWS_SERVER_2008.md
├── tests/                 # Arquivos de teste e debug
├── build/                 # Arquivos de build (spec files)
├── scripts/               # Scripts de automação
├── config/                # Arquivos de configuração
├── assets/                # Recursos (logos, imagens)
├── logs/                  # Arquivos de log
├── dist/                  # Executáveis compilados
├── output/                # Arquivos de saída
└── install/               # Arquivos de instalação
```

## 🎯 Princípios Aplicados

### Clean Code:
- **Separação de Responsabilidades:** Cada módulo tem uma função específica
- **Modularização:** Classes utilitárias separadas em `utils.py`
- **Documentação:** Documentação técnica organizada em `docs/`
- **Testes:** Arquivos de teste isolados em `tests/`

### Padrões de Projeto:
- **MVC:** Separação entre interface (gui.py) e lógica (file_renamer.py)
- **Factory:** Classes utilitárias para criação de objetos
- **Strategy:** Diferentes estratégias de processamento de arquivos
- **Observer:** Sistema de logs e notificações

## 🔧 Configuração de Desenvolvimento

### Imports Atualizados:
```python
# Antes
from file_renamer import FileRenamer
from text_file_editor import TextFileEditor

# Depois
from src.file_renamer import FileRenamer
from src.text_file_editor import TextFileEditor
```

### Caminhos de Recursos:
```python
# Antes
self.master.iconbitmap('logo/b.ico')

# Depois
self.master.iconbitmap('assets/logo/b.ico')
```

## 📋 Benefícios da Nova Estrutura

### Organização:
- ✅ Código fonte isolado em `src/`
- ✅ Documentação centralizada em `docs/`
- ✅ Testes organizados em `tests/`
- ✅ Scripts de automação em `scripts/`

### Manutenibilidade:
- ✅ Fácil localização de arquivos
- ✅ Separação clara de responsabilidades
- ✅ Estrutura escalável
- ✅ Padrões consistentes

### Colaboração:
- ✅ Estrutura familiar para desenvolvedores
- ✅ Documentação acessível
- ✅ Testes isolados
- ✅ Configuração centralizada

## 🚀 Próximos Passos

### Desenvolvimento:
1. Atualizar todos os imports para nova estrutura
2. Configurar ambiente de desenvolvimento
3. Implementar testes automatizados
4. Documentar APIs e interfaces

### Deploy:
1. Atualizar scripts de build
2. Configurar CI/CD
3. Testar em diferentes ambientes
4. Documentar processo de deploy

---
**Estrutura organizada seguindo princípios de Clean Code e padrões de projeto**
