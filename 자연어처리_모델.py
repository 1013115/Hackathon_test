
import pandas as pd
import re
data = pd.read_csv('/content/data_csv.csv')


# Simple tokenization function to split by spaces and punctuation
def simple_tokenize(text):
    # Check if the input is a string
    if isinstance(text, str):
        # Replace punctuations with spaces
        text = re.sub(r'[^\w\s]', ' ', text)
        # Split by spaces
        return text.split()
    else:
        # Return an empty list if the input is not a string
        return []

# CSV 파일을 불러옵니다

# 결측값이 있는 행을 삭제합니다
data = data.dropna(subset=['overview'])

# 토큰화 함수를 적용합니다
data['tokenized_overview'] = data['overview'].apply(simple_tokenize)

# 수정된 데이터를 다시 CSV 파일에 저장합니다
data.to_csv('/content/combined_detailfile.csv', index=False)

# Expanded and refined keywords for each category
detailed_categories = {
    "plant": ["소나무", "나무", "풀", "꽃", "청보리", "해초", "단풍", "식물", "숲", "풀밭", "초원", "해초류"],
    "artifact": ["의자", "카페", "숙박시설", "박물관", "패총", "민박집", "유적", "조각상", "기념비", "건축물", "교회", "사원", "성당"],
    "location": ["해변", "마을", "공원", "해수욕장", "올레길", "도로", "바다", "섬", "산", "강", "호수", "도시", "시골", "해안", "계곡","테마파크","마을"]
    }

# Enhanced function to categorize tokens with partial matching
def detailed_categorize_tokens(tokens):
    categorized = {
        "plant": [],
        "artifact": [],
        "location": [],
        "organization": []
    }

    for token in tokens:
        for category, keywords in detailed_categories.items():
            if any(keyword in token for keyword in keywords):
                categorized[category].append(token)

    return categorized

# Apply detailed categorization to tokenized_overviews
data['detailed_categorized_tokens'] = data['tokenized_overview'].apply(detailed_categorize_tokens)

# Extract the detailed categorized tokens
detailed_categorized_columns = pd.DataFrame(data['detailed_categorized_tokens'].tolist())

# Concatenate with the original data for output
detailed_output_data = pd.concat([data[['overview']], detailed_categorized_columns], axis=1)

# Function to refine categorized tokens by removing postpositional particles and duplicates
def refine_tokens(categorized_tokens):
    refined = {}
    for category, tokens in categorized_tokens.items():
        # Remove common Korean postpositional particles and duplicates
        refined_tokens = set()
        for token in tokens:
          if len(token) > 2:
                token = re.sub(r'(?<=\S)(은|는|이|가|를|을|에|에서|의|으로|로|과|와|도|에|하고|만|보다|인|이다|했다|했고|하였고|에게|이라|으로써|이자|이며|이었다|이나|하듯|하여)$', '', token)
            #refined_token = re.sub(r'(은|는|이|가|를|에|에서|의|으로|로|과|와|도|에|하고|만|보다|했다|했고)$', '', token)
          refined_tokens.add(token)
        refined[category] = list(refined_tokens)
    return refined

# Apply the refinement to the detailed categorized tokens
data['refined_categorized_tokens'] = data['detailed_categorized_tokens'].apply(refine_tokens)

# Extract the refined categorized tokens
refined_categorized_columns = pd.DataFrame(data['refined_categorized_tokens'].tolist())

# Concatenate with the original data for output
refined_output_data = pd.concat([data[['overview']], refined_categorized_columns], axis=1)

# Function to further refine tokens by removing plural expressions, all particles, and similar expressions

# Apply further refinement to the detailed categorized tokens
data['further_refined_categorized_tokens'] = data['refined_categorized_tokens'].apply(further_refine_tokens)

# Extract the further refined categorized tokens
further_refined_categorized_columns = pd.DataFrame(data['further_refined_categorized_tokens'].tolist())

# Concatenate with the original data for output
further_refined_output_data = pd.concat([data[['overview']], further_refined_categorized_columns], axis=1)

# Save the result to a new CSV file
further_refined_output_file_path = '/content/further_refined_categorized_tokens_overviews.csv'
further_refined_output_data.to_csv(further_refined_output_file_path, index=False)

# Function to further refine tokens by removing plural expressions, all particles, and similar expressions
def further_refine_tokens(categorized_tokens):
    refined = {}
    for category, tokens in categorized_tokens.items():
        refined_tokens = set()
        for token in tokens:
            # Remove plural expressions (e.g., "들")
            token = re.sub(r'들$', '', token)
            # Remove all particles but only if they are standalone or after a space,
            # and only if the remaining word length is more than 2
            if len(token) > 2:
                token = re.sub(r'(?<=\S)(은|는|이|가|를|을|에|에서|의|으로|로|과|와|도|에|하고|만|보다|인|이다|했다|했고|하였고|에게|이라|이자|이며|으로써|이었다|이나|하듯|하여)$', '', token)
            # Remove similar expressions (e.g., "유적" and "유적지")
            if token not in refined_tokens and not any(existing_token.startswith(token) for existing_token in refined_tokens):
                refined_tokens.add(token)
        refined[category] = list(refined_tokens)
    return refined

# Apply further refinement to the detailed categorized tokens
data['further_refined_categorized_tokens'] = data['refined_categorized_tokens'].apply(further_refine_tokens)

# Extract the further refined categorized tokens
further_refined_categorized_columns = pd.DataFrame(data['further_refined_categorized_tokens'].tolist())

# Concatenate with the original data for output
further_refined_output_data = pd.concat([data[['overview']], further_refined_categorized_columns], axis=1)

# Save the result to a new CSV file
further_refined_output_file_path = '/content/further_refined_categorized_tokens_overviews.csv'
further_refined_output_data.to_csv(further_refined_output_file_path, index=False)

further_refined_output_data
