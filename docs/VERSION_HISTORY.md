# 版本歷史紀錄

本文件記錄每次構建嘅變更內容，方便日後查閱同回滾。

---


## v1.0.0 — 2026-05-03
- **Description**: initial_build
- **Snapshot**: `build/versions/2026-05-03/20260503_090947_v1.0.0_initial_build.html`

## v1.0.1 — 2026-05-03
- **Description**: restored old pro blue style
- **Snapshot**: `build/versions/2026-05-03/20260503_092523_v1.0.1_restored_old_pro_blue_style.html`

## v1.0.2 — 2026-05-03
- **Description**: 修复搜索功能：擴展到所有產品欄位；修復 getStockInfo() bug (badgeLabel/badgeKey)；修復 no_results i18n key
- **Snapshot**: `build/versions/2026-05-03/20260503_094350_v1.0.2_修复搜索功能_擴展到所有產品欄位_修復_getStockInfo___bug__.html`

## v1.0.3 — 2026-05-03
- **Description**: 修復搜索功能（擴展到所有產品欄位）；修復getStockInfo() bug；更新no_results i18n加入{q}佔位
- **Snapshot**: `build/versions/2026-05-03/20260503_094442_v1.0.3_修復搜索功能_擴展到所有產品欄位__修復getStockInfo___bug_更.html`

## v1.0.4 — 2026-05-03
- **Description**: 更新hero_title/hero_sub為頁面正確名稱：Product Price and Stock / 產品價格及庫存 / ราคาและสต็อกสินค้า
- **Snapshot**: `build/versions/2026-05-03/20260503_094853_v1.0.4_更新hero_title_hero_sub為頁面正確名稱_Product_Pri.html`

## v1.0.5 — 2026-05-03
- **Description**: 修復庫存unknown問題：stock_level係數字唔係文字，改用數字判斷庫存狀態；新增in_stock/low_stock/out_of_stock/unknown i18n key
- **Snapshot**: `build/versions/2026-05-03/20260503_095325_v1.0.5_修復庫存unknown問題_stock_level係數字唔係文字_改用數字判斷庫.html`

## v1.0.6 — 2026-05-03
- **Description**: Description truncation with more/less toggle
- **Snapshot**: `build/versions/2026-05-03/20260503_095636_v1.0.6_Description_truncation_with_more_less_to.html`

## v1.0.7 — 2026-05-03
- **Description**: Card layout: description as title, model in chip, remove unknown badge
- **Snapshot**: `build/versions/2026-05-03/20260503_095930_v1.0.7_Card_layout__description_as_title__model.html`

## v1.0.8 — 2026-05-03
- **Description**: Search normalization: ignore hyphens (V8 matches V-8, HydroX matches Hydro-X)
- **Snapshot**: `build/versions/2026-05-03/20260503_100149_v1.0.8_Search_normalization__ignore_hyphens__V8.html`

## v1.0.9 — 2026-05-03
- **Description**: Fix inventory: skip header row, normalize search with spaces, sort results
- **Snapshot**: `build/versions/2026-05-03/20260503_101622_v1.0.9_Fix_inventory__skip_header_row__normaliz.html`

## v1.0.10 — 2026-05-03
- **Description**: v1.0.10: 新增Product Information欄位於圖片上方，移除藍色標題區的more按鈕
- **Snapshot**: `build/versions/2026-05-03/20260503_102604_v1.0.10_v1_0_10__新增Product_Information欄位於圖片上方_移除.html`

## v1.0.11 — 2026-05-03
- **Description**: v1.0.11: 藍色標題區改為只顯示Short Description，唔再用完整描述
- **Snapshot**: `build/versions/2026-05-03/20260503_102756_v1.0.11_v1_0_11__藍色標題區改為只顯示Short_Description_唔再用.html`

## v1.0.12 — 2026-05-03
- **Description**: v1.0.12: 修復庫存顯示—加入fallback庫存數據同console debug
- **Snapshot**: `build/versions/2026-05-03/20260503_103301_v1.0.12_v1_0_12__修復庫存顯示_加入fallback庫存數據同console_d.html`

## v1.0.13 — 2026-05-03
- **Description**: Order Estimation page changed to Coming Soon
- **Snapshot**: `build/versions/2026-05-03/20260503_103912_v1.0.13_Order_Estimation_page_changed_to_Coming_.html`

## v1.0.14 — 2026-05-03
- **Description**: Improve search relevance scoring
- **Snapshot**: `build/versions/2026-05-03/20260503_120916_v1.0.14_Improve_search_relevance_scoring.html`

## v1.0.15 — 2026-05-03
- **Description**: Fix search false matches: word-boundary regex prevents V-6 matching CV6001
- **Snapshot**: `build/versions/2026-05-03/20260503_121450_v1.0.15_Fix_search_false_matches__word-boundary_.html`

## v1.0.16 — 2026-05-03
- **Description**: Improve search: short_desc starts-with bonus + word-boundary fix
- **Snapshot**: `build/versions/2026-05-03/20260503_121624_v1.0.16_Improve_search__short_desc_starts-with_b.html`

## v1.0.17 — 2026-05-03
- **Description**: Fix: include HCS-1 (gviz rows already exclude headers, no need to skip row 0)
- **Snapshot**: `build/versions/2026-05-03/20260503_122736_v1.0.17_Fix__include_HCS-1__gviz_rows_already_ex.html`

## v1.0.18 — 2026-05-03
- **Description**: Fix: include HCS-1 (remove incorrect skip_header=1 in fetch_products/inventory)
- **Snapshot**: `build/versions/2026-05-03/20260503_122854_v1.0.18_Fix__include_HCS-1__remove_incorrect_ski.html`

## v1.0.19 — 2026-05-03
- **Description**: Add category headers for brand grouping
- **Snapshot**: `build/versions/2026-05-03/20260503_123532_v1.0.19_Add_category_headers_for_brand_grouping.html`

## v1.0.20 — 2026-05-03
- **Description**: Hide Image/Materials rows when no link
- **Snapshot**: `build/versions/2026-05-03/20260503_130458_v1.0.20_Hide_Image_Materials_rows_when_no_link.html`

## v1.0.21 — 2026-05-03
- **Description**: Add compatibility display in product card
- **Snapshot**: `build/versions/2026-05-03/20260503_132551_v1.0.21_Add_compatibility_display_in_product_car.html`

## v1.0.22 — 2026-05-03
- **Description**: v1.0.22: 搜索相关性修复(Hydro/HCS/fan词边界)、品牌分类标题、Image/Materials/Compatibility条件显示(有则显示无则隐藏)
- **Snapshot**: `build/versions/2026-05-03/20260503_133214_v1.0.22_v1_0_22__搜索相关性修复_Hydro_HCS_fan词边界__品牌分类标.html`

## v1.0.23 — 2026-05-03
- **Description**: v1.0.23: 產品翻譯zh-Hant+Thai(short_desc)，翻譯fallback邏輯(冇就收埋有就顯示)
- **Snapshot**: `build/versions/2026-05-03/20260503_143109_v1.0.23_v1_0_23__產品翻譯zh-Hant_Thai_short_desc__翻譯.html`

## v1.0.24 — 2026-05-03
- **Description**: UI优化：价格移至产品信息前，手机端Header优化
- **Snapshot**: `build/versions/2026-05-03/20260503_144509_v1.0.24_UI优化_价格移至产品信息前_手机端Header优化.html`

## v1.0.25 — 2026-05-03
- **Description**: 添加Footer Disclaimer免責聲明
- **Snapshot**: `build/versions/2026-05-03/20260503_145607_v1.0.25_添加Footer_Disclaimer免責聲明.html`
