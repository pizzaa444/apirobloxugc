import requests

# ⚠️ Troque pela URL do seu Webhook do Discord
WEBHOOK_URL = "SUA_WEBHOOK_URL_AQUI"

def get_ugc_items(limit_price=1000):
    url = "https://catalog.roblox.com/v1/search/items/details?Category=11&SortType=1&Limit=30"
    response = requests.get(url)

    if response.status_code != 200:
        print("❌ Erro ao buscar itens do Roblox")
        return []

    data = response.json()
    return [
        item for item in data.get("data", [])
        if item.get("price") is not None and item.get("price") < limit_price
    ]

def send_to_discord(items):
    if not items:
        requests.post(WEBHOOK_URL, json={"content": "⚠️ Nenhum item abaixo de 1000 Robux."})
        return

    message = "**Itens UGC abaixo de 1000 Robux:**\n\n"
    for item in items[:10]:  # mostra só os 10 primeiros
        name = item.get("name")
        price = item.get("price")
        item_id = item.get("id")
        link = f"https://www.roblox.com/catalog/{item_id}"
        message += f"- [{name}]({link}) → {price} Robux\n"

    requests.post(WEBHOOK_URL, json={"content": message})

if __name__ == "__main__":
    ugc_items = get_ugc_items()
    send_to_discord(ugc_items)
