# Week 15 — End-to-End Machine Learning · Speaker Notes

> 自動生成自 `speaker_notes.py`。請編輯該檔，不要直接編輯本檔。
> 對應的投影片：`week-15-slides.pptx` (49 張)。

---

## Slide 01 · Title

歡迎來到 Week 15。今天是這學期最技術性的一週 — 我們要把前面學過的 pandas、NumPy、視覺化全部串起來，
進入 machine learning。

今天的 anchor textbook 是 Aurélien Géron 的《Hands-on Machine Learning》第三版，
第二章那個經典的 California Housing 案例。我們會跟著這個案例走一遍完整的 pipeline，
然後再把同樣的工具套到一個 cogneuro 的情境上 — 預測 Stroop task 的反應時間。

提醒一下：今天涵蓋的都是 **shallow learning** — 也就是傳統 ML。Deep learning 屬於另一個範疇，
本週不涵蓋。重點是 **pipeline 與 algorithm taxonomy**，不是任何單一模型的極致最佳化。

---

## Slide 02 · Learning Objectives

這六個目標是今天結束時你應該能做到的事。

我特別強調第一個 — **Frame**。在寫任何 sklearn code 之前，你必須先回答四個問題：
這是 supervised 還是 unsupervised？是 regression 還是 classification？資料一次給齊還是逐筆進來？
模型是 model-based 還是 instance-based？

如果你能回答這四個問題，後面所有 sklearn 的選擇都會變得清楚。
反過來說，如果你跳過 framing 直接 import sklearn，你會 silently 選錯類型，所有 metric 就變得毫無意義。

---

## Slide 03 · Agenda

這是今天的時間規劃，總共三小時。

前 20 分鐘是 framing — 比較抽象但很重要。
接著 25 分鐘是 California Housing 的資料探索與切分。
然後 30 分鐘做 preprocessing pipeline — 這是整堂課的技術核心。
40 分鐘的 algorithm zoo 是內容最多的部分，會看五大類 algorithm。
25 分鐘 evaluation 與 tuning，15 分鐘 unsupervised 小品。
最後 25 分鐘把整套 pipeline 套到 cogneuro 情境上。

每個 section 後面都有一個 hands-on practice，請大家準備好 VS Code 與 Jupyter notebook。

---

## Slide 04 · Why this matters

你們已經會用 PsychoPy 收資料，會用 pandas 整理，會用 Streamlit 展示。
今天要補上最後一塊拼圖 — **從資料中學出一個可預測的 model**。

舉一個情境：實驗室收了 200 位受試者的 Stroop task，每人 60 個 trial。
你想知道：哪些 trial-level 變項最能預測 RT？能不能在新受試者身上預測他的 RT 分布？

這個問題本身就是 supervised regression。我們今天的策略是：
先用 California Housing 跑完一遍 — 因為這個資料集乾淨、文獻多、好除錯；
然後把完全一樣的 pipeline 套到 Stroop RT 上，讓你看到 pipeline 是 domain-agnostic 的。

---

## Slide 05 · §1 divider

進入第一個 section — ML 問題的框架化。

這個 section 沒有 code，但它決定了你後面所有 code 怎麼寫。

---

## Slide 06 · Four framing questions

這四個問題是寫任何 ML code 之前必須回答的。

第一：**有沒有 label？** 有觀測值就是 supervised；沒有就是 unsupervised；部分有就是 semi-supervised。

第二：**label 的型別？** 連續值是 regression，離散值是 classification。
注意：把 RT 當 classification 的 target — 例如「快/慢」二分類 — 你會 silently 失去 ordinal 結構，
也就是「520 ms 比 500 ms 慢一點」這個資訊被完全丟掉。

第三：**資料一次給齊嗎？** 跑完實驗收到所有人是 batch；像股票價格一直進來是 online。

第四：**模型怎麼學？** Instance-based 是「記住所有 train sample，新 sample 來時找最近的」 — k-NN 就是這類；
model-based 則是「學出一組 parameter」 — linear regression、neural network 都是。

下方的紅色提醒框很重要：選錯類型會讓所有 metric 變得無意義。

---

## Slide 07 · Algorithm taxonomy map

這張圖是今天會涵蓋的 algorithm 全景。

左半邊是 **supervised**，分五大家族：linear、instance-based、tree、ensemble、kernel。
這五家族並不是排他的 — 你可以有 kernel ridge regression（linear × kernel），
也可以有 ensemble of trees（tree × ensemble），但作為教學分類它們夠用了。

右半邊是 **unsupervised**。今天我們只看 k-means 與 IsolationForest，
而且不是當主角，是當 **feature engineering 工具** 與 **outlier filter**。

底下的灰字提醒：deep learning 屬於 representation learning 範疇，本週不涵蓋。

---

## Slide 08 · Hands-on 1

第一個 hands-on。請大家花 5 分鐘，跟同桌討論這三個情境，回答四個 framing 問題。

情境 A 比較直接：清醒 vs. 睡著是二元分類。
情境 B 注意：「自動分群」這個詞就告訴你沒有預先的 label — 是 unsupervised clustering。
情境 C 最有趣 — 它可以兩種 framing 都用：如果你有專家標好的 motion artifact label，就是 supervised；
如果沒有，就用 anomaly detection (unsupervised) 找「不像正常 volume 的 volume」。

5 分鐘後我們各組分享一個情境的答案。

---

## Slide 09 · §2 divider

進入 anchor case — California Housing。

這個資料集是 ML 教學界的標準案例，因為它乾淨、量適中、有現實意義。
今天我們會跟著 Géron 走一遍。

---

## Slide 10 · Data overview

這是 1990 美國加州人口普查的 block-level 資料 — 一個 block 大約 600-3000 人。
總共 20,640 個 block，10 個欄位。

Target 是 `median_house_value`，單位 USD。
Features 包括地理位置（經緯度）、房屋年齡中位數、總房間數、總臥房數、人口、家戶數、收入中位數，
以及一個文字欄位 `ocean_proximity`。

兩個重點：`total_bedrooms` 有 207 筆缺值，需要 impute；`ocean_proximity` 是文字，需要 encoding。
這兩個 issue 是我們等下 pipeline 要處理的核心。

下方的 code 是 Géron 提供的 loader — 第一次跑會下載到 `datasets/`，之後就從 cache 讀。

---

## Slide 11 · Golden rule: split first

這張投影片只有一個訊息，但它是整堂課最重要的一個：

**拿到資料的第一件事，是切出 test set，然後鎖起來，直到最後評估前都不准看。**

為什麼？因為如果你先做 EDA，例如看了某個 feature 的分布、發現有些 outlier 想剔除，
你就 silently 把 test 的資訊納入了 design choice。這叫 **data snooping bias**，
等於把答案抄進考卷 — 你最後在 test 上的成績完全失去意義。

`random_state=42` 是 reproducibility 的關鍵。為什麼是 42？因為 Douglas Adams。
但任何固定的整數都可以，重點是 **不要每次跑不同**。

---

## Slide 12 · Stratified split

純 random split 有個問題：當某個重要 feature 分布不均時，test set 可能不能代表母體。

以 housing 為例，`median_income` 右尾很長 — 大部分 block 收入中等，少數很高。
隨機切 20% 出來，可能 high-income block 在 test 中比例偏低。

解法：把 income 切 5 個 bin，按 bin 比例分層抽樣 — `StratifiedShuffleSplit`。

這個技巧到 cogneuro 也用得到。下方藍框提示：
如果你的 dataset 中年輕人遠多於老人，random split 後 test 可能只有兩三個老人，
模型在「老人 generalization」上的結果就不可靠。用 age group stratify 才能保證 test 反映母體。

---

## Slide 13 · Hands-on 2

第二個 hands-on — 8 分鐘獨立完成。

任務：給定一個模擬 RT dataset，先用 `pd.cut` 切 4 個 age bin，
再用 `StratifiedShuffleSplit` 切 20% test，最後驗證 train/test 各 bin 比例差異 < 1%。

寫完之後跟同桌互看程式碼。常見的卡點是 `pd.cut` 的 `bins` 與 `labels` 長度要差 1。

---

## Slide 14 · §3 divider

進入第三 section — preprocessing pipeline。

這個 section 是整堂課技術上最關鍵的部分。如果你只記得一件事，就是：
**所有 preprocessing 步驟，要先在 train 上 fit，再 transform 到 test。**

---

## Slide 15 · Pipeline why

為什麼需要 Pipeline？

最常見的錯誤是這樣：學生把 train 與 test concatenate 起來，一起 `fit_transform(StandardScaler())`。
結果是 test set 的 mean 與 std 偷渡進了 train。
模型在 train 上看似很好，在真實 deployment 時表現一落千丈。

`sklearn.pipeline.Pipeline` 就是強制你遵守「fit on train, transform on test」這條規則的工具。
整個 pipeline 像一個 model — 你對它 `fit(X_train, y_train)` 一次，對它 `predict(X_test)` 一次，
sklearn 內部會自動只用 train 的 statistics 去 transform test。

---

## Slide 16 · Pipeline flow diagram

這張流程圖把整個 preprocessing pipeline 視覺化 — 從原始 DataFrame 一路到 estimator。

上面是 raw DataFrame，混雜 numerical 與 categorical、有 missing values。
ColumnTransformer 把這個 DataFrame 「分流」 — 不同型別的欄位走不同路徑。

左邊 (藍色) 是 numerical track：先用 SimpleImputer 填中位數，再用 StandardScaler 做 z-score。
右邊 (橘色) 是 categorical track：用 OneHotEncoder 把文字類別轉成 binary columns。

兩條路徑的 output 最後 concat 起來變成 X_prepared，餵給 estimator (LinearRegression、RandomForest 等等)。

最重要的訊息在兩側：
**左綠**：對 train 用 fit_transform — 每個 step 都「學會」它需要的 statistics
（imputer 學每欄 median、scaler 學 mean 與 std、OneHotEncoder 學類別集合）。
**右紅**：對 test 只用 transform — **重用** train 學到的 statistics，**不可以**重新學一遍。

這是 leakage 防火牆的具象化 — 整條 pipeline 就是一個 model，
你對它 fit(X_train, y_train) 一次，對它 predict(X_test) 一次，sklearn 內部會自動只用 train 的 statistics。

---

## Slide 17 · Imputation

Step A — 處理 missing values。

三種選擇：drop rows、drop column、impute。前兩個都會丟資訊，所以推薦 impute。

`SimpleImputer(strategy='median')` 是最常用的 — 對 numerical feature 用 median 填，
median 比 mean 更 robust 於 outlier。

對 categorical feature 可以用 `strategy='most_frequent'`，也就是填眾數。
進階版本是 `KNNImputer` — 用鄰近 sample 的值估，但通常 SimpleImputer 就夠了。

注意：imputer 一定要放在 pipeline 裡，不要自己手動 `df.fillna(df.mean())` —
那樣做會在 cross-validation 時把整個 dataset 的 mean 算進去，造成 leakage。

---

## Slide 18 · Encoding

Step B — 處理文字類別。

兩種主要選擇：`OrdinalEncoder` 與 `OneHotEncoder`。

`OrdinalEncoder` 把每個類別映射到一個整數，例如 `<1H OCEAN` → 0、`INLAND` → 1、`ISLAND` → 2...
這對於 **有自然順序** 的類別（如 low/medium/high）是合適的，
但對於 **無序類別**（如 ocean_proximity），它會 silently 強加錯誤的順序。
Linear model 看到「INLAND 比 <1H OCEAN 大 1」會試圖學這個假關係，結果一團亂。

`OneHotEncoder` 把每個類別變成一個獨立的 binary column。
缺點是類別很多時會產生 sparse 高維 feature。但對於 < 50 個類別的情況，這是最安全的預設。

**一定要加** `handle_unknown="ignore"`，否則 test 出現訓練時沒看過的類別，整個 pipeline 會 crash。

---

## Slide 19 · Scaling

Step C — Feature scaling。

為什麼需要：基於距離的演算法 (k-NN、SVM、k-means) 與基於梯度的演算法 (linear + GD、neural net)
對 feature 的 scale 極度敏感。

舉例：housing 裡 latitude 在 ±90 範圍，median_income 在 0 到 15 範圍。
k-NN 算距離時，latitude 會壓過 income，模型基本上只在看地理座標。

三種主要 scaler：
StandardScaler：z-score 標準化，最常用。
MinMaxScaler：壓到 [0, 1]，對 outlier 敏感。
RobustScaler：用 median 與 IQR，outlier 多時的替代方案。

重要例外：**tree-based 演算法（RandomForest、GradientBoosting）不需要 scaling**。
因為 tree 是用「>X 還是 <X」做分割，與 scale 無關。但放在 pipeline 裡也沒壞處，只是浪費計算。

---

## Slide 20 · ColumnTransformer

Step D — 把所有步驟串成 ColumnTransformer。

`Pipeline` 是垂直 — 一個步驟接一個。
`ColumnTransformer` 是水平 — 不同欄位走不同路徑。

這裡的設計：numerical 欄位走 `imputer → scaler`，categorical 欄位走 `OneHotEncoder`。
兩條路徑的 output 自動 concatenate 成一個矩陣。

最關鍵的一行在下面的綠框：對 train 用 `fit_transform()`，對 test 只用 `transform()`。
pipeline 會自動處理這件事 — 你只要對整個 pipeline `fit(X_train, y_train)` 一次。

---

## Slide 21 · Hands-on 3

第三個 hands-on — 10 分鐘獨立完成。

任務：把剛剛學到的 ColumnTransformer 套到一個 trial-level dataframe 上。
有三個 feature：congruency 是字串、isi 是連續但有 missing、block_num 是整數。

最後 X 的 shape 應該是 (100, 4) — 兩個 numerical + 兩個 one-hot 的 congruency level。

如果你 shape 跑出來不對，第一個檢查點是 OneHotEncoder 後 column 數量。

---

## Slide 22 · §4 divider

進入第四 section — algorithm zoo。

到目前為止我們的 X_train_prepared 是一個乾淨的矩陣。
同一個矩陣可以餵給很多 algorithm。接下來我們會用 **完全相同的 evaluation protocol** 比較五大家族。

---

## Slide 23 · Taxonomy table

這張表是今天 algorithm 的速覽。記不住沒關係 — 重點是知道 **這五類各自的 inductive bias** 是什麼。

**Inductive bias** 是個重要概念：每個 algorithm 對「資料長什麼樣」都有先驗假設。
Linear 假設 target 是 feature 的線性組合；instance-based 假設鄰近 sample 相似；
tree 假設 feature 空間可以用 axis-aligned 切割；ensemble 沒有自己的 bias，
而是用多個 weak learner 的組合來修正單一 learner 的偏誤；kernel 在 high-dim space 找最大 margin。

選對 algorithm，就是讓它的 bias 跟資料的真實結構對上。
這也是為什麼「沒有最強的 algorithm」 — 只有「最適合這份資料的 algorithm」。

---

## Slide 24 · Linear family

第一家族：linear models。

最簡單的就是 LinearRegression — y = w·x + b，用最小平方法解。
Ridge 在 loss 加上 L2 penalty（w 的平方和），防止 coefficient 爆炸 — 在 feature 多或共線性嚴重時很有用。
Lasso 用 L1 penalty，會把某些 coefficient 壓到 0，等於自動 feature selection。

Linear model 的 **最大優點是可解釋** — 看 coefficient 你就知道每個 feature 對 target 的方向與強度。
缺點：對非線性與互動完全無感。如果你的資料是 `y = age × congruency` 這種互動結構，
linear model 永遠抓不到。

---

## Slide 25 · k-NN

第二家族：instance-based — k-Nearest Neighbors。

概念極簡：對一個新 sample，找最近的 k 個 train sample，取他們 target 的平均當預測值。
完全沒有「訓練」 — 它只記住所有 train sample。

k-NN 的兩個關鍵 gotcha：
第一，**必須先 scaling**。我們前面看過 latitude vs. income 的例子。
第二，**curse of dimensionality** — 在高維空間（>50 dim）所有點都「差不多遠」，k-NN 的概念失效。

k-NN 在低維、區域結構強、資料量大時非常有效。在認知神經科學中，
fMRI MVPA 的 searchlight 分析常用 k-NN 當 base classifier。

---

## Slide 26 · Decision Tree

第三家族：tree-based — Decision Tree。

概念：遞迴把 feature 空間切成 axis-aligned 區塊，每塊預測該區的 mean (regression) 或 majority class (classification)。
切分的依據是「哪個切法最能降低 impurity」 — 對 regression 通常是 MSE。

優點：天然處理 mixed-type feature、不需 scaling、可視化 decision path 很直觀。
**致命缺點**：single tree 容易 overfit — 沒限制深度時 train RMSE 趨近 0、test RMSE 爛透。

兩個基本控制 hyperparameter：
`max_depth` 限制樹深，`min_samples_leaf` 限制葉節點最小 sample 數。
不過 single tree 即使調好參數通常還是不夠 — 真正的解法是下一個 family：ensemble。

---

## Slide 27 · Ensemble

第四家族：ensemble — Random Forest 與 Gradient Boosting。

兩者都用「多棵 tree 的組合」，但路徑不同：

**Random Forest**：bagging 策略。平行訓練多棵 **deep** tree，
每棵看不同的 random subsample 與 random feature subset，最後平均。
重點是「平行」與「deep」 — 每棵 tree 都是 high-variance learner，
但平均之後 variance 大幅降低、bias 不變。

**Gradient Boosting**：boosting 策略。序列訓練多棵 **shallow** tree，
每棵學前一棵的 residual — 也就是「上一棵還沒解釋的部分」。
重點是「序列」與「shallow」 — 從 high-bias 開始，逐步降 bias。

實務上 GradientBoosting 通常表現更好，但比 RF 慢、對 hyperparameter 較敏感。
RF 是個 hyperparameter 不調也表現不錯的 default baseline；
GB（特別是 XGBoost、LightGBM）是 kaggle competition 的常勝軍。

---

## Slide 28 · Kernel methods

第五家族：kernel methods — Support Vector Regression。

SVR 的想法：在 high-dim feature space 找一個 margin-maximizing hyperplane。
透過 kernel trick，這個 high-dim space 可以是隱式的 — 不用真的 expand feature，
只算 kernel function 的值就好。

最常用的 kernel 是 RBF — radial basis function，等同 Gaussian 相似度。

SVR 的兩個 gotcha：
第一，**訓練複雜度 O(n²) 或 O(n³)** — 在大資料（>10k samples）會非常慢。
今天 housing 16k samples 跑 SVR 要等好幾分鐘 — 課堂示範我們 subsample 到 3000。
第二，**hyperparameter 很重要** — C 控制 margin 與 violation 的 tradeoff，
γ 控制 RBF 的寬度。沒調好 C 與 γ 的 SVR 通常輸給其他 family。

在中等大小、非線性結構的資料上，調好的 SVR 是強力選擇。

---

## Slide 29 · Unified evaluation

這張 code 是 algorithm zoo 的核心 — 用一個 for-loop 跑完五大家族。

關鍵點：**所有 model 都包在 make_pipeline(full_pipeline, model) 裡**。
這保證每個 model 都用完全一樣的 preprocessing，差別只在演算法本身。

`cross_val_score` 預設 5-fold CV，回傳 5 個 score。
`scoring="neg_root_mean_squared_error"` 因為 sklearn 的慣例是「越大越好」，
所以 RMSE 加負號。我們最後印的時候再轉回正號。

注意：SVR 在 16k samples 太慢 — 真正跑的時候要對 SVR 做 subsample，
或者直接跳過放在 code 註解。下一張投影片的 bar chart 就是這個 loop 的結果。

---

## Slide 30 · Results bar chart

這就是上面 loop 跑出來的結果，5-fold CV RMSE，單位 USD，**越低越好**。

幾個關鍵觀察：

第一，**RandomForest 大幅超越 DecisionTree** — 49500 vs 69100。
這證明了 ensemble 的價值：用多棵 high-variance 的 deep tree 平均，把 variance 降下來。

第二，**Linear 跟 SVR 差不多** — 都在 68000 上下。
這暗示資料的線性結構主導，沒調過 hyperparameter 的 SVR 沒有額外優勢。

第三，**GradientBoosting 也很強** — 51800，跟 RF 接近但稍差，因為我們也沒調。

第四，**k-NN 中等** — 區域結構有，但被 noise 干擾。

右邊的小字提醒：RMSE 與 target 同單位（USD），這比 R² 更好解讀 —
「平均誤差大概 50k」比「R² = 0.78」直觀得多。

---

## Slide 31 · Bias–Variance Tradeoff

這張圖把所有 algorithm 放在一個 spectrum 上。

左邊是 **high bias** — model 太簡單，連 train 都學不好（underfit）。LinearRegression 在這端。
右邊是 **high variance** — model 太複雜，記住所有 noise（overfit）。深度 Decision Tree 在這端。

中間是「剛剛好」的位置 — Ridge 比 Linear 稍微 regularize，RandomForest 用 ensemble 修 variance。

選 model **不是選最強的**，而是 **在這條軸上找到最適合資料的位置**。

下方綠色 callout 是 ensemble 的魅力 — 它用「多個 high-variance learner 的平均」
降 variance 而不增加 bias，相當於把 spectrum 上的點往左推。這就是為什麼 RF 幾乎永遠贏 single tree。

---

## Slide 32 · Hands-on 4

第四個 hands-on — 10 分鐘。

任務：把 `Ridge(alpha=1.0)` 與 `GradientBoostingRegressor(n_estimators=100)` 加進比較表，
看誰贏。然後解釋為什麼 ensemble 通常贏 single tree。

Ridge 是 LinearRegression 的 L2 regularized 版本，在多重共線性下會稍微強過 plain Linear。
GradientBoosting 我們剛剛已經看過了，預期會跟 RF 差不多。

寫完後互看 code，特別注意 `make_pipeline` 的接法有沒有對。

---

## Slide 33 · §5 divider

進入第五 section — model evaluation 與 hyperparameter tuning。

到目前為止我們用 5-fold CV 比較 model，但還沒調 hyperparameter。
這個 section 講怎麼系統性地調，並且最後怎麼用 test set 報告 final 結果。

---

## Slide 34 · No train accuracy

為什麼我們從頭到尾都用 CV，不用 train accuracy？

這張 code 給出最戲劇化的例子：
DecisionTree 沒限制深度，在 train 上 R² 接近 1，看似完美；
但在 test 上 R² 只有 0.62 — 它記住了所有 noise，這叫 **overfitting**。

如果你只看 train accuracy，你會選最 overfit 的 model，然後 deployment 時哭出來。

**唯一正確的做法是用 CV 評估** — 對 train 集做 k-fold split，每次留一個 fold 當 validation，
其他 fold 訓練。這樣 model 永遠在「沒看過」的資料上被評估。

---

## Slide 35 · K-Fold diagram

這張圖示 5-fold CV：把 train 集切 5 份，每次留一份當 test，其他 4 份訓練。
跑 5 次，得到 5 個 score。最後報告 mean ± std。

為什麼是 5 或 10 fold？
經驗法則：fold 數越多越接近 leave-one-out（unbiased 但 high variance），fold 越少越 biased 但 stable。
5 或 10 是 community 的 sweet spot。

下方的 code 就一行 — `cross_val_score`。記得 `scoring` 參數要加負號（neg_root_mean_squared_error）
因為 sklearn 規定 score 越大越好。

---

## Slide 36 · Grid vs Random

有了 CV，下一步是調 hyperparameter。三個工具：

**GridSearchCV**：窮舉所有組合。優點是徹底，缺點是組合爆炸 — 4 個參數每個 5 個值就是 625 個組合 × 5 folds = 3125 次訓練。

**RandomizedSearchCV**：在分布上抽 n_iter 次。對連續 hyperparameter 特別有效 — 比 grid 的離散化更靈活。

**HalvingRandomSearchCV**：successive halving — 一開始用少量資料評估很多 candidate，
逐輪淘汰差的、給好的更多資料。預算極度有限時用。

實務上 90% 的情況我會用 RandomizedSearchCV，因為 hyperparameter 通常有連續的（如 alpha）也有離散的（如 max_depth），
RandomizedSearch 通通能處理。

底下的 code 範例用 scipy 的 `randint` 定義 hyperparameter 的分布。

---

## Slide 37 · Final test

這張是另一個「整堂課最重要」的訊息：

**最終的 test set 評估，只能做一次。**

為什麼？因為如果你看完 test RMSE 不滿意，回去再調 hyperparameter 重跑，
test set 就變成 train set 的一部分了 — 它的「unseen」性質被破壞。
你最後得到的數字就是失真的。

紀律是：CV 階段你可以隨便調，但 test set 只能在「我確定要 submit 這個 model」的瞬間跑一次。
如果結果不滿意，就接受它，並把這個限制寫進 paper 的 limitation 段落。

下方綠字：誠實的科學家會接受 negative result。

---

## Slide 38 · §6 divider

進入第六 section — unsupervised 小品。

主軸還是 supervised，但 unsupervised 方法常作為 **feature engineering 工具** 或 **outlier filter** 出現。
這裡介紹兩個最常用的：k-means 與 IsolationForest。

---

## Slide 39 · KMeans as feature engineering

Géron 在原 notebook 用了一個漂亮的 trick：

把 (latitude, longitude) 餵給 k-means 聚成 10 個 cluster，
然後計算 **每個 sample 到 10 個 centroid 的 RBF 相似度** — 這變成 10 個新 feature。

效果：模型不用直接從 (lat, lon) 學「加州地理結構」，
而是直接拿到「離 LA 多近、離 SF 多近、離 San Diego 多近...」這 10 個 derived feature。

下方的 `ClusterSimilarity` class 是一個 custom transformer — 繼承 BaseEstimator 與 TransformerMixin，
就可以直接放進 sklearn pipeline。

Cogneuro 類比：對 fMRI ROI time series 做 k-means 找 functional clusters，
再以每個 voxel 與 cluster centroid 的相似度作為 feature。這就是 RSA (representational similarity analysis) 的近親。

---

## Slide 40 · IsolationForest

IsolationForest 是 multivariate outlier detection 的 workhorse。

概念：用一堆 random tree 來「孤立」每個 sample — outlier 應該很容易被孤立（少數幾步就分到自己一個 leaf），
normal sample 需要很多步。每個 sample 的 anomaly score 就是平均孤立深度的反比。

為什麼比 mean ± 3 SD 強？
mean ± 3 SD 是 univariate — 它對每個 feature 獨立看。
IsolationForest 能抓到「每個 feature 單看都正常，但組合起來很奇怪」的 multivariate outlier。

在 RT 分析中很有用：例如「正確、RT 正常」但 motor preparation 異常的 trial，
單看 RT 或 accuracy 都正常，IsolationForest 卻能在 multidimensional space 中認出它。

`contamination` 是先驗的 outlier 比例，0.01–0.05 是常用範圍。

---

## Slide 41 · §7 divider

進入最後一個 section — 把今天學的全部套到 cogneuro 問題上。

我們會跑兩遍：一遍用純線性的生成式，一遍加入 age × congruency 互動。
這兩遍會展示「最佳 model 取決於資料結構」的核心訊息。

---

## Slide 42 · RT pipeline code

這張 code 把今天學的所有元件串起來：

1. 用 `simulate_stroop()` 生成資料 — 200 受試者 × 30 trial。
2. 按 age 分 4 個 bin，做 stratified split。
3. 建一個 ColumnTransformer — `age, isi, trial_num` 走 numerical pipeline，`congruent` 走 OneHot。
4. 用 make_pipeline + cross_val_score 比較 Linear 與 RandomForest。

注意：**這個 pipeline 的結構跟 housing 完全一樣**。
唯一不同的是欄位名稱與 model 種類。這就是為什麼學會 housing 的人，
可以馬上跑任何結構類似的 tabular data — 不只 cogneuro，任何 trial-level 或 subject-level 資料都適用。

---

## Slide 43 · RT results

這張表是兩種生成方式的結果：

**Linear DGP (純線性)**：Linear RMSE 39.8，RF RMSE 44.5。
Linear 贏了 — 因為資料就是線性的，RF 多餘的容量只增加 variance。

**Interaction DGP (age × congruency)**：Linear RMSE 51.8，RF RMSE 44.6。
RF 贏了 — 因為 Linear 抓不到互動，RF 用 tree 結構自然 capture。

這個對比是整堂課的高潮：**沒有「最強的 algorithm」，只有「最適合這份資料的 algorithm」**。
所以永遠用 CV 比較，永遠對結果保持懷疑。

底下提醒：完整可重跑的程式在 `code/ml/06_cogneuro_rt_pipeline.py`，
回去自己跑一遍，把生成式參數改一改看 RMSE 怎麼變。

---

## Slide 44 · Hands-on 5

最後一個 hands-on — 課堂收尾。

任務：在合成資料的 RT 公式中，加入「老年人受 incongruent trial 影響更大」的 interaction。
重新訓練，這次哪個 model 贏？

修改只有一行：把 `cong_effect = 0 if congruent else 60`
改成 `cong_effect = 0 if congruent else (60 + 4.0 * (age - 45))`。

預期：RandomForest 會領先 Linear 大約 7 ms 左右。
這就是上一張投影片 interaction DGP 的結果。

跑完後思考：如果你的真實 RT 資料有 age × congruency 互動 — 而文獻說它確實有 —
那 RF 在你的資料上應該勝過 linear regression。但記得 RF 比較難解釋 coefficient，
所以對「解釋變項貢獻」這類問題，linear + interaction term 還是有它的位置。

---

## Slide 45 · Recap

今天結束前，記住這五件事就好：

第一：**先 frame 再 code；先切 test set 再 EDA**。順序錯了後面全錯。

第二：**Pipeline 是 leakage 防火牆**。`fit on train, transform on test` — 不要自己手動處理。

第三：**用 CV 比較 model，不用 train accuracy**。train accuracy 對 overfit model 有偏好。

第四：**Test set 只能評估一次**。看完結果就接受，不要回頭調。

第五：**Ensemble 是 tabular data 的強力 baseline**。如果不知道用什麼，先試 RandomForest。

---

## Slide 46 · Pitfalls

這張表列了五個最常見的錯誤，也是我在批改作業時最常扣分的地方。

第一：train + test 一起 fit StandardScaler — 嚴重 leakage，扣最多分。
第二：反覆調參直到 test 變好 — 這個我看不出來，但你自己的 final paper 結果會失真。
第三：OneHotEncoder 沒加 `handle_unknown='ignore'` — 上線後遇到新類別 crash。
第四：對 tree model 還做 StandardScaler — 不會錯，但浪費計算。
第五：報告 R² 而非 RMSE — R² 對 outlier 敏感、單位抽象，建議盡量用 RMSE。

明天作業出去前再看一次這張表。

---

## Slide 47 · Homework

這週的作業：把今天的 pipeline 套到一個合成的 Flanker task 資料集。

資料來源：作業說明裡附了 `simulate_flanker()` 函式，**請不要改參數**，否則 grading 對不上。
規模：250 受試者 × 80 trial = 20,000 rows。

七個 task 涵蓋了今天所有概念：EDA、stratified split、pipeline、algorithm comparison、tuning、final test、解釋。
最後要交一個 .ipynb 加一份一頁的 report.md。

特別注意 rubric — reproducibility 與 leakage 防範佔 30%，
algorithm 比較佔 25%，tuning 佔 20%。其他 25% 是解釋與報告品質。

下週三晚上 11:59 截止，上傳 eeclass。詳細規格在 `week-15-homework.md`。

---

## Slide 48 · References

延伸閱讀：

Géron 的書是今天的 anchor — 第二章值得從頭到尾跑一遍。GitHub 上的原 notebook 可以直接 fork。

scikit-learn user guide 的 cross-validation 與 preprocessing 章節是聖經 — 比任何中文教材都權威。

Hastie 等人的 ESL（Elements of Statistical Learning）是 bias-variance 數學的標準參考，
雖然密度很高，但「Chapter 7 Model Assessment and Selection」幾頁可以挑著讀。

最後 Varoquaux 與 Cheplygina 2022 那篇 npj Digital Medicine 是 **必讀** —
專講 ML 在 medical / brain imaging 上的常見方法學錯誤。你們未來寫 ML 相關 paper 一定會用到。

---

## Slide 49 · Closing

感謝大家今天的專注。

下週是 final project workshop — 把這學期學的所有東西做成一個可 deploy 的 Streamlit app，
然後做 peer review。

如果今天的作業有問題，office hour 直接來找我，或 email：audachang@gmail.com。

下週見。

---
