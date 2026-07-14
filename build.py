import os
import subprocess

# 定義檔案路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LISTS_DIR = os.path.join(BASE_DIR, 'Lists')
DRAFT_FILE = os.path.join(BASE_DIR, 'draft.txt')

def clean_and_sort_list_file(filepath):
    if not os.path.exists(filepath):
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    header = []
    sections = {}
    current_section = "Uncategorized"
    sections[current_section] = set()

    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 判斷是否為檔案開頭的 META 資訊 (不包含 === 的註解)
        if line.startswith('#') and '===' not in line and current_section == "Uncategorized" and len(sections[current_section]) == 0:
            header.append(line)
            continue
            
        # 判斷是否為分類標籤 (例如: # === 🍎 Apple ===)
        if line.startswith('#') and '===' in line:
            current_section = line
            if current_section not in sections:
                sections[current_section] = set()
            continue
            
        # 處理普通註解
        if line.startswith('#'):
            sections[current_section].add(line)
            continue

        # 處理規則 (去重複)
        sections[current_section].add(line)

    # 寫回檔案
    with open(filepath, 'w', encoding='utf-8') as f:
        # 寫入 Header
        for h in header:
            f.write(h + '\n')
        f.write('\n')

        # 寫入各分類
        for sec_title, rules in sections.items():
            if not rules and sec_title == "Uncategorized":
                continue
            
            if sec_title != "Uncategorized":
                f.write(sec_title + '\n')
            
            # 分離註解與規則來排序
            comments = sorted([r for r in rules if r.startswith('#')])
            actual_rules = sorted([r for r in rules if not r.startswith('#')])
            
            for c in comments:
                f.write(c + '\n')
            for r in actual_rules:
                f.write(r + '\n')
            
            f.write('\n')

def process_draft():
    if not os.path.exists(DRAFT_FILE):
        open(DRAFT_FILE, 'w', encoding='utf-8').close()
        return []

    with open(DRAFT_FILE, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines or all(line.startswith('#') for line in lines):
        return []

    target_mapping = {
        '[Proxy]': 'Proxy',
        '[TW]': 'TW',
        '[Reject]': 'Reject',
        '[Apple]': 'Apple',
        '[Tracker]': 'Tracker'
    }

    current_target = 'Proxy'
    new_domains_by_group = {}
    
    # 用來記錄加入的原始網域 (去除語法)，方便寫入 Commit Message
    raw_domains_added = []

    for line in lines:
        if line.startswith('#'):
            continue
        
        if line.startswith('[') and line.endswith(']'):
            if line in target_mapping:
                current_target = target_mapping[line]
            else:
                current_target = 'Proxy'
            continue

        # 記錄網域
        raw_domains_added.append((current_target, line))

        # 轉換格式
        if not line.startswith('DOMAIN'):
            line = f"DOMAIN-SUFFIX,{line},extended-matching"
        
        filename = f"Custom.{current_target}.list" if current_target in ['Proxy', 'Reject', 'Apple'] else f"{current_target}.list"
        if current_target == 'Tracker': filename = 'Tracker-domain.list'
            
        if filename not in new_domains_by_group:
            new_domains_by_group[filename] = []
        new_domains_by_group[filename].append(line)

    if not new_domains_by_group:
        return []

    print(f"📥 發現新網域，準備寫入對應清單...")

    inbox_header = "# === 📥 新增待分類 (Inbox) ==="
    
    for filename, domains in new_domains_by_group.items():
        filepath = os.path.join(LISTS_DIR, filename)
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if inbox_header not in content:
            content += f"\n\n{inbox_header}\n"
            
        content += "\n".join(domains) + "\n"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    with open(DRAFT_FILE, 'w', encoding='utf-8') as f:
        f.write("# 請在下方標籤內輸入網域 (每行一個)\n")
        f.write("[Proxy]\n\n[TW]\n\n[Reject]\n\n[Apple]\n\n")
        
    print("✨ 草稿已清空並重置！")
    return raw_domains_added

def auto_commit(added_items):
    if not added_items:
        # 沒有新網域，檢查是否有其他手動修改
        status = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True).stdout
        if status:
            print("📦 發現其他修改，執行常規更新...")
            subprocess.run(['git', 'add', '.'])
            subprocess.run(['git', 'commit', '-m', 'chore: update and optimize rules'])
        return

    # 分析新增了什麼來產出專業 Commit 標題
    groups = {}
    for group, domain in added_items:
        if group not in groups:
            groups[group] = []
        groups[group].append(domain)

    # 組合訊息，例如: "feat: add google.com to Proxy, hinet.net to TW"
    msg_parts = []
    for group, domains in groups.items():
        if len(domains) == 1:
            msg_parts.append(f"{domains[0]} to {group}")
        else:
            msg_parts.append(f"{domains[0]} and {len(domains)-1} more to {group}")
            
    commit_msg = f"feat: add {', '.join(msg_parts)}"

    # 執行 Git
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', commit_msg])
    print(f"✅ 成功打包 Commit！訊息為: '{commit_msg}'")

if __name__ == "__main__":
    print("🚀 開始執行 Surge 規則整理腳本...")
    added_items = process_draft()
    
    for filename in os.listdir(LISTS_DIR):
        if filename.endswith('.list'):
            filepath = os.path.join(LISTS_DIR, filename)
            clean_and_sort_list_file(filepath)
            
    auto_commit(added_items)
    print("🎉 整理與打包完成！您只要執行 `git push` 就好。")
