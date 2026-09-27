# Resultados dos experimentos de 27/09/2026

Todos os experimentos foram pré-registrados no commit `fbe4b6f` antes de qualquer execução. Os resultados estão no commit `6c27c4d`. Cada número abaixo foi lido do `result.json` indicado.

**Desvio do E0:** não foi possível criar uma release no Zenodo/OSF deste ambiente; a única prova de ordem é o push do commit de pré-registro e o PR #56.

| Exp. | Preenche | Veredito contra o critério pré-registrado |
|---|---|---|
| E3.1 | R3.1 | Armadilhas do **desenho**: a §4.1 fica (ocular cruza: sim; dependência: não; gravação: não) |
| E3.2 | R3.2 | Critério **não atingido**: B melhor em 11/15, Wilcoxon p = 0.762 |
| E3.3 | R3.3 | Critério **não atingido** (não depende, pela barra conjunta): razão 13/15 (p = 0.00168), AUC de detecção 0.409 |
| E3.4 | R3.4 | **Adiado**: só a partir de 07/10/2026 (ver `E3.4_DEFERRED.md`) |
| E2.1 | R2.1 | Teste **sensível** (versão aplicada): jovens 19/20, idosos 17/20; versão descrita (4 Hz): jovens 17/20, idosos 18/20 |
| E2.2 | R2.2 | I-CARE 15/21 estruturados (passa a barra de 0,60); Fantasia jovens 20/20, idosos 16/20 |
| E2.3 | R2.3 | Descritivo: mediana bom 1.82 × ruim 2.07, Mann–Whitney p = 0.163 |
| E2.4 | R2.4 | CHB-MIT 0/30 com ECG; VitalDB 5871/6388 casos com EEG bruto |
| E1.1 | R-A1 | Previsão **atingida** |
| E1.2 | R-A2 | Previsão **atingida** (inclinação 1.006) |

---

## E3.1 — Controle pareado (Paper 3, R3.1)

Pipeline padrão (OAS → MDM) com normalização pelo traço e janelas sobrepostas. Mediana [IQR; mín–máx]:

| Armadilha | Estatística | Mediana | IQR | Mín–máx | n | Barra | Cruza? |
|---|---|---|---|---|---|---|---|
| Dependência | shuffled − blocked, por gravação | 0.003 | 0.002–0.006 | -0.001–0.053 | 151 | ≥ 0,05 | não |
| Ocular | queda sem EOG, por sujeito | 0.092 | 0.049–0.132 | 0.002–0.248 | 78 | ≥ 0,05 | sim |
| Gravação | acurácia balanceada, mesmo estado | 0.608 | 0.538–0.692 | 0.436–0.933 | 15 | ≥ 0,70 | não |
| Pseudorreplicação | por gravação − por sujeito (pooled) | -0.0001 | — | — | 2791656 janelas | ≥ 0,05 | não |

Wilcoxon unilateral da queda ocular: p = 8.4e-15. Olhos abertos × fechados (referência): mediana 0.849. Duas gravações de sono estavam truncadas no cache (SC4012E0, SC4041E0) e foram puladas, como no registro original (151 de 153).

**Veredito (do `result.json`):** TRAPS OF THE DESIGN (trace normalization + overlap): Paper 3 §4.1 stands. Dependence (shuffled - blocked): median +0.003 over 151 recordings (bar 0.05) -> below. Ocular (drop without EOG): median +0.092 over 78 subjects, one-sided Wilcoxon p = 8.4e-15 (bar 0.05) -> crosses. Recording (two same-state recordings): median balanced accuracy 0.608 over 15 subjects (bar 0.70; eyes open vs closed 0.849) -> below. Pseudo-replication (grouped by recording - by subject): -0.0001 (bar 0.05; not part of the reading rule) -> below.

## E3.2 — Informação além da potência alfa (Paper 3, R3.2)

| Sujeito | log-loss A | log-loss B | B melhor? |
|---|---|---|---|
| S001 | 0.312 | 0.175 | sim |
| S002 | 0.608 | 0.492 | sim |
| S003 | 0.354 | 0.245 | sim |
| S004 | 0.224 | 0.123 | sim |
| S005 | 0.760 | 1.431 | não |
| S006 | 0.876 | 1.629 | não |
| S007 | 1.004 | 1.509 | não |
| S008 | 0.474 | 0.131 | sim |
| S009 | 0.518 | 0.193 | sim |
| S010 | 0.406 | 0.272 | sim |
| S011 | 0.406 | 0.370 | sim |
| S012 | 0.818 | 0.644 | sim |
| S013 | 0.665 | 1.110 | não |
| S014 | 0.496 | 0.456 | sim |
| S015 | 0.567 | 0.373 | sim |

Contagem 11/15; Wilcoxon pareado p = 0.762 (bilateral) / 0.381 (unilateral). Controle (T0 R03 × T0 R07): acurácia balanceada mediana A 0.53, B 0.55; log-loss mediano A 0.695, B 0.721 (acaso = 0,693).

**Veredito (do `result.json`):** NO EVIDENCE THAT THE GEOMETRY ADDS INFORMATION BEYOND ALPHA POWER (pre-registered bar: B better in >= 11/15 and two-sided paired Wilcoxon p < 0.05). Held-out log-loss lower with the geometry in 11/15 subjects; median log-loss A 0.518, B 0.373; Wilcoxon p = 0.762 two-sided (0.381 one-sided). Control (two same-state recordings): median held-out balanced accuracy A 0.53, B 0.55; median log-loss A 0.695, B 0.721 (chance log-loss ln 2 = 0.693).

## E3.3 — Densidade de canais (Paper 3, R3.3)

| Sujeito | razão geométrica OC | controle SS | alfa relativa OC | alfa relativa SS |
|---|---|---|---|---|
| S001 | 1.40 | 1.09 | 4.09 | 1.28 |
| S002 | 1.03 | 0.70 | 4.18 | 0.48 |
| S003 | 2.10 | 0.78 | 7.00 | 0.77 |
| S004 | 3.34 | 0.76 | 7.82 | 1.47 |
| S005 | 0.86 | 0.76 | 2.11 | 2.18 |
| S006 | 0.91 | 1.23 | 0.58 | 0.58 |
| S007 | 1.11 | 0.74 | 3.16 | 2.29 |
| S008 | 1.75 | 0.66 | 5.90 | 0.55 |
| S009 | 0.88 | 1.15 | 4.01 | 0.98 |
| S010 | 1.24 | 0.93 | 1.02 | 0.53 |
| S011 | 1.27 | 0.86 | 4.02 | 0.34 |
| S012 | 1.82 | 0.74 | 1.53 | 0.60 |
| S013 | 1.14 | 1.01 | 2.84 | 1.05 |
| S014 | 2.08 | 0.86 | 5.17 | 1.01 |
| S015 | 0.82 | 0.73 | 1.01 | 0.99 |

AUCs de detecção (64 canais): mudança de estado × mudança de gravação 0.409; mudança de gravação × dentro da gravação 0.573; estado × dentro 0.458.
Nota: o `between_recording_control` original tem um teste de sanidade que compara a mediana com o valor de 7 canais; com 64 canais ele acusa diferença por construção e não se aplica aqui. O critério do E3.3 é calculado à parte.

**Veredito (do `result.json`):** RESULTS DO NOT DEPEND ON CHANNEL DENSITY (by the pre-registered bar): with 64 channels the eyes-open/closed geometric ratio exceeds the same-state control in 13/15 subjects (one-sided Wilcoxon p = 0.00168; bar >= 12/15 and p < 0.01; 7 channels: 11/15, p = 0.024), and the detection statistic separates a change of state from a same-state change of recording at AUC 0.409 (bar 0.80; 7 channels: 0.72). A recording change alone fires it at AUC 0.573. Relative alpha power with 64 channels: median ratio 4.01 (eyes open/closed) against 0.98 (same state).

## E2.1 — Controle positivo no Fantasia (Paper 2, R2.1)

**Versão aplicada ao I-CARE (por batimento):** jovens 19/20 (95%), idosos 17/20 (85%).

| Sujeito | T | p |
|---|---|---|
| f1y01 | +0.6781 | 0.005 |
| f1y02 | +0.6687 | 0.005 |
| f1y03 | +0.3199 | 0.005 |
| f1y04 | +0.2430 | 0.005 |
| f1y05 | +1.1205 | 0.005 |
| f1y06 | +0.8020 | 0.005 |
| f1y07 | +1.0153 | 0.005 |
| f1y08 | +0.3462 | 0.005 |
| f1y09 | +0.3658 | 0.005 |
| f1y10 | +0.4866 | 0.005 |
| f2y01 | +0.4390 | 0.005 |
| f2y02 | +0.5601 | 0.005 |
| f2y03 | -0.1784 | 0.005 |
| f2y04 | -0.3470 | 0.005 |
| f2y05 | -0.0188 | 0.597 |
| f2y06 | +0.2447 | 0.005 |
| f2y07 | +0.8979 | 0.005 |
| f2y08 | +0.6452 | 0.005 |
| f2y09 | +1.0092 | 0.005 |
| f2y10 | +0.5376 | 0.005 |
| f1o01 | -0.2588 | 0.005 |
| f1o02 | -0.1925 | 0.005 |
| f1o03 | +0.6259 | 0.005 |
| f1o04 | +1.1023 | 0.005 |
| f1o05 | +0.1896 | 0.005 |
| f1o06 | +0.1087 | 0.010 |
| f1o07 | +1.2057 | 0.005 |
| f1o08 | +0.4825 | 0.005 |
| f1o09 | +0.0910 | 0.030 |
| f1o10 | +0.0504 | 0.144 |
| f2o01 | -0.3330 | 0.005 |
| f2o02 | +0.1845 | 0.005 |
| f2o03 | +0.6176 | 0.005 |
| f2o04 | +0.0115 | 0.716 |
| f2o05 | +2.4254 | 0.005 |
| f2o06 | +0.0953 | 0.010 |
| f2o07 | -0.3241 | 0.005 |
| f2o08 | +0.0481 | 0.249 |
| f2o09 | -0.7428 | 0.005 |
| f2o10 | +1.2779 | 0.005 |

**Versão descrita no paper (4 Hz):** jovens 17/20 (85%), idosos 18/20 (90%).

| Sujeito | T | p |
|---|---|---|
| f1y01 | +0.1665 | 0.005 |
| f1y02 | +0.2729 | 0.005 |
| f1y03 | +0.1761 | 0.005 |
| f1y04 | +0.0309 | 0.338 |
| f1y05 | +0.7774 | 0.005 |
| f1y06 | +0.4982 | 0.005 |
| f1y07 | +0.5122 | 0.005 |
| f1y08 | +0.1611 | 0.005 |
| f1y09 | +0.0637 | 0.040 |
| f1y10 | -0.0137 | 0.488 |
| f2y01 | +0.0781 | 0.010 |
| f2y02 | +0.1405 | 0.005 |
| f2y03 | -0.2403 | 0.005 |
| f2y04 | -0.3656 | 0.005 |
| f2y05 | -0.0537 | 0.184 |
| f2y06 | +0.1470 | 0.005 |
| f2y07 | +0.5672 | 0.005 |
| f2y08 | +0.2921 | 0.005 |
| f2y09 | -0.8490 | 0.005 |
| f2y10 | +0.1706 | 0.005 |
| f1o01 | -0.4183 | 0.005 |
| f1o02 | -0.2486 | 0.005 |
| f1o03 | +0.2223 | 0.005 |
| f1o04 | +0.5334 | 0.005 |
| f1o05 | -0.7846 | 0.005 |
| f1o06 | +0.0679 | 0.010 |
| f1o07 | +0.2360 | 0.005 |
| f1o08 | +0.2873 | 0.005 |
| f1o09 | -0.2508 | 0.005 |
| f1o10 | -0.0595 | 0.244 |
| f2o01 | -1.7772 | 0.005 |
| f2o02 | -0.0930 | 0.005 |
| f2o03 | +0.2214 | 0.005 |
| f2o04 | -0.0776 | 0.025 |
| f2o05 | +0.9456 | 0.005 |
| f2o06 | -0.1230 | 0.005 |
| f2o07 | -0.4216 | 0.005 |
| f2o08 | -0.8961 | 0.005 |
| f2o09 | -1.0783 | 0.005 |
| f2o10 | -0.0340 | 0.194 |


**Veredito (do `result.json`):** PRIMARY (gate as applied to I-CARE, beat-indexed): SENSITIVE -- young 19/20 (95%), elderly 17/20 (85%); bar 60% in the young. SECONDARY (gate as described, 4 Hz): SENSITIVE -- young 17/20 (85%), elderly 18/20 (90%). Prediction young > elderly: met (primary), not met (secondary).

## E2.2 — Versão por batimento e multiescala (Paper 2, R2.2)

Fantasia jovens 20/20, idosos 16/20, I-CARE 15/21. Dos 6 estruturados originais do I-CARE, 5 continuam estruturados.
Checagem de reprodução: 21/21 segmentos dão exatamente o número de intervalos RR do piloto.
Secundário (teste como descrito, 4 Hz) no I-CARE: 16/21.

| I-CARE | resumo (média de \|z\|) | p | estruturado | estruturado no piloto |
|---|---|---|---|---|
| 0284 | 1.54 | 0.01 | sim | sim |
| 0286 | 1.99 | 0.00 | sim | sim |
| 0296 | 1.05 | 0.12 | não | sim |
| 0303 | 0.97 | 0.21 | não | não |
| 0306 | 0.82 | 0.43 | não | não |
| 0312 | 1.06 | 0.11 | não | não |
| 0313 | 50.21 | 0.00 | sim | não |
| 0316 | 1.30 | 0.00 | sim | não |
| 0328 | 1.71 | 0.00 | sim | sim |
| 0337 | 1.09 | 0.05 | não | não |
| 0340 | 1.97 | 0.00 | sim | não |
| 0342 | 2.96 | 0.00 | sim | não |
| 0344 | 2.04 | 0.00 | sim | não |
| 0346 | 1.53 | 0.00 | sim | não |
| 0347 | 1.32 | 0.00 | sim | não |
| 0348 | 1.83 | 0.01 | sim | não |
| 0349 | 0.98 | 0.18 | não | não |
| 0350 | 3.94 | 0.00 | sim | sim |
| 0351 | 2.33 | 0.00 | sim | sim |
| 0352 | 1.76 | 0.00 | sim | não |
| 0353 | 1.31 | 0.01 | sim | não |

**Veredito (do `result.json`):** Structured fraction (multiscale, beat-indexed, p < 0.05; bar 0.60): Fantasia young 20/20, elderly 16/20, I-CARE 15/21. Of the 6 I-CARE patients the pilot called structured, 5 remain structured after cleaning. Reproduction check: 21/21 segments give the pilot's exact RR count. Secondary (gate as described, 4 Hz) on I-CARE: 16/21 (76%).

## E2.3 — I-CARE por desfecho, descritivo (Paper 2, R2.3)

Bom desfecho (n = 50): resumo mediano 1.82 [IQR 1.14–3.16], fração estruturada 74%; idade mediana 55.0, homens 80%, ritmo chocável 70%, TTM {'33': 24, 'nan': 12, '36': 14}.
Desfecho ruim (n = 50): resumo mediano 2.07 [IQR 1.26–4.71], fração estruturada 80%; idade mediana 64.0, homens 62%, ritmo chocável 31%, TTM {'33': 29, '36': 8, 'nan': 13}.
Mann–Whitney bilateral p = 0.163. Pulados por falta de 30 min limpos: bom 59, ruim 62. **Isto não testa a dissociação.**

**Veredito (do `result.json`):** DESCRIPTIVE (not a test of the dissociation). Multiscale asymmetry summary (mean |z|, scales 1-10, first 1800 s of clean beats): good outcome median 1.82 (n = 50), poor outcome median 2.07 (n = 50); two-sided Mann-Whitney p = 0.163. Structured fraction (p < 0.05): good 74%, poor 80%. Skipped for lack of 30 clean minutes in 3 segments: good 59, poor 62.

## E2.4 — Checagem da auditoria (Paper 2, R2.4)

CHB-MIT (regra pré-registrada, 30 primeiros arquivos): 0/30 com ECG/EKG. Os 30 são todos do paciente chb01.
Exploratório, não pré-registrado (primeiro arquivo de cada paciente): 0/24 pacientes com ECG.
VitalDB: 5871/6388 casos com trilhas de EEG bruto (BIS/EEG1_WAV, BIS/EEG2_WAV). A Tabela 1 classifica o VitalDB como sem EEG bruto (só índice); isso está errado. Continua sem o contraste recuperação × não-recuperação.
TUH EEG: não checado (exige pedido de acesso).

**Veredito (do `result.json`):** CHB-MIT: 0/30 of the first EDF files carry an ECG/EKG channel (patients none of chb01). TUH EEG: not checked (access requires an application). VitalDB: 5871 of 6388 cases have a track named EEG (BIS/EEG1_WAV, BIS/EEG2_WAV). None of these corpora has a recovery/non-recovery contrast; this only corrects Table 1's P1 column.

## E1.1 — Rastreamento de saída × estado completo (Paper 1, R-A1)

| Condição | c | k | var(y) média | var(y)/(σ²/2) | var(x − r) média |
|---|---|---|---|---|---|
| output | 0.0 | 0.0 | 0.4931 | 0.986 | 0.4994 |
| output | 0.0 | 0.5 | 0.4931 | 0.986 | 0.3328 |
| output | 0.0 | 1.0 | 0.4931 | 0.986 | 0.2498 |
| output | 0.0 | 2.0 | 0.4931 | 0.986 | 0.1668 |
| output | 0.0 | 5.0 | 0.4931 | 0.986 | 0.0837 |
| output | 0.0 | 10.0 | 0.4931 | 0.986 | 0.0458 |
| output | 0.0 | 20.0 | 0.4931 | 0.986 | 0.0241 |
| output | 0.0 | 50.0 | 0.4931 | 0.986 | 0.0101 |
| output | 0.3 | 0.0 | 0.5388 | 1.078 | 0.5456 |
| output | 0.3 | 0.5 | 0.5225 | 1.045 | 0.3525 |
| output | 0.3 | 1.0 | 0.5148 | 1.030 | 0.2607 |
| output | 0.3 | 2.0 | 0.5073 | 1.015 | 0.1715 |
| output | 0.3 | 5.0 | 0.5001 | 1.000 | 0.0849 |
| output | 0.3 | 10.0 | 0.4969 | 0.994 | 0.0462 |
| output | 0.3 | 20.0 | 0.4951 | 0.990 | 0.0242 |
| output | 0.3 | 50.0 | 0.4939 | 0.988 | 0.0101 |
| full_state | 0.0 | 0.0 | 0.4931 | 0.986 | 0.4994 |
| full_state | 0.0 | 0.5 | 0.3305 | 0.661 | 0.3328 |
| full_state | 0.0 | 1.0 | 0.2488 | 0.498 | 0.2498 |
| full_state | 0.0 | 2.0 | 0.1667 | 0.333 | 0.1668 |
| full_state | 0.0 | 5.0 | 0.0838 | 0.168 | 0.0837 |
| full_state | 0.0 | 10.0 | 0.0459 | 0.092 | 0.0458 |
| full_state | 0.0 | 20.0 | 0.0242 | 0.048 | 0.0241 |
| full_state | 0.0 | 50.0 | 0.0101 | 0.020 | 0.0101 |
| full_state | 0.3 | 0.0 | 0.5388 | 1.078 | 0.5456 |
| full_state | 0.3 | 0.5 | 0.3434 | 0.687 | 0.3457 |
| full_state | 0.3 | 1.0 | 0.2542 | 0.508 | 0.2552 |
| full_state | 0.3 | 2.0 | 0.1683 | 0.337 | 0.1684 |
| full_state | 0.3 | 5.0 | 0.0840 | 0.168 | 0.0839 |
| full_state | 0.3 | 10.0 | 0.0459 | 0.092 | 0.0459 |
| full_state | 0.3 | 20.0 | 0.0242 | 0.048 | 0.0241 |
| full_state | 0.3 | 50.0 | 0.0101 | 0.020 | 0.0101 |

**Veredito (do `result.json`):** PREDICTION MET. Full-state tracking: var(y) falls monotonically with k for c = 0 and 0.3 (yes) and at k = 50 is 2.0% (c = 0) and 2.0% (c = 0.3) of sigma^2/2 (bar < 5%). Output tracking: with c = 0, var(y)/(sigma^2/2) ranges 0.986-0.986 over k (bar within +/-10%); with c = 0.3 it is 0.988 at k = 50 (bar >= 0.90). Seed means of 10 seeds; variances over t in [1200, 2000].

## E1.2 — Tempo de recorrência × dimensão (Paper 1, R-A2)

| d | média | desvio | Kac (10ᵈ) | razão | dentro de ±15% |
|---|---|---|---|---|---|
| 1 | 10.2 | 3.1 | 10 | 1.022 | sim |
| 2 | 88.4 | 119.3 | 100 | 0.884 | sim |
| 3 | 964.8 | 651.7 | 1000 | 0.965 | sim |
| 4 | 10363.5 | 14853.7 | 10000 | 1.036 | sim |
| 5 | 101051.6 | 100060.9 | 100000 | 1.011 | sim |

Inclinação de log₁₀(média) contra d: 1.006.

**Veredito (do `result.json`):** PREDICTION MET. Mean return time / Kac value (10^d) for d = 1..5: 1.022, 0.884, 0.965, 1.036, 1.011 (bar within +/-15% each: yes); slope of log10(mean) on d = 1.006 (bar 0.9-1.1). 0 of 1000 starts hit the cap.

## E3.4 — Recodificação do survey (R3.4)

Não executado: o plano fixa início a partir de 07/10/2026 e exige recodificação cega. Ver `experiments/E3.4_DEFERRED.md`.

## Leitura por paper (resultados negativos primeiro)

- **Paper 2 — contra o texto atual.** O teste de estrutura é sensível (E2.1), e aplicado ao I-CARE como o paper o descreve (4 Hz) dá 16/21 estruturados; na versão multiescala, 15/21 (E2.2). O "6/21" do paper vem da versão por batimento que foi de fato executada, não da descrita. A conclusão de que a maioria dos segmentos do I-CARE não passa no teste precisa ser revista. A Tabela 1 está errada para o VitalDB (há EEG bruto em 5871/6388 casos) (E2.4). O paciente 0313 tem resumo 50.21, provável artefato, a inspecionar. No E2.3 os grupos não diferem (p = 0.163) e diferem em covariáveis (idade, ritmo chocável); é descritivo e não testa a dissociação.
- **Paper 3 — negativo para a geometria, coerente com o enquadramento de negativo metodológico.** A geometria não acrescenta informação além da potência alfa pelo critério pré-registrado (E3.2). Com 64 canais a razão geométrica melhora (13/15), mas a detecção cai para AUC 0.409, e o critério conjunto não é atingido (E3.3). A §4.1 se mantém (E3.1).
- **Paper 1 — a favor, apenas como ilustração.** As duas computações do Apêndice A se confirmam (E1.1, E1.2). São simulações de brinquedo; não são evidência empírica para a tese.

Nenhum destes resultados torna qualquer paper pronto para submissão.

