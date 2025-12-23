import os, re, stat, subprocess, shutil, math
from datetime import datetime, timezone, timedelta

CACHE_DIR = ".cache"
DATASET_DIR = "datasets"

# =========================
# === Repo Management  ====
# =========================

def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def clone_repos():
    """Clone repositories listed in repos.txt into .cache/"""
    if not os.path.exists("repos.txt"):
        print("repos.txt not found!")
        return

    with open("repos.txt", "r") as f:
        repos = list(filter(None, f.read().splitlines()))

    os.makedirs(CACHE_DIR, exist_ok=True)

    for repo_url in repos:
        repo_name = re.sub(r"[:/]+", "_", repo_url.strip().replace(".git", ""))
        target_dir = os.path.join(CACHE_DIR, repo_name)

        if os.path.exists(target_dir):
            print(f"[skip] {repo_name} already cloned.")
            continue

        print(f"[clone] Cloning {repo_url} ...")
        try:
            subprocess.run(["git", "clone", repo_url, target_dir], check=True)
        except subprocess.CalledProcessError as e:
            print(f"[error] Failed to clone {repo_url}: {e}")
            continue

def get_repo_paths():
    """Return all directories under .cache/ that contain a .git folder"""
    paths = []
    for root, dirs, files in os.walk(CACHE_DIR):
        for d in dirs:
            repo_dir = os.path.join(root, d)
            if os.path.exists(os.path.join(repo_dir, ".git")):
                paths.append(repo_dir)
        break
    return paths

# ===============================
# === Bug Fix Commit Detection ==
# ===============================

def is_bug_fix_commit(message):
    """Detect if a commit message indicates a bug fix"""
    message = message.lower()
    return (
        re.search(r"\b(fix|bug|defect|issue|error|patch|resolve[sd]?)\b", message)
        and not re.search(r"\b(doc|test|typo|example|comment)\b", message)
    )

# ===============================
# === Helper Metric Functions ===
# ===============================

def commit_entropy(repo, file_path):
    """Entropy of changes (measure of commit spread)"""
    entropies = []
    for commit in repo.iter_commits(paths=file_path):
        try:
            num_files = len(commit.stats.files)
            if num_files > 1:
                entropies.append(-math.log(1/num_files))
        except Exception:
            continue
    return sum(entropies) / len(entropies) if entropies else 0

def comment_density(path):
    """Approximate comment density"""
    if not os.path.exists(path):
        return 0
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception:
        return 0
    total = len(lines)
    comment = sum(1 for l in lines if re.match(r"\s*(//|#|/\*|\*)", l))
    return comment / total if total > 0 else 0

# ===============================
# === Data Collection ===========
# ===============================

def collect_repo_data(repo_path):
    """Collect file-level metrics and defect labels from a repo"""
    from git import Repo
    import lizard
    import pandas as pd
    from tqdm import tqdm

    repo = Repo(repo_path)
    file_data = {}

    commits = list(repo.iter_commits())
    print(f"[info] Processing {len(commits)} commits in {os.path.basename(repo_path)}")

    for commit in tqdm(commits):
        msg = commit.message
        bug_fix = is_bug_fix_commit(msg)

        try:
            stats = commit.stats.files
        except Exception as e:
            print(f"[skip] Commit {commit.hexsha[:7]}: {e}")
            continue

        for f, stat in stats.items():
            if not (f.endswith(".py") or f.endswith(".cs") or f.endswith(".java")):
                continue

            d = file_data.setdefault(
                f,
                {
                    "changes": 0,
                    "authors": {},
                    "fix_count": 0,
                    "first_commit": commit.committed_datetime,
                    "last_commit": commit.committed_datetime,
                    "lines_added": 0,
                    "lines_deleted": 0,
                },
            )

            d["changes"] += 1
            d["authors"][commit.author.email] = d["authors"].get(commit.author.email, 0) + 1
            d["lines_added"] += stat.get("insertions", 0)
            d["lines_deleted"] += stat.get("deletions", 0)
            if bug_fix:
                d["fix_count"] += 1
            if commit.committed_datetime < d["first_commit"]:
                d["first_commit"] = commit.committed_datetime
            if commit.committed_datetime > d["last_commit"]:
                d["last_commit"] = commit.committed_datetime

    # --- Static metrics from Lizard ---
    all_files = [os.path.join(repo_path, f) for f in file_data.keys() if os.path.exists(os.path.join(repo_path, f))]

    print(f"[info] Running lizard on {len(all_files)} files...")
    try:
        lizard_metrics = lizard.analyze_files(all_files)
    except Exception as e:
        print(f"[error] Lizard failed: {e}")
        return pd.DataFrame()

    rows = []
    for m in lizard_metrics:
        f_rel = os.path.relpath(m.filename, repo_path).replace("\\", "/")
        if f_rel not in file_data:
            alt = next((k for k in file_data.keys() if k.endswith(f_rel)), None)
            if not alt:
                continue
            f_rel = alt
        f = f_rel
        d = file_data[f]

        # Base static metrics
        nloc = m.nloc
        func_ccns = [func.cyclomatic_complexity for func in m.function_list]
        ccn_avg = sum(func_ccns) / len(func_ccns) if func_ccns else 0
        ccn_std = (sum((x - ccn_avg)**2 for x in func_ccns) / len(func_ccns))**0.5 if func_ccns else 0
        num_functions = len(m.function_list)

        # Process metrics
        age_days = (datetime.now(timezone.utc) - d["first_commit"].astimezone(timezone.utc)).days
        last_mod_days = (datetime.now(timezone.utc) - d["last_commit"].astimezone(timezone.utc)).days
        main_author_ratio = max(d["authors"].values()) / sum(d["authors"].values()) if d["authors"] else 1.0
        bugfix_ratio = d["fix_count"] / d["changes"] if d["changes"] > 0 else 0
        churn_total = d["lines_added"] + d["lines_deleted"]
        churn_rate = churn_total / (nloc + 1)
        entropy = commit_entropy(repo, f)
        comments = comment_density(os.path.join(repo_path, f))

        # Normalized
        changes_per_kloc = d["changes"] / (nloc / 1000 + 1)
        fixes_per_age = d["fix_count"] / (age_days + 1)

        rows.append(
            {
                "file": f,
                "nloc": nloc,
                "ccn_avg": ccn_avg,
                "ccn_std": ccn_std,
                "num_functions": num_functions,
                "changes": d["changes"],
                "authors": len(d["authors"]),
                "main_author_ratio": main_author_ratio,
                "age_days": age_days,
                "last_mod_days": last_mod_days,
                "lines_added": d["lines_added"],
                "lines_deleted": d["lines_deleted"],
                "churn_rate": churn_rate,
                "entropy": entropy,
                "comment_density": comments,
                "bugfix_ratio": bugfix_ratio,
                "changes_per_kloc": changes_per_kloc,
                "fixes_per_age": fixes_per_age,
                "fix_count": d["fix_count"],
                "defective": 1 if d["fix_count"] > 0 else 0,
            }
        )

    import pandas as pd
    df = pd.DataFrame(rows)
    print(f"[info] Collected {len(df)} file records.")
    return df

# ===============================
# === Main =====================
# ===============================

if __name__ == "__main__":
    clone_repos()
    repos = get_repo_paths()
    print(f"[info] Found {len(repos)} repos: {repos}")

    os.makedirs(DATASET_DIR, exist_ok=True)

    import pandas as pd
    for repo_path in repos:
        if 'mono' in repo_path: continue
        repo_name = os.path.basename(repo_path)
        out_path = os.path.join(DATASET_DIR, f"{repo_name}_metrics.csv")
        if os.path.exists(out_path):
            continue
        
        repo_name = os.path.basename(repo_path)
        print(f"\n=== Collecting from {repo_name} ===")
        data = collect_repo_data(repo_path)

        if data.empty:
            print(f"[warn] No data collected from {repo_name}.")
            continue

        out_path = os.path.join(DATASET_DIR, f"{repo_name}_metrics.csv")
        data.to_csv(out_path, index=False, encoding="utf-8")
        print(f"[save] Saved {len(data)} rows to {out_path}\n")

    print("Done collecting all repositories.")
