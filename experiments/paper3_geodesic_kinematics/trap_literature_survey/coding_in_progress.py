# WORK IN PROGRESS (paused 2026-09-23): candidates 1-5 coded; screening resumes at rank 6.
# Not results. Coding rules: PRE-REGISTRATION.md.
# survey coding, appended batch by batch: rank -> dict
CODES = {}
EXCL = {}
def inc(rank, pmc, **kw): CODES[rank] = dict(pmcid=pmc, **kw)
def exc(rank, pmc, why): EXCL[rank] = dict(pmcid=pmc, why=why)

inc(1,"PMC11991455", task="MI and P300 BCI benchmark (MOABB, 20 databases)",
    centre=("N/A",""),
    dependence=("Yes","'estimated via a within-session stratified 5-fold cross-validation' (trials of a session assigned to folds at random)"),
    pseudo=("No","paired tests across subjects within each database"),
    ocular=("Yes","'all available trials were used without any artifact rejection' (cue-based MI/P300; frontal channels in the covariance)"),
    recording=("No","MI/P300 classes interleaved within runs"))
exc(2,"PMC12521986","fNIRS, not EEG")
inc(3,"PMC12431285", task="same-limb motor imagery (BCI Competition IV-2a, custom NeuroSCP)",
    centre=("N/A",""),
    dependence=("Yes","'a stratified five-fold cross-validation was applied' to trials within subject"),
    pseudo=("N/A","per-subject evaluation"),
    ocular=("Yes","'we did not use artifact removal and rejection methods' (cue-based MI)"),
    recording=("No","classes interleaved within runs / segmented phases within trials"))
inc(4,"PMC11963017", task="GREEN: age, dementia, eyes-closed vs eyes-open prediction",
    centre=("N/A",""),
    dependence=("Unclear","'100 Monte-Carlo splits, 20 % test set size'; whether splits are by subject or by window is not stated in the extracted methods"),
    pseudo=("Unclear","not determinable from methods text"),
    ocular=("No","'For the eyes-open versus eyes-closed classification task, we additionally included an ICA ... step to remove ocular artifacts that would otherwise be trivially predictive'"),
    recording=("Unclear","origin of EO/EC labels (separate recordings or segments) not stated in extracted text"))
inc(5,"PMC12319850", task="Deep Riemannian networks (SPDNet) for MI/ERP decoding, five public datasets",
    centre=("N/A",""),
    dependence=("No","'For final evaluation we used the default train/test splits of all datasets' (session-wise splits)"),
    pseudo=("N/A","per-subject evaluation"),
    ocular=("Yes","no ocular artefact handling reported; frontal channels in MI montages"),
    recording=("No","classes interleaved within runs"))
