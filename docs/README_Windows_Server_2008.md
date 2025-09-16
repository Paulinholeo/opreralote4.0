# OperaLote 4.3 - Versão 32-bit para Windows Server 2008

## 📋 Informações da Versão

- **Versão:** 4.3 (32-bit)
- **Compatibilidade:** Windows Server 2008 SP2 e superiores
- **Arquitetura:** x86 (32-bit)
- **Tamanho do Executável:** ~30.5 MB
- **Tamanho do Instalador:** ~32.0 MB

## 🚀 Instalação

### Opção 1: Instalador Automático
1. Execute `operalote4.3_32bit.exe` (instalador)
2. Siga as instruções do assistente de instalação
3. O programa será instalado em `C:\Program Files\OperaLote4\`

### Opção 2: Executável Portátil
1. Copie `OperaLote4.3_32bit.exe` para o diretório desejado
2. Execute diretamente (não requer instalação)

## ⚠️ Requisitos do Sistema

### Mínimos:
- **Sistema Operacional:** Windows Server 2008 SP2 ou superior
- **Arquitetura:** x86 (32-bit)
- **RAM:** 512 MB mínimo
- **Espaço em Disco:** 100 MB livre
- **Framework:** .NET Framework 3.5 ou superior (geralmente já instalado)

### Recomendados:
- **RAM:** 1 GB ou mais
- **Espaço em Disco:** 200 MB livre
- **Processador:** 1 GHz ou superior

## 🔧 Funcionalidades

### ✅ Recursos Implementados:
- **Interface com Configuração de Ano:** Checkbox para adicionar/remover ano nos códigos de infração
- **Campo de Ano Personalizável:** Permite especificar o ano (padrão: 2023)
- **Correção de Nomes JPG:** Algoritmo aprimorado para corrigir duplicação de dígitos
- **Suporte a Arquivos RAR:** Processamento de arquivos compactados
- **Interface Moderna:** CustomTkinter com tema escuro/claro
- **Logs Detalhados:** Acompanhamento completo das operações

### 📁 Tipos de Arquivo Suportados:
- `.txt` - Arquivos de texto com dados de infrações
- `.jpg` - Imagens de infrações
- `.zip` - Arquivos compactados
- `.rar` - Arquivos RAR

## 🛠️ Solução de Problemas

### Problema: "Não é possível executar este aplicativo no seu PC"
**Solução:** 
- Verifique se está executando a versão 32-bit em sistema 32-bit
- Execute como Administrador se necessário

### Problema: Erro de dependências
**Solução:**
- Instale o Visual C++ Redistributable 2015-2022 (x86)
- Baixe em: https://aka.ms/vs/17/release/vc_redist.x86.exe

### Problema: Interface não carrega
**Solução:**
- Verifique se o .NET Framework 3.5 está instalado
- Execute: `dism /online /enable-feature /featurename:NetFX3 /all`

## 📞 Suporte

Para suporte técnico ou dúvidas:
- **Empresa:** Brascontrol, Inc.
- **Website:** www.brascontrol.com.br
- **Versão:** 4.3 (32-bit)

## 📝 Notas de Versão

### Versão 4.3 (32-bit)
- ✅ Compilação específica para arquitetura x86
- ✅ Compatibilidade com Windows Server 2008 SP2+
- ✅ Todas as funcionalidades da versão 4.3
- ✅ Otimizações para sistemas mais antigos
- ✅ Exclusão de módulos desnecessários para reduzir tamanho

### Diferenças da Versão 64-bit:
- Menor tamanho de arquivo
- Compatibilidade com sistemas 32-bit
- Exclusão de módulos numpy avançados
- Otimizações específicas para sistemas mais antigos

## 🔒 Segurança

- O executável é assinado digitalmente
- Todas as operações são locais (sem envio de dados)
- Logs detalhados para auditoria
- Backup automático antes de modificações

---
**© 2025 Brascontrol, Inc. - Todos os direitos reservados.**
