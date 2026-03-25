# 🏛️ Monitor Legislativo

Acompanhe proposições da **Câmara dos Deputados** e do **Senado Federal** com análise por IA e exportação de relatórios.

## O que o projeto faz

- 🔍 **Busca** proposições por número e ano em ambas as casas
- 📜 **Exibe** o histórico completo de tramitação
- 📋 **Monitora** PLs e detecta mudanças de situação
- 🤖 **Analisa** textos com Inteligência Artificial (Claude)
- 📥 **Exporta** relatórios em Excel, PDF ou CSV

---

## Como instalar e rodar

### 1. Instale o Python
Acesse https://www.python.org/downloads/ e instale a versão mais recente.

### 2. Abra o terminal na pasta do projeto
No Windows: clique com botão direito na pasta → "Abrir no Terminal"
No Mac/Linux: abra o Terminal e navegue até a pasta.

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Rode o aplicativo
```bash
streamlit run app.py
```

O navegador abrirá automaticamente em `http://localhost:8501`.

---

## Estrutura do projeto

```
monitor_legislativo/
├── app.py                  # Interface principal (Streamlit)
├── requirements.txt        # Dependências Python
├── data/
│   └── monitorados.json    # Proposições salvas (criado automaticamente)
├── exports/                # Relatórios exportados (criado automaticamente)
└── src/
    ├── camara.py           # API da Câmara dos Deputados
    ├── senado.py           # API do Senado Federal
    ├── monitor.py          # Monitoramento e detecção de mudanças
    ├── ai_analysis.py      # Análise com Claude (IA)
    └── exporter.py         # Exportação Excel / PDF / CSV
```

---

## Análise com IA (opcional)

Para usar a análise por IA, você precisa de uma chave da API da Anthropic:
1. Acesse https://console.anthropic.com
2. Crie uma conta e gere uma chave de API
3. Cole a chave no campo indicado na aba "Análise IA"

---

## APIs utilizadas

| Casa | URL Base | Documentação |
|------|----------|--------------|
| Câmara | `https://dadosabertos.camara.leg.br/api/v2` | [Swagger](https://dadosabertos.camara.leg.br/swagger/openapi.html) |
| Senado | `https://legis.senado.leg.br/dadosabertos` | [Docs](https://legis.senado.leg.br/dadosabertos/docs) |

Ambas são **gratuitas e abertas**, sem necessidade de cadastro.
