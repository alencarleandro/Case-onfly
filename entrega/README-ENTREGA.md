# Onfly — Entrega do case

## Investigação

Executei o CLI original com os dois CSVs de reservas e comparei a amostra com os valores do enunciado. A amostra retornou −33 noites e R$ 5.962,41, enquanto a execução da base completa registrou 200 das 300 reservas. Em seguida, rastreei os desvios na leitura do CSV, nas regras de negócio e na montagem do ranking.

## Defeitos corrigidos

| Defeito | Causa raiz | Correção |
| --- | --- | --- |
| Relatório incompleto | O leitor interrompia a iteração ao acumular 200 reservas. | Ler todas as linhas do CSV. |
| Faturamento indevido | O filtro excluía apenas `CANCELLED` e incluía `NO_SHOW` nos agregados. | Contar todos os status e agregar somente `CONFIRMED`. |
| Noites incorretas na virada de mês ou ano | O cálculo subtraía os números dos dias do mês e descartava mês e ano. | Subtrair as datas completas e multiplicar a diferença em dias pelo número de quartos. |
| Conversão cambial incorreta | A conversão dividia o valor pela taxa após transformar os operandos em `float`. | Multiplicar o valor pela taxa usando `Decimal` e arredondar na serialização. |
| Ranking invertido | A chave de ordenação classificava o total em ordem crescente. | Ordenar pelo total decrescente e desempatar pelo ID crescente. |

## Validação

Na raiz do projeto, com Python 3.11 ou superior, execute no PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check src tests

$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m onfly_report --input data/exemplo-validacao.csv --rates data/taxas_cambio.csv --output output/exemplo.json
.\.venv\Scripts\python.exe -m onfly_report --input data/reservas_hoteis.csv --rates data/taxas_cambio.csv
```

- **pytest 8.3.4 no Python 3.11.18 e 3.12.14** — `6 passed` em ambas as versões. Os cinco testes fornecidos passaram e o teste adicional cobre a leitura após a reserva 200.
- **CLI no Python 3.11.18** — os relatórios da amostra e da base completa coincidiram com os gerados no Python 3.12.14, exceto pelo horário de geração.
- **Ruff 0.8.4** — todas as verificações passaram.
- **Amostra** — o resumo, os totais por mês e o ranking coincidiram com o enunciado. Foram 12 reservas, 9 confirmadas, 28 noites e R$ 7.566,00, com diária média de R$ 270,21.
- **Base completa** — `output/report.json` registrou 300 reservas, 235 confirmadas, 31 canceladas, 34 não comparecimentos, 1.347 noites e R$ 396.170,00, com diária média de R$ 294,11.
- **Integridade** — os hashes dos arquivos originais de `data/` e `tests/` coincidiram antes e depois das alterações.
