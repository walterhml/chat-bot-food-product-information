import telebot
import requests

# Inicialização do bot
bot = telebot.TeleBot("7188266986:AAFNu6J_uokHFpfF6n5y8nDTH6Miq5LSLkQ")

# Comando para mostrar o menu principal
@bot.message_handler(func=['start', 'ajuda'])
def menu_principal(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton('/buscar por nome'), 
               telebot.types.KeyboardButton('/buscar por código de barras'),
               telebot.types.KeyboardButton('/ajuda'))
    bot.send_message(message.chat.id, "Olá! Como posso ajudar você?", reply_markup=markup)

# Comando para buscar um produto por nome
@bot.message_handler(commands=['buscar por nome'])
def buscar_por_nome(message):
    bot.send_message(message.chat.id, "Por favor, digite o nome do produto que deseja buscar.")

# Responder à mensagem com o nome do produto e mostrar opções de pesquisa
@bot.message_handler(func=lambda message: True)
def buscar_produto(message):
    nome_produto = message.text
    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={nome_produto}&search_simple=1&action=process&json=1"
    response = requests.get(url)
    if response.status_code == 200:
        resultados = response.json()['products']
        if resultados:
            resposta = "Resultados da Busca:\n"
            for produto in resultados[:5]:  # Mostrar os primeiros 5 resultados
                resposta += f"Nome: {produto['product_name']}\nCódigo de Barras: {produto['code']}\n\n"
            bot.send_message(message.chat.id, resposta)
        else:
            bot.send_message(message.chat.id, "Nenhum produto encontrado.")
    else:
        bot.send_message(message.chat.id, "Erro ao buscar produtos. Por favor, tente novamente mais tarde.")

# Comando para buscar um produto por código de barras
@bot.message_handler(commands=['buscar por código de barras'])
def buscar_por_codigo(message):
    bot.send_message(message.chat.id, "Por favor, digite o código de barras do produto que deseja buscar.")

# Lidar com mensagens não reconhecidas
@bot.message_handler(func=lambda message: True)
def mensagem_nao_reconhecida(message):
    bot.send_message(message.chat.id, "Desculpe, não entendi o que você quer dizer. Por favor, use comandos válidos.")

# Iniciar o bot
bot.polling()
