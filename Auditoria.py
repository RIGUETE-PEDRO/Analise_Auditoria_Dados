import pandas as pd


class Auditoria:

    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.abas = pd.read_excel(arquivo, sheet_name=None)

    def listar_abas(self):
        return list(self.abas.keys())

    def obter_dataframe(self, nome_aba):
        return self.abas[nome_aba]