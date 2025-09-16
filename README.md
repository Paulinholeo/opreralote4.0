# OperaLote 4.3 - Sistema de Análise de Infrações

## 📋 Visão Geral

O OperaLote é um sistema desenvolvido pela Brascontrol para análise e processamento de infrações de trânsito. A versão 4.3 inclui funcionalidades avançadas de renomeação de lotes, correção de nomes de arquivos JPG e configuração personalizada de anos.

## 🏗️ Estrutura do Projeto

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
│   ├── build_all.bat
│   ├── build_exe.bat
│   └── build_installer.bat
├── config/                # Arquivos de configuração
│   └── requirements.txt
├── assets/                # Recursos (logos, imagens)
│   └── logo/
├── logs/                  # Arquivos de log
├── dist/                  # Executáveis compilados
├── output/                # Arquivos de saída
└── install/               # Arquivos de instalação
```

## 🚀 Funcionalidades

### ✅ Recursos Implementados:
- **Interface Moderna:** CustomTkinter com tema escuro/claro
- **Configuração de Ano:** Checkbox para adicionar/remover ano nos códigos
- **Campo de Ano Personalizável:** Permite especificar o ano (padrão: 2023)
- **Correção de Nomes JPG:** Algoritmo aprimorado para duplicação de dígitos
- **Suporte a Arquivos RAR:** Processamento de arquivos compactados
- **Logs Detalhados:** Acompanhamento completo das operações
- **Refatoração Clean Code:** Código modularizado e organizado

### 📁 Tipos de Arquivo Suportados:
- `.txt` - Arquivos de texto com dados de infrações
- `.jpg` - Imagens de infrações
- `.zip` - Arquivos compactados
- `.rar` - Arquivos RAR

## 🛠️ Instalação e Uso

### Pré-requisitos:
- Windows 7/8/10/11 ou Windows Server 2008+
- Python 3.8+ (para desenvolvimento)
- .NET Framework 3.5+ (geralmente já instalado)

### Instalação:
1. **Executável:** Execute `dist/OperaLote4.3.exe`
2. **Instalador:** Execute `output/install/operalote4.3.exe`
3. **Desenvolvimento:** Veja seção de desenvolvimento abaixo

### Uso:
1. Selecione o diretório do lote
2. Escolha o lote a ser renomeado
3. Digite o novo nome do lote
4. Configure o ano (opcional)
5. Clique em "Executar"

## 🔧 Desenvolvimento

### Estrutura do Código:
- **Clean Code:** Princípios SOLID aplicados
- **Modularização:** Classes utilitárias separadas
- **Testes:** Arquivos de teste organizados em `tests/`
- **Documentação:** Documentação técnica em `docs/`

### Compilação:
```cmd
# Build completo
scripts/build_all.bat

# Apenas executável
scripts/build_exe.bat

# Apenas instalador
scripts/build_installer.bat
```

### Dependências:
```cmd
pip install -r config/requirements.txt
```

## 📊 Versões

| Versão | Arquitetura | Compatibilidade | Tamanho | Uso Recomendado |
|--------|-------------|-----------------|---------|-----------------|
| OperaLote4.3.exe | 64-bit | Windows 10/11 | 30.8 MB | Sistemas modernos |
| OperaLote4.3_Legacy.exe | 64-bit | Windows 7+ | 30.2 MB | Máxima compatibilidade |

## 🐛 Solução de Problemas

### Problemas Comuns:
- **"Não é um Win32 válido":** Use a versão Legacy
- **Interface não carrega:** Verifique .NET Framework 3.5
- **Erro de dependências:** Instale Visual C++ Redistributable

### Logs:
- Verifique a pasta `logs/` para arquivos de log
- Execute em modo console para debug detalhado

## 📞 Suporte

- **Empresa:** Brascontrol, Inc.
- **Website:** www.brascontrol.com.br
- **Versão:** 4.3
- **Documentação:** Veja pasta `docs/`

## 📝 Changelog

### Versão 4.3:
- ✅ Interface com configuração de ano
- ✅ Correção de nomes JPG aprimorada
- ✅ Refatoração Clean Code
- ✅ Suporte a Windows Server 2008
- ✅ Documentação completa

### Versão 4.2:
- ✅ Correção de bugs de JPG
- ✅ Melhorias na interface

### Versão 4.1:
- ✅ Suporte a arquivos RAR
- ✅ Logs detalhados

## 🔒 Licença

© 2025 Brascontrol, Inc. - Todos os direitos reservados.

---
**Desenvolvido com ❤️ pela equipe Brascontrol**
