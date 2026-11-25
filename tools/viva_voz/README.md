# Viva Voz — treinador de arguição

Treinador local e turn-based para a banca: o script **fala a pergunta**, grava
sua resposta, transcreve com Whisper e salva a sessão em Markdown.

Não usa LLM. As perguntas vêm de `perguntas.json`; assim o treino é
reprodutível e não depende de modelo generativo.

## Uso rápido

```bash
cd /home/emiyakiritsugu/Projetos_Antigravity/TCC_00
python3 tools/viva_voz/viva_voz.py --segundos 60
```

- Pressione Enter para começar a gravar.
- Fale por até 60 segundos.
- O script transcreve, mostra o texto e pergunta sua autoavaliação.
- Ao final, a sessão fica em `tools/viva_voz/respostas/`.

Opções:

```bash
python3 tools/viva_voz/viva_voz.py --max 5          # 5 perguntas
python3 tools/viva_voz/viva_voz.py --texto          # responde digitando
python3 tools/viva_voz/viva_voz.py --sem-audio      # não fala as perguntas
python3 tools/viva_voz/viva_voz.py --tts-only       # só gera os áudios
```

Para treinar sem microfone, use `--texto --sem-audio`.

## O que está instalado

- **Piper** em `tools/viva_voz/.venv/bin/piper`
- Voz **pt_BR-faber-medium** em `tools/viva_voz/models/`
- **Whisper** no PATH (`whisper --model small`)
- **arecord** (alsa-utils) e **aplay**

O modelo do Whisper é baixado na primeira execução. A voz do Piper já está
local.

## Se precisar reinstalar o Piper

```bash
cd /home/emiyakiritsugu/Projetos_Antigravity/TCC_00
uv venv tools/viva_voz/.venv --python 3.11
uv pip install --python tools/viva_voz/.venv/bin/python piper-tts
mkdir -p tools/viva_voz/models
curl -L -o tools/viva_voz/models/pt_BR-faber-medium.onnx \
  https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx
curl -L -o tools/viva_voz/models/pt_BR-faber-medium.onnx.json \
  https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx.json
```

## Como avaliar depois

1. Rode a sessão.
2. Abra o arquivo em `respostas/`.
3. Cole a transcrição no chat para receber feedback de conteúdo, números e
   estrutura.
4. Se quiser simular a banca completa, use `--max 12`.

## Limitações

- É **turn-based**, não uma conversa em tempo real.
- Não avalia entonação, pronúncia ou nervosismo; só o conteúdo transcrito.
- O Whisper pode errar nomes próprios (“Pollard” → “Polarde”); leia a
  transcrição antes de avaliar.
- O treinador é scripted e não depende de LLM. Se quiser follow-ups
  dinâmicos, um modelo local pequeno (3B–7B) pode ser baixado; os modelos
  antigos do Ollama foram removidos.
