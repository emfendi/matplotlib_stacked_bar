import numpy as np
import matplotlib.pyplot as plt
from extractFeature import load_bacterium
from sklearn.decomposition import PCA, IncrementalPCA

def run(filename, group_filename) :
    bacterium = load_bacterium(filename, group_filename)
    X = bacterium['data']
    y = bacterium['target']
    target_names = bacterium['target_names']

    n_components = 2
    ipca = IncrementalPCA(n_components=n_components, batch_size=10)
    X_ipca = ipca.fit_transform(X)

    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X)

    colors = ['navy', 'darkorange']

    for X_transformed, title in [(X_ipca, "Incremental PCA"), (X_pca, "PCA")]:
        plt.figure(figsize=(6, 6))
        for color, i, target_name in zip(colors, [0, 1], target_names):
            plt.scatter(X_transformed[y == i, 0], X_transformed[y == i, 1],
                        color=color, lw=2, label=target_name)

        if "Incremental" in title:
            err = np.abs(np.abs(X_pca) - np.abs(X_ipca)).mean()
            plt.title(title + " of bacterium dataset\nMean absolute unsigned error "
                      "%.6f" % err)
        else:
            plt.title(title + " of bacterium dataset")
        plt.legend(loc="best", shadow=False, scatterpoints=1)
        plt.axis([-1, 1, -0.5, 0.5])

    plt.show()

if __name__ == "__main__":
    filename = './data/CRS_above_genus.csv'
    group_filename = './data/control_case_group.csv'
    run(filename, group_filename)

