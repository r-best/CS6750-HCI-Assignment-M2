import pandas
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

def preprocess(data):
    """
    Takes in pandas data frame and performs a few simple preprocessing steps on the reviews
    """
    data['Comment'].replace(r'[\.,!\?:;\'\"\-_\+=@\(\)\*]', "", inplace=True, regex=True)
    data['Comment'] = data['Comment'].str.lower()
    data['Comment'] = data['Comment'].str.replace(r'\b(?:{})\b'.format('|'.join(stopwords.words('english'))), "", regex=True)
    data['Comment'] = data['Comment'].str.replace(r'\s+', " ", regex=True)
    return data


def getReviewLengths(reviews, normalize=False):
    """
    Takes in a list of strings (reviews) and returns a frequency array of their lengths,
    where the value at each index is the number of strings of length (index)
    """
    # Calculate length frequencies
    lengths = dict()
    longest = 0
    highest_freq = 0
    for review in reviews:
        length = len(review.split(" "))
        if length not in lengths:
            lengths[length] = 0
        lengths[length] += 1
        if length > longest:
            longest = length
        if lengths[length] > highest_freq:
            highest_freq = lengths[length]

    # Turn dict into equivalent list, where list[x] = number of strings of length x
    lengthsList = [0] * (longest+1)
    for k,v in lengths.items():
        lengthsList[k] = v
    
    if normalize:
        lengthsList = [x/highest_freq for x in lengthsList]

    return lengthsList

def getFreqs(reviews, n=1):
    """
    Takes in a list of strings (reviews) and returns a dictionary of n-grams present in
    them mapped to the frequency with which they appear
    """
    ngrams = dict()
    for review in reviews:
        words = [x for x in review.split(" ") if x != ""]
        if len(words) < n:
            continue

        for i in range(len(words)-n):
            ngram = " ".join(words[i:i+n])
            if ngram not in ngrams:
                ngrams[ngram] = 0
            ngrams[ngram] += 1
    return ngrams

if __name__ == "__main__":
    # Load and preprocess dataset
    data = pandas.read_csv('data/reviews.csv', encoding='utf-16', sep='|')
    data = preprocess(data)

    onestar = data.loc[data['Stars']==1]
    fivestar = data.loc[data['Stars']==5]

    # Calculate review length frequencies
    with open("output/review_lengths/1star_lengths_norm.csv", 'w') as fp:
        fp.write("length,frequency\n")
        for i, v in enumerate(getReviewLengths(onestar['Comment'].tolist(), True)):
            fp.write(f"{i},{v}\n")
    with open("output/review_lengths/5star_lengths_norm.csv", 'w') as fp:
        fp.write("length,frequency\n")
        for i, v in enumerate(getReviewLengths(fivestar['Comment'].tolist(), True)):
            fp.write(f"{i},{v}\n")

    # Calculate 5-star ngram frequencies
    with open("output/ngrams/5star_1grams.csv", 'w', encoding='utf-8') as fp:
        x = getFreqs(fivestar['Comment'].tolist(), 1)
        fp.write("ngram,frequency\n")
        for k,v in dict(sorted(x.items(), reverse=True, key=lambda item: item[1])).items():
            fp.write(f"{k},{v}\n")
    with open("output/ngrams/5star_2grams.csv", 'w', encoding='utf-8') as fp:
        x = getFreqs(fivestar['Comment'].tolist(), 2)
        fp.write("ngram,frequency\n")
        for k,v in dict(sorted(x.items(), reverse=True, key=lambda item: item[1])).items():
            fp.write(f"{k},{v}\n")
    with open("output/ngrams/5star_3grams.csv", 'w', encoding='utf-8') as fp:
        x = getFreqs(fivestar['Comment'].tolist(), 3)
        fp.write("ngram,frequency\n")
        for k,v in dict(sorted(x.items(), reverse=True, key=lambda item: item[1])).items():
            fp.write(f"{k},{v}\n")

    # Calculate 1-star ngram frequencies
    with open("output/ngrams/1star_1grams.csv", 'w', encoding='utf-8') as fp:
        x = getFreqs(onestar['Comment'].tolist(), 1)
        fp.write("ngram,frequency\n")
        for k,v in dict(sorted(x.items(), reverse=True, key=lambda item: item[1])).items():
            fp.write(f"{k},{v}\n")
    with open("output/ngrams/1star_2grams.csv", 'w', encoding='utf-8') as fp:
        x = getFreqs(onestar['Comment'].tolist(), 2)
        fp.write("ngram,frequency\n")
        for k,v in dict(sorted(x.items(), reverse=True, key=lambda item: item[1])).items():
            fp.write(f"{k},{v}\n")
    with open("output/ngrams/1star_3grams.csv", 'w', encoding='utf-8') as fp:
        x = getFreqs(onestar['Comment'].tolist(), 3)
        fp.write("ngram,frequency\n")
        for k,v in dict(sorted(x.items(), reverse=True, key=lambda item: item[1])).items():
            fp.write(f"{k},{v}\n")
