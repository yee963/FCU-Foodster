# API 路由與頁面設計 (API Design)

本文件描述逢甲「食」客 (FCU Foodie Hub) 專案中 F-02 模組（揪團與訂單拆帳）的 Flask 路由規劃。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **揪團大廳** | GET | `/groups` | `templates/groups/index.html` | 顯示所有開放中的揪團列表 |
| **新增揪團頁面** | GET | `/groups/new` | `templates/groups/new.html` | 顯示發起揪團的表單 |
| **建立揪團** | POST | `/groups` | — | 接收表單，存入 DB，重導向至大廳 |
| **揪團詳情與拆帳** | GET | `/groups/<int:id>` | `templates/groups/detail.html` | 顯示該團的詳細資訊、所有訂單與結算金額 |
| **結單與平攤運費** | POST | `/groups/<int:id>/close` | — | 團長專用：關閉揪團，計算 `split_fee`，重導向回詳情頁 |
| **點餐參團頁面** | GET | `/groups/<int:group_id>/orders/new` | `templates/orders/new.html` | 顯示參團點餐表單 |
| **送出點餐** | POST | `/groups/<int:group_id>/orders` | — | 接收餐點表單，存入 `orders` 與 `order_items`，重導向回揪團詳情 |
| **更新付款狀態** | POST | `/orders/<int:id>/pay` | — | 標記該訂單為 `paid` (已付款)，重導向回揪團詳情 |

---

## 2. 每個路由的詳細說明

### `GET /groups`
- **輸入**: 無
- **處理邏輯**: 呼叫 `Group.get_all()` 取得列表。
- **輸出**: 渲染 `groups/index.html`。

### `GET /groups/new`
- **輸入**: 無
- **處理邏輯**: 無。
- **輸出**: 渲染 `groups/new.html`。

### `POST /groups`
- **輸入**: 表單資料 (store_id, delivery_fee, pickup_location, deadline)。
- **處理邏輯**: 呼叫 `Group.create()` 寫入資料庫，狀態預設為 `open`。
- **輸出**: 重導向至 `/groups`。
- **錯誤處理**: 若缺漏必填欄位，使用 flash 顯示錯誤並重導向回 `/groups/new`。

### `GET /groups/<int:id>`
- **輸入**: URL 參數 `id`。
- **處理邏輯**:
  1. 呼叫 `Group.get_by_id(id)` 取得揪團資訊。
  2. 呼叫 `Order.get_by_group_id(id)` 取得該團所有的訂單。
- **輸出**: 渲染 `groups/detail.html`，供團員確認進度，供團長查看拆帳狀況。

### `POST /groups/<int:id>/close`
- **輸入**: URL 參數 `id`。
- **處理邏輯**: 
  1. 取得該團的 `delivery_fee` 以及該團目前的訂單總數 $N$。
  2. 檢查 $N > 0$，若大於零則計算 `split_fee = delivery_fee / N` (無條件進位或四捨五入)。
  3. 針對該團的每一筆訂單，呼叫 `Order.update()` 寫入 `split_fee` 與 `final_amount` (`items_total + split_fee`)。
  4. 呼叫 `Group.update()` 將狀態改為 `closed`。
- **輸出**: 重導向至 `/groups/<id>`。

### `GET /groups/<int:group_id>/orders/new`
- **輸入**: URL 參數 `group_id`。
- **處理邏輯**: 確認該團狀態為 `open` 才允許點餐。
- **輸出**: 渲染 `orders/new.html` 讓使用者填寫想吃的品項。

### `POST /groups/<int:group_id>/orders`
- **輸入**: URL 參數 `group_id`，表單資料 (品項名稱、單價、數量等陣列)。
- **處理邏輯**:
  1. 計算表單內餐點的純餐費總和 (`items_total`)。
  2. 呼叫 `Order.create()` 建立主檔。
  3. 迴圈呼叫 `OrderItem.create()` 寫入每一項餐點。
- **輸出**: 重導向至 `/groups/<group_id>`。

### `POST /orders/<int:id>/pay`
- **輸入**: URL 參數 `id`。
- **處理邏輯**: 呼叫 `Order.update(id, {'payment_status': 'paid'})`。
- **輸出**: 重導向回所屬的揪團詳情頁。

---

## 3. Jinja2 模板清單

所有的 HTML 將放在 `app/templates/` 內，統一繼承 `base.html`。
- `base.html`: 包含 Bootstrap 與 Flash Message 區塊。
- `groups/index.html`: 揪團大廳列表。
- `groups/new.html`: 發起揪團表單。
- `groups/detail.html`: 詳情頁，會根據 `group.status` 決定要顯示「參團按鈕」還是「結單後的應付金額表」。
- `orders/new.html`: 參團點餐表單。
