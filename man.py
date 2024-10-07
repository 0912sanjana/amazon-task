import os
from anthropic import Anthropic
import pandas as pd
import numpy as np
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("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"))

def load_dataset(file_path):
    data = pd.read_csv(file_path)
    return data

dataset_path = r'C:\Users\shrad\Downloads\amazon-task-main\reviews_supplements.csv'
data = load_dataset(dataset_path)

def generate_synthetic_review(prompt, max_length=200):
    response = client.messages.create(
        max_tokens=max_length,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="claude-3-opus-20240229",
    )
    return response.content

def generate_synthetic_dataset(original_reviews, num_samples=100):
    synthetic_reviews = []
    for i in range(num_samples):
        prompt = np.random.choice(original_reviews)
        if prompt:
            synthetic_review = generate_synthetic_review(prompt)
            synthetic_reviews.append(synthetic_review)
            print(f"Generated {i+1}/{num_samples} synthetic reviews")
        else:
            print("Empty prompt, skipping...")
    return synthetic_reviews

def save_synthetic_dataset(synthetic_reviews, output_file):
    df_synthetic = pd.DataFrame(synthetic_reviews, columns=['Synthetic_Review'])
    df_synthetic.to_csv(output_file, index=False)
    print(f"Synthetic dataset saved to {output_file}")

def main():
    original_dataset_path = 'C:/Users/shrad/Downloads/amazon-task-main/reviews_supplements.csv'
    data = load_dataset(original_dataset_path)
    original_reviews = data['text'].dropna().tolist()
    num_synthetic_samples = 100
    synthetic_reviews = generate_synthetic_dataset(original_reviews, num_synthetic_samples)
    output_file = 'synthetic_reviews.csv'
    save_synthetic_dataset(synthetic_reviews, output_file)

if __name__ == "__main__":
    main()
