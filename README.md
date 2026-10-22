# Hui Hui Xie · 谢辉辉

个人学术主页，适用于现有 GitHub Pages 仓库 `xhh22900/xhh22900.github.io`。

## 预览

直接用浏览器打开根目录的 `index.html` 即可。样式、语言切换、论文筛选和搜索均不依赖网络资源。

也可以在仓库目录运行：

```sh
python -m http.server 8765 --bind 127.0.0.1
```

然后打开 `http://127.0.0.1:8765`。

## 更新内容

主要学术内容保存在 `_data/academic.json`：论文、研究简介、教育经历、会议报告与基金项目。

修改数据后运行：

```sh
python _homepage/build.py
```

此命令仅使用 Python 标准库，重新生成 `index.html`。默认显示五篇代表作及其中英文导读，可筛选全部 14 篇已发表论文、七篇第一作者论文或量子信息工作。导读只在代表作视图显示。

- 页面模板：`_homepage/index.template.html`
- 样式与移动端布局：`assets/css/academic.css`
- 语言切换、论文搜索、导航：`assets/js/academic.js`
- 公开版学术简历：`assets/files/huihui-xie-academic-cv.pdf`
- 公开版英文简历：`assets/files/huihui-xie-academic-cv-en.pdf`
- 引用元数据：`_data/citations.json`
- 完整 BibTeX 文件：`assets/files/huihui-xie-publications.bib`
- 各论文 BibTeX 文件：`assets/files/bibtex/`

主页和公开版简历不包含电话、出生年月或政治面貌。中文公开版简历单独维护；英文简历读取共享学术记录和 `_data/cv_en.json`，运行 `python _homepage/build_cv_en.py` 生成，需要 ReportLab。

每篇期刊论文提供 DOI 和可展开、复制、下载的 BibTeX。arXiv 链接按 DOI 在 INSPIRE 文献记录中匹配，只有确认存在对应版本的文章才显示链接。引用作者、期刊、卷期与文章号依据 Crossref DOI 元数据核对；现有合集包含 14 篇已发表期刊论文。个人学术入口采用已确认的 ORCID。

## 页面风格与数学符号

采用白底、深灰正文和蓝色链接，正文 16–17 px，论文标题 21–22 px，作者与期刊信息 15–16 px。首屏直接展示姓名、单位和简介。研究联系示意图采用浏览器原生 MathML 排版，不依赖远程字体或公式渲染服务。

示意图以核电荷密度 ρ_ch(r) 为起点，分别连接电荷半径与径向矩、能级与束缚电子 g 因子、电子散射微分截面；各条计算路径相互独立。半径与径向矩连接 Pb、Ca 同位素电荷半径演化和晕核电荷性质的研究。缪原子光谱单独采用双向虚线，表达理论计算、光谱反演提取与实验约束之间的联系；不把径向矩画成计算能级、g 因子或散射截面的必经步骤。

## GitHub Pages

保留原仓库的 Jekyll / Minima 配置。新 `index.html` 是完整静态页面，不需要安装 Node、前端依赖或额外构建服务。

旧的 `index.markdown` 保留为 `/archive/original-home/`，避免与新的根目录首页发生输出路径冲突。原有博客与其他页面的来源文件保留。

发布时只需将本次改动提交到原仓库已有的 Pages 发布分支。没有新增域名、账户或托管服务。

## Content notes

- Published papers, manuscripts under review, and preprints are listed separately.
- The PRL manuscript remains marked **under review** until the author confirms a status change.
- RCHB is described as a code used and adapted for research outputs, not as an originally developed code.
- Chinese terminology: FNS → 核体积效应; generalized pseudospectral method → 一般伪谱法.
- Master’s advisors: 焦利光 (precision atomic calculations), 曾国模 (quantum information).

Last content update: 2026-10-22.
