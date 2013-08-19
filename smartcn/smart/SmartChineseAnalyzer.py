class SmartChineseAnalyzer:
    def __init__(self):
        pass

    def create_components(self, filename):
        #tokenizer = SentenceTokenize(filename)
        #result = WordTokenFilter(tokenizer)
        #result = PorterStemFilter(result)
        
        if self.stopwords:
            result = StopFilter(result, self.stopwords)
        return TokenStreamComponents(tokenizer, result)


        
