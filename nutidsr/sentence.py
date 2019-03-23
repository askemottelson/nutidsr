from db.db_handler import db
from db.models import Word, Form
import re


class Sentence():

    def __init__(self, sentence):
        if not isinstance(sentence, list):
            raise Exception("Sentence() takes a list as argument")

        self.sentence = sentence

        # get each word from db
        self.candidates = [
            self.get_words(w) for w in self.sentence
        ]

        # easy; words with one candidate *are* correct
        self.words = []
        for c in self.candidates:
            if len(c) == 1:
                self.words.append(c[0])
            else:
                # add a place holder for now
                self.words.append(None)

        # now try the rule based hiearchi
        for i, w in enumerate(self.words):
            if w is None:
                self.words[i] = self.pick_a_word(i)

    def pick_first(self, candidates, category, revert=False):
        for cand in candidates:
            if revert:
                if not cand.category == category:
                    return cand
            else:
                if cand.category == category:
                    return cand
        raise Exception("no category in candidate list")

    def pick_a_word(self, index):
        candidates = self.candidates[index]

        # if it's not a real word, we don't know
        if len(candidates) == 0:
            return None

        # if they're all same category, who cares
        if len(list(set([c.category for c in candidates]))) == 1:
            return candidates[0]

        # now to the tricky part
        try:
            pre = self.get_obj(index - 1)

            if pre.category == 'konj.':
                return self.pick_first(candidates, 'vb.')

            if pre.word == 'at' or pre.word == 'jeg':
                return self.pick_first(candidates, 'vb.')

            if pre.category == 'pron.':
                return self.pick_first(candidates, 'sb.')

            if pre.category == 'vb.':
                return self.pick_first(candidates, 'sb.', True)

            if pre.category == 'pl.':
                return self.pick_first(candidates, 'sb.')

            if pre.category == 'sb.':
                return self.pick_first(candidates, 'vb.')

            # desperate times
            self.pick_first(candidates, 'pron.')

        except Exception:
            # didn't have what we were looking for
            pass

        # out of options, pick the first
        return candidates[0]

    def get_words(self, word):
        # clean stuff away
        word = word.translate('"»«“”‘’\'')

        if len(word) == 0:
            return []

        words = db.query(Word).filter(Word.word == word).all()
        forms = [
            f.word for f in db.query(Form).filter(Form.form == word).all()
        ]

        genitives = []
        if word[-1] == 's':
            genitives = self.get_words(word[0:-1])

        lower_case = []
        if not word.lower() == word:
            lower_case = self.get_words(word.lower())

        sign = []
        if word[-1] in ";,.-'?!":
            sign = self.get_words(word[0:-1])

        paran = []
        if word[0] == '(' and word[-1] == ')':
            paran = self.get_words(word[1:-1])

        return words + forms + genitives + lower_case + sign + paran

    def get_obj(self, index):
        o = self.words[index]
        if o is None:
            o = self.pick_a_word(index)
            self.words[index] = o
        return o

    def get_all(self):
        return [
            self.get_obj(i) for i in range(0, len(self.words))
        ]


class Sentences():

    def __init__(self, text):
        self.sentences = []

        sentences = re.compile(r"[\.,]\s").split(text)
        approved_sentences = []

        # glue abbreviations
        count = 0
        skip_next = False
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) == 0:
                count += 1
                continue

            if skip_next:
                skip_next = False
                count += 1
                continue

            plus_dot = sentence.split()[-1] + '.'
            words = db.query(Word).filter(Word.word == plus_dot).all()
            if len(words) > 0:
                # glue together here
                if len(sentences) > count:
                    approved_sentences.append(
                        sentences[count] + '. ' + sentences[count + 1])
                    skip_next = True
                else:
                    approved_sentences.append(sentences[count] + '.')
            else:
                approved_sentences.append(sentences[count])

            count += 1

        for sentence in approved_sentences:
            clean = sentence.strip().split()
            if len(clean) > 0:
                s = Sentence(clean)
                self.sentences.append(s)


if __name__ == "__main__":
    # just some tests

    o = Sentence(["fuglen", "kan", "lide", "at", "pikkerd"]).get_obj(4)
    assert o is None

    o = Sentence(["det", "er", "min", "pik"]).get_obj(3)
    assert o.category == 'sb.'

    o = Sentence(["det", "er", "mine", "pikke"]).get_obj(3)
    assert o.category == 'sb.'

    o = Sentence(["fuglen", "pikker"]).get_obj(1)
    assert o.category == 'vb.'

    o = Sentence(["fuglen", "kan", "lide", "at", "pikke"]).get_obj(4)
    assert o.category == 'vb.'

    o = Sentence(["fuglen", "og", "dens", "ben", "og", "næb"]).get_obj(3)
    assert o.category == 'sb.'

    o = Sentence(["fuglen", "svinger", "med", "pikken"]).get_obj(3)
    assert o.category == 'sb.'

    o = Sentence(["fuglen", "svinger", "med", "pikkens", "pik"]).get_obj(3)
    assert o.category == 'sb.'

    o = Sentence(["Fuglen", "svinger", "med", "pikkens", "pik"]).get_obj(3)
    assert o.category == 'sb.'

    text = """
    På det seneste har man i medierne kunnet læse om biologistuderende, der har følt sig krænkede over, at deres underviser kategoriserede data efter køn i forbindelse med nogle statistiske eksempler. Tidligere er det også beskrevet, hvordan en mørklødet forsker på CBS havde følt sig krænket over, at man havde sunget en sang fra Højskolesangbogen med strofen: »Den danske sang er en ung blond pige«.

    Man kunne få det indtryk, at der på universiteterne er opstået en kultur med normer og værdier, der afviger stærkt fra det omgivende samfund, hvor det ellers er kutyme at inddele mennesker efter køn. Hvilket her sker velvidende, at der også findes få gråzoner og mellemvarianter f.eks. hermafroditter, transseksuelle eller personer, som er i gang med et kønsskifte.

    Tanken om, at det skulle være forkert eller ligefrem krænkende at kategorisere personer efter køn, er i tråd med nogle ideer fra Sverige. Der taler man om ikke at bruge begreberne ‘han’ og ‘hun’ i forbindelse med børneopdragelse, men i stedet den kønsneutrale betegnelse ‘hen’. Denne opfattelse af kønsforskelle harmonerer bedst med ideen om køn som en primært kulturel eller social konstruktion.

    Videnskabelige grundvilkår
    Har man dog at gøre med et fag som biologi, kommer man ikke uden om også at betragte køn som noget fysisk og mere objektivt. I biologien handler kønsforskelle om forskelle i gennemsnitshøjde, genitalier, hormonbalancer og lignende.

    Videnskaben bruger kategoriseringer og dualistisk tænkning som hunkøn og hankøn, og det er ikke noget tilfælde. Det er en del af en meget gammel tradition, som kan spores tilbage til den tidlige videnskab i oldtidens Grækenland. Herunder særligt til filosoffen Aristoteles, som var elev af Platon og naturvidenskabsmand. Han udførte et omfattende arbejde med registrering og kategorisering af dyrearter og racer.

    Når man i videnskaben benytter sig af kategoriseringer f.eks. med hensyn til arter eller køn, er det ikke for at fornærme nogen eller for at negligere, at der også kan eksistere noget, der ikke passer ind i disse båse, men for at skabe en forenkling og et overblik over en ofte rodet og uoverskuelig verden.
    """

    s = Sentences(text)

    for sentence in s.sentences:
        print(sentence.sentence)
        assert sentence.get_obj(0) is not None
