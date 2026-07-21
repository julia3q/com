# Personal Surge Rules (julia3q)

這是我的個人 Surge 自訂分流清單與模組設定檔。主要用於補足現有大型規則（如 skk.moe 等）未覆蓋的台灣本地化需求及個人常用開發服務。

## 目錄結構 (Directory Structure)

- **/Lists**: 包含各種自訂的 `.list` 分流規則（如 Proxy、ProxyLocal、Reject、台灣專屬等）。
- **根目錄 `*.sgmodule`**: 自訂的 Surge 模組，如去廣告、銀行白名單、臺灣去廣告等。

## 遠端引用 (Remote URLs)

如果你需要在自己的 Surge 中引用這些清單，可以使用以下 Raw URLs (配合 `RULE-SET` 使用)：

### 規則清單 (Rule-Set)
* **Custom Proxy (自訂代理 & 開發者工具)**
  `https://raw.githubusercontent.com/julia3q/sync/refs/heads/main/Lists/Custom.Proxy.list`
* **Custom ProxyLocal (最近節點 / CDN)**
  `https://raw.githubusercontent.com/julia3q/sync/refs/heads/main/Lists/Custom.ProxyLocal.list`
* **Custom Reject (自訂阻擋/去廣告)**
  `https://raw.githubusercontent.com/julia3q/sync/refs/heads/main/Lists/Custom.Reject.list`
* **TW (台灣專屬規則)**
  `https://raw.githubusercontent.com/julia3q/sync/refs/heads/main/Lists/TW.list`

### 模組 (Modules)
* **AppleRouting (Apple 服務分流 / 非國區 AI 解鎖)**
  `https://raw.githubusercontent.com/julia3q/sync/refs/heads/main/AppleRouting.sgmodule`
* **Bank Bypass (銀行網銀繞過代理)**
  `https://raw.githubusercontent.com/julia3q/sync/refs/heads/main/Bank_Bypass.sgmodule`
* **AdBlock (去廣告/追蹤：網域·IP 版，免 MITM)**
  `https://raw.githubusercontent.com/julia3q/sync/refs/heads/main/AdBlock.sgmodule`

## 維護方式
本專案僅包含可公開的清單 (`Lists/`) 與根目錄模組 (`*.sgmodule`)。
