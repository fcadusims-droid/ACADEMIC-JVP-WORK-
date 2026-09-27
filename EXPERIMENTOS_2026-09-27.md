# Experimentos para rodar em casa — 27/09/2026

Todos usam só computador e dados públicos (PhysioNet), sem laboratório nem outra pessoa. Cada um preenche um espaço `[RESULT …]` de um dos três papers. Os critérios abaixo são os mesmos que já estão escritos nos papers e não podem mudar depois que você ver os dados.

## E0 — Registre antes de rodar (faça primeiro)

1. Comite e dê push dos três papers novos e deste arquivo no repositório, **sem nenhum resultado**.
2. Crie uma release no GitHub e arquive no Zenodo pela integração GitHub–Zenodo (gratuita), ou registre no OSF. Isso gera data e DOI externos, e os critérios passam a ter uma anterioridade verificável.
3. Só então rode os experimentos. Se precisar mudar algum parâmetro depois de começar, registre a mudança como desvio, com o motivo, antes de olhar o resultado dela.

Ordem sugerida: E3.1 → E3.2 → E2.1 → E2.2 → E3.3 → E1.1 → E1.2 → E2.3 → E3.4 → E2.4. O P3 vem primeiro porque é o que está mais perto de submissão; o E2.1 decide se o teste de corte do P2 diz alguma coisa.

---

## Paper 3

### E3.1 — Controle pareado (preenche R3.1) · prioridade máxima

- **Pergunta:** o pipeline padrão cai nas armadilhas quando recebe o mesmo desenho do seu método (normalização pelo traço + janelas sobrepostas)?
- **Como:** copie `mdm_trap_control` e mude só duas coisas:
    1. depois de estimar cada covariância, divida pelo traço;
    2. use janelas sobrepostas: 1 s com passo de 0,25 s no olhos abertos/fechados; 2 s com passo de 1 s no sono.
  Classificador (OAS + MDM, pyRiemann 0.12), tarefas, canais, folds e testes ficam idênticos.
- **Critérios (iguais aos do controle original):**
    - dependência: shuffled − blocked ≥ 0,05;
    - pseudorreplicação: diferença entre agrupar por gravação e por sujeito ≥ 0,05;
    - ocular: queda sem EOG ≥ 0,05;
    - gravação: acurácia balanceada em duas gravações do mesmo estado ≥ 0,70.
- **Regra de leitura:** se pelo menos uma das armadilhas de dependência, ocular ou gravação passar do limite, vale "armadilhas do desenho" (a §4.1 fica). Se nenhuma passar, as armadilhas são do CUSUM geodésico em si, e a interpretação da §4.1 tem de ser retirada.
- **Me mande:** os quatro números, com mediana e intervalo por sujeito, mais `result.json` e o hash do commit.

### E3.2 — Informação além da potência alfa (preenche R3.2)

- **Dados:** EEGMMIDB, R01 e R02, 15 sujeitos, canais O1, Oz, O2, PO3, POz, PO4, Pz, épocas de 2 s sem sobreposição.
- **Modelo A:** regressão logística com a potência alfa relativa por canal (8–13 Hz sobre 1–40 Hz, sinal sem filtro de banda).
- **Modelo B:** o modelo A mais as coordenadas no espaço tangente da covariância normalizada pelo traço (filtro alfa), calculadas na média riemanniana do conjunto de treino.
- **Validação:** leave-one-subject-out. Métrica: log-loss no sujeito deixado de fora.
- **Critério:** a geometria carrega informação além da alfa se B tiver log-loss menor que A em pelo menos 11 de 15 sujeitos **e** o Wilcoxon pareado der p < 0,05.
- **Controle:** os mesmos modelos treinados para separar T0 de R03 contra T0 de R07 (mesmo estado). Os dois devem ficar no acaso.
- **Me mande:** o log-loss de A e de B por sujeito, a contagem, o p e o resultado do controle.

### E3.3 — Densidade de canais (preenche R3.3)

- **Como:** repita `between_recording_control` e `detection_between_recording_control` com os 64 canais do EEGMMIDB, sem mudar mais nada.
- **Critério:** os resultados dependem da densidade se a razão olhos abertos/fechados superar o controle de mesmo estado em pelo menos 12 de 15 sujeitos (Wilcoxon p < 0,01) **e** a detecção separar "mudança de estado" de "mudança de gravação" com AUC ≥ 0,80 (com 7 canais foi 0,72).
- **Me mande:** razões por sujeito, contagem, p, as duas AUCs e as mesmas medidas para a potência alfa relativa com 64 canais.

### E3.4 — Recodificação do survey (preenche R3.4)

- **Quando:** a partir de 07/10/2026, pelo menos duas semanas depois da primeira codificação.
- **Como:** recodifique os 20 estudos sem abrir os códigos antigos, usando as regras fixadas. Depois compare as duas rodadas.
- **Me mande:** o kappa de Cohen por armadilha e a lista de divergências. No paper isso entra como concordância *intra*-avaliador, não substitui um segundo codificador.

---

## Paper 2

### E2.1 — Controle positivo do teste de corte (preenche R2.1) · decide o P2

- **Dados:** PhysioNet Fantasia (20 jovens, 20 idosos, 120 min, anotações de batimento revisadas). Use as anotações, não um detector.
- **Como:** exatamente o mesmo teste de corte do I-CARE: série RR reamostrada a 4 Hz, T no lag 1, 200 surrogates IAAFT, p < 0,05 bicaudal por sujeito.
- **Critério:** o teste é sensível se a fração estruturada nos jovens for ≥ 0,60. Se for menor, a falha no I-CARE não diz nada sobre o I-CARE, porque o instrumento não passa nem onde deveria.
- **Previsão (Costa et al. 2005):** jovens > idosos.
- **Me mande:** a fração em cada grupo, T e p por sujeito.

### E2.2 — Versão por batimento e multiescala (preenche R2.2)

- **Dados:** Fantasia e os mesmos 21 pacientes do piloto do I-CARE.
- **Como:**
    1. série RR indexada por batimento, sem interpolação;
    2. remova batimentos ectópicos ou artefatos (RR que difere mais de 20% da mediana local de 5 batimentos);
    3. para cada escala τ = 1 a 10, crie a série de grão grosso (média de blocos não sobrepostos de τ batimentos) e calcule T no lag 1;
    4. para cada escala, gere 100 surrogates IAAFT e calcule o z-score de T;
    5. resumo por sujeito = média dos |z| nas 10 escalas;
    6. para obter o p, calcule o mesmo resumo para cada surrogate, tratando-o como se fosse a série real (z contra os outros 99). O p é a fração de surrogates com resumo maior ou igual ao da série real.
- **Critério:** estruturado se p < 0,05 no resumo. Aplique a mesma barra de 0,60.
- **Me mande:** a fração por grupo (Fantasia jovem, Fantasia idoso, I-CARE) e, no I-CARE, quantos dos 6 "estruturados" originais continuam estruturados depois da limpeza.

### E2.3 — I-CARE por desfecho (preenche R2.3, descritivo)

- **Como:** pegue os primeiros 50 pacientes com desfecho bom (CPC 1–2) e os primeiros 50 com desfecho ruim (CPC 3–5), na ordem do RECORDS, com pelo menos um segmento de ECG que renda 30 min limpos. Calcule o resumo do E2.2 e compare os grupos com Mann–Whitney. Registre idade, sexo, ritmo inicial e temperatura-alvo.
- **Atenção:** isso não testa a dissociação, é só descrição.
- **Me mande:** as distribuições por grupo, o p e as covariáveis.

### E2.4 — Checar a auditoria (preenche R2.4, baixa prioridade)

- **Como:** baixe os cabeçalhos EDF de pelo menos 30 registros do CHB-MIT (acesso aberto) e conte quantos têm canal ECG/EKG. O TUH EEG exige um pedido de acesso; faça só se você já tiver. No VitalDB, confira na lista de trilhas se há sinal de EEG bruto (não só o índice BIS) e em quantos casos.
- **Me mande:** as contagens. Mesmo com ECG ou EEG bruto, esses corpora não têm o contraste recuperação × não-recuperação; o objetivo é só corrigir a coluna P1 da Tabela 1.

---

## Paper 1

### E1.1 — Rastreamento de saída × rastreamento de estado completo (preenche R-A1)

- **Modelo:** dx = (−x + c·y + u)dt + σ dW_x ; dy = (−y + c·x + v)dt + σ dW_y, com σ = 1.
- **Referência:** r(t) = 0 na primeira metade e 1 na segunda (o "alvo novo").
- **Duas condições:**
    - só saída: u = −k(x − r), v = 0;
    - estado completo: u = −k(x − r), v = −k·y.
- **Parâmetros:**
    - k ∈ {0; 0,5; 1; 2; 5; 10; 20; 50}, c ∈ {0; 0,3};
    - Euler–Maruyama com dt = 0,001, T = 2000;
    - variância medida na segunda metade, descartando as primeiras 200 unidades de tempo depois do degrau e subtraindo a média;
    - 10 sementes.
- **Critério:**
    - estado completo: var(y) cai monotonamente e fica abaixo de 5% de σ²/2 em k = 50;
    - só saída: var(y) fica dentro de ±10% de σ²/2 em todos os k quando c = 0, e ≥ 90% de σ²/2 em k = 50 quando c = 0,3.
- **Me mande:** uma tabela de var(y) e var(x − r) por k, c e condição.

### E1.2 — Tempo de recorrência × dimensão (preenche R-A2)

- **Modelo:** rotação do toro θ ↦ θ + α (mod 1), com α_i = parte fracionária de √p_i para os primos 2, 3, 5, 7, 11; dimensões d = 1 a 5.
- **Como:** conjunto de retorno A = caixa de lado 0,1 centrada em (0,5, …, 0,5), logo μ(A) = 10⁻ᵈ. Sorteie 200 pontos iniciais uniformes dentro de A e conte os passos até a primeira volta a A (limite de 10⁷ passos).
- **Critério:** a média fica dentro de ±15% de 10ᵈ em cada d, e a inclinação de log₁₀(média) contra d fica entre 0,9 e 1,1.
- **Me mande:** média e desvio por d e a inclinação.

---

## O que me mandar de cada experimento

Para cada um: (1) o hash do commit do código, (2) o `result.json` com os números brutos, (3) o veredito contra o critério escrito aqui e (4) qualquer desvio do plano, com o motivo. Com isso eu preencho o espaço `[RESULT …]` correspondente e ajusto o texto: se um resultado for contra a interpretação do paper, o paper muda, não o resultado.
