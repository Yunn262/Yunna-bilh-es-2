import streamlit as st

# Funções auxiliares
def calcular_valor_mao(cartas):
    valor = 0
    ases = 0
    for carta in cartas:
        if carta in ['J', 'Q', 'K']:
            valor += 10
        elif carta == 'A':
            valor += 11
            ases += 1
        else:
            valor += int(carta)
    while valor > 21 and ases:
        valor -= 10
        ases -= 1
    return valor

def sugestao_jogada(valor_jogador, carta_dealer):
    if valor_jogador >= 17:
        return "Stand"
    elif valor_jogador <= 11:
        return "Hit"
    elif 12 <= valor_jogador <= 16:
        if carta_dealer in ['7', '8', '9', '10', 'A']:
            return "Hit"
        else:
            return "Stand"
    else:
        return "Hit"

# Inicializar estado
if 'jogo_iniciado' not in st.session_state:
    st.session_state.jogo_iniciado = False
    st.session_state.cartas_jogador = []

st.set_page_config(page_title="Yunna Bilhões", layout="centered")
st.markdown(
    """
    <div style="background-color: black; padding: 10px;">
        <h1 style="color: white; text-align: center;">♠️♥️♣️♦️ Yunna Bilhões ♠️♥️♣️♦️</h1>
    </div>
    """, unsafe_allow_html=True
)

st.write("🎲 Seja bem-vindo ao Yunna Bilhões!")

st.subheader("Informações da sua mão:")

# Entrar cartas iniciais do jogador
carta1 = st.text_input("Primeira carta (A, 2-10, J, Q, K):", key="carta1")
naipe1 = st.selectbox("Naipe da primeira carta", ["♠️", "♥️", "♣️", "♦️"], key="naipe1")
carta2 = st.text_input("Segunda carta (A, 2-10, J, Q, K):", key="carta2")
naipe2 = st.selectbox("Naipe da segunda carta", ["♠️", "♥️", "♣️", "♦️"], key="naipe2")

st.subheader("Informações do Dealer:")
dealer_carta = st.text_input("Carta visível do Dealer (A, 2-10, J, Q, K):", key="dealer_carta")
dealer_naipe = st.selectbox("Naipe da carta do Dealer", ["♠️", "♥️", "♣️", "♦️"], key="dealer_naipe")

# Botão para prever jogada inicial
if st.button("Prever Jogada"):
    st.session_state.cartas_jogador = [carta1.upper(), carta2.upper()]
    st.session_state.valor_jogador = calcular_valor_mao(st.session_state.cartas_jogador)
    st.session_state.dealer_valor = dealer_carta.upper()
    st.session_state.jogo_iniciado = True
    st.session_state.jogada = sugestao_jogada(st.session_state.valor_jogador, st.session_state.dealer_valor)

# Exibe resultado se o jogo foi iniciado
if st.session_state.jogo_iniciado:
    st.success(f"Valor atual da sua mão: {st.session_state.valor_jogador}")
    st.info(f"Sugestão: {st.session_state.jogada}")

    # Se HIT ou DOUBLE, permitir adicionar terceira carta
    if st.session_state.jogada in ["Hit", "Double"]:
        st.subheader("Adicione a Terceira Carta:")
        terceira_carta = st.text_input("Terceira carta (A, 2-10, J, Q, K):", key="terceira_carta")
        naipe_terceira = st.selectbox("Naipe da terceira carta", ["♠️", "♥️", "♣️", "♦️"], key="naipe_terceira")

        if st.button("Confirmar Terceira Carta"):
            st.session_state.cartas_jogador.append(terceira_carta.upper())
            novo_valor = calcular_valor_mao(st.session_state.cartas_jogador)
            st.success(f"Novo valor da mão: {novo_valor}")
            nova_jogada = sugestao_jogada(novo_valor, st.session_state.dealer_valor)
            st.info(f"Nova sugestão: {nova_jogada}")
