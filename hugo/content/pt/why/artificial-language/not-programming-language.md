---
title: "Por que linguagens de programação não são suficientes"
weight: 10
date: 2026-02-26T12:00:19+09:00
lastmod: 2026-02-26T12:00:19+09:00
tags: ["linguagem de programação", "descrição", "representação do conhecimento"]
summary: "Linguagens de programação descrevem procedimentos. Não conseguem descrever o mundo. JSON oferece estrutura, mas não significado. Até LISP apenas empresta a sintaxe."
author: "Junwoo Park"
authorLink: "https://parkjunwoo.com/1/about"
image: "/images/og-default.webp"
---

## Linguagens de programação descrevem procedimentos. Não conseguem descrever o mundo.

---

## Linguagens de programação estão entre as maiores invenções da humanidade

Linguagens de programação são inequívocas.
`x = 3 + 4` resulta em 7, não importa quando ou onde seja executado.
Não há margem para interpretação.

Linguagens de programação são verificáveis.
Erros de sintaxe são detectados antes da compilação.
Erros de tipo são detectados antes da execução.
Quando os testes rodam, o resultado é ou aprovação ou falha.

Linguagens de programação são Turing-completas.
Podem expressar qualquer coisa que seja computável.
Com tempo e memória suficientes, qualquer procedimento pode ser descrito.

Tudo o que esta série identificou como limitações da linguagem natural — ambiguidade, impossibilidade de verificação, falta de estrutura — as linguagens de programação resolveram.

Então, por que não usar uma linguagem de programação para representar o contexto de uma IA?

Não funciona.

---

## Linguagens de programação descrevem procedimentos

O código Python a seguir é válido.

```python
def calculate_revenue(units_sold, unit_price):
    return units_sold * unit_price
```

Este código é claro, verificável e executável.
Mas o que ele expressa?

"Multiplique a quantidade vendida pelo preço unitário para obter a receita."

Isto é um procedimento. Um método. O COMO.
Descreve o que fazer quando a entrada chega.

Agora tente expressar o seguinte.

"A receita da Samsung Electronics no terceiro trimestre de 2024 foi de 79 trilhões de wons."

Isto não é um procedimento. É um fato. O QUÊ.
Nada é executado. Descreve o estado do mundo.

Como expressar isso em Python?

```python
samsung_revenue_2024_q3 = 79_000_000_000_000
```

Um número é atribuído a uma variável.
Funciona. Mas isto não é descrição. É armazenamento.
Este código não sabe:

- Que tipo de entidade é "Samsung Electronics".
- O que "receita" significa. É um indicador financeiro? Uma grandeza física?
- Se "Q3 2024" é um tempo, uma versão ou um rótulo.
- Qual é a fonte do valor de 79 trilhões de wons.
- Quão certo esse valor é.

O nome da variável `samsung_revenue_2024_q3` permite que um humano adivinhe o significado.
Para a máquina, é uma string arbitrária.
Renomeie para `xyzzy_42` e o resultado da execução será idêntico.

Em linguagens de programação, nomes de variáveis não carregam significado.
O significado vive fora do código, na cabeça do programador.

---

## Mais sofisticação não ajuda

E se criarmos uma classe?

```python
class FinancialReport:
    def __init__(self, company, metric, period, value, currency):
        self.company = company
        self.metric = metric
        self.period = period
        self.value = value
        self.currency = currency

report = FinancialReport("삼성전자", "매출", "2024-Q3", 79_000_000_000_000, "KRW")
```

Melhor. Há estrutura agora.
Mas os problemas permanecem.

`company` é a string "삼성전자" (Samsung Electronics).
"Samsung Electronics", "SEC" e "005930" se referem à mesma empresa.
O código sabe disso? Não.
Ele só pode comparar se as strings são iguais ou não.

`metric` é a string "매출" (receita).
"매출", "매출액" e "revenue" são a mesma coisa ou coisas diferentes?
O código não sabe. As strings são diferentes, então são coisas diferentes.

E se definirmos um schema?
Gerenciar a lista de empresas com Enums, gerenciar a lista de indicadores.
Claro. Funciona.

Então tente expressar o seguinte.

"Yi Sun-sin foi grandioso."

```python
opinion = Opinion("이순신", "was", "위대했다")
```

O que é isso?
Uma string "이순신" (Yi Sun-sin) vinculada a uma string "위대했다" (foi grandioso).
Isso não expressa "Yi Sun-sin foi grandioso".
Armazena "이순신" e "위대했다".

O código não conhece o significado de "위대했다" (foi grandioso).
Se "위대했다" (foi grandioso) e "훌륭했다" (foi admirável) são semelhantes,
se "비겁했다" (foi covarde) é o oposto —
o código não tem como saber.

Fatos estruturados como dados financeiros são razoavelmente gerenciáveis.
Avaliações, contexto, relações, descrições abstratas ficam além do alcance expressivo das linguagens de programação.

---

## O código não sabe o que faz

```python
def process(data):
    result = []
    for item in data:
        if item["value"] > threshold:
            result.append(transform(item))
    return result
```

Este código executa perfeitamente.
Mas o que ele faz?

Está filtrando dados de receita?
Selecionando registros de pacientes?
Limpando dados de sensores?

O código em si não sabe.
`data`, `value`, `threshold`, `transform` — todos nomes abstratos.
Se este código pertence a um sistema financeiro ou médico
depende de contexto fora do código.

Pode-se escrever comentários.
Mas comentários são linguagem natural. Máquinas não os entendem.
Se um comentário contradiz o código, o compilador não percebe.
Comentários são para humanos, não para máquinas.

Quando uma IA recebe código como contexto, esse problema se manifesta diretamente.
Como o código não tem autoidentidade,
a IA precisa reconstruir essa identidade por inferência toda vez.
Como é inferência, custa computação e pode errar.

---

## A razão fundamental

Que linguagens de programação não conseguem descrever o mundo não é uma falha de design.
O propósito é diferente.

O propósito de uma linguagem de programação é instruir a máquina sobre procedimentos.
"Quando esta entrada chegar, execute esta operação."
A semântica de uma linguagem de programação é a semântica da execução.
Cada construção é interpretada como "o que a máquina faz".

`x = 3` é a instrução "armazene 3 no local de memória chamado x".
`if x > 0` é a instrução "se x for maior que 0, execute o próximo bloco".
`return x` é a instrução "retorne o valor de x para o chamador".

Tudo verbos. Tudo ações. Tudo procedimentos.

"Samsung Electronics é uma empresa coreana" não é um verbo.
Não é uma ação. Não é um procedimento.
Descreve o estado em que o mundo se encontra.

Linguagens de programação não têm lugar para isso.
Pode-se armazenar em uma variável, mas isso é armazenamento, não descrição.
O significado do valor armazenado não é da alçada do código.

---

## E JSON, YAML, XML?

Se não linguagens de programação, e os formatos de dados?

```json
{
  "company": "삼성전자",
  "metric": "매출",
  "period": "2024-Q3",
  "value": 79000000000000,
  "currency": "KRW"
}
```

Há estrutura. Os campos são explícitos.
Mas não há significado.

Se "company" significa uma corporação, JSON não sabe.
Se "삼성전자" é o mesmo que "Samsung Electronics" em outro lugar, JSON não sabe.
Se este objeto JSON e aquele objeto JSON descrevem a mesma entidade, JSON não sabe.

JSON fornece estrutura, mas não significado.
São pares chave-valor, não entidade-relacionamento-atributo.

Definir schemas ajuda.
JSON Schema, Protocol Buffers, GraphQL.
Tipos de campo são definidos, obrigatoriedade é definida, referências são definidas.

Mas todos esses são estruturas projetadas para sistemas específicos.
Não são representação de conhecimento de uso geral.
Um schema de dados financeiros não consegue expressar a avaliação de uma figura histórica.
Um schema de dados médicos não consegue expressar relações competitivas entre empresas.

Um schema separado para cada domínio.
Uma ferramenta separada para cada schema.
Nenhuma interoperabilidade entre schemas.

Essa limitação é discutida em mais detalhe em [Por que MD/JSON/XML não funcionam](/pt/why/not-md-json-xml/).

---

## E LISP?

Alguns leitores podem ter pensado em um contraexemplo.

LISP.

```lisp
(is 삼성전자 (company korea))
(revenue 삼성전자 2024-Q3 79000000000000)
(great 이순신)
```

S-expressions são estruturas de árvore,
e código é dados e dados são código.
Homoiconicidade (homoiconicity).

Na verdade, a IA primitiva era inteiramente baseada em LISP.
SHRDLU, CYC, sistemas especialistas.
O conhecimento era representado em LISP e os motores de inferência rodavam sobre ele.
Parece uma contraprova histórica de que "linguagens de programação não conseguem descrever o mundo".

Mas o contraexemplo falha por três razões.

### O que LISP sabe versus o que o programador decidiu

Em `(is 삼성전자 company)`, LISP não sabe
que `is` significa a relação "é um".
O programador é que decidiu isso.

Substitua `is` por `zzz` e LISP não se importa.
`(zzz 삼성전자 company)` é uma expressão perfeitamente válida para LISP.

LISP fornece estrutura. Uma árvore chamada S-expression.
Mas o significado dentro dessa estrutura foi atribuído pelo programador, não pela linguagem.
Isso é fundamentalmente o mesmo que JSON não conhecer o significado de suas chaves.

Fornecer estrutura e incorporar significado são coisas diferentes.

### Os 30 anos do CYC

A tentativa mais ambiciosa foi o CYC.

Iniciado em 1984.
Tentou representar conhecimento geral usando LISP.
Milhões de regras foram inseridas manualmente.

O que 30 anos provaram não foi a viabilidade, mas as limitações.

Ontologias tinham que ser projetadas manualmente para cada domínio.
A interoperabilidade entre domínios não funcionava.
Não conseguia acompanhar a flexibilidade da linguagem natural.
À medida que a escala crescia, manter a consistência tornava-se quase impossível.

Que a representação do conhecimento "pode ser feita" em LISP é verdade.
Que "funciona bem" é o que 30 anos de resultados refutam.

### Se você não vai usar eval, não há razão para usar LISP

O problema mais fundamental.

O poder de LISP é o `eval`.
Como código é dados, dados podem ser executados.
Metaprogramação, macros, geração de código em tempo de execução.
Isso é o que faz LISP ser LISP.

Mas o que acontece quando você faz `eval` de `(is 삼성전자 company)`?

Vira uma chamada de função passando `삼성전자` e `company` como argumentos para uma função chamada `is`.
Não descrição — execução.

Para usar como representação de conhecimento, não se deve avaliar.
Se não vai avaliar, não está usando a semântica de LISP.
Está apenas emprestando a sintaxe das S-expressions.

Isso não é "descrever o mundo em LISP".
É "armazenar dados usando a notação de parênteses de LISP".

A semântica de LISP como linguagem de programação — a semântica da execução —
continua projetada para descrever procedimentos.
Emprestar a sintaxe não muda a semântica.

---

## O que uma linguagem para descrever o mundo precisa

Linguagens de programação descrevem procedimentos.
Formatos de dados fornecem estrutura, mas não significado.
Até LISP apenas empresta sintaxe sem a semântica da descrição.

O que uma linguagem para descrever o mundo precisa?

**Identidade de entidade.** "Samsung Electronics" deve ter um identificador único. A máquina deve saber que é o mesmo que "삼성전자". Não comparação de strings, mas equivalência de identidade.

**Expressão de relacionamentos.** Em "Samsung Electronics é uma empresa coreana", deve ser possível expressar o relacionamento "empresa coreana". Não atribuição de variáveis, mas descrição de relacionamentos.

**Descrições autocontidas.** Sobre o que a descrição trata, quem a disse, a partir de quando, e quão certa é — tudo deve estar incluído na própria descrição. Dentro do código, não fora.

**Independência de domínio.** Dados financeiros, fatos históricos, avaliações subjetivas, relações abstratas — tudo deve ser expressável no mesmo formato. Não um schema separado para cada domínio, mas uma estrutura universal.

Linguagens de programação não possuem nenhuma dessas quatro propriedades.
Porque linguagens de programação não foram construídas para isso.
Foram construídas para descrever procedimentos.

A linguagem natural pode fazer as quatro coisas. De forma ambígua.
O que se precisa é a combinação do alcance expressivo da linguagem natural com a precisão das linguagens de programação.

---

## Resumo

Linguagens de programação são inequívocas, verificáveis e Turing-completas.
Mas não conseguem descrever o mundo.

Linguagens de programação descrevem procedimentos.
"Quando esta entrada chegar, faça isto." Tudo verbos, tudo ações.
"Samsung Electronics é uma empresa coreana" não é uma ação.
Linguagens de programação não têm lugar para isso.

O código não conhece sua própria identidade.
A que domínio pertence, que propósito serve —
nada disso está registrado dentro do código.

Formatos de dados como JSON e YAML fornecem estrutura, mas não significado.
LISP pode emprestar sintaxe, mas não tem semântica de descrição.
O CYC passou 30 anos tentando representação de conhecimento baseada em LISP, e o que provou foi a limitação.

Descrever o mundo requer identidade de entidade, expressão de relacionamentos, descrições autocontidas e independência de domínio.
Linguagens de programação não foram construídas para isso.
A linguagem natural consegue, mas de forma ambígua.
O que se precisa está em algum lugar entre os dois.
