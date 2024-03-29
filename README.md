# PacMan

Esse projeto foi desenvolvido durante a disciplina de Inteligência Artificial. (Outubro/2023)

# Objetivo

O objetivo do projeto era desenvolver uma réplica do jogo original do Pac-Man implementando algoritmos de aprendizagem de máquina para controlar os fantasmas e dificultar o jogo. Alguns algoritmos utilizados foram o A* e o Método Guloso.

# Execução

Para executar o jogo, baixe todos os arquivos e mantenha-os no mesmo diretório, é necessário ter Python e a biblioteca Pygame instalados para poder executar o projeto, com tudo preparado, apenas execute o arquivo pacman.py

# Conclusão

Por diversos motivos, o desenvolvimento desse projeto passou por alguns problemas que dificultaram sua execução, por isso, pode se notar alguns problemas, como o funcionamento da movimentação do jogador e dos fantasmas, uma vez que o mapa foi planejado de uma maneira que os fantasmas tentam traçar sua rota o tempo todo, e não apenas quando uma nova possibilidade de direção existe, problema esse que seria facilmente resolvido com a utilização de "nós", onde o algoritmo de aprendizagem de máquina seria executado para encontrar o novo destino do fantasma, apenas quando ele pudesse de fato mudar de direção, deixando o jogo mais fluído. Além disso, o Pacman pode acabar entrando no meio das paredes devido a como as coordenadas foram tratadas no desenvolvimento, outro problema que seria resolvido com a utilização do mapa em "nós". O mapa em nós seria basicamente identificado como um grafo
