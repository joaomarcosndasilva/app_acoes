def analisar_ativo(codigo_ativo='BEEF3', periodo_analisado='9'):
    import pandas as pd
    import yfinance as yf
    yf.pdr_override()
    global df3, lr, y_de_amanha
    ativo, periodo = codigo_ativo, periodo_analisado

    ticket = f'{ativo}.SA'
    ticketII = yf.Ticker(ticket)
    df_inicial = ticketII.history(period=f'{periodo}y')
    df_inicial = df_inicial.drop(['Dividends', 'Stock Splits'], axis=1)
    df_inicial['mm9'] = df_inicial['Close'].rolling(9).mean().round(2)
    df_inicial['mm21'] = df_inicial['Close'].rolling(21).mean().round(2)
    df = df_inicial[:]
    df['Close'] = df['Close'].shift(-1)
    df = df.dropna()

    total = len(df)
    total_inicial = len(df_inicial)

    treino = total - 700
    treino_inicial = total_inicial - 700

    teste = total - 15
    teste_inicial = total_inicial - 15

    ########################################################################################################################
    print(f'Treino 0:{treino} - Teste {treino}:{teste} - Validação {teste}:{total}')
    print(
        f'Treino 0:{treino_inicial} - Teste {treino_inicial}:{teste_inicial} - Validação {teste_inicial}:{total_inicial}')
    ########################################################################################################################

    df = df.reset_index()
    df_inicial = df_inicial.reset_index()

    x_features = df.drop(['Date', 'Close'], axis=1)
    x_features_inicial = df_inicial.drop(['Date', 'Close'], axis=1)

    x_features_list = list(x_features)

    y_labels = df['Close']
    y_labels_inicial = df_inicial['Close']

    from sklearn.feature_selection import SelectKBest

    k_best_features = SelectKBest(k='all')
    k_best_features.fit_transform(x_features, y_labels)
    k_best_features_score = k_best_features.scores_
    melhores = zip(x_features_list, k_best_features_score)
    melhores_ordenados = list(reversed(sorted(melhores, key=lambda x: x[1])))

    melhores_variaveis = dict(melhores_ordenados[:15])
    melhores_selecionadas = melhores_variaveis.keys()

    x_features = x_features.drop('Volume', axis=1)
    x_features_inicial = df_inicial.drop(['Date', 'Close', 'Volume'], axis=1)

    from sklearn.preprocessing import StandardScaler

    scaler = StandardScaler()
    scaler.fit(x_features)
    x_features_normalizado = scaler.fit_transform(x_features)

    x_features_inicial = x_features_inicial.dropna()
    scaler.fit(x_features_inicial)
    x_features_inicial_normalizado = scaler.fit_transform(x_features_inicial)

    x_features_normal = pd.DataFrame(x_features_normalizado, columns=list(x_features.columns))
    x_features_normal

    x_features_normal_inicial = pd.DataFrame(x_features_inicial_normalizado, columns=list(x_features_inicial.columns))
    x_features_normal_inicial

    x_train = x_features_normal[0:treino]
    x_train_inicial = x_features_inicial_normalizado[0:treino_inicial]

    x_test = x_features_normal[treino:teste]
    x_test_inicial = x_features_inicial_normalizado[treino_inicial:teste_inicial]

    y_train = y_labels[0:treino]
    y_train_inicial = y_labels[0:treino_inicial]

    y_test = y_labels[treino:teste]
    y_test_inicial = y_labels[treino_inicial:teste_inicial]

    print()
    print(f'O modelo aprenderá com os dados da linha 0 a {treino} das variáveis {list(x_features.columns)}')
    print(f'O modelo testará com os dados da linha {treino} a {teste} da variável Close')
    print()
    print(
        f'O modelo aprenderá com os dados da linha 0 a {treino_inicial} das variáveis {list(x_features_inicial.columns)}')
    print(f'O modelo testará com os dados da linha {treino_inicial} a {teste_inicial} da variável Close')

    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import r2_score

    lr = LinearRegression()
    lr.fit(x_train, y_train)
    y_predito = lr.predict(x_test)

    # lr.fit()
    coeficiente = r2_score(y_test, y_predito)

    f'''O coeficiente é de {coeficiente * 100:.2f}, isto é,  {coeficiente * 100:.2f} das variações no valor dopreço futuro de
    Fechamento (Close) é explicada pela variação nas variávies {list(x_features.columns)} do dia anterior'''

    previsao = x_features_normal[teste:total]
    dia = df['Date'][teste:total]
    real = df['Close'][teste:total]

    previsao_hoje = x_features_normal_inicial[teste:total]
    dia_hoje = df_inicial['Date'][teste_inicial:total_inicial]
    real_hoje = df_inicial['Close'][teste_inicial:total_inicial]

    y_pred = lr.predict(previsao)
    y_de_amanha = lr.predict(x_features_inicial_normalizado)

    df2 = pd.DataFrame({'Data': dia, 'Cotacao': real, 'Previsto': y_pred})
    df2['Cotacao'] = df2['Cotacao'].shift(+1)
    # Nessa linha acima, estamos devolvendo as cotações ao valor verdadeiro, isto é, desfazemos o que fizemos acima

    # df3 = pd.DataFrame({'Data':dia_hoje, 'Cotacao':real_hoje, 'Previsto':y_de_amanha})
    # df3['Cotacao'] = df2['Cotacao'].shift(+1)
    #df3 = df2.dropna()
    #df3['Erro'] = df3['Cotacao'] - df3['Previsto']
    #df3.round(2)

    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    fig, ax = plt.subplots(figsize=(16, 8))

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax.xaxis.set_tick_params(rotation=30)

    ax.set_title(f'Ativo: {ativo} -> {round(coeficiente * 100, 2)}%- By J. Brutus', fontsize=16)
    ax.set_ylabel('Preço do ativo em R$', fontsize=14)
    ax.plot(df2['Data'], df2['Cotacao'], marker='o', label='Cotação Real', color='blue')
    ax.plot(df2['Data'], df2['Previsto'], marker='o', label='Cotação Prevista', color='red')

    plt.grid()
    plt.show()
    # fig, ax = plt.subplots(figsize=(16,8))
    ###################################################################################################


analisar_ativo()

