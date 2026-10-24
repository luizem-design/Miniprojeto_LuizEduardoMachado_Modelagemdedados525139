import pandas as pd

# Importação da base de dados
# Dica: se houver erro de caracteres estranhos nos nomes dos produtos, adicione encoding="latin1" após o sep=";"
df = pd.read_csv("Base Varejo.csv", sep=";")

# Informações gerais sobre o DataFrame (descomentado para exibir no terminal)
print("Números de registros:", df.shape[0])
print("Números de colunas:", df.shape[1])
print("\nColunas:")
print(df.columns.tolist())
print("\nTipos de dados:")
print(df.dtypes)
print("\nPrimeiras linhas:")
print(df.head())

# Análise dos dados
print("\nValores nulos por coluna:")
print(df.isna().sum())
print("\nValores duplicados:")
print(df.duplicated().sum())

colunas_texto = df.select_dtypes(include='object').columns

for coluna in colunas_texto:
    vazios = df[coluna].isna().sum()
    print(f"{coluna}: {vazios}")

datas_convertidas = pd.to_datetime(df["DATA"], format="%d/%m/%Y", errors="coerce")
datas_invalidas = df["DATA"][datas_convertidas.isna()].tolist()
print("\nDatas inválidas:")
print(len(datas_invalidas))

df_limpo = df.copy()

# Removendo colunas com valores nulos (ex: as 'Unnamed' que vieram na exportação)
colunas_vazias = df_limpo.columns[df_limpo.isna().any()].tolist()
df_limpo = df_limpo.drop(columns=colunas_vazias)

print("Colunas removidas:", colunas_vazias)

# Ajuste do tipo de dados da coluna DATA
df_limpo["DATA"] = pd.to_datetime(df_limpo["DATA"], format="%d/%m/%Y", errors="raise")

print("\nTipos após limpeza:")
print(df_limpo.dtypes)
print(df_limpo.shape)

# Linhas totalmente idênticas em todos os campos são duplicações, então vamos removê-las
registros_antes = len(df_limpo)

# Mantêm a primeira e remove as demais iguais
df_limpo = df_limpo.drop_duplicates().reset_index(drop=True)

# CORREÇÃO: Cálculo correto dos registros removidos
registros_removidos = registros_antes - len(df_limpo)

print("\n______RESULTADO DA LIMPEZA_______")
print("Registros removidos:", registros_removidos)
print("Registros restantes:", len(df_limpo))
print("Colunas restantes:", df_limpo.shape[1])
print("Duplicatas restantes:", df_limpo.duplicated().sum())


# ==========================================
# ETAPA 4: Estatísticas descritivas (CL_FHL)
# ==========================================
print("\n--- 4. ESTATÍSTICAS DESCRITIVAS: NÚMERO DE FILHOS (CL_FHL) ---")
print(f"Contagem: {df_limpo['CL_FHL'].count()}")
print(f"Média: {df_limpo['CL_FHL'].mean():.2f}")
print(f"Mediana: {df_limpo['CL_FHL'].median()}")
print(f"Desvio Padrão: {df_limpo['CL_FHL'].std():.2f}")
print(f"Moda: {df_limpo['CL_FHL'].mode()[0]}")
print(f"Máximo: {df_limpo['CL_FHL'].max()}")
print(f"Mínimo: {df_limpo['CL_FHL'].min()}")


# ==========================================
# ETAPA 5: Padrões de Agrupamento
# ==========================================
print("\n--- 5. PADRÕES DE AGRUPAMENTO ---")

# Agrupamento 1: Quantidade de produtos comprados por Gênero
compras_por_genero = df_limpo.groupby('CL_GENERO')['PR_ID'].count().reset_index(name='Qtd_Produtos')
compras_por_genero = compras_por_genero.sort_values(by='Qtd_Produtos', ascending=False)
print("Produtos Comprados por Gênero:")
print(compras_por_genero)

# Agrupamento 2: Top 5 Categorias de produtos mais vendidas
vendas_por_categoria = df_limpo['PR_CAT'].value_counts().reset_index()
vendas_por_categoria.columns = ['Categoria', 'Qtd_Vendas']
print("\nTop 5 Categorias de Produtos Mais Vendidas:")
print(vendas_por_categoria.head())


# ==========================================
# ETAPA 6: Conclusões
# ==========================================
print("\n--- 6. CONCLUSÕES ---")
print("- A base possuía colunas vazias residuais (prováveis erros de exportação), que foram removidas dinamicamente ao mapear valores nulos.")
print("- A conversão da coluna DATA para datetime foi bem-sucedida, não havendo resíduos de formatos de data corrompidos, o que viabiliza análises temporais.")
print("- As estatísticas da coluna CL_FHL ajudam a traçar o perfil demográfico, mostrando a média de dependentes dos clientes para futuras campanhas direcionadas.")
print("- A base precisou passar por deduplicação estrita, garantindo que compras idênticas lançadas em duplicidade não inflem os resultados dos agrupamentos.")