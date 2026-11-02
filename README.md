# Bot de boosts do Discord

Bot em Python que detecta quando um membro começa ou deixa de fazer boost no servidor e aplica/removem um cargo especial.

## Como funciona
- o usuário faz boost manualmente no Discord
- o bot detecta com `on_member_update`
- se a pessoa começou a boostar, recebe o cargo `Double Booster`
- se a pessoa deixou de boostar, o cargo é removido

## Requisitos
- Python 3.10+
- `discord.py`
- `python-dotenv`

## Instalação

```bash
pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz do projeto:

```env
DISCORD_TOKEN=SEU_TOKEN_AQUI
```

## Execução

```bash
python main.py
```

## Configuração no servidor
Use o comando slash:

```text
/configurar
```

Isso cria o cargo `Double Booster` e o canal `notificações-boosts`.
