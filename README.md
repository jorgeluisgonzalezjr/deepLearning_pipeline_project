# deepLearning_pipeline_project

An intelligent data engine that predicts video performance trends. Instead of relying on static, outdated spreadsheets, this project uses a live data pipeline connected directly to YouTube to analyze viewer sentiment on a JoJo's Bizarre Adventure video using an LSTM neural network.

## Data Collection: YouTube Data API v3

The first step of this pipeline is scraping the raw data directly from the source rather than downloading a pre-made CSV. Using the YouTube Data API v3, a Python script connects to the video and extracts the comments.

* **Authentication:** Secured via an API key generated in the Google Cloud Console.
* **Extraction:** The script targets the specific video ID, handling pagination to pull the top-level comments and replies.
* **Formatting:** The raw JSON response is parsed and converted directly into a pandas DataFrame, which serves as the foundation for the cleaning and NLP phases.

## The Data

Once extracted, the raw comments are cleaned and labeled. Features engineered during this phase include text normalization, brand safety checks, and toxicity scoring. 

## Data Sample

| comments | comments_norm | is_reply | brand_safe | tox_toxicity | spam_model_prob | label_name | label |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| The full album is a fckk masterpiece 😭😭 | the full album is a fck masterpiece | 0 | 1 | 0.084131 | 0.086141 | positive | 2 |
| They have certainly grown up… love their music... | they have certainly grown up love their music ... | 0 | 1 | 0.009205 | 0.152647 | positive | 2 |
| IF YOU DONT FEAR OF DEATH THIS SONG WAS GOOD T... | if you dont fear of death this song was good t... | 0 | 1 | 0.017461 | 0.077319 | positive | 2 |
| You are now an official member of The Passione… | you are now an official member of the passione | 0 | 1 | 0.002998 | 0.091827 | neutral | 1 |
| I wish I could put into words what that song d... | i wish i could put into words what that song d... | 0 | 1 | 0.000595 | 0.135743 | neutral | 1 |

*(Note: Some toxicity columns omitted in this preview for readability)*

## Model Architecture & Training

The core of the sentiment predictor is an LSTM model. 

* **Training details:** The model was trained over 8 epochs.
* **Overfitting control:** `EarlyStopping` was implemented monitoring `val_loss`. The model successfully halted training at Epoch 5 and restored the best weights from Epoch 3, achieving a final validation accuracy of roughly 70%.
* 
The core of the sentiment predictor is an LSTM model. The model was trained over 8 epochs with `EarlyStopping` monitoring `val_loss`. 

```
Epoch 1/8
57/57 ━━━━━━━━━━━━━━━━━━━━ 11s 112ms/step - accuracy: 0.4721 - loss: 1.1405 - val_accuracy: 0.5784 - val_loss: 0.9274
Epoch 2/8
57/57 ━━━━━━━━━━━━━━━━━━━━ 5s 86ms/step - accuracy: 0.5423 - loss: 0.9516 - val_accuracy: 0.6556 - val_loss: 0.7852
Epoch 3/8
57/57 ━━━━━━━━━━━━━━━━━━━━ 5s 87ms/step - accuracy: 0.7452 - loss: 0.6395 - val_accuracy: 0.6887 - val_loss: 0.7740
Epoch 4/8
57/57 ━━━━━━━━━━━━━━━━━━━━ 6s 101ms/step - accuracy: 0.8970 - loss: 0.3362 - val_accuracy: 0.7042 - val_loss: 0.8534
Epoch 5/8
57/57 ━━━━━━━━━━━━━━━━━━━━ 11s 108ms/step - accuracy: 0.9439 - loss: 0.1824 - val_accuracy: 0.6976 - val_loss: 1.1831
```
## Evaluation & Class Imbalance

The overall accuracy sits at 70%, but the metrics reveal a heavy class imbalance in the dataset.

* **Neutral / Positive:** The model performs well here, with f1-scores of 0.72 and 0.71 respectively.
* **Negative:** The model struggles with negative sentiment (f1-score of 0.49), frequently misclassifying negative comments as neutral or positive. 

This behavior is expected given the training data distribution: the dataset is heavily skewed toward neutral (1,475) and positive (1,062) comments, with very few negative (285) examples.
## Confusion Matrix

<img width="578" height="589" alt="confusion_matrix" src="https://github.com/user-attachments/assets/02aed639-eacd-4a59-bba7-e2e36024afef" />


## Next Steps
Future iterations of this pipeline will require addressing the class imbalance by applying class weights during training or sourcing a larger dataset of negative comments to improve the model's predictive precision on minority classes.
