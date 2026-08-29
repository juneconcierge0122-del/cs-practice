# Git 練習筆記：建立 Private Repo → Clone → Push 全流程

## 情境
在 GitHub 上開一個新的 **private repo**（`exercise`），本機還沒設定過 git 身份，習慣用 **fine-grained PAT** 做驗證。目標：在本機建立 `exercise1/ex1`，push 回 GitHub。

---

## 1. 設定本機 git 身份

`user.name` / `user.email` 只是**commit 作者資訊**，跟登入驗證（PAT）是兩件不同的事。

### global（所有 repo 通用）
```bash
git config --global user.name "你的名字或帳號"
git config --global user.email "你的Email"
```

### local（只套用在單一 repo）
```bash
cd <repo資料夾>          # 必須先在 git repo 裡面才能用 --local
git config --local user.name "你的名字或帳號"
git config --local user.email "你的Email"
```

**常見錯誤**：`致命錯誤: --local 只能在一個版本庫內使用`
→ 代表目前所在資料夾不是 git repo（沒有 `.git`）。要先 `git clone` 或 `git init` 之後才能設 local。

**優先順序**：`local` > `global` > `system`
```bash
git config user.name                  # 查看目前生效值
git config --show-origin user.name    # 查看該值來自哪個設定檔
```

---

## 2. Clone Private Repo

Private repo **不能匿名 clone**，過程會要求驗證：

```bash
git clone https://github.com/<帳號>/exercise.git
```

跳出提示時：
- Username → GitHub 帳號
- Password → **貼上 fine-grained PAT**（不是登入密碼，GitHub 已移除密碼登入）

### PAT 權限檢查清單（Fine-grained token）
GitHub → Settings → Developer settings → Fine-grained tokens：
- Repository access → Only select repositories → 勾選 `exercise`
- Permissions → **Contents: Read and write**

⚠️ 若權限不足，clone 會出現看似「repo 不存在」的誤導性錯誤：
```
remote: Repository not found.
fatal: repository '...' not found
```
這其實常常是權限問題，不代表 repo 名稱打錯或不存在。

---

## 3. 避免每次都輸入 PAT（Credential Helper）

```bash
# macOS
git config --global credential.helper osxkeychain

# Windows
git config --global credential.helper manager

# Linux
git config --global credential.helper store
```

設定一次後，之後同機器的 push/pull 都會自動帶入，不用重複貼 token。

---

## 4. 建立資料夾與檔案、Commit、Push

```bash
mkdir exercise1
touch exercise1/ex1

git add exercise1/ex1
git commit -m "Add exercise1/ex1"
git push -u origin main
```

---

## 5. 收尾：本機要清掉時，移除身份資訊是否安全？

**結論：可行，不影響已 push 的 commit。**

- `user.name` / `user.email` 只在 **commit 當下**被寫入該次 commit 的 metadata；一旦 push 上去就已經永久記錄在該 commit 裡，事後清掉 config 不會回頭改動它（除非做 rebase / history rewrite）。
- 移除方式：
  ```bash
  git config --local --unset user.name
  git config --local --unset user.email
  ```
- ⚠️ 但若這台機器之後還要在同 repo 或其他 repo 繼續 commit，且沒有 global 值當備援，git 會要求重新設定身份才能 commit。

### 另外要分清楚：登入用的 PAT ≠ user.name/email
PAT 存放在 credential helper（如 osxkeychain / manager / store），不是 `git config` 管理的範圍。

- 想讓這台機器**徹底無法再用這組 PAT**：
  → 去 GitHub → Settings → Developer settings → Fine-grained tokens → **Revoke** 該 token（最乾淨、最符合 fine-grain token 用完即棄的精神）
- 想只清除本機殘留的憑證快取：
  → 依平台從系統憑證管理員（macOS 鑰匙圈 / Windows 認證管理員）手動移除 github.com 項目

---

## 重點觀念總結

| 項目 | 作用 | 存放位置 | 是否影響已 push 的 commit |
|---|---|---|---|
| `user.name` / `user.email` | commit 作者資訊 | `.git/config`（local）或 `~/.gitconfig`（global） | 不影響（已烙印在 commit 裡） |
| Fine-grained PAT | 登入驗證（push/pull 權限） | Credential helper / 系統憑證管理員 | 不影響，但可 revoke 讓其失效 |
