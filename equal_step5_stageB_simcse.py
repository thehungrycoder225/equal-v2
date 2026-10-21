"""Stage B: unsupervised SimCSE domain adaptation of the Stage A encoder.
Train/test split is by employer_id; all metrics are computed on held-out employers only."""
import os, re, json
os.environ["LOKY_MAX_CPU_COUNT"] = "4"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
import numpy as np, pandas as pd, torch
from sentence_transformers import SentenceTransformer, losses, InputExample
from torch.utils.data import DataLoader
from sklearn.model_selection import GroupKFold, cross_val_predict
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, silhouette_score
from sklearn.cluster import KMeans

SEED = 42
BASE = "paraphrase-multilingual-MiniLM-L12-v2"
OUT = "outputs/equal_step5_stageB_simcse"
os.makedirs(OUT, exist_ok=True)
torch.manual_seed(SEED); np.random.seed(SEED)

u = pd.read_csv("outputs/equal_step4_sentence_embeddings/step4_sentence_units.csv")
emps = np.array(sorted(u.employer_id.unique()))
rng = np.random.RandomState(SEED); rng.shuffle(emps)
test_emps = set(emps[: int(0.2 * len(emps))])
train = u[~u.employer_id.isin(test_emps)]
test = u[u.employer_id.isin(test_emps)]
train_texts = train.sentence.drop_duplicates().tolist()
test_texts = test.sentence.drop_duplicates().tolist()
print(f"employers train/test: {len(emps)-len(test_emps)}/{len(test_emps)}; unique sentences train/test: {len(train_texts)}/{len(test_texts)}")

# Unsupervised SimCSE: positive pair = same sentence encoded twice (dropout noise)
model = SentenceTransformer(BASE)
model.max_seq_length = 128
ex = [InputExample(texts=[t, t]) for t in train_texts]
dl = DataLoader(ex, shuffle=True, batch_size=64)
loss = losses.MultipleNegativesRankingLoss(model, scale=20.0)
model.fit(train_objectives=[(dl, loss)], epochs=1, warmup_steps=10,
          optimizer_params={"lr": 2e-5}, show_progress_bar=False)
model.save(f"{OUT}/model")
base = SentenceTransformer(BASE)

def enc(m, t):
    return m.encode(t, batch_size=128, normalize_embeddings=True, show_progress_bar=False)

def cos(m, a, b):
    return (enc(m, a) * enc(m, b)).sum(1)

rows = []
sample = pd.Series(test_texts).sample(min(600, len(test_texts)), random_state=SEED).tolist()

def perturb_tests(name, m):
    E = enc(m, sample)
    rp = rng.randint(0, len(sample), (2000, 2))
    rnd = (E[rp[:, 0]] * E[rp[:, 1]]).sum(1)
    rows.append((name, "random_pair_median", float(np.median(rnd))))
    for pn, f in [("lowercase", str.lower), ("UPPERCASE", str.upper),
                  ("bullet_prefix", lambda s: "• " + s)]:
        P = enc(m, [f(s) for s in sample])
        c = (E * P).sum(1)
        top1 = ((P @ E.T).argmax(1) == np.arange(len(sample))).mean()
        rows.append((name, f"{pn}_median_cos", float(np.median(c))))
        rows.append((name, f"{pn}_self_top1", float(top1)))

perturb_tests("base", base); perturb_tests("simcse", model)

pairs = {
    "gender_swap": [("Preferably Male", "Preferably Female"), ("Male applicants only", "Female applicants only")],
    "negation": [("Willing to work night shift", "Not willing to work night shift"),
                 ("With work experience", "Without work experience")],
    "numeric": [("At least 1 year experience", "At least 5 years experience"),
                ("At least 1 year experience", "At most 1 year experience")],
    "paraphrase": [("Must be a college graduate", "Should hold a college degree"),
                   ("Good communication skills", "Excellent communication skills")],
}
for k, ps in pairs.items():
    a, b = [p[0] for p in ps], [p[1] for p in ps]
    for name, m in [("base", base), ("simcse", model)]:
        rows.append((name, f"pair_{k}_mean_cos", float(cos(m, a, b).mean())))

# probe: years-of-experience bucket on held-out employers only (grouped CV)
def yrs(s):
    m = re.search(r"(\d+)\s*(?:\+)?\s*(?:year|yr)", s, re.I)
    if not m: return None
    n = int(m.group(1)); return "0-1" if n <= 1 else ("2-3" if n <= 3 else "4+")
tt = test.drop_duplicates("sentence").copy()
tt["y"] = tt.sentence.map(yrs)
ty = tt.dropna(subset=["y"])
for name, m in [("base", base), ("simcse", model)]:
    X = enc(m, ty.sentence.tolist())
    pred = cross_val_predict(LogisticRegression(max_iter=2000, class_weight="balanced"), X, ty.y,
                             groups=ty.employer_id, cv=GroupKFold(5))
    rows.append((name, "probe_years_macroF1", float(f1_score(ty.y, pred, average="macro"))))
    Xa = enc(m, tt.sentence.tolist())
    lab = KMeans(6, n_init=10, random_state=SEED).fit_predict(Xa)
    rows.append((name, "silhouette_k6", float(silhouette_score(Xa, lab))))

res = pd.DataFrame(rows, columns=["model", "metric", "value"]).pivot(index="metric", columns="model", values="value")
res["delta"] = res["simcse"] - res["base"]
res.round(3).to_csv(f"{OUT}/step5_base_vs_simcse.csv")
print(res.round(3).to_string())
print("probe n:", len(ty), ty.y.value_counts().to_dict())
