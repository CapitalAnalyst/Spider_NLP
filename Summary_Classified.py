from datetime import datetime

import pandas as pd
from transformers import pipeline

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Optional: Initialize the classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


today_str = datetime.date.today().strftime("%Y-%m-%d")
# Read the CSV file
df = pd.read_csv(f"./Data/{today_str}.csv")

# Prepare lists to store the summary and classification results
summaries = []
labels = []
scores = []
final_labels = []
# Specify candidate labels for classification
candidate_labels = ["cyber security", "business", "finance", "technology"]

# Iterate over each content item
for content in df['Content']:
    # Perform summarization
    summary_result = summarizer(content, max_length=30, min_length=10, do_sample=False)
    summary_text = summary_result[0]['summary_text']
    summaries.append(summary_text)

    # Optional: Perform classification
    classification_result = classifier(content, candidate_labels)
    labels.append(", ".join(classification_result['labels']))
    scores.append(", ".join([str(score) for score in classification_result['scores']]))

    # Determine the final label based on the highest score
    max_score_index = classification_result['scores'].index(max(classification_result['scores']))
    final_label = classification_result['labels'][max_score_index]
    final_labels.append(final_label)

# Add the summary, classification results, and final label as new columns in the DataFrame
df['Summary'] = summaries
df['Labels'] = labels
df['Scores'] = scores
df['Final Label'] = final_labels

# **改动 1：只保留需要的列**
df = df[['Summary', 'URL', 'Date', 'Final Label']]

# **改动 2：将最终 DataFrame 保存到新的 CSV 文件**
df.to_csv(f"./Data/{today_str}_final.csv", index=False)

print("Summarization and classification results have been added to '2024-08-20_final.csv'")
