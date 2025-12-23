import os
import shutil
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier

def main():
    data_file = "data_grouped_raw.csv"
    fig_dir = "fig"

    # Prepare /fig directory
    if os.path.exists(fig_dir):
        shutil.rmtree(fig_dir)
    os.makedirs(fig_dir, exist_ok=True)

    # Load dataset
    df = pd.read_csv(data_file)
    print(f"Loaded {len(df)} rows from {data_file}")

    # Drop non-numeric / identifier columns
    df = df.drop(columns=["repo", "file", "fix_count", 'bugfix_ratio', 'fixes_per_age'], errors="ignore")

    # ---- Basic Statistics ----
    stats = df.describe(include="all")
    stats.to_csv(os.path.join(fig_dir, "statistics.csv"))
    print("Saved descriptive statistics.")

    # ---- Correlation Heatmap ----
    numeric_df = df.select_dtypes(include=["number"])
    plt.figure(figsize=(10, 8))
    sns.heatmap(numeric_df.corr(), annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "correlation_heatmap.png"))
    plt.close()

    # ---- Pairplot ----
    subset_cols = [c for c in df.columns if c != "defective"]
    sns.pairplot(df, vars=subset_cols, hue="defective", corner=True)
    plt.savefig(os.path.join(fig_dir, "pairplot.png"))
    plt.close()
    print("Saved pairplot.")

    # ---- PCA ----
    features = [c for c in df.columns if c != "defective"]
    X = df[features].dropna()
    y = df.loc[X.index, "defective"]

    X_scaled = StandardScaler().fit_transform(X)

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    pca_df = pd.DataFrame(X_pca, columns=["PC1", "PC2"])
    pca_df["defective"] = y.values

    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=pca_df, x="PC1", y="PC2", hue="defective", palette="coolwarm", alpha=0.7)
    plt.title("PCA - 2 Components")
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "pca_scatter.png"))
    plt.close()

    # Explained variance plot
    plt.figure()
    plt.plot(range(1, len(pca.explained_variance_ratio_)+1), pca.explained_variance_ratio_, "o-")
    plt.title("PCA Explained Variance")
    plt.xlabel("Principal Component")
    plt.ylabel("Variance Ratio")
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "pca_variance.png"))
    plt.close()
    print("Saved PCA plots.")

    # ---- Feature Importance ----
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    importances = pd.Series(clf.feature_importances_, index=features).sort_values(ascending=False)

    plt.figure(figsize=(8, 6))
    sns.barplot(x=importances.values, y=importances.index, palette="viridis")
    plt.title("Feature Importance (Random Forest)")
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, "feature_importance.png"))
    plt.close()
    print("Saved feature importance plot.")

    print(f"✅ All analysis completed. Results saved in '{fig_dir}/'")

if __name__ == "__main__":
    main()
