import os
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

arquivo = os.path.join('data\prouni_database2020.csv')
database = np.loadtxt(arquivo, delimiter = ";", dtype= str, skiprows=1)


'''Funções comuns'''

def indexacao(i):
  return np.unique(database[:,i], return_counts=True)

def criarMatriz(tipo, ocorrencia):
  return np.column_stack((tipo,ocorrencia))

def idadeAluno(entrada):
  data_atual = datetime.now()
  data_nascimento = datetime.strptime(entrada, "%d/%m/%Y")
  diferenca = data_atual - data_nascimento
  return diferenca.days // 365

def conversorTxt(text, nArray): 
  titulo = text
  for i in range(len(nArray)):
    conteudo = f"\n{nArray[i,0]} - {nArray[i,1]}"
    titulo += conteudo
  return titulo    


'''indicativos'''

# Qtde bolsas por UF ------
uf, ocorrenciaUf = indexacao(15)
bolsasUf = criarMatriz(uf, ocorrenciaUf)

# Qtde bolsas por região ------
regiao, ocorrenciRegiao = indexacao(14)
bolsasRegiao = criarMatriz(regiao, ocorrenciRegiao)

# Qtde tipo de bolsa (EAD / PRESENCIAL) ------
tipo, ocorrenciaBolsa = indexacao(6)
tipoBolsa = criarMatriz(tipo, ocorrenciaBolsa)

# Quantidade / sexo ------
sexo, ocorrenciaS = indexacao(10)
sexoMatriz = criarMatriz(sexo, ocorrenciaS)

# Cursos ofertados ------
curso, ocorrenciaCurso = indexacao(7)
cursos = criarMatriz(curso, ocorrenciaCurso)
np.sort(cursos)
topCursos = cursos[cursos[:,1].astype(int)>8500] #Verificando cursos com maiores inscrições

# Bolsas para PPD ------
ppd, ocorrenciaPpd = indexacao(13)
ppdMatriz = criarMatriz(ppd, ocorrenciaPpd)

# Bolsas integrais ou parciais ------
bolsa, ocorrenciaB = indexacao(5)
bolsaIntegral = criarMatriz(bolsa, ocorrenciaB)

# Quantidade por raça ------
raca, ocorrenciaRaca = indexacao(11)
racaMatriz = criarMatriz(raca, ocorrenciaRaca)

#Qtde por idade de aluno ------
dateNascimento, ocorrenciaD = indexacao(12)
dateMatriz = criarMatriz(dateNascimento, ocorrenciaD)
# Encontrando a idade para cada ano de nascimento:
for i in range(len(dateMatriz)):
  dateMatriz[i,0] = idadeAluno(dateMatriz[i,0])


''' GRÁFICOS '''

# Bolsas por gênero - PIZZA
generos = sexoMatriz[:, 0]
valores = sexoMatriz[:, 1].astype(int)
plt.pie(valores, labels=generos, autopct='%1.1f%%', colors= ['grey','orange'])
plt.title('Distribuição por Gênero')
plt.axis('equal')
plt.show()

# Bolsas integrais / Bolsas parciais - BARRAS
tipoBolsa = bolsaIntegral[:,0]
qtdeBolsa = bolsaIntegral[:,1].astype(int)
limiteBarra = np.arange(len(tipoBolsa))
plt.bar(limiteBarra, qtdeBolsa, color = ['grey','orange'])
plt.xticks(limiteBarra, tipoBolsa)
plt.xlabel('Categoria da bolsa PROUNI')
plt.ylabel('Quantidade ofertada')
plt.show()

# Bolsas por etnia/raça
nomeRaca = racaMatriz[:,0]
qtdRaca = racaMatriz[:,1].astype(int)
limiteBarra = np.arange(len(nomeRaca))
plt.bar(limiteBarra, qtdRaca, color = ['grey','orange'])
plt.xticks(limiteBarra, nomeRaca)
plt.xlabel('Raça / Etnia')
plt.ylabel('Quantidade ofertada')
plt.show()

# Bolsas por PPD - PIZZA
portador = ppdMatriz[:, 0]
valores = ppdMatriz[:, 1].astype(int)
plt.pie(valores, labels=portador, autopct='%1.1f%%', colors= ['grey','orange'])
plt.title('Distribuição para deficientes físicos')
plt.axis('equal')
plt.show()


''' RELATÓRIO FINAL '''

with open('report\prouni2020_relatorio.txt', 'w') as arquivo:
  arquivo.write("\n\t\tRelatório PROUNI/2020")

with open('report\prouni2020_relatorio.txt', 'a') as arquivo:
  def e(text):
    arquivo.write(text)

  e(f"\n\tQuantidade de vagas ofertadas = {database.shape[0]} bolsas\n\n")

  e(f"\n\t\tBolsas separadas por UF:\
    \n{conversorTxt('Bolsas/UF:', bolsasUf)}\n\n")
  
  e(f"\n\t\tBolsas separadas por Região do país:\
    \n{conversorTxt('Bolsas/Região:',bolsasRegiao)}\n\n")
  
  e(f"\n\t\tDivisão de bolsa / sexo:\
    \n{conversorTxt('Feminino (F) - Masculino (M):', sexoMatriz)}\n\n")
  
  e(f"\n\t\tOs 5 cursos com maiores inscrições do PROUNI/2020:\
    \n{conversorTxt('Top 05:', topCursos)}\n\n")
  
  e(f"\n\t\tComparativo de vagas para PPD - PROUNI/2020:\
    \n{conversorTxt('Portador (S) / Não portador (N):', ppdMatriz)}\n\n")
  
  e(f"\n\t\tPanorama de bolsas integrais e parciais:\
    \n{conversorTxt('Comparativo bolsas integrais / parciais', bolsaIntegral)}\n\n")
  
  e(f"\n\t\tPanorama de bolsas por raça / etnia:\
    \n{conversorTxt('Bolsas por raça:', racaMatriz)}\n\n")
  
  # e(f"\n\t\tComparativo de bolsas por idade de aluno:\
  #   \n{conversorTxt('Quantidade bolsas / idade:', dateMatriz)}\n\n")  

  










