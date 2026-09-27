"""Compose experiments/RESULTADOS_2026-09-27.md from the committed result.json files.

Every number in the output is read from a result.json; nothing is typed by hand.
Usage:
    python experiments/make_resultados_2026_09_27.py <commit-hash-of-results>
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "_results")
PREREG_COMMIT = "fbe4b6f"


def load(name):
    p = os.path.join(R, name, "result.json")
    return json.load(open(p)) if os.path.exists(p) else None


def pct(x):
    return "—" if x is None else f"{x:.0%}"


def main(commit):
    out = ["# Resultados dos experimentos de 27/09/2026", "",
           f"Todos os experimentos foram pré-registrados no commit `{PREREG_COMMIT}` antes de qualquer execução. "
           f"Os resultados estão no commit `{commit}`. Cada número abaixo foi lido do `result.json` indicado.",
           "",
           "**Desvio do E0:** não foi possível criar uma release no Zenodo/OSF deste ambiente; a única prova de "
           "ordem é o push do commit de pré-registro e o PR #56.", "",
           "| Exp. | Preenche | Veredito contra o critério pré-registrado |", "|---|---|---|"]
    rows = []

    e31 = load("mdm_matched_control")
    if e31:
        c = e31["crosses_bar"]
        rows.append(("E3.1", "R3.1", ("Armadilhas do **desenho**: a §4.1 fica" if e31["reading_rule_met"] else
                                       "Armadilhas do **CUSUM**: a §4.1 deve ser retirada")
                     + f" (ocular cruza: {c['T1_ocular']}; dependência: {c['T4_dependence']}; gravação: {c['T2_recording']})"))
    e32 = load("alpha_incremental_test")
    if e32:
        rows.append(("E3.2", "R3.2", ("Critério **atingido**" if e32["criterion_met"] else "Critério **não atingido**")
                     + f": B melhor em {e32['n_B_better']}/15, Wilcoxon p = {e32['wilcoxon_p_two_sided']:.3g}"))
    e33 = load("channel_density_control")
    if e33:
        rows.append(("E3.3", "R3.3", ("Depende da densidade" if e33["criterion_met_depends_on_density"] else
                                       "Critério **não atingido** (não depende, pela barra conjunta)")
                     + f": razão {e33['geometry']['n_OC_gt_SS']}/15 (p = {e33['geometry']['wilcoxon_p_one_sided']:.3g}), "
                       f"AUC de detecção {e33['detection']['auc_OC_vs_SS']:.3f}"))
    rows.append(("E3.4", "R3.4", "**Adiado**: só a partir de 07/10/2026 (ver `E3.4_DEFERRED.md`)"))
    e21 = load("fantasia_positive_control")
    if e21:
        p = e21["results"]["as_applied_beat_indexed"]; s = e21["results"]["as_described_4hz"]
        rows.append(("E2.1", "R2.1", ("Teste **sensível**" if p["sensitive"] else "Teste **não sensível**")
                     + f" (versão aplicada): jovens {p['young']['n_structured']}/{p['young']['n']}, idosos "
                       f"{p['elderly']['n_structured']}/{p['elderly']['n']}; versão descrita (4 Hz): jovens "
                       f"{s['young']['n_structured']}/{s['young']['n']}, idosos {s['elderly']['n_structured']}/{s['elderly']['n']}"))
    e22 = load("multiscale_asymmetry")
    if e22:
        r = e22["results"]
        rows.append(("E2.2", "R2.2", f"I-CARE {r['icare']['n_structured']}/{r['icare']['n']} estruturados "
                     f"({'passa' if r['icare']['passes_0.60'] else 'não passa'} a barra de 0,60); Fantasia jovens "
                     f"{r['fantasia_young']['n_structured']}/{r['fantasia_young']['n']}, idosos "
                     f"{r['fantasia_elderly']['n_structured']}/{r['fantasia_elderly']['n']}"))
    e23 = load("icare_outcome_descriptive")
    if e23:
        rows.append(("E2.3", "R2.3", f"Descritivo: mediana bom {e23['good']['summary_distribution']['median']:.2f} × ruim "
                     f"{e23['poor']['summary_distribution']['median']:.2f}, Mann–Whitney p = {e23['mann_whitney_p_two_sided']:.3g}"))
    e24 = load("audit_recheck")
    if e24:
        v = e24["vitaldb"]
        rows.append(("E2.4", "R2.4", f"CHB-MIT {e24['chbmit']['n_with_cardiac']}/{e24['chbmit']['n_files']} com ECG; "
                     f"VitalDB {v.get('cases_with_any_eeg_track')}/{v.get('n_cases_total')} casos com EEG bruto"))
    e11 = load("output_vs_fullstate_tracking")
    if e11:
        rows.append(("E1.1", "R-A1", "Previsão **atingida**" if e11["prediction_met"] else "Previsão **não atingida**"))
    e12 = load("kac_recurrence_dimension")
    if e12:
        rows.append(("E1.2", "R-A2", ("Previsão **atingida**" if e12["prediction_met"] else "Previsão **não atingida**")
                     + f" (inclinação {e12['slope_log10_mean_vs_d']:.3f})"))
    out += [f"| {a} | {b} | {c} |" for a, b, c in rows]
    out += ["", "---", ""]

    def section(title, res, lines):
        out.extend([f"## {title}", ""] + lines + ["", f"**Veredito (do `result.json`):** {res['verdict']}", ""])

    if e31:
        t = e31
        section("E3.1 — Controle pareado (Paper 3, R3.1)", t, [
            "Pipeline padrão (OAS → MDM) com normalização pelo traço e janelas sobrepostas. Mediana [IQR; mín–máx]:", "",
            "| Armadilha | Estatística | Mediana | IQR | Mín–máx | n | Barra | Cruza? |", "|---|---|---|---|---|---|---|---|",
            *[f"| {name} | {lab} | {d['median']:.3f} | {d['q25']:.3f}–{d['q75']:.3f} | {d['min']:.3f}–{d['max']:.3f} | {d['n']} | {bar} | {cr} |"
              for name, lab, d, bar, cr in (
                  ("Dependência", "shuffled − blocked, por gravação", t["T4_dependence"]["shuffled_minus_blocked"], "≥ 0,05", t["crosses_bar"]["T4_dependence"]),
                  ("Ocular", "queda sem EOG, por sujeito", t["T1_ocular"]["per_subject_drop"], "≥ 0,05", t["crosses_bar"]["T1_ocular"]),
                  ("Gravação", "acurácia balanceada, mesmo estado", t["T2_recording"]["same_state_acc"], "≥ 0,70", t["crosses_bar"]["T2_recording"]))],
            f"| Pseudorreplicação | por gravação − por sujeito (pooled) | {t['T3_pseudoreplication']['gap']:+.4f} | — | — | "
            f"{t['T3_pseudoreplication']['n_windows_pooled']} janelas | ≥ 0,05 | {t['crosses_bar']['T3_pseudoreplication']} |", "",
            f"Wilcoxon unilateral da queda ocular: p = {t['T1_ocular']['wilcoxon_p_one_sided']:.2g}. Olhos abertos × fechados "
            f"(referência): mediana {t['T2_recording']['open_closed_acc']['median']:.3f}. Duas gravações de sono estavam truncadas "
            f"no cache (SC4012E0, SC4041E0) e foram puladas, como no registro original (151 de 153)."])
    if e32:
        t = e32
        section("E3.2 — Informação além da potência alfa (Paper 3, R3.2)", t, [
            "| Sujeito | log-loss A | log-loss B | B melhor? |", "|---|---|---|---|",
            *[f"| {r['subject']} | {r['logloss_A']:.3f} | {r['logloss_B']:.3f} | {'sim' if r['logloss_B'] < r['logloss_A'] else 'não'} |" for r in t["per_subject"]],
            "", f"Contagem {t['n_B_better']}/15; Wilcoxon pareado p = {t['wilcoxon_p_two_sided']:.3g} (bilateral) / "
                f"{t['wilcoxon_p_one_sided']:.3g} (unilateral). Controle (T0 R03 × T0 R07): acurácia balanceada mediana A "
                f"{t['control_same_state']['median_balacc_A']:.2f}, B {t['control_same_state']['median_balacc_B']:.2f}; log-loss "
                f"mediano A {t['control_same_state']['median_logloss_A']:.3f}, B {t['control_same_state']['median_logloss_B']:.3f} (acaso = 0,693)."])
    if e33:
        t = e33
        section("E3.3 — Densidade de canais (Paper 3, R3.3)", t, [
            "| Sujeito | razão geométrica OC | controle SS | alfa relativa OC | alfa relativa SS |", "|---|---|---|---|---|",
            *[f"| S{int(r['subject']):03d} | {r['G_OC']:.2f} | {r['G_SS']:.2f} | {r['S_OC']:.2f} | {r['S_SS']:.2f} |" for r in t["per_subject_ratios"]],
            "", f"AUCs de detecção (64 canais): mudança de estado × mudança de gravação {t['detection']['auc_OC_vs_SS']:.3f}; "
                f"mudança de gravação × dentro da gravação {t['detection']['auc_SS_vs_WN']:.3f}; estado × dentro {t['detection']['auc_OC_vs_WN']:.3f}.",
            "Nota: o `between_recording_control` original tem um teste de sanidade que compara a mediana com o valor de 7 canais; "
            "com 64 canais ele acusa diferença por construção e não se aplica aqui. O critério do E3.3 é calculado à parte."])
    if e21:
        lines = []
        for ver, lab in (("as_applied_beat_indexed", "Versão aplicada ao I-CARE (por batimento)"), ("as_described_4hz", "Versão descrita no paper (4 Hz)")):
            v = e21["results"][ver]
            lines += [f"**{lab}:** jovens {v['young']['n_structured']}/{v['young']['n']} ({pct(v['young']['fraction_structured'])}), "
                      f"idosos {v['elderly']['n_structured']}/{v['elderly']['n']} ({pct(v['elderly']['fraction_structured'])}).", "",
                      "| Sujeito | T | p |", "|---|---|---|",
                      *[f"| {r['record']} | {r['t_rev']:+.4f} | {r['p']:.3f} |" for r in v['young']['per_subject'] + v['elderly']['per_subject']], ""]
        section("E2.1 — Controle positivo no Fantasia (Paper 2, R2.1)", e21, lines)
    if e22:
        t = e22
        section("E2.2 — Versão por batimento e multiescala (Paper 2, R2.2)", t, [
            f"Fantasia jovens {t['results']['fantasia_young']['n_structured']}/{t['results']['fantasia_young']['n']}, "
            f"idosos {t['results']['fantasia_elderly']['n_structured']}/{t['results']['fantasia_elderly']['n']}, "
            f"I-CARE {t['results']['icare']['n_structured']}/{t['results']['icare']['n']}. Dos {t['icare_original_structured']} "
            f"estruturados originais do I-CARE, {t['icare_original_still_structured']} continuam estruturados.",
            f"Checagem de reprodução: {sum(r['same_segment'] for r in t['reproduction_check'])}/{len(t['reproduction_check'])} "
            f"segmentos dão exatamente o número de intervalos RR do piloto.",
            f"Secundário (teste como descrito, 4 Hz) no I-CARE: {t['secondary_icare_gate_as_described_4hz']['n_structured']}/"
            f"{t['secondary_icare_gate_as_described_4hz']['n']}.", "",
            "| I-CARE | resumo (média de \\|z\\|) | p | estruturado | estruturado no piloto |", "|---|---|---|---|---|",
            *[f"| {r['subject']} | {r['summary_mean_abs_z']:.2f} | {r['p']:.2f} | {'sim' if r['structured'] else 'não'} | {'sim' if r['pilot_structured'] else 'não'} |"
              for r in t["results"]["icare"]["per_subject"]]])
    if e23:
        t = e23
        section("E2.3 — I-CARE por desfecho, descritivo (Paper 2, R2.3)", t, [
            f"Bom desfecho (n = {t['good']['covariates']['n']}): resumo mediano {t['good']['summary_distribution']['median']:.2f} "
            f"[IQR {t['good']['summary_distribution']['q25']:.2f}–{t['good']['summary_distribution']['q75']:.2f}], fração estruturada {pct(t['good']['structured_fraction'])}; "
            f"idade mediana {t['good']['covariates']['age_median']}, homens {pct(t['good']['covariates']['male_share'])}, ritmo chocável {pct(t['good']['covariates']['shockable_share'])}, "
            f"TTM {t['good']['covariates']['TTM_counts']}.",
            f"Desfecho ruim (n = {t['poor']['covariates']['n']}): resumo mediano {t['poor']['summary_distribution']['median']:.2f} "
            f"[IQR {t['poor']['summary_distribution']['q25']:.2f}–{t['poor']['summary_distribution']['q75']:.2f}], fração estruturada {pct(t['poor']['structured_fraction'])}; "
            f"idade mediana {t['poor']['covariates']['age_median']}, homens {pct(t['poor']['covariates']['male_share'])}, ritmo chocável {pct(t['poor']['covariates']['shockable_share'])}, "
            f"TTM {t['poor']['covariates']['TTM_counts']}.",
            f"Mann–Whitney bilateral p = {t['mann_whitney_p_two_sided']:.3g}. Pulados por falta de 30 min limpos: bom "
            f"{len(t['skipped']['good'])}, ruim {len(t['skipped']['poor'])}. **Isto não testa a dissociação.**"])
    if e24:
        t = e24
        ex = t.get("exploratory_not_preregistered", {})
        section("E2.4 — Checagem da auditoria (Paper 2, R2.4)", t, [
            f"CHB-MIT (regra pré-registrada, 30 primeiros arquivos): {t['chbmit']['n_with_cardiac']}/{t['chbmit']['n_files']} com ECG/EKG. "
            f"Os 30 são todos do paciente chb01.",
            f"Exploratório, não pré-registrado (primeiro arquivo de cada paciente): {ex.get('n_with_cardiac')}/{ex.get('n_patients')} pacientes com ECG." if ex else "",
            f"VitalDB: {t['vitaldb'].get('cases_with_any_eeg_track')}/{t['vitaldb'].get('n_cases_total')} casos com trilhas de EEG bruto "
            f"({', '.join(t['vitaldb'].get('eeg_track_names', []))}). A Tabela 1 classifica o VitalDB como sem EEG bruto (só índice); isso está errado. "
            f"Continua sem o contraste recuperação × não-recuperação.", "TUH EEG: não checado (exige pedido de acesso)."])
    if e11:
        t = e11
        section("E1.1 — Rastreamento de saída × estado completo (Paper 1, R-A1)", t, [
            "| Condição | c | k | var(y) média | var(y)/(σ²/2) | var(x − r) média |", "|---|---|---|---|---|---|",
            *[f"| {r['condition']} | {r['c']} | {r['k']} | {r['var_y_mean']:.4f} | {r['var_y_over_ref']:.3f} | {r['var_x_minus_r_mean']:.4f} |" for r in t["table"]]])
    if e12:
        t = e12
        section("E1.2 — Tempo de recorrência × dimensão (Paper 1, R-A2)", t, [
            "| d | média | desvio | Kac (10ᵈ) | razão | dentro de ±15% |", "|---|---|---|---|---|---|",
            *[f"| {r['d']} | {r['mean']:.1f} | {r['sd']:.1f} | {r['kac_expected']:.0f} | {r['ratio_to_kac']:.3f} | {'sim' if r['within_15pct'] else 'não'} |" for r in t["rows"]],
            "", f"Inclinação de log₁₀(média) contra d: {t['slope_log10_mean_vs_d']:.3f}."])
    out += ["## E3.4 — Recodificação do survey (R3.4)", "",
            "Não executado: o plano fixa início a partir de 07/10/2026 e exige recodificação cega. Ver `experiments/E3.4_DEFERRED.md`.", ""]
    open(os.path.join(HERE, "RESULTADOS_2026-09-27.md"), "w").write("\n".join(l for l in out if l is not None) + "\n")
    print("wrote RESULTADOS_2026-09-27.md")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "HEAD")
