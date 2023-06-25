## Flood-It AI SOLVER
Criado por Bruna Miranda e David Vinicius para a disciplina CI1209 - Inteligência Artificial - 2023-1 da UFPR

- Baseado no projeto: https://github.com/LeanMilk/Flood-It
- Binários produzidos por Fabiano Silva

### Heurística utilizada
Neste projeto utilizamos as seguintes heuristicas:

Inicialmente ao ler o arquivo do tabuleiro foi mapeado quais os grupos onde existem cores adjagentes, por essas cores usamos as seguintes heuristica:

Heuristica no passo 1 - Escolhemos todas as cores da linha x ( ou seja do sentido canto superior esquerdo (A) -> canto superior direito (B) ) até a metade da quantidade de colunas do tabuleiro, partindo o y0 

Heuristica no passo 2 - Escolhemos todas as cores da linha y ( ou seja do sentido A -> canto inferior esquerdo (D) ) até a metade da quantidade de linhas do tabuleiro

Heuristica no passo 3 - Escolhemos todas as cores da linha x ( ou seja do sentido A -> B) até a 1/3 da quantidade de colunas do tabuleiro, partindo da posição atual do y 

Heuristica no passo 4 - Escolhemos todas as cores da linha y ( ou seja do sentido A -> D) até a metade da quantidade de linhas do tabuleiro, partindo da posição atual do x 

Heuristica no passo 5 - Escolhemos a cor da posição que está mais perto do canto inferior direito (C) e intercalamos com a busca gulosa da cor mais frequente.

### Para rodar 
```
python floodit.py < exemplo_mapa_10_10_4.txt > solucao.txt
```

###### Verificando solução 
```
cat exemplo_mapa_10_10_4.txt solucao.txt | ./anima
```

### Verifica solução sem mapa
```
programa para verificar se um determinado mapa é resolvido por uma determinada sequencia de cores, retornando 0 
se sim e 1 caso contrário, exemplo de uso:
    $ cat exemplo_mapa_30_30_10.txt exemplo_solucao_30_30_10.txt | ./verifica
para pegar o resultado no bash:
    if [ "$?" -eq 0 ]
      then
        echo ok
      else
        echo fail
    fi
```

### Gera mapa
```
./geramapa <numero_de_linhas> <numero_de_colunas> <numero_de_cores>
```

