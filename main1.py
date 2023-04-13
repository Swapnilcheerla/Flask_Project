import boto3


def do_translate(input, Target):
    translate = boto3.client(service_name="translate",
                             region_name="us-east-1", use_ssl=True)
    result = translate.translate_text(
        Text=input, SourceLanguageCode='en', TargetLanguageCode=Target)
    return result.get("TranslatedText")


def do_sentiment_analysis(input):
    comprehend = boto3.client(service_name="comprehend",
                              region_name="us-east-1")
    result = comprehend.detect_sentiment(
        Text=input, LanguageCode='en')
    positive = result['SentimentScore']['Positive']
    negative = result['SentimentScore']['Negative']
    neutral = result['SentimentScore']['Neutral']
    lst = [positive, negative, neutral]

    return lst
