from Auditoria import Auditoria
import pandas as pd
import matplotlib.pyplot as plt


class Principal:

    # ==========================================
    # TESTE 1 - TRANSAÇÕES DUPLICADAS
    # ==========================================

    def TestOne(self, Transacoes):

        duplicadas = Transacoes[
            Transacoes.duplicated(
                subset=["Fornecedor", "Valor (R$)", "Data"],
                keep=False
            )
        ]

        for indice, transacao in duplicadas.iterrows():

            id = transacao["ID"]
            data = transacao["Data"]
            fornecedor = transacao["Fornecedor"]
            valor = transacao["Valor (R$)"]
            funcionario = transacao["Funcionario_Responsavel"]
            cargo = transacao["Cargo"]

            print(f"""
ID: {id}
Data: {data}
Fornecedor: {fornecedor}
Valor: R$ {valor:.2f}
Funcionário: {funcionario}
Cargo: {cargo}
--------------------------------
""")

        return duplicadas


    # ==========================================
    # TESTE 2 - OUTLIERS
    # ==========================================

    def TestTwo(self, Transacoes):

        media = Transacoes["Valor (R$)"].mean()
        desvio = Transacoes["Valor (R$)"].std()

        limite_superior = media + (2 * desvio)

        outliers = Transacoes[
            Transacoes["Valor (R$)"] > limite_superior
        ]

        print("\n")
        print("=" * 70)
        print("              ANÁLISE DE VALORES FORA DO PADRÃO")
        print("=" * 70)

        print(f"Média das transações : R$ {media:,.2f}")
        print(f"Desvio padrão        : R$ {desvio:,.2f}")
        print(f"Limite superior      : R$ {limite_superior:,.2f}")
        print(f"Outliers encontrados : {len(outliers)}")

        print("=" * 70)

        if outliers.empty:
            print("Nenhuma transação fora do padrão foi encontrada.")
            print("=" * 70)
            return outliers

        print("\nTRANSAÇÕES ACIMA DO PADRÃO")
        print("-" * 70)

        for indice, transacao in outliers.iterrows():

            print(f"ID            : {transacao['ID']}")
            print(f"Data          : {transacao['Data']}")
            print(f"Fornecedor    : {transacao['Fornecedor']}")
            print(f"Valor         : R$ {transacao['Valor (R$)']:,.2f}")
            print(f"Funcionário   : {transacao['Funcionario_Responsavel']}")
            print(f"Cargo         : {transacao['Cargo']}")

            print("-" * 70)

        print("=" * 70)

        return outliers


    # ==========================================
    # TESTE 3 - HORÁRIO IRREGULAR
    # ==========================================

    def TestTree(self, Transacoes):

        HORA_INICIO = 8
        HORA_FIM = 18

        dias_semana = {
            0: "Segunda-feira",
            1: "Terça-feira",
            2: "Quarta-feira",
            3: "Quinta-feira",
            4: "Sexta-feira",
            5: "Sábado",
            6: "Domingo"
        }

        irregulares = []

        for indice, transacao in Transacoes.iterrows():

            data = transacao["Data"]

            dia_semana = data.weekday()
            nome_dia = dias_semana[dia_semana]

            hora = data.hour

            fim_de_semana = dia_semana >= 5
            fora_do_horario = not (HORA_INICIO <= hora < HORA_FIM)

            if fim_de_semana or fora_do_horario:

                motivo = []

                if fim_de_semana:
                    motivo.append("Final de semana")

                if fora_do_horario:
                    motivo.append("Fora do horário comercial")

                irregulares.append(transacao)

                print(f"""
========================================
        LANÇAMENTO IRREGULAR
========================================
ID: {transacao["ID"]}
Data: {data} ({nome_dia})
Fornecedor: {transacao["Fornecedor"]}
Valor: R$ {transacao["Valor (R$)"]:.2f}
Funcionário: {transacao["Funcionario_Responsavel"]}
Cargo: {transacao["Cargo"]}
Motivo: {" / ".join(motivo)}
========================================
""")

        print(
            f"[TestTree] {len(irregulares)} lançamento(s) irregular(es)."
        )

        return pd.DataFrame(irregulares)


    # ==========================================
    # GRÁFICO 1 - TRANSAÇÕES DUPLICADAS
    # ==========================================

    def GraficoDuplicadas(self, Transacoes):

        duplicadas = Transacoes[
            Transacoes.duplicated(
                subset=["Fornecedor", "Valor (R$)", "Data"],
                keep=False
            )
        ]

        quantidade_duplicadas = len(duplicadas)
        quantidade_normais = len(Transacoes) - quantidade_duplicadas

        plt.figure(figsize=(8, 5))

        plt.bar(
            ["Normais", "Duplicadas"],
            [quantidade_normais, quantidade_duplicadas]
        )

        plt.title("Transações Duplicadas")
        plt.xlabel("Tipo de Transação")
        plt.ylabel("Quantidade")

        plt.tight_layout()
        plt.show()


    # ==========================================
    # GRÁFICO 2 - OUTLIERS
    # ==========================================

    def GraficoOutliers(self, Transacoes):

        media = Transacoes["Valor (R$)"].mean()
        desvio = Transacoes["Valor (R$)"].std()

        limite_superior = media + (2 * desvio)

        outliers = Transacoes[
            Transacoes["Valor (R$)"] > limite_superior
        ]

        normais = Transacoes[
            Transacoes["Valor (R$)"] <= limite_superior
        ]

        plt.figure(figsize=(8, 5))

        plt.bar(
            ["Normais", "Outliers"],
            [len(normais), len(outliers)]
        )

        plt.title("Transações Fora do Padrão")
        plt.xlabel("Tipo de Transação")
        plt.ylabel("Quantidade")

        plt.tight_layout()
        plt.show()


    # ==========================================
    # GRÁFICO 3 - HORÁRIO DAS TRANSAÇÕES
    # ==========================================

    def GraficoIrregularidades(self, Transacoes):

        HORA_INICIO = 8
        HORA_FIM = 18

        dentro_horario = 0
        fora_horario = 0
        fim_semana = 0

        for indice, transacao in Transacoes.iterrows():

            data = transacao["Data"]

            dia_semana = data.weekday()
            hora = data.hour

            if dia_semana >= 5:

                fim_semana += 1

            elif not (HORA_INICIO <= hora < HORA_FIM):

                fora_horario += 1

            else:

                dentro_horario += 1

        plt.figure(figsize=(8, 5))

        plt.bar(
            [
                "Dentro do horário",
                "Fora do horário",
                "Fim de semana"
            ],
            [
                dentro_horario,
                fora_horario,
                fim_semana
            ]
        )

        plt.title("Análise de Horário das Transações")
        plt.xlabel("Classificação")
        plt.ylabel("Quantidade")

        plt.xticks(rotation=15)

        plt.tight_layout()
        plt.show()


    # ==========================================
    # PROCESSAR TODOS OS DADOS
    # ==========================================

    def ProcessarDados(self, Transacoes):

        self.TestOne(Transacoes)

        self.TestTwo(Transacoes)

        self.TestTree(Transacoes)

        print("\nGerando gráficos...")

        self.GraficoDuplicadas(Transacoes)

        self.GraficoOutliers(Transacoes)

        self.GraficoIrregularidades(Transacoes)


    # ==========================================
    # CARREGAR EXCEL
    # ==========================================

    def GerarDatasFrames(self):

        arquivo = "transacoes-auditoria.xlsx"

        auditoria = Auditoria(arquivo)

        Transacoes = auditoria.obter_dataframe("Transacoes")

        CargosELimites = auditoria.obter_dataframe(
            "Cargos_e_Limites"
        )

        return Transacoes, CargosELimites


# ==============================================
# EXECUÇÃO
# ==============================================

if __name__ == "__main__":

    principal = Principal()

    Transacoes, CargosELimites = principal.GerarDatasFrames()

    principal.ProcessarDados(Transacoes)