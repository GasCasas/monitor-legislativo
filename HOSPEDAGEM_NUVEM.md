# ☁️ Como hospedar na nuvem (Streamlit Cloud)

Com o app na nuvem você acessa de qualquer lugar — celular, computador,
sem precisar ter nada rodando em casa. E é **gratuito**!

---

## Passo 1 — Criar conta no GitHub

O Streamlit Cloud publica o app a partir do GitHub.

1. Acesse https://github.com e clique em **Sign up**
2. Crie sua conta gratuitamente

---

## Passo 2 — Criar um repositório

1. Após logar, clique no **+** no canto superior direito → **New repository**
2. Nome: `monitor-legislativo`
3. Deixe como **Private** (privado)
4. Clique em **Create repository**

---

## Passo 3 — Enviar os arquivos

Na página do repositório criado, clique em **uploading an existing file** e
arraste toda a pasta `monitor_legislativo` para lá.

Clique em **Commit changes**.

---

## Passo 4 — Publicar no Streamlit Cloud

1. Acesse https://share.streamlit.io e faça login com sua conta GitHub
2. Clique em **New app**
3. Selecione seu repositório `monitor-legislativo`
4. Em **Main file path**, coloque: `app.py`
5. Clique em **Deploy**

Aguarde alguns minutos. Seu app vai ganhar um link como:
`https://seuusuario-monitor-legislativo.streamlit.app`

---

## Passo 5 — Acessar pelo celular

Abra o link no navegador do celular. Para instalar como app:

**Android (Chrome):**
- Toque no menu (⋮) → **Adicionar à tela inicial**

**iPhone (Safari):**
- Toque em compartilhar (□↑) → **Adicionar à Tela de Início**

---

## ⚠️ Atenção sobre notificações na nuvem

Quando o app estiver na nuvem, as verificações automáticas funcionam
**enquanto alguém estiver com o app aberto** no navegador.

Para verificações em segundo plano (mesmo com o app fechado), seria
necessário configurar um serviço externo como o **GitHub Actions** —
posso ajudar com isso se precisar!
