# Changelog

All notable changes to the TrolMaster Product Search App will be documented in this file.

## [1.0.25] - 2026-05-03

### Added
- **Footer Disclaimer 免責聲明**：
  - 添加免責聲明文字：「價格僅供參考，最終價格以 TrolMaster 確認為準」
  - 三語支持：EN / 繁體中文 / 泰文
  - 位置：Footer 最底部
  - CSS 樣式：`.footer-disclaimer`（灰色小字）

### Technical Details
- 修改 `src/i18n/en.json` - 添加 `disclaimer` 翻譯
- 修改 `src/i18n/zh-Hant.json` - 添加 `disclaimer` 翻譯
- 修改 `src/i18n/th.json` - 添加 `disclaimer` 翻譯
- 修改 `src/templates/index.html.template` - Footer 添加免責聲明行
- 修改 `src/static/styles.css` - 添加 `.footer-disclaimer` 樣式

### Deployment
- ✅ 已部署到 GitHub Pages: https://rain-trolmaster.github.io/trolmaster-portal/

## [1.0.24] - 2026-05-03

### Changed
- **UI优化 - 价格前置**：产品卡片信息重排序，价格表格移至Product Information之前
  - 原因：用户主要用来查价格和库存，应该优先显示
  - 新顺序：价格表格 → Product Information → 库存信息
  
- **手机端Header优化**：
  - Logo高度：30px → 28px
  - 公司名防止换行（添加 `white-space: nowrap; overflow: hidden; text-overflow: ellipsis;`）
  - 隐藏 "Data sourced from Google Sheets" 行（手机端简化显示）
  
### Technical Details
- 修改 `src/static/app.js` - `buildProductCard()` 重排序HTML结构
- 修改 `src/static/styles.css` - 添加响应式规则 @media (max-width: 600px)
- 修改 `src/templates/index.html.template` - 添加 `.header-sub` class
- 构建输出：build/index.html (645.2 KB)

### Deployment
- ✅ 已部署到 GitHub Pages: https://rain-trolmaster.github.io/trolmaster-portal/

## [1.0.23] - 2026-05-03

### Added
- 产品 short_desc 多语言翻译（繁体中文 + 泰文）
- 翻译文件：`src/i18n/product_translations_zh.json`、`src/i18n/product_translations_th.json`
- 覆盖率：zh-Hant 177/177 (100%)，Thai 151/178 (84%)
- 翻译逻辑："冇就收埋，有就要显示" - 空翻译自动fallback回英文

### Technical Details
- 使用AI直接翻译并写入Python script生成JSON（googletrans/deep-translator/MyMemory都失败）
- 修改 `src/static/app.js` - `buildProductCard()` 翻译逻辑改为只覆盖非空翻译
- full_description 和 features 暂时留空（可后续补充）

### Deployment
- ✅ 已部署到 GitHub Pages
