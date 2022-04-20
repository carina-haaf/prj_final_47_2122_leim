# prj_final_47_2122_leim
Projeto #47: Anotação de Eventos Sonoros em Vídeo



Em geral a evolução, de um atleta (amador ou profissional), numa qualquer modalidade desportiva
pressupõe a análise do seu desempenho no decurso dos jogos (e.g., treinos, competições) em que
participa. Essa análise deve basear-se numa perspetiva exterior à do próprio jogo. Por exemplo, o
treinador não participa no jogo e esta perspetiva externa (aliada ao seu conhecimento) permite-lhe
analisar o desempenho dos atletas e assim orientar a sua evolução.
Esta perspetiva externa pode ser registada em vídeo e analisada com detalhe em momento posterior.
Este registo em vídeo e análise à-posteriori é essencial para a competição profissional e especialmente
interessante para o atleta amador que possivelmente não terá um treinador a assistir aos seus jogos. É
também muito provável que o treinador de um atleta amador nem sequer tenha disponibilidade para
visionar na íntegra (e comentar) os vídeos dos vários jogadores que acompanha.
Neste contexto surge a necessidade de uma ferramenta que apoie a extração (e análise) de "eventos
relevantes" registados em vídeo. Esses "eventos relevantes" são muitas vezes identificáveis pelo áudio
que integra o próprio vídeo. Como exemplo de "evento relevante", podemos considerar o som emitido
pelo impacto da bola numa raquete, ou no chão, em competições do tipo ténis (ou padel). A extração
(semi)automática destes eventos permite construir vários indicadores (e.g., períodos com maior ou
menor troca de bolas) e apoiar também a construção de vídeos-de-síntese (e.g., os pontos mais longos).
Como primeira abordagem, pretende usar-se o áudio registado em vídeos de competições desportivas
para extrair "eventos relevantes" e com eles construir indicadores úteis para um atleta. O objetivo é
fazer-se um processamento "offline" e produzir, por exemplo, uma "timeline" (tipo histograma) que
apresente os períodos de tempo com trocas consecutivas de bola (e.g., num jogo de padel) e a
quantidade dessas trocas em cada um desses períodos.
Os blocos essenciais do sistema são:

- câmara de vídeo (disponibilizada)
- sistema de gestão de conteúdos (e.g., Django, baseado em Python),
- algoritmos de software de deteção do som,
- algoritmos de software de inteligência artificial.


Trabalho realizado por:
- Carina Fernandes


Orientadores:
- Joel Paulo
- Paulo Trigo
- Paulo Vieira


