# Limpeza de Arquivos Antigos - Downloads

Script Python para identificar e gerenciar arquivos na pasta Downloads que não foram utilizados há mais de 30 dias.

## Características

- Identifica arquivos não acessados há mais de 30 dias (configurável)
- Exibe informações detalhadas: tamanho, data do último acesso, idade em dias
- Calcula espaço total ocupado pelos arquivos antigos
- Múltiplas opções de ação:
  - Listar detalhes completos
  - Mover para pasta de backup
  - Deletar arquivos
  - Exportar relatório em texto
- Funciona em Linux, macOS e Windows
- Interface amigável com emojis e formatação clara

## Requisitos

- Python 3.6 ou superior
- Nenhuma dependência externa (usa apenas bibliotecas padrão)

## Como Usar

### Uso Básico (30 dias)

```bash
python3 cleanup_old_downloads.py
```

### Customizar número de dias

```bash
# Buscar arquivos não usados há mais de 60 dias
python3 cleanup_old_downloads.py 60

# Buscar arquivos não usados há mais de 7 dias
python3 cleanup_old_downloads.py 7
```

### Tornar executável (Linux/macOS)

```bash
chmod +x cleanup_old_downloads.py
./cleanup_old_downloads.py
```

## Opções do Menu

Após executar o script, você terá as seguintes opções:

1. **Listar detalhes completos**: Mostra o caminho completo e informações detalhadas de cada arquivo

2. **Mover para pasta 'old_downloads'**: Move os arquivos para uma subpasta, mantendo-os seguros caso precise recuperá-los

3. **Deletar arquivos**: Remove permanentemente os arquivos (requer confirmação digitando "DELETAR")

4. **Exportar para arquivo texto**: Gera um relatório detalhado em formato texto na pasta Downloads

5. **Sair sem fazer nada**: Apenas visualiza os arquivos sem realizar nenhuma ação

## Exemplo de Saída

```
================================================================================
🧹 LIMPEZA DE ARQUIVOS ANTIGOS - PASTA DOWNLOADS
================================================================================

🔍 Analisando arquivos em: /home/user/Downloads
📅 Buscando arquivos não acessados desde: 2025-09-29 10:30:00

📋 Encontrados 15 arquivo(s) antigo(s):

#    Nome do Arquivo                                    Tamanho      Último Acesso         Dias
---------------------------------------------------------------------------------------------------------
1    documento_antigo.pdf                               2.45 MB      2025-08-15 14:23:10   75
2    video_exemplo.mp4                                  124.67 MB    2025-09-01 09:15:22   58
3    instalador_programa.exe                            45.32 MB     2025-08-20 16:45:30   70
...

💾 Espaço total ocupado: 534.28 MB
```

## Segurança

- O script **nunca** deleta arquivos automaticamente
- Sempre pede confirmação antes de deletar
- Opção de mover arquivos em vez de deletar (recomendado)
- Ignora diretórios, processa apenas arquivos
- Trata erros de permissão adequadamente

## Notas Importantes

- O script usa o **último acesso** (atime) do arquivo como critério
- Em alguns sistemas, o atime pode não ser atualizado a cada leitura (depende das configurações do sistema de arquivos)
- Arquivos movidos para 'old_downloads' podem ser recuperados facilmente
- Sempre revise a lista antes de deletar permanentemente

## Personalização

Você pode modificar o script para:
- Alterar a pasta padrão (modificar `get_downloads_folder()`)
- Adicionar filtros por tipo de arquivo
- Mudar critério de tempo (modificar `st_atime` para `st_mtime` para usar última modificação)
- Adicionar mais opções de ação

## Solução de Problemas

**Problema**: Pasta Downloads não encontrada

**Solução**: Modifique a função `get_downloads_folder()` no script para especificar o caminho correto.

**Problema**: Erro de permissão

**Solução**: Execute o script com permissões adequadas ou mude as permissões dos arquivos.

**Problema**: Nenhum arquivo encontrado mas sei que existem arquivos antigos

**Solução**: Tente usar um número maior de dias ou verifique se o sistema de arquivos atualiza o atime.

## Licença

Script livre para uso pessoal e modificação.
