#!/usr/bin/env python3
"""
Script para revisar e limpar arquivos antigos na pasta Downloads.
Identifica arquivos não utilizados há mais de 30 dias.
"""

import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple

def get_downloads_folder() -> Path:
    """Retorna o caminho da pasta Downloads do usuário."""
    home = Path.home()

    # Tenta diferentes localizações comuns da pasta Downloads
    possible_paths = [
        home / "Downloads",
        home / "downloads",
        home / "Download",
        home / "download"
    ]

    for path in possible_paths:
        if path.exists() and path.is_dir():
            return path

    # Se não encontrar, retorna o padrão
    return home / "Downloads"

def format_size(size_bytes: int) -> str:
    """Formata o tamanho do arquivo em formato legível."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

def format_date(timestamp: float) -> str:
    """Formata timestamp em data legível."""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def find_old_files(downloads_path: Path, days: int = 30) -> List[Tuple[Path, os.stat_result]]:
    """
    Encontra arquivos que não foram acessados há mais de X dias.

    Args:
        downloads_path: Caminho da pasta Downloads
        days: Número de dias (padrão: 30)

    Returns:
        Lista de tuplas (caminho_arquivo, stats)
    """
    cutoff_time = time.time() - (days * 24 * 60 * 60)
    old_files = []

    print(f"🔍 Analisando arquivos em: {downloads_path}")
    print(f"📅 Buscando arquivos não acessados desde: {format_date(cutoff_time)}\n")

    try:
        for item in downloads_path.iterdir():
            # Ignora diretórios, processa apenas arquivos
            if not item.is_file():
                continue

            try:
                stats = item.stat()
                # Usa o último acesso (atime) para determinar se o arquivo é antigo
                last_access = stats.st_atime

                if last_access < cutoff_time:
                    old_files.append((item, stats))
            except (PermissionError, OSError) as e:
                print(f"⚠️  Não foi possível acessar: {item.name} - {e}")
                continue

    except PermissionError:
        print(f"❌ Erro: Sem permissão para acessar {downloads_path}")
        sys.exit(1)

    return old_files

def display_files(files: List[Tuple[Path, os.stat_result]]) -> None:
    """Exibe informações sobre os arquivos encontrados."""
    if not files:
        print("✅ Nenhum arquivo antigo encontrado!")
        return

    print(f"📋 Encontrados {len(files)} arquivo(s) antigo(s):\n")
    print(f"{'#':<4} {'Nome do Arquivo':<50} {'Tamanho':<12} {'Último Acesso':<20} {'Dias':<6}")
    print("-" * 105)

    total_size = 0
    now = time.time()

    for idx, (file_path, stats) in enumerate(files, 1):
        size = stats.st_size
        last_access = stats.st_atime
        days_old = int((now - last_access) / (24 * 60 * 60))

        # Trunca nome do arquivo se for muito longo
        file_name = file_path.name
        if len(file_name) > 47:
            file_name = file_name[:44] + "..."

        print(f"{idx:<4} {file_name:<50} {format_size(size):<12} {format_date(last_access):<20} {days_old:<6}")
        total_size += size

    print("-" * 105)
    print(f"💾 Espaço total ocupado: {format_size(total_size)}\n")

def get_user_choice() -> str:
    """Pergunta ao usuário o que fazer com os arquivos."""
    print("\n🤔 O que você deseja fazer?")
    print("  1) Listar detalhes completos (caminho completo)")
    print("  2) Mover arquivos para uma pasta 'old_downloads'")
    print("  3) Deletar arquivos (CUIDADO: irreversível!)")
    print("  4) Exportar lista para arquivo texto")
    print("  5) Sair sem fazer nada")

    while True:
        choice = input("\nEscolha uma opção (1-5): ").strip()
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        print("⚠️  Opção inválida. Por favor, escolha 1, 2, 3, 4 ou 5.")

def list_full_details(files: List[Tuple[Path, os.stat_result]]) -> None:
    """Lista detalhes completos dos arquivos."""
    print("\n📝 Detalhes completos:\n")
    for idx, (file_path, stats) in enumerate(files, 1):
        print(f"{idx}. {file_path}")
        print(f"   Tamanho: {format_size(stats.st_size)}")
        print(f"   Último acesso: {format_date(stats.st_atime)}")
        print(f"   Última modificação: {format_date(stats.st_mtime)}")
        print()

def move_files(files: List[Tuple[Path, os.stat_result]], downloads_path: Path) -> None:
    """Move arquivos para uma pasta old_downloads."""
    old_folder = downloads_path / "old_downloads"
    old_folder.mkdir(exist_ok=True)

    print(f"\n📦 Movendo arquivos para: {old_folder}\n")

    moved_count = 0
    for file_path, _ in files:
        try:
            destination = old_folder / file_path.name
            # Se já existe arquivo com mesmo nome, adiciona timestamp
            if destination.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                destination = old_folder / f"{file_path.stem}_{timestamp}{file_path.suffix}"

            file_path.rename(destination)
            print(f"✅ Movido: {file_path.name}")
            moved_count += 1
        except Exception as e:
            print(f"❌ Erro ao mover {file_path.name}: {e}")

    print(f"\n✅ {moved_count} arquivo(s) movido(s) com sucesso!")

def delete_files(files: List[Tuple[Path, os.stat_result]]) -> None:
    """Deleta os arquivos após confirmação."""
    print("\n⚠️  ATENÇÃO: Esta ação é irreversível!")
    confirm = input("Digite 'DELETAR' (em maiúsculas) para confirmar: ").strip()

    if confirm != "DELETAR":
        print("❌ Operação cancelada.")
        return

    print("\n🗑️  Deletando arquivos...\n")

    deleted_count = 0
    for file_path, _ in files:
        try:
            file_path.unlink()
            print(f"✅ Deletado: {file_path.name}")
            deleted_count += 1
        except Exception as e:
            print(f"❌ Erro ao deletar {file_path.name}: {e}")

    print(f"\n✅ {deleted_count} arquivo(s) deletado(s)!")

def export_to_file(files: List[Tuple[Path, os.stat_result]], downloads_path: Path) -> None:
    """Exporta lista de arquivos para um arquivo texto."""
    export_file = downloads_path / f"old_files_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    try:
        with open(export_file, 'w', encoding='utf-8') as f:
            f.write("RELATÓRIO DE ARQUIVOS ANTIGOS - DOWNLOADS\n")
            f.write(f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")

            total_size = 0
            for idx, (file_path, stats) in enumerate(files, 1):
                days_old = int((time.time() - stats.st_atime) / (24 * 60 * 60))
                f.write(f"{idx}. {file_path}\n")
                f.write(f"   Tamanho: {format_size(stats.st_size)}\n")
                f.write(f"   Último acesso: {format_date(stats.st_atime)} ({days_old} dias atrás)\n")
                f.write(f"   Última modificação: {format_date(stats.st_mtime)}\n\n")
                total_size += stats.st_size

            f.write("=" * 80 + "\n")
            f.write(f"Total: {len(files)} arquivos, {format_size(total_size)}\n")

        print(f"\n✅ Relatório exportado para: {export_file}")
    except Exception as e:
        print(f"❌ Erro ao exportar: {e}")

def main():
    """Função principal."""
    print("=" * 80)
    print("🧹 LIMPEZA DE ARQUIVOS ANTIGOS - PASTA DOWNLOADS")
    print("=" * 80 + "\n")

    # Permite customizar o número de dias
    days = 30
    if len(sys.argv) > 1:
        try:
            days = int(sys.argv[1])
            print(f"ℹ️  Usando {days} dias como critério (customizado)\n")
        except ValueError:
            print(f"⚠️  Argumento inválido. Usando padrão de {days} dias.\n")

    downloads_path = get_downloads_folder()

    if not downloads_path.exists():
        print(f"❌ Pasta Downloads não encontrada: {downloads_path}")
        print("💡 Dica: Você pode modificar o script para especificar um caminho customizado.")
        sys.exit(1)

    # Encontra arquivos antigos
    old_files = find_old_files(downloads_path, days)

    # Exibe arquivos encontrados
    display_files(old_files)

    if not old_files:
        return

    # Menu de ações
    choice = get_user_choice()

    if choice == '1':
        list_full_details(old_files)
    elif choice == '2':
        move_files(old_files, downloads_path)
    elif choice == '3':
        delete_files(old_files)
    elif choice == '4':
        export_to_file(old_files, downloads_path)
    else:
        print("\n👋 Saindo sem fazer alterações.")

    print("\n" + "=" * 80)
    print("✅ Concluído!")
    print("=" * 80)

if __name__ == "__main__":
    main()
