#!/usr/bin/env python3
"""Treinador de arguição por voz para a banca do TCC.

Fluxo: o script fala a pergunta (Piper), grava a resposta (arecord),
transcreve (Whisper) e salva tudo em Markdown para revisão.

Uso:
  python3 tools/viva_voz/viva_voz.py --segundos 60
  python3 tools/viva_voz/viva_voz.py --texto          # sem microfone
  python3 tools/viva_voz/viva_voz.py --tts-only       # só gera áudios
  python3 tools/viva_voz/viva_voz.py --max 5          # 5 perguntas

Requisitos:
  - Piper em tools/viva_voz/.venv/bin/piper
  - voz em tools/viva_voz/models/pt_BR-faber-medium.onnx
  - arecord (alsa-utils) e whisper no PATH
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
RAIZ = BASE.parent.parent
MODELO_PADRAO = BASE / "models" / "pt_BR-faber-medium.onnx"
PIPER_PADRAO = BASE / ".venv" / "bin" / "piper"
PERGUNTAS = BASE / "perguntas.json"
AUDIO = BASE / "audio"
RESPOSTAS = BASE / "respostas"


def _ts() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _falar(texto: str, *, piper: Path, modelo: Path, sem_audio: bool) -> None:
    if sem_audio:
        return
    AUDIO.mkdir(parents=True, exist_ok=True)
    wav = AUDIO / f"fala_{int(time.time() * 1000)}.wav"
    subprocess.run(
        [str(piper), "-m", str(modelo), "-f", str(wav)],
        input=texto, text=True, check=True,
    )
    player = shutil.which("aplay") or shutil.which("ffplay")
    if not player:
        print(f"[audio] arquivo gerado: {wav}")
        return
    try:
        if Path(player).name == "aplay":
            subprocess.run([player, str(wav)], check=True)
        else:
            subprocess.run([player, "-nodisp", "-autoexit", str(wav)],
                           check=True)
    except subprocess.CalledProcessError:
        print(f"[audio] não foi possível reproduzir; arquivo: {wav}")


def _gravar(segundos: int) -> Path:
    AUDIO.mkdir(parents=True, exist_ok=True)
    wav = AUDIO / f"resposta_{_ts()}.wav"
    print(f"[gravando {segundos}s] fale agora...")
    subprocess.run(
        ["arecord", "-f", "S16_LE", "-r", "16000", "-c", "1",
         "-d", str(segundos), str(wav)],
        check=True,
    )
    return wav


def _transcrever(wav: Path, modelo: str) -> str:
    outdir = AUDIO / "stt"
    outdir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["whisper", str(wav), "--model", modelo, "--language", "Portuguese",
         "--output_format", "txt", "--output_dir", str(outdir),
         "--verbose", "False"],
        check=True,
    )
    txt = outdir / f"{wav.stem}.txt"
    if not txt.exists():
        raise FileNotFoundError(f"transcrição não encontrada: {txt}")
    return txt.read_text(encoding="utf-8").strip()


def _checar(piper: Path, modelo: Path, sem_audio: bool, texto: bool) -> None:
    if not sem_audio:
        if not piper.exists():
            sys.exit(
                f"Piper não encontrado em {piper}. Rode o setup do README "
                "ou use --sem-audio."
            )
        if not modelo.exists():
            sys.exit(
                f"Voz não encontrada em {modelo}. Baixe pt_BR-faber-medium.onnx "
                "e .onnx.json (veja o README)."
            )
    if not texto:
        if shutil.which("arecord") is None:
            sys.exit("arecord não encontrado; use --texto ou instale alsa-utils.")
        if shutil.which("whisper") is None:
            sys.exit("whisper não encontrado; use --texto ou instale openai-whisper.")


def _carregar(maximo: int) -> list[dict]:
    dados = json.loads(PERGUNTAS.read_text(encoding="utf-8"))
    if maximo > 0:
        dados = dados[:maximo]
    return dados


def _tts_only(perguntas: list[dict], piper: Path, modelo: Path) -> None:
    destino = AUDIO / "perguntas"
    destino.mkdir(parents=True, exist_ok=True)
    for i, item in enumerate(perguntas, 1):
        wav = destino / f"pergunta_{i:02d}.wav"
        subprocess.run(
            [str(piper), "-m", str(modelo), "-f", str(wav)],
            input=item["pergunta"], text=True, check=True,
        )
        print(f"{wav}  ({item['tema']})")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--segundos", type=int, default=60,
                        help="tempo de gravação por pergunta (padrão: 60)")
    parser.add_argument("--max", type=int, default=0,
                        help="limita o número de perguntas (0 = todas)")
    parser.add_argument("--texto", action="store_true",
                        help="responde digitando, sem microfone")
    parser.add_argument("--sem-audio", action="store_true",
                        help="não fala as perguntas")
    parser.add_argument("--tts-only", action="store_true",
                        help="apenas gera os áudios das perguntas")
    parser.add_argument("--modelo", type=Path, default=MODELO_PADRAO)
    parser.add_argument("--piper", type=Path,
                        default=Path(os.environ.get("PIPER_BIN", PIPER_PADRAO)))
    parser.add_argument("--whisper-model", default="small")
    args = parser.parse_args()

    perguntas = _carregar(args.max)
    if not perguntas:
        sys.exit("nenhuma pergunta encontrada")

    _checar(args.piper, args.modelo, args.sem_audio, args.texto)

    if args.tts_only:
        _tts_only(perguntas, args.piper, args.modelo)
        return

    RESPOSTAS.mkdir(parents=True, exist_ok=True)
    sessao = RESPOSTAS / f"sessao_{_ts()}.md"
    linhas = [
        "# Sessão de arguição",
        "",
        f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        f"Perguntas: {len(perguntas)}",
        "",
        "---",
        "",
    ]

    print("\nSessão de arguição — responda em voz alta, sem consultar.")
    for i, item in enumerate(perguntas, 1):
        print(f"\n=== Pergunta {i}/{len(perguntas)} — {item['tema']} ===")
        print(item["pergunta"])
        _falar(item["pergunta"], piper=args.piper, modelo=args.modelo,
               sem_audio=args.sem_audio)

        if args.texto:
            resposta = input("\nSua resposta: ").strip()
        else:
            input("\nPressione Enter para gravar...")
            try:
                wav = _gravar(args.segundos)
                print("[transcrevendo...]")
                resposta = _transcrever(wav, args.whisper_model)
            except (subprocess.CalledProcessError, FileNotFoundError) as exc:
                print(f"[erro] {exc}")
                resposta = input("Digite a resposta (ou Enter para pular): ").strip()
            print("\nTranscrição:")
            print(resposta or "(vazia)")

        nota = input("\nAutoavaliação de 1 a 5 (Enter para pular): ").strip()
        linhas += [
            f"## Pergunta {i} — {item['tema']}",
            "",
            f"**Pergunta:** {item['pergunta']}",
            "",
            "**Resposta transcrita:**",
            "",
            resposta or "(vazia)",
            "",
        ]
        if nota:
            linhas += [f"**Autoavaliação:** {nota}/5", ""]
        linhas += ["---", ""]
        input("Enter para a próxima...")

    sessao.write_text("\n".join(linhas), encoding="utf-8")
    print(f"\nSessão salva em: {sessao}")
    print("Cole a transcrição no chat para receber feedback.")
    _falar("Fim da sessão. Obrigado.", piper=args.piper,
           modelo=args.modelo, sem_audio=args.sem_audio)


if __name__ == "__main__":
    main()
