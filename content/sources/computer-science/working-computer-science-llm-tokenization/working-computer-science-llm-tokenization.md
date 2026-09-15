---
archive_policy: text-only
confidentiality: public
domain: computer-science
evidence_items:
- evidence_id: evidence-71f18a9532e5
  position:
    end: 303
    start: 223
    type: TextPositionSelector
  selector:
    exact: 分词器是语言模型的数据入口：把原始文本（字符串/字节）编码成 token 索引序列——语言模型正是在这种序列上定义概率分布——也能把 token
      解码回字符串。
    prefix: '），未锚定的联网断言在"待验证项"列出。


      ## 一句话结论


      '
    suffix: 模型不能直接处理原始字节，计算效率太低，所以主流做法是子词分词：
    type: TextQuoteSelector
  snapshot_sha256: sha256:09691c3597978e987a8c11e2b704db68d212e978cbfa784cfc4a6855643d9057
extractor: personal-note/1
id: working-computer-science-llm-tokenization
media_type: text/markdown
origin: personal
read_status: retrieved
retrieval:
  acquisition: personal-note
schema_version: source/v1
snapshot_sha256: sha256:09691c3597978e987a8c11e2b704db68d212e978cbfa784cfc4a6855643d9057
source_type: personal-note
vault_id: public
---
---
domain: computer-science
title: 分词 Tokenization
---

# 分词 Tokenization

> 来源：Stanford CS336（cs336-p01 转录 + 官方 lecture_01.py）为地基，联网/官方资料补充见文末"参考"与"待补充到 sources 的来源清单"。CS336 引文逐字保留（ASR 误差原样），未锚定的联网断言在"待验证项"列出。

## 一句话结论

分词器是语言模型的数据入口：把原始文本（字符串/字节）编码成 token 索引序列——语言模型正是在这种序列上定义概率分布——也能把 token 解码回字符串。模型不能直接处理原始字节，计算效率太低，所以主流做法是子词分词：常见序列压成单个 token，罕见序列拆成多个，在缩短序列（降低 attention 的 O(N²) 成本）与词表可控之间取平衡，再用字节回退保证任何输入都不会落到 unk。现代分词器词表集中在 100k–200k，训练完就和模型绑死、不可修改。分词器质量直接决定"中文税"这类跨语言成本差异，选模型时这是最实际的工程问题之一。

## 核心概念

- **token / 词元**：模型操作的最小单元，用整数索引表示；语言模型在 token 序列上定义概率分布。
- **分词器（tokenizer）**：完成"字符串→token"与"token→字符串"往返转换的组件，往返可验证是硬性要求。
- **压缩比**：字节数 ÷ token 数，即每个 token 对应的字节数。越高越好——序列越短，attention 二次方成本越低。
- **词表（vocabulary）**：token 的集合。词表越大压缩比越高，但稀疏性和 embedding 显存成本也越高；2026 主流 100k–200k。
- **子词（subword）**：介于字符与词之间的切分单元，兼顾压缩与泛化（形态变化、OOV 不落到 unk）。
- **BPE（字节对编码）**：从数据压缩引入的子词算法，反复合并最高频相邻对直到目标词表；生成式 LLM 主流。
- **字节回退（byte fallback）**：拆不出的输入按原始 UTF-8 字节编码，从机制上保证不出现 [UNK]。
- **特殊 token**：`<s>/</s>/<pad>/<unk>/<|im_start|>` 等，训练前手工预留固定 ID，不参与学习。
- **自适应计算**：常见块 1 个 token、罕见块拆多 token，让算力按信息量分配。

## 工作机制

1. **训练**：从字节/字符基础词表出发，统计相邻对频次，反复合并最高频对（或按似然增益）直到目标词表大小；多语言按语言加权采样。
2. **编码（推理）**：文本 → 归一化 → 预分词 → 按学到的合并规则切分 → 追加特殊 token/chat 模板 → token id 序列。
3. **解码（推理）**：token id → 还原字符串；流式输出就是每出一个 token 解一次。
4. **无 unk 保证**：字节回退让训练时没见过的字符按字节兜底，而不是落入 unk。

（详细讲解见"详细章节"。）

## 示例或代码

- **压缩量级（官方口径）**：CS336 官方课件给出 1000 字节 → 约 250 token（压缩比约 4）。OpenAI 口径 1000 token ≈ 750 英文词 ≈ 500 汉字。
- **BPE 合并**："the cat in the hat" 反复合并最高频字节对（如 116 104 = "th"）→ 新 token 从 256 起编号；英文/中文分词差异见详细章节 2.2。（"the cat in the hat" 压缩比约 1.5、20 字节/8 token = 2.5 等是课堂口述举例，只作示意，以官方口径为准。）
- **中文税**：同一句 16 个汉字，GPT-4 切 19 个 token、Qwen 切 6 个（"人工智能"在 Qwen 是 1 个 token）。
- **词表档位（HF 可查）**：GPT-4o `o200k_base` 200,019；Llama 4 200,000；Gemma 3 262,144；Qwen 3 151,643；DeepSeek V3 128,000；GLM-5 154,880；Kimi K2 163,840；MiniMax M2 200,064。

## 常见误区

- 未见词用 unk 兜底是正常做法 → 澄清：unk"真的很糟糕""会搞乱你的困惑度计算"。但真正从机制上消除 unk 的是字节级 BPE / 字节回退——WordPiece 这类非字节级子词方法对未见字符仍会落 [UNK]。
- 词表越大越好 → 澄清：词表大压缩比高，但稀疏性、embedding/显存成本线性增长；2026 主流停在 100k–200k 是有原因的。
- "空格+单词"与"单词"是同一个 token → 澄清：两个完全不同的索引、彼此无关（hello 例子）。
- 每个数字拆成单个 token 无害 → 澄清：token 数大增、压缩比大跌，放大 attention 二次方成本。
- 分词器只需能编码 → 澄清：必须能往返转换，"如果你实现的分词器做不到往返转换，那就有问题了"。
- BPE 是深度学习发明 → 澄清：BPE 是 1994 年数据压缩算法，Sennrich 2016 引入 NMT，GPT-2 首篇用于 LM。
- 中文贵是因为中文"难" → 澄清：主要是英文中心语料训练出的分词器没给中文分配词表空间；换中文优化分词器 1 字≈1 token，差距立刻消失。
- token 越少模型理解越好 → 澄清：过度合并（整词一个 token）可能损害子词层面的形态/泛化信息；分词效率与理解质量是两个维度。

## 待验证项

- **课堂口述数字只作示意**：课堂口述的压缩比数字（"the cat in the hat"≈1.5、20 字节/8=2.5）未在官方材料复现，仅举例；以官方 "1000 bytes → ~250 tokens" 口径为准。
- **二手联网数据待正式锚定**："同一句 16 汉字 GPT 19 token vs Qwen 6"、"1000 token≈750 词/500 汉字"、代码 2.8–3.1 字符/token、cl100k 中文 1.35–1.59×、印度语 8×→4.6×——均来自二手文章，需用真实分词器复算后锚定。
- **闭源词表未公开（正常）**：GPT-5.x、Claude、Gemini 3 不发布 tokenizer，查不到属正常；本表以开源模型为准。
- **分词效率对下游能力（推理/代码/多语言）的影响**：量化研究仍不充分（见 3.4 的初步实证与 arxiv 2604.14210）。

## 关联知识

- [[llm-transformer-architecture]]：分词提供 Transformer 需要的"序列抽象表示"，把长序列压缩以缓解 attention 的 O(N²) 成本。
- [[llm-scaling-laws]]：词表/分词效率影响序列长度，进而影响训练算力与数据配比；多语言惩罚是训练成本的一部分。
- [[llm-data-sources]] / [[llm-data-pipeline]]：分词器训练语料的来源与预处理（去重/过滤）决定词表质量。
- [[llm-inference-optimization]]：token 数是 KV cache 显存、推理成本、上下文窗口的直接分母。
- [[llm-multimodal]]：多模态模型把图像等也"token 化"（离散 token），延续同一抽象思想。

## 详细章节

六个正交维度：本质 → 算法 → 度量 → 训练 → 推理 → 未来。各节独立成维、不重复覆盖。

### 1. 本质与动机

#### 1.1 分词是什么

分词器做两件事：编码（字符串 → token 整数序列）和解码（token 序列 → 字符串），"分词器基本上就是能完成这个往返过程的东西"（cs336-p01）。往返可验证是硬性要求："一个分词器应该能够完成这种往返转换"。官方代码里 Tokenizer 就是只有 `encode`/`decode` 两个方法的抽象接口（lecture_01.py）。

token 是模型操作的最小单元，"语言模型会在token序列上定义一个概率分布，而这些token通常是用索引来表示的"（cs336-p01）。模型不读文本，只认 token 编号。

分词提供的是一种"序列抽象表示"：Transformer 需要在某种抽象序列上操作；对视频、DNA 等非文本输入，"单个字节或单元的信息量低"，必须先做抽象。

#### 1.2 为什么需要分词（四大动机）

1. **模型无法直接处理原始字节**——"因为那样做计算效率会非常低，至少对于今天的模型架构来说是这样"（cs336-p01）。官方表述是 "working with raw bytes is elegant, but compute-inefficient with today's model architectures"（lecture_01.py）。分词设计动机是"减少内存占用或者降低浮点运算次数"，并"受更快推理和更快数据过滤的需求所影响"。
2. **压缩**：分词"会把一个很长的序列压缩成数量更少的token"；官方量级是 1000 字节 → 约 250 token（lecture_01.py）。序列越短越好，因为 attention 计算量随序列长度二次方增长（"因为attention的计算量是二次方的"）。这正是第 3 节"压缩比"要量化的东西。
3. **自适应计算**：分词"让你能够进行自适应计算"，官方表述是 "more modeling capacity on interesting parts of input"（lecture_01.py）——常见字节块压成 1 个 token，罕见或更有趣的部分保留为多个 token，让算力按信息量分配。
   - 压缩和自适应看着矛盾，其实不冲突：压缩管总量（整体序列平均变短），自适应管分配（token 预算按信息量分配、可以不均）。罕见内容拆成多个 token，是把算力花在更难的词上；只要常见内容压缩得够多，总量上仍是压缩——zip 对高熵段也压缩不动甚至变大，但整体仍压缩。两者目标不同：压缩省的是序列长度（attention 成本），自适应省的是把 token 预算花在刀刃上。
4. **消除未登录词（OOV）**：词级分词遇到没见过的词会落 unk，"真的很糟糕""会搞乱你的困惑度计算"。子词分词把罕见序列拆成更小单元来减少 unk，但要注意：子词本身不必然消除 unk——WordPiece（BERT）对未见字符仍映射到 [UNK]，早期字符级 BPE（如 GPT-1 时代）对未见字符也会产生 unk。真正从机制上消除 unk 的是字节级 BPE / 字节回退（基础词表覆盖全部 256 字节，任何输入都能按字节拆分）；CS336 说的"任何内容都能被分辞"指的正是这类实现。

### 2. 方法与算法

这一维度讲"怎么做"，含可复现例子。算法是机制，度量（第 3 节）是衡量，两者正交。

#### 2.1 粒度谱系：三种朴素方案及其缺点

先看同一句输入在不同粒度下的实际输出（`␣` 表示空格）：

| 方案 | 原理 | "the cat" 的实际输出 | 优点 | 缺点 |
| --- | --- | --- | --- | --- |
| 字符级 | 每 Unicode 字符一个 token | `[t][h][e][␣][c][a][t]` | 词表小（字符集规模）、无 OOV | 词表可达约 15 万但"很多字符很少用到""利用效率很低"；token 太多、压缩比差 |
| 字节级 | 每 UTF-8 字节一个 token | `[116][104][101][32][99][97][116]`（ASCII 下与字符级同长；中文"人"= 3 字节） | 词表固定 256 起步、覆盖一切 | "序列变长了""压缩比是1"，序列过长 |
| 词级 | 按空格/正则切块 | `[the][cat]`（"hats" → `[UNK]`） | token 有语义、压缩比不错 | 词表=语料不同块数，可能"没有边界"；形态变化（run/running）无法共享；未见词落 unk |

字符级和字节级"都很糟糕"（cs336-p01），词级有 OOV 这个致命缺陷，于是用子词方案。

#### 2.2 子词算法家族（含实际例子）

下面每个算法给出"同一输入 → 实际输出"，可以直接对照理解；最后一张表把所有方法放在同一词上对比。

**BPE（字节对编码）**——数据压缩算法（Gage 1994）被 Sennrich 等（2016）引入神经机器翻译，GPT-2 首篇用于语言模型。贪婪、基于频次：反复合并语料中出现频率最高的相邻 token 对，直到词表达目标大小；合并出的新 token 从 256（字节基础表之上）起编号。

```text
输入: "the cat in the hat"
1. 转字节:  116 104 101 ␣ 99 97 116 ␣ 105 110 ␣ 116 104 101 ␣ 104 97 116
2. 统计最高频相邻对 → (116,104) = "th" 出现 2 次，合并为 token 256
3. 替换:    256 101 ␣ 99 97 116 ␣ 105 110 ␣ 256 101 ␣ 104 97 116
4. 继续合并最高频对（如 256+101 → "the"+空格），直到词表达目标大小
最终（语料驱动）: [the][cat][in][the][hat] 或按语料切成更细子词
```

另一个例子（HF 课程）：语料全是 `low low low ... lowest ... newer ... widest` 时，第一次合并必然是 (l,o)→lo，再 (lo,w)→low，然后 (e,r)→er、(lo,we)... 最终 low/lowest/newer/widest 各成词表项——**子词是从语料的高频模式里长出来的**。局限：贪心按频次，可能合出无语义碎片；经典字符级 BPE（GPT-1）对未见字符会产生 unk。

**WordPiece**——谷歌 2012 语音搜索提出（Schuster & Nakajima），BERT 采用。合并准则不是频次而是似然增益：`freq(pair) / (freq(first) × freq(second))`——分母惩罚高频单字，避免把两个都很常见的字符过早合并，更"语义导向"。

```text
输入: "tokenization"
输出: [token][##ization]        ## 表示"接续前一个词的子词"
未收录字符: 字母 m 不在基础词表 → [mug] → [UNK][##ug]
```

WordPiece 是有 [UNK] 兜底的方法，对未见字符仍映射 [UNK]。

**Unigram**——概率语言模型视角，训练用 EM 从超大子词集合逐步删掉对似然贡献最小的子词直到目标词表；与 SentencePiece 配合。

```text
输入: "tokenization"
输出: [token][ization]          在候选子词里选概率最大的切分（无 ## 标记）
```

**SentencePiece / 字节级 BPE（BBPE）**——SentencePiece 把空格当作普通字符（转成 `▁`），天然支持中文/日语等无空格语言；字节级 BPE（GPT-2 引入的 byte-level BPE）以 256 字节为基本词表，配合字节回退（byte_fallback）——拆不出的输入按原始字节编码，从机制上保证永不出现 [UNK]。

```text
输入: "New York"
输出: [▁New][▁York]             空格转成 ▁（metaspace），保留词边界
中文: "你好世界" → [▁你好][▁世界]  无空格语言按语料切（具体切分依赖训练语料）
字节回退: emoji 😀 不在词表 → 按 4 个 UTF-8 字节 token 输出，不落 [UNK]
```

**横向对比：同一词 "tokenization" 在各方法下的输出**

| 方法 | 输出 | 核心机制 | 一句话特点 |
| --- | --- | --- | --- |
| 字符级 | `t o k e n i z a t i o n`（12 个 token） | 每字符一 token | 最长；无 OOV |
| 字节级 | 每个 ASCII 字符 1 字节 token（中文每汉字 3 字节 token） | 每字节一 token | 覆盖一切字符 |
| 词级 | `[UNK]`（若词表无此词） | 空格/正则切块 | OOV 致命 |
| BPE | `[token][ization]`（语料驱动） | 贪心合并最高频对 | 生成式主流 |
| WordPiece | `[token][##ization]` | 似然增益合并 | 有 [UNK] 兜底 |
| Unigram | `[token][ization]`（概率最优） | EM 删子词 | 概率视角 |
| SentencePiece | `[▁token][ization]` | 空格▁化 + 字节回退 | 无空格语言友好 |

（BPE/WordPiece/Unigram 对 "tokenization" 的切分是典型语料下的结果；实际以训练出的词表/合并规则为准。）

**中文 vs 英文的机制差异**：英文有空格天然成词；中文无空格、1 汉字 = 3 UTF-8 字节，英文中心语料里中文字节合并不充分，于是中文常被拆成单字/多字节 token（GPT-2 时代"人"= 3 字节 token）。量化差异见第 3 节。

#### 2.3 编码（推理）时：三种算法怎么把文本切成 token

> 训练决定"词表长什么样"，编码决定"新文本怎么切"。三者**编码机制完全不同**——"贪婪匹配"这个直觉只对了一半：它是 WordPiece 的机制，不是 BPE 的；Unigram 又完全是另一套。

| 算法 | 编码（推理）机制 | 贪心？ | 结果性质 |
| --- | --- | --- | --- |
| BPE | **按学习顺序贪心应用合并规则**：每步找当前序列里"优先级最高（最早学到）且存在"的相邻 token 对，合并，重复到无可合并 | 贪心（对"合并对"） | 确定且唯一 |
| WordPiece | **贪心最长匹配（MaxMatch）**：从左到右，每步取"剩余文本中词表能匹配的最长前缀"，从不回溯；无任何前缀可匹配 → [UNK] | 贪心（对"词表前缀"） | 确定，但可能次优 |
| Unigram | **Viterbi 动态规划**：在 token 格子上找整体似然最大的切分 | 非贪心（全局最优） | 确定（在给定 token 概率下） |

**BPE**（按合并规则贪心，例子：规则 (l,o)→lo、(lo,w)→low、(e,r)→er 按此顺序学到）：
```text
"lower" → l o w e r
  (l,o) 优先级最高且存在 → lo w e r
  (lo,w) → low e r
  (e,r) → low er
  → [low][er]
```
BPE 编码不查"整词在不在词表"，只按合并规则跑——除非 tiktoken/Llama3 那种"整词在词表直接 1 token"的跳过优化（这时行为上接近 WordPiece）。

**WordPiece**（贪心最长匹配，Fast WordPiece 论文 Example 1）：
```text
词表含 a, ##b, ##c, ##dz ...
"abcdz" → 位置0最长可匹配前缀 "a" → [a]
          剩余 "bcdz" → 最长前缀 "##b" → [a,##b]
          "cdz" → "##c" → [a,##b,##c]
          "dz" → "##dz" → [a,##b,##c,##dz]
```
贪心从不回溯，因此对歧义词可能产生次优切分（论文承认 "can occasionally produce suboptimal segmentations"）；朴素实现 O(n·m)，有 O(n) 的 Aho-Corasick 启发加速（arxiv 2012.15524）。MaxMatch 也是中文分词 1980 年代以来的经典方法。

**Unigram**（Viterbi，Kudo 2018）：
```text
"tokenization" 有多个候选切分（token+ization / tokeni+zation / t+o+k+...）
Viterbi 在格子上算每个候选的对数似然和，选整体最大的那个
```
不是每步贪心，而是全局最优；SentencePiece 的 unigram 模式就是它（Kudo & Richardson 2018）。

**一句话**：你猜的"贪婪匹配"是 **WordPiece 的 MaxMatch**；BPE 是"按合并规则贪心"，Unigram 是"Viterbi 全局最优"。

（来源：WordPiece——Google 博客《A Fast WordPiece Tokenization System》/ arxiv 2012.15524；Unigram——Kudo 2018《Subword Regularization》/ EMNLP 2020《Byte Pair Encoding is Suboptimal for Language Model Pretraining》；BPE——Sennrich 2016 / HF tokenizers 实现。）

#### 2.4 选型准则（怎么分才合理）

- **词表大小**：核心权衡（压缩 vs 稀疏性/显存），2026 主流 100k–200k。
- **训练语料必须与预训练语料匹配**："Match the tokenizer training mix to the pretraining mix"——分词器在什么语料上训练决定一切；英文语料主导会让中文/低资源语言效率大跌（见第 3 节）。
- **多语言按语言加权采样**：SentencePiece 的 `alpha` 参数给稀有语言公平的词表份额。
- **特殊 token 手工保留、不参与学习**：`<s>`/`</s>`/`<pad>`/`<unk>`/`<|im_start|>` 等由训练器预留固定 ID；若可能扩展，先留空位。
- **字节回退是"合理性"底线**：好的分词器应能处理训练时完全没见过的字符（emoji、新造字），而不是退化成 unk。

### 3. 度量与比较

这一维度讲"怎么衡量和比较分词器"：先给尺子（压缩比），再用尺子量语言差异、量各家模型。

#### 3.1 压缩比：定义、计算、例子

- **压缩比 = 字节数 ÷ token 数**，即"每个 token 对应的字节数"（cs336-p01 口径）。
- **方向**：压缩比越高，每个 token 覆盖的字节越多，序列越短，越好（attention 二次方成本越低）。别和"每 token 多少字符"记混，数值含义相反。
- **例子**：官方口径 1000 字节 → 250 token，压缩比约 4（lecture_01.py）；OpenAI 口径 1000 token ≈ 750 英文词 ≈ 500 汉字 → 英文约 4–6 字符/token。（20 字节/8 token = 2.5、"the cat in the hat"≈1.5 是课堂口述举例，仅示意。）
- **代码**：每 token 覆盖字符最少的内容之一（约 2.8–3.1 字符/token，即压缩比低、同样内容 token 更多、更费），括号/缩进/短名难以合并，代码类 prompt 更费 token。
- **数字**：1–3 位数字通常 1 个 token，4 位数字约 2 个；把每个数字拆成单 token 会大幅拉低压缩比。
- **词表大小与压缩比的权衡**：增大词表可提升压缩比，但"这样又会遇到稀疏性问题""因为词表中的每个元素都被当作一个独立的个体来处理"（cs336-p01），且 embedding 参数量、显存随词表线性增长。

#### 3.2 跨语言差异（用标尺量）

- **英文**：有空格天然分词，压缩效率最好（约 4–6 字符/token）。
- **中文（"中文税"）**：无空格 + 表意文字，UTF-8 每汉字 3 字节。英文中心分词器下：GPT-4 `cl100k` 常用汉字 1–2 token/字、整体差于英文；经验口径 GPT 系约 1.5–2 token/汉字，国产模型（Qwen/DeepSeek/文心/通义）约 1 汉字 ≈ 1 token；tiktoken 各编码对中文惩罚系数 1.35–1.59×。同一句 16 个汉字，GPT-4 切 19 token、Qwen 切 6 个。
- **代价不只是账单**：同样 200k 上下文窗口，英文中心分词器装中文材料能塞进的内容比英文少 40%–70%——更贵，工作空间更小。
- **反直觉点**：token 省不等于推理省。用更少 token 表达更密的信息（如古文），是把"解压"转嫁给模型的推理负担，理解准确率可能反而下降。
- **新语言 / 低资源语言**：字节回退兜底（不会被 unk 卡死但效率差，每字 3 字节 → 3 token）；惩罚量级——英文中心分词器对印度语系约 8×（cl100k），扩表到 o200k 降到 4.6×，Gemma 3 用 256k 词表压到 <3×；正确做法是在均衡多语言语料上训练自己的词表，低资源语言的根本瓶颈是训练数据稀缺而非算法。

#### 3.3 模型对比（2025–2026.09）

词表大小都可在 HuggingFace / ModelScope 的 `tokenizer_config.json` / `config.json` 里查到（`vocab_size` 字段）。**闭源模型（GPT/Claude/Gemini）不发布 tokenizer，查不到很正常；本表以开源模型为准**。本表只收录"词表大小"这一可查证的硬事实；每个模型的实现流派见下文"实现流派"一节，按可确认程度标注，不写猜测。

| 模型（2025–2026.09） | 词表大小 | 备注 |
| --- | --- | --- |
| GPT-5.x（5/5.2/5.4/5.5） | 未公开 | 闭源；tiktoken 系，具体编码未公布 |
| Claude Opus 4.x / Fable 5 | 未公开 | 闭源；自研 BBPE，未公开 |
| Gemini 3 / 3.1 / 3.5 | 未公开 | 闭源 |
| Llama 4 Scout / Maverick | 200,000 | HF 可查；实现流派待核 |
| Mistral Large 3 | 131,072 | HF 可查；是否 Tekken 系待核 |
| Gemma 3 | 262,144 | HF 可查；SentencePiece 系（确认） |
| DeepSeek V3 / V3.1 / V3.2 / V4 | 128,000 | HF 可查；V3 为 SentencePiece 系，V3.2/V4 为自定义 |
| Qwen 3 / 3.5 / 3.7 | 151,643（Qwen 3） | HF 可查；qwen.tiktoken（tiktoken 系，确认） |
| GLM-4.5 / GLM-5 | 151,552 / 154,880 | HF 可查；SentencePiece 系（二手，待核） |
| Kimi K2 / K2.5 / K2.6 | 163,840（K2） | HF 可查；tiktoken.model（二手，待核） |
| MiniMax M2.x / M3 | 200,064（M2） | HF 可查；实现待核 |
| GPT-OSS | 199,998 | OpenAI 开源；tiktoken 系（确认） |

**实现流派：当前基本就两派（正确命名是"字节级 BPE"vs"码点级 BPE"）**

两大流派的分界不在"BPE vs SentencePiece"（底层算法都是 BPE），而在 **BPE 在什么粒度上跑**：

| 流派 | 工作粒度 | 空格/预切分 | 代表模型（确认度） | 关键实现 |
| --- | --- | --- | --- | --- |
| 字节级 BPE（tiktoken 风格） | 直接在 UTF-8 字节上合并 | 正则预切分 + 字节级 | GPT 全系、GPT-OSS（官方确认）；Qwen（qwen.tiktoken，HF 文件确认）；Kimi K2（tiktoken.model，二手）；Llama 3（tiktoken 行为，HF 论坛） | tiktoken（Rust） |
| 码点级 BPE（SentencePiece 风格） | 在 Unicode 码点上合并，罕见字符回退到字节 | 空格 ▁ 化、无预切分 | Llama 1/2、Gemma 2/3、T5（确认）；Mistral 旧版、DeepSeek V3（确认）；GLM、MiniCPM（二手，待核） | SentencePiece（C++） |

两个关键差异（fast.ai / HF 论坛）：
- **tiktoken**：词已在词表里就直接一个 token，**跳过合并规则**；**SentencePiece**：严格按合并规则切——"hugging" 若在词表里，tiktoken 给 1 个 token，SentencePiece 按规则给 [hug][ging]。
- **tiktoken** 永远字节级、无 unk；**SentencePiece** 码点级，靠 `byte_fallback` 才保证无 unk。

**特例（不完全属于两派）**：
- Mistral **Tekken**（131k）：自研 v3 tokenizer，vLLM 特判（`MistralTokenizer`）
- DeepSeek **V3.2/V4**：SentencePiece 基础上的自定义 tokenizer，vLLM 特判（`deepseek_v32`/`deepseek_v4`）
- Claude：自研 BBPE（字节级，未公开）；OpenAI **harmony**（o1/o3/o4）：tiktoken 派生的推理专用编码（显式 channel token）
- WordPiece：只剩 BERT 时代，当前生成式模型不用

**工程现实**：vLLM 里绝大多数模型走模型自带的 hub tokenizer_class（通用 HF fast tokenizer），只有 Mistral Tekken、DeepSeek V3.2/V4、Kimi audio 等少数需要特判——两派在推理引擎层面基本被统一了。

**演进趋势**：
- 词表一路涨：GPT-2/3 50k → GPT-4o `o200k_base` 200k；LLaMA 2 32k → LLaMA 4 200k；Gemma 3 256k。驱动力是多语言——"a bigger vocab buys back the per-token efficiency loss on non-English text"。
- **tiktoken 行为在扩散**：Llama 3 从 SentencePiece（Llama 2）转向 tiktoken 行为；Kimi K2 直接用 tiktoken.model——"码点级"向"字节级"收敛。
- 2025–2026 两条线：闭源扩表做多语言（Gemini 3 ~256k）；国产模型（Qwen/DeepSeek/GLM/Kimi/MiniMax）用"中文/代码优化词表"打性价比。

**结论**：做中文/多语言场景，分词器效率应和模型能力并列作为选型标准；具体选型时用实际分词器按你的语料试算 token 数，别只看品牌。

#### 3.4 分词效率：度量指标与实证（2025–2026）

- **度量指标**：除压缩比外，常用 fertility（每个词的 token 数）、token purity、每字符 token 数（tokens-per-character）；跨语言用"token 溢价/惩罚系数"。
- **词表最优规模**（Ali et al. 2023）：单语英语约 33k–50k 词表即可；多语言（5+ 语言）需 ~100k 才能维持同等每词 token 数。
- **成本是现实驱动**：按 token 计费下，同一文本在不同分词器可能是 1200 → 800 token（省约 1/3）；在代码/JSON/多语言上差距可达 2×+。每天 10M token 的多语言客服场景，30% 的效率差就是真金白银。
- **2025–2026 关键变化**：OpenAI 为 o1/o3/o4 推理模型发了 `harmony` 对话格式与配套编码（openai-harmony）；Llama 4、DeepSeek V4 标准化到 128k–200k tiktoken 风格词表、多语言覆盖更强；业界认为闭源/开源的分词效率差距基本收窄。
- **中英文效率的实证纠偏**：arxiv 2604.14210 标题即 "Mythbuster: Chinese Is Not More Efficient Than English in Vibe Coding"——在 vibe coding（自然语言生成代码）场景，中文并不比英文省 token、解题率也没更高；"中文更省"要分场景，不能一概而论。
- **工程建议**（futureagi.com）：按语言各取 10K 样本测 tokens-per-character 做审计；把分词器版本当模型版本一样 pin 在 CI；跟踪 tokens-per-character 漂移（新模型发布可能换分词器，成本先变）。
- **前沿方向**：语言感知/形态感知分词、动态词表更新、跨语言 embedding 共享（见 emergentmind 综述）。

### 4. 训练工程

这一维度讲"怎么造/改一个分词器"：工程流程与场景，与第 2 维度的算法机制正交。

#### 4.1 从零训练一个分词器

1. **准备语料**：与预训练语料同分布、有代表性、已去重；多语言按语言加权采样（`alpha` 控制稀有语言份额）。
2. **选算法与工具**：HuggingFace `tokenizers`（`BpeTrainer`/`WordPieceTrainer`/`UnigramTrainer`，初始化→train→save）；SentencePiece（`spm.SentencePieceTrainer.Train(...)`，`model_type`、`byte_fallback`、`pad_id/unk_id/bos_id/eos_id`、`user_defined_symbols`）；OpenAI tiktoken（Rust 字节级 BPE，GPT 系）。
3. **关键超参**：`vocab_size`（100k–200k）、`min_frequency`（≥2）、`initial_alphabet`（字节级 256 基础表）、`special_tokens`（手工预留）。
4. **训练成本量级**：100MB 语料约 1–2 分钟，1GB 约 10–20 分钟（HF tokenizers）。
5. **训后纪律**：分词器一经训练即为模型制品的一部分，不可修改；可以往词表追加特殊 token（embedding resize），但不能改合并规则——那会改变已有 token 的切分、破坏已训练 embedding 的对齐。
6. **验证**：压缩比、unk 出现率、各语言 token 惩罚系数、往返一致性。

#### 4.2 已有分词器上扩展新语言

场景：英文中心分词器（如 Llama 3）要支持印地语/新语言——英文中心词表里该语言字符占比极低（例：Nemotron 的 131,072 词表只有 1,569 个天城文条目，仅 1.2%）。四步：

1. **生成新 token**：在新语言语料上训练新分词器（或 SentencePiece 混合语料重训），提取原词表没有的新 token；也可复用现成的扩展分词器（如 Nanda 为 Llama-3 扩展 25,600 个印地语 token）。
2. **追加词表**：新 token 索引从当前词表长度开始；`add_tokens`/`add_special_tokens` 加入，`resize_token_embeddings` 调整 embedding 矩阵。
3. **初始化新 token 的 embedding**（关键，影响 CPT 收敛）：随机初始化会训练不稳。常用策略按效果排序（arxiv 2608.03494 在 2000+ 策略上的系统实验）：子词组合（subword composition）最好（非对称变体最优）> 外部/学习式初始化（FOCUS、top-k 语义检索、残差 MLP 映射）> 词表平均（vocabulary averaging）；还需 norm 校准。
4. **继续预训练（CPT）整合**：只加词表不训练没用——必须在包含新 token 的语料上 CPT/微调。量级参考：Nemotron-Mini-4B 在 400B 印英 token 上 CPT。

**陷阱**（arxiv 2512.03989）：单纯"训练新分词器 + 追加其 token"会引入不参与合并的无用 token——BPE 严格遵循合并序列，新 token 不进 merge 序列就不会被用到，压缩率反而下降。正确做法是让新 token 真正参与合并。

#### 4.3 领域扩展（专业 token）

向预训练 LLM 追加领域 token（医学/法律/代码术语、`ChatGPT` 这种会被拆成 Chat+GPT 的词）是微调前的常见操作：减少语义碎片化、降低微调所需数据量、引入自定义格式 token。步骤与 4.2 相同（加 token → resize → 初始化 → 微调）；属"词表扩容 + 微调"，效果受限于新 token 在数据中的实际出现。

#### 4.4 整体替换分词器（vocab replacement）

把英文中心分词器整体换成更好的多语言分词器（如用 Nanda tokenizer 换掉 Llama-3 的），词表完全重来。与 4.2 的区别：4.2 保留原词表 + 追加；4.4 全量替换。代价大：所有文本要重新映射到新 token、全部 embedding 要重初始化（子词组合）、需要大规模 CPT。通常只在预算充足或重训阶段做。

#### 4.5 词表剪枝与压缩（vocab pruning）

词表过大导致 embedding/显存开销高时，删低频/无用 token 缩小词表。风险：改变合并序列、影响已有切分；需重新校准并验证压缩比不回退。相关讨论见 arxiv 2512.03989（"Pruning infrequent ..."）。

### 5. 推理工程

这一维度讲"推理/部署侧怎么用分词器"，含 transformers、vLLM、SGLang 三个落地面。

#### 5.1 通用流程（编码 → 生成 → 解码）

1. **编码（encode）**：prompt 文本 → 归一化（Unicode/大小写）→ 预分词 → 模型切分 → 追加特殊 token/chat 模板 → token id 序列。这是 LLM 推理入口的第一步。
2. **chat 模板与特殊 token**：`<s>`/`</s>`、`<|begin_of_text|>`、`<|im_start|>`/`<|im_end|>` 等把角色包起来；模板错会直接导致输出格式错乱。
3. **截断与上下文窗口**：超长输入按 `max_length` 截断，token 数决定能否塞进上下文窗口。
4. **解码（decode）**：生成时逐个/逐块把 token id 还原成文本；流式输出每出一个 token 解一次，要处理多字节 UTF-8 拆分（如汉字被拆成多字节 token 时的拼接）。
5. **计费与配额**：按 token 计费/限流，必须先编码数 token；中文在英文中心分词器下账单更高。
6. **与 KV cache 的关系**：KV cache 按 token 存，上下文越长显存越大。
7. **字节回退在推理侧**：输入 emoji/生僻字/新词时，好的分词器安静地拆成字节 token 继续跑，而不是吐出 [UNK]。

#### 5.2 transformers（HuggingFace）实现

- **加载**：`AutoTokenizer.from_pretrained(model_id)`。fast vs slow：fast 走 HF `tokenizers` 的 Rust 后端（快、支持 batch/offset 映射），slow 是纯 Python 回退；`use_fast=True/False` 可选。
- **编码**：`tokenizer.encode(text, add_special_tokens=True)`；批量 `tokenizer(texts, padding=True, truncation=True, max_length=..., return_tensors="pt")` 返回 `input_ids`/`attention_mask`（需要 `token_type_ids` 的模型如 BERT 也有）。
- **chat 模板**：`tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True)`——用 tokenizer 自带的 Jinja2 模板把 messages 转成带特殊 token 的输入。
- **解码**：`tokenizer.decode(ids, skip_special_tokens=True)`；`batch_decode`。
- **流式生成**：`model.generate(..., streamer=TextIteratorStreamer(tokenizer))`——每个新 token 出来即增量解码并 yield 文本片段。
- **自定义**：`tokenizer.add_tokens([...])` + `model.resize_token_embeddings(len(tokenizer))`（对应第 4 节扩展场景）；`vocab_size` 直接可读。

#### 5.3 vLLM 实现（含本地源码）

> 以下来自本地源码（`vLLM 仓库`），逐行核对。SGLang 见 5.4，同一核心思路、不同结构。

**先分清两侧：encode 和 decode 的难度完全不同。**
- **encode（tokenize）侧**：一次性、非流式，难点在并发安全与批量效率。
- **decode（detokenize）侧**：流式、逐 token，有 cleanup heuristic 和 UTF-8 拆分两个坑。

##### encode（tokenize）侧

1. `InputProcessor.process_inputs` → `renderer.render_cmpl`：chat 请求先用 tokenizer 的 **Jinja2 chat template**（`apply_chat_template(messages, tokenize=True, add_generation_prompt=True)`）把 messages 拼成带角色特殊 token 的输入。
2. `tokenizer.encode` 走 HF tokenizers 的 5 段管线：**normalize → pre-tokenize → model（BPE 合并）→ post-process（追加特殊 token）**——即第 2 节讲的算法在推理侧的落地。
3. **线程安全是 encode 侧的核心工程问题**：HF fast tokenizer 非线程安全，而服务要并发处理请求。`maybe_make_thread_pool`（`vllm/tokenizers/hf.py`）维护一个**深拷贝 tokenizer 池**（queue）：每次 encode 从池里借一个、用完归还，队列空就现深拷贝一个——并发请求各自拿到独立实例。
4. `CachedHfTokenizer` 缓存常用属性（special ids 等）；非 HF 模型（Mistral Tekken、DeepSeek V3.2/V4、Kimi audio）走 `tokenizers/registry.py` 的自定义类；`skip_tokenizer_init` 直接吃外部 input_ids。

##### decode（detokenize）侧

**为什么难**：tokenizer 的 `decode` 有两个坑，直接单 token 解码会出错：
1. **cleanup heuristic**：decode 依据**前后 token** 决定是否在词间加空格，单解一个 token 会丢/多空格（源码注释原文：*"defeat cleanup algorithms in the decode which decide to add a space or not depending on the surrounding ids"*）。
2. **UTF-8 多字节拆分**：字节级 BPE 把汉字（3 字节）/emoji（4 字节）拆成多个字节 token，单解中间字节 token 出乱码 `�`（U+FFFD）。

所以正确做法是**带着上下文整段解，再切出增量**。完整链路：

```
请求 → InputProcessor（chat template + tokenize）→ GPU 生成 token_ids
     → OutputProcessor（每请求一个 IncrementalDetokenizer）
     → update() 逐 token 增量解码 → get_next_output_text(delta=True) 只发增量给客户端
```

**核心算法** `detokenize_incrementally`（`vllm/tokenizers/detokenizer_utils.py`，源自 HF TGI，Apache 2.0）。状态 = `prev_tokens + prefix_offset + read_offset`：

```text
已有 tokens: [t1 t2 t3 t4]（上次解到 read_offset=4）
新来 t5：
  对 output_tokens[prefix_offset:]  = [t3 t4 t5] 整体 decode → "abc def"   （带上下文，空格正确）
  对 output_tokens[prefix_offset:read_offset] = [t3 t4] decode → "abc "
  增量 = new_text[len(prefix_text):] = "def"
  若 new_text 以 "�" 结尾 → 返回空串、offset 不动（扣住未完成字节）
```

`prefix_offset` 的意义：decode 的加空格依赖上下文，所以每次都从 `prefix_offset`（保守起点，`INITIAL_INCREMENTAL_DETOKENIZATION_OFFSET = 5`）重解，再用 `read_offset` 切出增量。

**UTF-8 续接例子**（汉字"好" = 3 个字节 token）：
```text
收到 字节token1 → decode → "�"（不完整）→ 扣住，不发给客户端
收到 字节token2 → decode(1,2) → "�"（仍不完整）→ 扣住
收到 字节token3 → decode(1,2,3) → "好" → 这才发给客户端
```
判断条件 `if len(new_text) <= len(prefix_text) or new_text.endswith("�")`；`�` 在末尾 = 正常未完成序列（hold），在中间 = 真非法 id（错误）。

**两个 detokenizer 后端**（`vllm/v1/engine/detokenizer.py`）：`LLMDetokenizer` 用 HF `tokenizers.decoders.DecodeStream`（Rust，内部自带字节续接状态机）；`FastLLMDetokenizer` 用上面的增量算法。

**附带细节**：SentencePiece 前导空格 `▁` 恢复（`_get_leading_space_marker`/`_restore_leading_spaces`，Metaspace decode 吃掉前导 ▁，按原始 vocab piece 补回空格；ByteLevel/GPT-2 无此问题）；越界 id 防护（`_replace_none_with_empty`）；`INVALID_PREFIX_ERR_MSG` 时重置 DecodeStream 不崩。

#### 5.4 SGLang 实现（含本地源码）

> 与 vLLM 同一核心思路（滑动窗口重解 + `endswith("�")` 扣字节，机制见 5.3 decode 的"为什么难"），本节只讲 SGLang 自己的结构与工程差异。

##### encode（tokenize）侧

1. `TokenizerManager._tokenize_one_request` → `_tokenize_texts`：先 `_detect_input_format` / `_prepare_tokenizer_input` 准备输入，再 apply_chat_template + encode → input_ids。
2. **`AsyncDynamicbatchTokenizer`**：把多个并发请求的 encode **异步动态成批**——队列攒请求，满 `max_batch_size=32` 或等 `batch_wait_timeout_s=0.002` 秒就批量 encode 一次。高并发下省大量开销，这是 SGLang encode 侧的主要优化。
3. **multi-tokenizer**：一个服务同时服务多个模型时，不同请求路由到各自模型的分词器。
4. 同样支持 `skip_tokenizer_init`；`input_embeds` 路径（不走 tokenize）也在这里分流。

##### decode（detokenize）侧

`DetokenizerManager`（独立进程）用 `DecodeStatus` 状态机：`decode_ids / surr_offset / read_offset / sent_offset / decoded_text`。核心在 `_decode_batch_token_id_output`：

```text
每步（对一批请求）：
  read_ids = decode_ids[surr_offset:]               # 本次要解的全部
  surr_ids = decode_ids[surr_offset:read_offset]    # 上次解过的（作上下文前缀）
  两段都 decode → read_texts / surr_texts
  增量 = read_texts[i][len(surr_texts[i]):]         # 用 surr 前缀切掉已发部分
  若 new_text 不以 "�" 结尾 → 提交：advance surr_offset/read_offset/sent_offset，发增量
  否则 → 只发"可打印前缀"（find_printable_text），不提交（offset 不动，下次带更多 token 重试）
完成时 → 一次性 materialize + trim 掉匹配的 stop + 发 output_str[sent_offset:]
```

工程差异：SGLang 把多请求的 `surr_ids`/`read_ids` **分组批量 decode**（`_grouped_batch_decode`，减少高并发下 per-request 开销），并提供 `disable_tokenizer_batch_decode`（某些 tokenizer 如 gpt-oss 有批处理边界问题，需逐条解）；`_clamp_decode_ids` 兜底越界 id。

#### 5.5 两引擎对照与长上下文计费

**核心对照**（同概念、不同命名）：

| 概念 | vLLM | SGLang |
| --- | --- | --- |
| 上下文窗口起点 | `prefix_offset` | `surr_offset` |
| 当前位置 | `read_offset` | `read_offset` |
| 已发送游标（流式增量） | `_last_output_text_offset` | `sent_offset` |
| UTF-8 未完成判断 | `endswith("�")` → 空串 | `endswith("�")` → 可打印前缀 |
| 解码后端 | HF `DecodeStream`（Rust）/ 增量算法 | 分组批量 decode（可关） |
| encode 批量 | 线程池深拷贝 tokenizer | `AsyncDynamicbatchTokenizer`（攒批 32/2ms） |

**RadixAttention 与分词**（SGLang）：前缀复用要求请求共享相同 token 前缀（chat 模板、RAG 上下文、agent 多轮）；分词质量直接影响前缀能否对齐、能否复用 KV。

**长上下文与计费**：长上下文模型（如 Llama 4 Scout 10M）需要预切分确认超限截断；token 数是上下文窗口、KV cache、计费的直接分母。计费/限流在服务端通过 tokenizer encode 计数实现；同一输入不同分词器 token 数差异很大（中文税），选型时应以实际分词器试算为准。

### 6. 未来方向：端到端免分词

官方愿景："The dream: tokenizer-free model architectures, which operate directly on bytes"（lecture_01.py），引用的家族是 ByT5、MegaByte、BLT（Byte Latent Transformer）、T-FREE、H-Net（对应 cs336-p01 转录里的 "Hanet"）。官方判断："These are promising, but have not yet been scaled up to the frontier"（lecture_01.py）。

任何替代方案都要满足（cs336-p01）：(1) 提供序列抽象表示（视频/DNA 序列时最明显）；(2) 数据块可变、支持自适应计算（"并非所有字节都生而平等"）。

## 待补充到 sources 的来源清单

以下来源后续应归档进 `content/sources/`（作为 Source）以便正式锚定；标注了当前获取方式。

- **官方课程**：`content/sources/computer-science/cs336-2026/official-materials/lectures/lecture_01.py`（已在库，可直接锚定）；Stanford CS336 官网。
- **算法论文**：Sennrich et al. 2016（BPE for NMT）；Schuster & Nakajima 2012（WordPiece）；Kudo & Richardson 2018（SentencePiece）；Gage 1994（BPE 数据压缩）；Kudo 2018《Subword Regularization》（Unigram）；arxiv 2012.15524 + Google 博客《A Fast WordPiece Tokenization System》（WordPiece 编码/加速）；EMNLP 2020《Byte Pair Encoding is Suboptimal for Language Model Pretraining》。
- **免分词**：ByT5、MegaByte、BLT（Byte Latent Transformer）、T-FREE、H-Net（2023–2025，官方引用）。
- **词汇扩展**：arxiv 2608.03494（Token Embedding Initialization for Vocabulary Extension）；arxiv 2512.03989（Teaching Old Tokenizers New Words）；Nanda tokenizer（扩展 Llama）。
- **词表实证**：arxiv 2605.30813（Incremental BPE Tokenization，H.3 词表表）。
- **模型 tokenizer**：HuggingFace / ModelScope 各模型页的 `tokenizer_config.json`、`config.json`（GLM-5、Kimi-K2、MiniMax-M2、DeepSeek-V3、Qwen3、Llama-4、Mistral-Large-3、Gemma-3、GPT-OSS）——`vocab_size` 字段即词表大小。
- **工具文档**：HuggingFace `tokenizers`/`transformers` 文档（tokenizer 训练、fast/slow、apply_chat_template）；SentencePiece GitHub；tiktoken（OpenAI）GitHub；vLLM 文档（OpenAI 兼容服务、chat template、/tokenize /detokenize）；SGLang 文档（RadixAttention）；Ray `working-with-llms`（LLM 阶段管线）。
- **中文税文章**：36kr《AI 大模型的「中文税」》（含 Opus 4.7 中文 1.000×）；腾讯云《主流大模型 Token 计算方式全解析》；章北海《一个汉字多少 Token》。
- **分词效率研究**：presenc.ai/research/llm-tokenizer-efficiency-comparison-2026（Claude Opus 4.7/GPT-5.5/Gemini 3.1/DeepSeek V4/Qwen 3.5 每词 token 对比）；futureagi.com/blog/what-is-tokenization-llms-2026（2025–2026 分词器变化 + 工程审计建议）；arxiv 2604.14210（中文 vibe coding 效率 Mythbuster）；Ali et al. 2023（最优词表规模）；Arnett et al. 2025（最优词表分配/幂律）；Wegmann et al. 2025（task-aware probes 预测下游效果）；emergentmind 的 language-specific / multilingual tokenizer 综述。
- **推理引擎源码（本地）**：`vllm/tokenizers/detokenizer_utils.py`、`.../vllm/v1/engine/detokenizer.py`；`.../sglang/python/sglang/srt/managers/detokenizer_manager.py`。
- **OpenAI 官方口径**：platform.openai.com tokenizer 页与文档（1000 token ≈ 750 英文词 ≈ 500 汉字）。

## 参考

- cs336-p01 转录（Stanford CS336 第一讲，[00:23:38–01:04:56] 分词段落）+ 官方 `lecture_01.py`（分词小节）——本文件已核实的主要来源
- 词表对比与趋势：arxiv.org/html/2605.30813v1（H.3 表）、iotdigitaltwinplm.com、rohan-paul.com、iternal.ai/llm-selection-guide、zhuanlan.zhihu.com/p/2050733508507833888、gradually.ai/en/llm-statistics
- 词表实查：huggingface.co（zai-org/GLM-5、moonshotai/Kimi-K2-Instruct、MiniMaxAI/MiniMax-M2、transformers 文档 minimax_m2/glm_moe_dsa/glm4_moe）
- 中文税与中英对比：36kr.com/p/3793050208984071、cloud.tencent.com/developer/article/2550219、blog.zhanglearning.com、blog.csdn.net/Leon_Jinhai_Sun
- 训练/扩展：kunwar.page/chapter/014、huggingface.co/learn/llm-course、news.qq.com/rain/a/20250320A05LYX00、arxiv.org/html/2608.03494v1、arxiv.org/html/2512.03989v2
- 推理实现（源码级）：本地 `vLLM 仓库`（detokenizer_utils.py、v1/engine/detokenizer.py）与 `.../sglang`（srt/managers/detokenizer_manager.py）；docs.vllm.ai、docs.ray.io/en/latest/data/working-with-llms.html、jarvislabs.ai/blog/vllm-sglang-trtllm-comparison、huggingface.co/docs/transformers（tokenizer/chat template）
- 分词效率：presenc.ai/research/llm-tokenizer-efficiency-comparison-2026、futureagi.com/blog/what-is-tokenization-llms-2026、arxiv 2604.14210（中文 vibe coding Mythbuster）、emergentmind.com/topics/language-specific-tokenizer-design（Ali et al. 2023 最优词表规模）
- 算法起源：Sennrich et al. 2016、Schuster & Nakajima 2012、Kudo & Richardson 2018
- 模型架构背景：magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison、www.turingpost.com/p/chinesemodels、finance.sina.cn/stock/jdts/2026-02-27
