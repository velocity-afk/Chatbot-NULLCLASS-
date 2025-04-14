import nltk
from nltk.tokenize import sent_tokenize
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from rouge import Rouge

# Ensure necessary data is downloaded
nltk.download('punkt')

# Function to read text from a file
def read_text_from_file():
    file_path = input("Enter the file path (e.g., example.txt) or press Enter to input text directly: ")
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print("File not found. Please check the path.")
            return None
    else:
        return input("Enter your text here: ")

# Function to select summarizer
def get_summarizer(algorithm):
    if algorithm == "LexRank":
        return LexRankSummarizer()
    elif algorithm == "LSA":
        return LsaSummarizer()
    elif algorithm == "TextRank":
        return TextRankSummarizer()
    else:
        print("Invalid algorithm. Using LexRank by default.")
        return LexRankSummarizer()

# Function to calculate the number of sentences
def calculate_summary_length(text):
    total_sentences = len(sent_tokenize(text))
    return max(2, total_sentences // 4)  # 25% of the original text

# Summarization function
def summarize_text(text, algorithm="LexRank"):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = get_summarizer(algorithm)
    num_sentences = calculate_summary_length(text)

    print(f"\nUsing {algorithm} algorithm for summarization.")
    print(f"Summarizing to approximately {num_sentences} sentences.\n")
    
    summary = summarizer(parser.document, num_sentences)
    return " ".join(str(sentence) for sentence in summary)

# Evaluation using ROUGE
def evaluate_summary(original, summary):
    rouge = Rouge()
    scores = rouge.get_scores(summary, original)
    return scores

# Main Function
def main():
    text = read_text_from_file()
    if not text:
        return
    
    print("\nChoose a summarization algorithm: LexRank, LSA, TextRank")
    algorithm = input("Enter your choice: ").strip()

    # Generate summary
    summary = summarize_text(text, algorithm)
    print("\nGenerated Summary:\n", summary)
    
    # Evaluate summary
    scores = evaluate_summary(text, summary)
    print("\nROUGE Scores:", scores)

    # Additional Info
    print(f"\nOriginal Length: {len(text.split())} words")
    print(f"Summary Length: {len(summary.split())} words")
    print(f"Compression Ratio: {len(summary.split()) / len(text.split()) * 100:.2f}%")

if __name__ == "__main__":
    main()
