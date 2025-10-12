## TPC 3 — Analisador Léxico de Queries SPARQL
###  Enunciado

Desenvolver um pequeno analisador léxico (tokenizer) em Python que reconheça os principais tokens de queries SPARQL. O analisador deve identificar e classificar os elementos básicos da linguagem, permitindo uma análise estrutural da query.

**O programa deve reconhecer os seguintes elementos:**

- **Palavras-chave:** `SELECT, WHERE, PREFIX, OPTIONAL, FILTER`<br>
Ex: `SELECT ?a ?b ?c` → `[('SELECT', 'SELECT', 0, (0, 6)), ('VAR', '?a', 0, (7, 9)), ...]`

- **Variáveis:** iniciadas por `?`<br>
Ex: `?a` → `('VAR', '?a', linha, (start, end))`

- **Identificadores:** iniciados por `:`<br>
Ex: `:Pessoa` → `('IDENT', ':Pessoa', linha, (start, end))`

- **URIs:** delimitadas por `< >`<br>
Ex: `<http://exemplo.org>` → `('URI', '<http://exemplo.org>', linha, (start, end))`

- **Literais de texto:** delimitados por aspas `" "`<br>
Ex: `"texto"` → `('STRING', '"texto"', linha, (start, end))`

- **Operadores:** `=, !=, <, >`<br>
Ex: `?a = ?b` → `('VAR', '?a', ...), ('OP', '=', ...), ('VAR', '?b', ...)`

- **Pontuação:** `{, }, ., ;, ,`<br>
Ex: `{ ?a :temIdade ?b . }` → `('PUNCT', '{', ...), ('PUNCT', '.', ...), ('PUNCT', '}', ...)`

- **Quebras de linha:** `\n`<br>
Ex: cada nova linha incrementa o contador de linha.

- **Erro:** qualquer caractere não reconhecido é classificado como `ERRO`.

### Exemplo de Entrada
```
SELECT ?a ?b ?c WHERE {
  ?a a :Pessoa ;
  :temIdade ?b ;
  :eIrmaoDe ?c .
}
```

### Resolução

- [TPC 3 — Analisador Léxico de Queries](tpc3.ipynb)
