# this class for analyzing the text and extract the meta tag of website 
# using pip install --upgrade google-cloud-aiplatform
from google.cloud import aiplatform
import vertexai.preview


class TagNlp():
    def __init__(self):
       


    def analyze_entity(text):
        """Analyze entities in text."""
        client = aiplatform.gapic.TranslationServiceClient()
        # text = 'Hawaiian pizza is the best!'
        response = client.analyze_entities(text=text)
        for entity in response.entities:
            print(u"Representative name for the entity: {}".format(entity.name))
            print(u"Entity type: {}".format(aiplatform.Entity.Type(entity.type_).name))
            print(u"Salience score: {}".format(entity.salience))
            for metadata_name, metadata_value in entity.metadata.items():
                print(u"{}: {}".format(metadata_name, metadata_value))
            for mention in entity.mentions:
                print(u"Mention text: {}".format(mention.text.content))
                print(u"Mention type: {}".format(aiplatform.EntityMention.Type(mention.type_).name))   
    def analyze_sentiment(text):
        """Analyze sentiment in text."""
        client =
        aiplatform.gapic.TranslationServiceClient()
        # text = 'Hawaiian pizza is the best!'
        response = client.analyze_sentiment(text=text)
        print(u"Document sentiment score: {}".format(response.document_sentiment.score))
        print(u"Document sentiment magnitude: {}".format(response.document_sentiment.magnitude))
        for sentence in response.sentences:
            print(u"Sentence text: {}".format(sentence.text.content))
            print(u"Sentence sentiment score: {}".format(sentence.sentiment.score))
            print(u"Sentence sentiment magnitude: {}".format(sentence.sentiment.magnitude))
    def analyze_syntax(text):
        """Analyze syntax in text."""
        client = aiplatform.gapic.TranslationServiceClient()
        # text = 'Hawaiian pizza is the best!'
        response = client.analyze_syntax(text=text)
        for token in response.tokens:
            print(u"Token text: {}".format(token.text.content))
            print(u"Token part of speech: {}".format(aiplatform.PartOfSpeech.Tag(token.part_of_speech.tag).name))
            print(u"Dependency edge: {}".format(aiplatform.DependencyEdge.Label(token.dependency_edge.label).name))
    def analyze_text_entities(text):
        """Detects entities in the text."""
        client = aiplatform.gapic.TranslationServiceClient()


        # text = 'Hawaiian pizza is the best!'
        response = client.analyze_entities(text=text)
        for entity in response.entities:
            print(u"Entity: {}".format(entity.name))
            print(u"Entity type: {}".format(aiplatform.Entity.Type(entity.type_).name))
            print(u"Salience score: {}".format(entity.salience))
            for metadata_name, metadata_value in entity.metadata.items():
                print(u"{}: {}".format(metadata_name, metadata_value))
            for mention in entity.mentions:
                print(u"Mention: {}".format(mention.text.content))
                print(u"Mention type: {}".format(aiplatform.EntityMention.Type(mention.type_).name))
    def analyze_text_sentiment(text):
        """Detects sentiment in the text."""
        client = aiplatform.gapic.TranslationServiceClient()
        # text = 'Hawaiian pizza is the best!'
        response = client.analyze_sentiment(text=text)
        print(u"Document sentiment score: {}".format(response.document_sentiment.score))
        print(u"Document sentiment magnitude: {}".format(response.document_sentiment.magnitude))
    def analyze_text_syntax(text):
        """Detects syntax in the text."""
        client = aiplatform.gapic.TranslationServiceClient()
        # text = 'Hawaiian pizza is the best!'
        response = client.analyze_syntax(text=text)
        for token in response.tokens:
            print(u"Token text: {}".format(token.text.content))
            print(u"Token part of speech: {}".format(aiplatform.PartOfSpeech.Tag(token.part_of_speech.tag).name))
            print(u"Dependency edge: {}".format(aiplatform.DependencyEdge.Label(token.dependency_edge.label).name))
    def analyze_text_sentiment(text):
        """Detects sentiment in the text."""
        client= aiplatform.gapic.TranslationServiceClient()
