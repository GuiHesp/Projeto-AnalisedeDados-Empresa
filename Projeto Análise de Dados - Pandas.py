#!/usr/bin/env python
# coding: utf-8

# # Exercício - Mini Projeto de Análise de Dados
# 
# Vamos fazer um exercício completo de pandas para um miniprojeto de análise de dados.
# 
# Esse exercício vai obrigar a gente a usar boa parte dos conhecimento de pandas e até de outros módulos que já aprendemos ao longo do curso.
# 
# ### O que temos?
# 
# Temos os dados de 2019 de uma empresa de prestação de serviços. 
# 
# - CadastroFuncionarios
# - CadastroClientes
# - BaseServiçosPrestados
# 
# Obs1: Para ler arquivos csv, temos o read_csv<br>
# Obs2: Para ler arquivos xlsx (arquivos em excel normais, que não são padrão csv), temos o read_excel
# 
# ### O que queremos saber/fazer?
# 
# 1. Valor Total da Folha Salarial -> Qual foi o gasto total com salários de funcionários pela empresa? <br>
#     Sugestão: calcule o salário total de cada funcionário, salário + benefícios + impostos, depois some todos os salários
#     
#     
# 2. Qual foi o faturamento da empresa?<br>
#     Sugestão: calcule o faturamento total de cada serviço e depois some o faturamento de todos
#     
#     
# 3. Qual o % de funcionários que já fechou algum contrato?<br>
#     Sugestão: na base de serviços temos o funcionário que fechou cada serviço. Mas nem todos os funcionários que a empresa tem já fecharam algum serviço.<br>
#     . Na base de funcionários temos uma lista com todos os funcionários<br>
#     . Queremos calcular Qtde_Funcionarios_Fecharam_Serviço / Qtde_Funcionários_Totais<br>
#     . Para calcular a qtde de funcionários que fecharam algum serviço, use a base de serviços e conte quantos funcionários tem ali. Mas lembre-se, cada funcionário só pode ser contado uma única vez.<br><br>
#     Dica: se você aplicar o método .unique() em uma variável que é apenas 1 coluna de um dataframe, ele vai excluir todos os valores duplicados daquela coluna.<br>
#     Ex: unicos_colunaA = dataframe['colunaA'].unique() te dá como resposta uma lista com todos os itens da colunaA aparecendo uma única vez. Todos os valores repetidos da colunaA são excluidos da variável unicos_colunaA 
#     
#     
# 4. Calcule o total de contratos que cada área da empresa já fechou
# 
# 
# 5. Calcule o total de funcionários por área
# 
# 
# 6. Qual o ticket médio mensal (faturamento médio mensal) dos contratos?<br>
#     Dica: .mean() calcula a média -> exemplo: media_colunaA = dataframe['colunaA'].mean()
# 
# Obs: Lembrando as opções mais usuais de encoding:<br>
# encoding='latin1', encoding='ISO-8859-1', encoding='utf-8' ou então encoding='cp1252'
# 
# Observação Importante: Se o seu código der um erro na hora de importar os arquivos:<br>
# - CadastroClientes.csv
# - CadastroFuncionarios.csv
# 
# Use separador ";" (ponto e vírgula) para resolver

# ### IMPORTANDO 

# In[2]:


#1.
import pandas as pd
funcionarios_df = pd.read_csv('--CadastroFuncionarios.csv', sep=';', decimal=',')
clientes_df = pd.read_csv('--CadastroClientes.csv', sep=';', decimal=',')
servicos_df = pd.read_excel('--BaseServiçosPrestados.xlsx')

#retirar colunas Estado Civil e Cargo da tabela funcionarios:
funcionarios_df = funcionarios_df.drop(['Estado Civil', 'Cargo'], axis=1)

display(funcionarios_df)
display(clientes_df)
display(servicos_df)
    
        


# ### Primeiro Exercício: Folha Salarial

# In[3]:


funcionarios_df['Salario Total'] = funcionarios_df['Salario Base'] + funcionarios_df['Impostos'] + funcionarios_df['Beneficios'] + funcionarios_df['VT'] + funcionarios_df['VR']
print('Total da Folha Salarial é de: R${:,.2f}'.format(funcionarios_df['Salario Total'].sum()))


# ### Segundo Exercício: Qual foi o faturamento da empresa?

# In[4]:


faturamentos_df = servicos_df[['ID Cliente', 'Tempo Total de Contrato (Meses)']].merge(clientes_df[['ID Cliente', 'Valor Contrato Mensal']], on='ID Cliente')
#display(faturamentos_df)

faturamentos_df['Faturamento Empresa'] = faturamentos_df['Tempo Total de Contrato (Meses)'] * faturamentos_df['Valor Contrato Mensal']
print('Faturamento da Empresa foi de R${:,.2f}'.format(faturamentos_df['Faturamento Empresa'].sum()))


# ### Terceiro Exercício: Qual o % de funcionários que já fechou algum contrato?

# In[13]:


funcionarios_fecharam_contrato_df = servicos_df['ID Funcionário'].unique()
#display(len(funcionarios_fecharam_contrato_df))
porcentagem_funcionarios = len(funcionarios_fecharam_contrato_df) / len(funcionarios_df['ID Funcionário'])
print('A porcentagem de funcionários que já fechou um contrato é de {:.2%}'.format(porcentagem_funcionarios))


# ### Quarto Exercício: Calcule o total de contratos que cada área da empresa já fechou

# In[37]:


contratos_area_df = servicos_df[['ID Funcionário']].merge(funcionarios_df[['ID Funcionário', 'Area']], on='ID Funcionário')
contratos_area_qtde = contratos_area_df['Area'].value_counts()
print(contratos_area_qtde)
contratos_area_qtde.plot(kind='bar')


# ### 5. Calcule o total de funcionários por área

# In[38]:


funcionario_area = funcionarios_df['Area'].value_counts()
print(funcionario_area)
funcionario_area.plot(kind='bar')


# ### 6. Qual o ticket médio mensal (faturamento médio mensal) dos contratos?

# In[43]:


ticket_medio_mensal = clientes_df['Valor Contrato Mensal'].mean()
print('Ticket médio mensal dos contratos: R$ {:,.2f} reais.'.format(ticket_medio_mensal))

