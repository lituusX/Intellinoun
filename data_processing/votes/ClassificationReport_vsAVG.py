import csv
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score, classification_report
import pandas as pd


def score_to_category(score, thresholds):
    if score > thresholds["Positive"]:
        return "Positive"
    elif score < thresholds["Negative"]:
        return "Negative"
    else:
        return "Neutral"


thresholds = {
    "Positive": 0.5,
    "Negative": -0.5
}

csv_path = "../../data/processed/datasets/votes_sentimentAVG.csv"

f1_scores = {}
classification_reports = {}

for score_label in ["Score A", "Score B", "Score C", "Score D"]:
    y_true = []
    y_pred = []

    with open(csv_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            avg_score = float(row["Score Avg"])
            score = float(row[score_label])

            y_true.append(score_to_category(avg_score, thresholds))
            y_pred.append(score_to_category(score, thresholds))

    f1 = f1_score(y_true, y_pred, average='weighted')
    f1_scores[score_label] = f1
    print(f"F1 Score for {score_label} against Score Avg: {f1}")

    classification_rep = classification_report(y_true, y_pred, target_names=['Negative', 'Neutral', 'Positive'],
                                               output_dict=True)
    classification_reports[score_label] = pd.DataFrame(classification_rep).transpose()

fig, axes = plt.subplots(1, 5, figsize=(20, 4))

axes[0].bar(f1_scores.keys(), f1_scores.values())
axes[0].set_xlabel('Score Labels')
axes[0].set_ylabel('F1 Score')
axes[0].set_title('F1 Scores for Different Score Labels Against Score Avg')
axes[0].set_ylim([0, 1])
axes[0].grid(True)

for ax, (score_label, classification_report_df) in zip(axes[1:], classification_reports.items()):
    classification_report_df_rounded = classification_report_df.round(3)

    table = ax.table(cellText=classification_report_df_rounded.values,
                     colLabels=classification_report_df_rounded.columns,
                     rowLabels=classification_report_df_rounded.index,
                     cellLoc='center', rowLoc='center',
                     loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)
    ax.axis('off')

plt.tight_layout()
plt.savefig('../../data/processed/datasets/ClassificationReport_vsAVG.png', bbox_inches='tight',
            dpi=300)
