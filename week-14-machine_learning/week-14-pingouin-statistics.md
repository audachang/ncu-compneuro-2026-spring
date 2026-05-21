# Week 14 (Supplement): 統計分析的 Python 套件 — Pingouin

> **Course**: NS5116 電腦硬體與程式語言在行為科學實驗與大數據分析之應用
> **Week / Date**: Week 14 — 2026 Spring
> **Companion to**: Chapter 03 *Fundamental Statistics* (week-14-machine_learning_v1)
> **Prerequisites**: NumPy (W7), pandas (W12), Plotly (W13), Streamlit (W11–W12)

---

## Learning Objectives (學習目標)

完成本單元後，學生應能：

1. **說明** `pingouin` 與 `scipy.stats`、`statsmodels` 在 API 設計與輸出格式上的差異。
2. **執行** 行為實驗常用的 statistical test：independent / paired t-test、Wilcoxon、ANOVA、repeated-measures ANOVA。
3. **解讀** pingouin 輸出表格中的 effect size (Cohen's d, η²)、confidence interval、Bayes Factor。
4. **計算** Pearson、Spearman、partial correlation，並繪製 correlation matrix。
5. **整合** pingouin 結果與 Plotly 視覺化，並用 Streamlit 部署為互動式統計報告 dashboard。
6. **判斷** 在 publication-ready 報告中應引用哪些欄位（p-value、effect size、CI、df）。

---

## Why This Matters (動機)

你剛跑完一個 Stroop 實驗，需要回答兩個問題：(1) congruent vs. incongruent 的 RT 差異是否顯著？(2) 這個差異有多大？

過去你可能會寫：

```python
from scipy import stats
t, p = stats.ttest_rel(congruent_rt, incongruent_rt)
print(t, p)
```

但 **論文 Methods 與 Results 章節要求的不只是 `t` 與 `p`**：reviewer 會要求 effect size (Cohen's d)、degrees of freedom、95% CI，有時還要 Bayes Factor。用 `scipy.stats` 你得自己組起來；用 `pingouin`，一行就能拿到全部欄位，且輸出是一個整齊的 `pandas.DataFrame`，可以直接 `to_latex()` 或 `st.dataframe()`。

對 behavioral / cognitive neuroscience 研究者而言，pingouin 的 API 設計 *貼近你寫論文時思考的單位* — 一個 test 一個表格，而不是分散的 namedtuple。

---

## Demo Scripts 索引

所有範例程式碼都放在 [`code/pingouin/`](code/pingouin/)，每個 script 可獨立執行（含完整 `import` 與 `np.random.seed`），對應講義的章節如下：

| 章節 | Script | 主題 |
|------|--------|------|
| §1 安裝與 API 哲學 | [`01_intro_api.py`](code/pingouin/01_intro_api.py) | scipy.stats vs. pingouin 對照 |
| §2 t-test 家族 | [`02_ttest_family.py`](code/pingouin/02_ttest_family.py) | paired / independent / one-sample + Wilcoxon + effect size |
| §3 ANOVA | [`03_anova.py`](code/pingouin/03_anova.py) | one-way / rm-ANOVA / mixed ANOVA + post-hoc |
| §4 Correlation | [`04_correlation.py`](code/pingouin/04_correlation.py) | Pearson / Spearman / partial corr / matrix |
| §5 Streamlit 部署 | [`05_streamlit_stats_app.py`](code/pingouin/05_streamlit_stats_app.py) | 互動式 dashboard |
| — | [`requirements.txt`](code/pingouin/requirements.txt) | 套件版本鎖定（部署用） |
| — | [`README.md`](code/pingouin/README.md) | 執行與部署完整說明 |

**快速開始**：

```bash
cd code/pingouin
pip install -r requirements.txt
python 01_intro_api.py            # 跑單一範例
streamlit run 05_streamlit_stats_app.py  # 啟動 dashboard
```

---

## In-Class Topics (課堂內容)

### 1. 安裝與 API 哲學 (10 min)

**為什麼重要**：理解 pingouin 的 *one test = one DataFrame* 設計，能幫你之後快速組裝 publication-ready 表格。

```bash
pip install pingouin
```

**最小範例** — 用 `scipy.stats` 與 `pingouin` 跑同一個 paired t-test：

*📄 [`code/pingouin/01_intro_api.py`](code/pingouin/01_intro_api.py)*

```python
import numpy as np
import pandas as pd
from scipy import stats
import pingouin as pg

np.random.seed(42)
# 模擬 30 位受試者的 Stroop RT (within-subject)
congruent = np.random.normal(450, 60, 30)
incongruent = np.random.normal(520, 80, 30)

# --- scipy.stats: 簡潔但欄位少 ---
t_scipy, p_scipy = stats.ttest_rel(congruent, incongruent)
print(f"scipy: t={t_scipy:.3f}, p={p_scipy:.4f}")

# --- pingouin: 一行回傳整個表格 ---
result = pg.ttest(congruent, incongruent, paired=True)
print(result)
```

預期輸出（pingouin 部分，version ≥ 0.6）：

```
              T  dof alternative      p_val            CI95   cohen_d     power     BF10
T_test  -4.478   29   two-sided   0.000112  [-99.6, -37.5]    1.101    0.9999  242.203
```

**注意**：pingouin 一次給你 `T`, `dof`, `p_val`, `CI95`, `cohen_d`, `BF10`, `power` — 寫論文時的 Methods 與 Results 段都能直接抄。

> ⚠️ **欄位命名注意**：pingouin 0.6 之後欄位名改用 underscore（`p_val`, `cohen_d`, `CI95`），舊版（≤ 0.5）是 `p-val`, `cohen-d`, `CI95%`。本講義以 0.6.1 為準。請先用 `pip show pingouin` 確認版本。

#### 🔬 Hands-on Practice 1: 比較兩個工具的輸出

**任務**：對相同的 RT 資料分別跑 `scipy.stats.ttest_rel` 與 `pg.ttest`，並把 pingouin 的 effect size (`cohen-d`) 與 Bayes Factor (`BF10`) 印出來。寫一句話：BF10 > 10 代表什麼？

```python
import numpy as np
import pingouin as pg
np.random.seed(0)
young = np.random.normal(400, 50, 25)
old   = np.random.normal(480, 70, 25)
# 你的程式碼從這裡開始
```

<details>
<summary>✅ 參考解答</summary>

```python
res = pg.ttest(young, old, paired=False)
print(res[['T', 'p_val', 'cohen_d', 'BF10']])
# BF10 > 10 表示 H1 (兩群有差異) 的證據強度是 H0 的 10 倍以上 — strong evidence
```

</details>

---

### 2. 行為實驗常見 test：t-test 家族與 effect size (20 min)

**為什麼重要**：reaction time、accuracy 是行為實驗最常見的 dependent variable，比較組別差異幾乎都用 t-test 或其 non-parametric 版本。

#### 2.1 三種 t-test 寫法

*📄 [`code/pingouin/02_ttest_family.py`](code/pingouin/02_ttest_family.py)*

```python
import numpy as np
import pingouin as pg
np.random.seed(42)

# 模擬 Stroop 資料
n = 30
congruent   = np.random.normal(450, 60, n)
incongruent = np.random.normal(520, 80, n)
baseline    = np.full(n, 500)  # 對照基準值

# (a) Paired (within-subject)
print("Paired t-test (congruent vs. incongruent):")
print(pg.ttest(congruent, incongruent, paired=True))

# (b) Independent (between-group)
print("\nIndependent t-test (congruent vs. baseline as different groups):")
print(pg.ttest(congruent, baseline, paired=False))

# (c) One-sample (與某個固定值比較)
print("\nOne-sample t-test (RT vs. 500ms):")
print(pg.ttest(congruent, 500))
```

#### 2.2 違反 normality 假設時：Wilcoxon

當 RT 分布嚴重 skewed（常見於老人受試者或臨床族群），改用 non-parametric test：

```python
print(pg.wilcoxon(congruent, incongruent, alternative='two-sided'))
# 或 Mann-Whitney U（independent samples）
print(pg.mwu(congruent, baseline))
```

#### 2.3 effect size：為什麼 p < .05 不夠

```python
# 直接計算 Cohen's d
d = pg.compute_effsize(congruent, incongruent, paired=True, eftype='cohen')
print(f"Cohen's d = {d:.3f}")
# 慣例：|d| ≈ 0.2 small, 0.5 medium, 0.8 large
```

**常見錯誤**：
- ❌ 只報告 `p < .05`，不附 effect size → reviewer 會打回票。
- ❌ 在 paired data 上用 `pg.ttest(..., paired=False)` → 失去 within-subject power。
- ✅ 確認 design 是 within 或 between，再選 `paired=True/False`。

#### 🔬 Hands-on Practice 2: 完整的 Stroop effect 報告

**任務**：用以下資料，產出 *一張 DataFrame*，包含：(1) paired t-test 結果，(2) Wilcoxon test 結果。並印出一句 APA-style 結果報告。

```python
import numpy as np
import pingouin as pg
import pandas as pd
np.random.seed(7)
congruent = np.random.normal(460, 55, 28)
incongruent = np.random.normal(530, 75, 28)
# 你的程式碼從這裡開始
```

<details>
<summary>💡 提示</summary>

`pd.concat([df1, df2])` 可把兩個結果表合併。APA-style 範例：*Paired-samples t-test revealed a significant Stroop effect, t(27) = -4.21, p < .001, Cohen's d = 0.77, 95% CI [-94, -33]*。

</details>

<details>
<summary>✅ 參考解答</summary>

```python
t_res = pg.ttest(congruent, incongruent, paired=True)
w_res = pg.wilcoxon(congruent, incongruent)
report = pd.concat([t_res, w_res], keys=['paired-t', 'wilcoxon'])
print(report[['p_val', 'CI95', 'cohen_d']])

r = t_res.iloc[0]
print(f"\nt({int(r['dof'])}) = {r['T']:.2f}, p = {r['p_val']:.3f}, "
      f"d = {r['cohen_d']:.2f}, 95% CI {r['CI95']}")
```

</details>

---

### 3. ANOVA 與 repeated-measures ANOVA (25 min)

**為什麼重要**：認知實驗常是 2 × 2 factorial design — 例如 *age (young/old) × condition (congruent/incongruent)*。Repeated-measures ANOVA (rm-ANOVA) 是這類設計的核心工具。

#### 3.1 One-way ANOVA：N-back 三個 working memory load

*📄 [`code/pingouin/03_anova.py`](code/pingouin/03_anova.py)*

```python
import numpy as np
import pandas as pd
import pingouin as pg
np.random.seed(42)

# 模擬 N-back 任務：每位受試者跑 1-back, 2-back, 3-back
def simulate_nback(n_subjects=30):
    rows = []
    for sid in range(n_subjects):
        for load, base_rt in [('1-back', 500), ('2-back', 580), ('3-back', 680)]:
            rt = np.random.normal(base_rt, 70)
            rows.append({'subject': sid, 'load': load, 'rt': rt})
    return pd.DataFrame(rows)

df = simulate_nback()
print(df.head())

# Between-subject one-way ANOVA（如果 load 是 between）
print("\nOne-way ANOVA:")
print(pg.anova(data=df, dv='rt', between='load', detailed=True))
```

輸出包含 `SS`, `DF`, `MS`, `F`, `p_unc`, `np2` (partial η²) — 全部寫論文需要的欄位。

#### 3.2 Repeated-measures ANOVA：同一受試者跑多個 condition

```python
# 同一筆資料，但是 within-subject design
print("\nRepeated-measures ANOVA:")
rm = pg.rm_anova(data=df, dv='rt', within='load', subject='subject', detailed=True)
print(rm)
```

注意 `rm_anova` 輸出多了 `eps` (Greenhouse-Geisser ε) 與 `ng2` (generalized η²)。在 0.6+ 版本中，rm_anova 使用 `ng2` 取代舊版的 `np2`；若需要 partial η²，可以另外用 `pg.anova(...)` 或自行計算。若 ε < 0.75，引用時要用修正後的 p-value。

#### 3.3 Post-hoc：哪兩個 condition 有差？

```python
# Pairwise t-tests with Bonferroni correction
posthoc = pg.pairwise_tests(
    data=df, dv='rt', within='load', subject='subject',
    padjust='bonf'
)
print(posthoc[['A', 'B', 'T', 'p_corr', 'p_adjust', 'hedges']])
```

#### 3.4 Two-way mixed ANOVA：age × condition

```python
np.random.seed(1)
rows = []
for sid in range(40):
    age = 'young' if sid < 20 else 'old'
    for cond in ['congruent', 'incongruent']:
        base = 450 if cond == 'congruent' else 520
        if age == 'old':
            base += 80
        rt = np.random.normal(base, 60)
        rows.append({'subject': sid, 'age': age, 'cond': cond, 'rt': rt})

mixed_df = pd.DataFrame(rows)
print(pg.mixed_anova(data=mixed_df, dv='rt',
                     within='cond', between='age', subject='subject'))
```

**常見錯誤**：
- ❌ 資料是 wide format（每個 condition 一個 column）→ pingouin 需要 *long format*。先用 `df.melt()` 轉換。
- ❌ 忘了傳 `subject=` → rm-ANOVA 會錯誤識別為 between-subject。

#### 🔬 Hands-on Practice 3: 三組老化研究

**任務**：模擬 young / middle-aged / old 三組，每組 20 人，做一次 reaction-time task。跑 one-way ANOVA 與 post-hoc Tukey HSD，並指出哪兩組有顯著差異。

```python
import numpy as np
import pandas as pd
import pingouin as pg
np.random.seed(42)
rows = []
for grp, mu in [('young', 420), ('middle', 480), ('old', 560)]:
    for _ in range(20):
        rows.append({'group': grp, 'rt': np.random.normal(mu, 70)})
df = pd.DataFrame(rows)
# 你的程式碼從這裡開始
```

<details>
<summary>✅ 參考解答</summary>

```python
print(pg.anova(data=df, dv='rt', between='group', detailed=True))
print(pg.pairwise_tukey(data=df, dv='rt', between='group'))
```

</details>

---

### 4. Correlation 與 partial correlation (20 min)

**為什麼重要**：在 individual differences 研究中（例如 working memory capacity 與 fluid intelligence 的關係），你常需要控制第三變項 (age, education)。`pingouin` 的 `partial_corr` 是這類分析最乾淨的 API。

#### 4.1 兩變項 correlation

*📄 [`code/pingouin/04_correlation.py`](code/pingouin/04_correlation.py)*

```python
import numpy as np
import pandas as pd
import pingouin as pg
np.random.seed(42)

n = 100
wm = np.random.normal(50, 10, n)              # working memory score
gf = 0.5 * wm + np.random.normal(0, 8, n)     # fluid intelligence
age = np.random.uniform(20, 70, n)            # 干擾變項

df = pd.DataFrame({'wm': wm, 'gf': gf, 'age': age})

# Pearson
print(pg.corr(df['wm'], df['gf'], method='pearson'))
# Spearman (rank-based, robust to outliers)
print(pg.corr(df['wm'], df['gf'], method='spearman'))
```

輸出包含 `n`, `r`, `CI95`, `p_val`, `BF10`, `power`。

#### 4.2 Partial correlation：控制 age 後 wm-gf 關係

```python
# 控制 age 之後，wm 與 gf 的相關
print(pg.partial_corr(data=df, x='wm', y='gf', covar='age'))
```

如果 `r` 在控制 age 後大幅下降，代表原始相關有一部分是 age 造成的 spurious correlation。

#### 4.3 整個 correlation matrix

```python
# 一次跑所有變項兩兩相關，含 p-value 與 FDR 校正
print(df.rcorr(padjust='fdr_bh', stars=True))
```

輸出右上三角是 r，左下三角是星號標示的 p-value，適合直接放進 supplementary table。

#### 🔬 Hands-on Practice 4: WM、Gf、Education 三變項

**任務**：用 `pg.partial_corr` 分別控制 (a) age, (b) education，看 WM-Gf 相關係數如何變化。

```python
import numpy as np
import pandas as pd
import pingouin as pg
np.random.seed(0)
n = 80
age = np.random.uniform(20, 70, n)
edu = np.random.uniform(9, 20, n)
wm  = 0.3*edu - 0.1*age + np.random.normal(50, 8, n)
gf  = 0.4*wm + 0.2*edu + np.random.normal(0, 5, n)
df = pd.DataFrame({'wm': wm, 'gf': gf, 'age': age, 'edu': edu})
# 你的程式碼從這裡開始
```

<details>
<summary>✅ 參考解答</summary>

```python
print("Control age:")
print(pg.partial_corr(data=df, x='wm', y='gf', covar='age'))
print("\nControl edu:")
print(pg.partial_corr(data=df, x='wm', y='gf', covar='edu'))
print("\nControl both:")
print(pg.partial_corr(data=df, x='wm', y='gf', covar=['age', 'edu']))
```

</details>

---

### 5. Streamlit 部署：互動式統計報告 Dashboard (25 min)

**為什麼重要**：分析結果若只在 Jupyter 裡，合作者無法即時探索。把 pingouin 的 DataFrame 接到 Streamlit，能讓 PI 或實驗夥伴用瀏覽器自己挑 condition、看結果。

#### 5.1 應用情境

我們做一個 **Stroop / Flanker / N-back dashboard**：
- 上傳或選擇一個 task 的 trial-by-trial CSV。
- 自動跑 paired t-test、rm-ANOVA、effect size。
- 用 Plotly 畫 RT distribution 與 condition × group 對比。
- 結果表格可直接下載 (CSV)。

#### 5.2 完整程式碼

*📄 [`code/pingouin/05_streamlit_stats_app.py`](code/pingouin/05_streamlit_stats_app.py)*

```python
"""
Streamlit 互動式統計報告 dashboard
執行方式：streamlit run streamlit_stats_app.py
"""
import numpy as np
import pandas as pd
import pingouin as pg
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Behavioral Stats Dashboard", layout="wide")
st.title("行為實驗統計報告 Dashboard")
st.caption("Pingouin + Plotly + Streamlit — Week 14 demo")

# --- 1. 資料：上傳或使用模擬資料 ---
@st.cache_data
def simulate_data(n_subj=30, seed=42):
    rng = np.random.default_rng(seed)
    rows = []
    for sid in range(n_subj):
        group = 'young' if sid < n_subj // 2 else 'old'
        age_offset = 0 if group == 'young' else 80
        for cond, mu in [('congruent', 450), ('incongruent', 520)]:
            for trial in range(20):
                rt = rng.normal(mu + age_offset, 60)
                acc = rng.binomial(1, 0.9 if cond == 'congruent' else 0.82)
                rows.append({
                    'subject': sid, 'group': group, 'condition': cond,
                    'trial': trial, 'rt': rt, 'accuracy': acc,
                })
    return pd.DataFrame(rows)

with st.sidebar:
    st.header("資料來源")
    uploaded = st.file_uploader("上傳 trial CSV", type=['csv'])
    if uploaded is not None:
        df = pd.read_csv(uploaded)
    else:
        st.info("使用模擬資料（30 受試者 × 2 condition × 20 trials）")
        df = simulate_data()

    st.header("分析參數")
    rt_lower = st.slider("RT lower bound (ms)", 100, 400, 200)
    rt_upper = st.slider("RT upper bound (ms)", 800, 2000, 1500)
    only_correct = st.checkbox("只分析 correct trials", value=True)

# --- 2. Cleaning ---
df_clean = df[(df['rt'] >= rt_lower) & (df['rt'] <= rt_upper)]
if only_correct and 'accuracy' in df.columns:
    df_clean = df_clean[df_clean['accuracy'] == 1]

st.subheader("資料概覽")
c1, c2, c3 = st.columns(3)
c1.metric("受試者數", df_clean['subject'].nunique())
c2.metric("總 trial 數", len(df_clean))
c3.metric("Conditions", df_clean['condition'].nunique())

# --- 3. 每位受試者的 mean RT ---
subj_mean = (
    df_clean.groupby(['subject', 'group', 'condition'])['rt']
    .mean()
    .reset_index()
)

# --- 4. Visualisation ---
st.subheader("RT 分布")
fig = px.box(
    subj_mean, x='condition', y='rt', color='group',
    points='all', title="Subject-level mean RT by condition × group"
)
st.plotly_chart(fig, use_container_width=True)

# --- 5. 統計分析 (Pingouin) ---
st.subheader("統計分析")

tab1, tab2, tab3 = st.tabs(["Paired t-test", "Mixed ANOVA", "Correlation"])

with tab1:
    st.write("**Stroop effect — paired t-test (congruent vs. incongruent)**")
    wide = subj_mean.pivot(index='subject', columns='condition', values='rt').dropna()
    t_res = pg.ttest(wide['congruent'], wide['incongruent'], paired=True)
    st.dataframe(t_res.round(4))
    st.download_button(
        "下載 t-test 結果 CSV",
        t_res.to_csv(index=False).encode('utf-8'),
        file_name="ttest_result.csv",
    )

with tab2:
    st.write("**Mixed ANOVA — condition (within) × group (between)**")
    aov = pg.mixed_anova(
        data=subj_mean, dv='rt', within='condition',
        between='group', subject='subject'
    )
    st.dataframe(aov.round(4))

    st.write("**Post-hoc pairwise tests (Bonferroni)**")
    posthoc = pg.pairwise_tests(
        data=subj_mean, dv='rt', within='condition',
        between='group', subject='subject', padjust='bonf'
    )
    st.dataframe(posthoc.round(4))

with tab3:
    st.write("**Correlation matrix（每位受試者層級）**")
    wide_corr = subj_mean.pivot(
        index='subject', columns='condition', values='rt'
    )
    wide_corr['stroop_effect'] = wide_corr['incongruent'] - wide_corr['congruent']
    st.dataframe(wide_corr.rcorr(stars=True))

st.markdown("---")
st.caption("Built with pingouin + plotly + streamlit · NS5116 2026 Spring")
```

#### 5.3 執行與部署

本機執行：

```bash
cd code/pingouin
pip install -r requirements.txt
streamlit run 05_streamlit_stats_app.py
```

部署到 Streamlit Community Cloud：
1. 把這個檔案與同目錄的 [`code/pingouin/requirements.txt`](code/pingouin/requirements.txt) push 到 GitHub repo。
2. 到 [share.streamlit.io](https://share.streamlit.io) → New app → 選 repo / branch → Main file path 設為 `code/pingouin/05_streamlit_stats_app.py` → Deploy。
3. 取得 public URL，可貼到 supplementary materials 或分享給 collaborator。

> 詳見 [`code/pingouin/README.md`](code/pingouin/README.md) 完整說明（包含所有 demo scripts 的執行方式與 troubleshooting）。

#### 🔬 Hands-on Practice 5: 加入 Wilcoxon tab

**任務**：在現有 app 中加入第四個 tab "Non-parametric"，當使用者點選時，跑 Wilcoxon signed-rank test 並顯示結果與 effect size (`r` from Wilcoxon)。

<details>
<summary>💡 提示</summary>

```python
with tab4:  # 新增 tab4
    w = pg.wilcoxon(wide['congruent'], wide['incongruent'])
    st.dataframe(w.round(4))
```

別忘了改 `st.tabs([...])` 加入新名稱。

</details>

---

## Recap & Common Pitfalls (重點回顧與常見錯誤)

| 概念 | 一句話總結 |
|------|-----------|
| API 哲學 | 一個 test = 一個 DataFrame，欄位涵蓋 publication 所需 |
| t-test | `pg.ttest()` 自動回傳 Cohen's d, CI, BF10, power |
| ANOVA | `pg.anova` (between)、`pg.rm_anova` (within)、`pg.mixed_anova` (兩者) |
| Post-hoc | `pg.pairwise_tests(padjust='bonf')` 或 `pg.pairwise_tukey` |
| Correlation | `pg.corr` (兩變項)、`pg.partial_corr` (控制 covariates)、`df.rcorr()` (matrix) |
| Streamlit 整合 | pingouin 回傳的就是 DataFrame，直接餵給 `st.dataframe` 與 `st.download_button` |

**最容易犯的錯**：

1. **Wide format 餵給 long format API** — `rm_anova` 要 long format，用 `df.melt()` 轉。
2. **忽略 effect size** — 只報 p-value，論文 reviewer 會要求補。
3. **Paired/Independent 弄反** — within-subject design 一定要 `paired=True`。
4. **Sphericity 違反** — `pg.rm_anova` 會自動回報 Greenhouse-Geisser ε；若 ε < 0.75，引用 GG 修正後的 p-value 而不是 `p_unc`。
5. **多重比較未校正** — 跑 pairwise 時一定加 `padjust='bonf'` 或 `'fdr_bh'`。

---

## Homework (作業)

**繳交格式**：`week-14-pingouin-hw.ipynb` + 部署上線的 Streamlit URL。

**任務**：

1. **資料準備**（10%）：使用課程 GitHub 上提供的 `flanker_data.csv`（或自行用 `simulate_data()` 生成），檔案需包含 columns: `subject`, `group`, `condition`, `rt`, `accuracy`。
2. **描述性統計**（15%）：用 pingouin 的 `pg.normality()` 與 `pg.homoscedasticity()` 檢查假設。
3. **推論統計**（30%）：
   - 跑 mixed ANOVA (`group × condition`)。
   - 若有顯著互動，做 simple effects analysis。
   - 報告 effect size 與 95% CI。
4. **Correlation 分析**（15%）：計算每位受試者的 Flanker effect (incongruent − congruent RT)，並與 accuracy 做 partial correlation（控制 age）。
5. **Streamlit dashboard**（25%）：擴充課堂範例，加入：
   - 多個任務切換 (Stroop / Flanker / N-back)
   - 一個讓使用者選擇 effect size 計算方法的 selectbox (Cohen's d / Hedges' g)
   - 統計結果表格的下載按鈕
6. **APA-style writeup**（5%）：用一段（≤ 200 字）描述你的分析結果，符合 APA 7th 引文格式。

**Rubric**：每題依「程式可執行（40%）」、「分析正確（40%）」、「報告清晰（20%）」評分。

---

## References & Further Reading

- Vallat, R. (2018). Pingouin: statistics in Python. *Journal of Open Source Software*, 3(31), 1026. [https://doi.org/10.21105/joss.01026](https://doi.org/10.21105/joss.01026)
- Pingouin documentation: [https://pingouin-stats.org/](https://pingouin-stats.org/)
- Streamlit documentation: [https://docs.streamlit.io/](https://docs.streamlit.io/)
- Lakens, D. (2013). Calculating and reporting effect sizes to facilitate cumulative science. *Frontiers in Psychology*, 4, 863.

---

*Last updated: 2026-05-21*
