from enum import Enum

class Tid(Enum):
    bydeform = 0
    nutid = 1
    datid = 2
    foernutid = 3
    foerdatid = 4

    def __str__(self):
        return str(self.value)

    def __int__(self):
        return int(self.value)


annotated = [
    ("at arbejde i netto", Tid.bydeform),
    ("jeg arbejder i netto", Tid.nutid),
    ("jeg arbejdede i netto", Tid.datid),
    ("jeg har arbejdet i netto", Tid.foernutid),
    ("jeg havde arbejdet i netto", Tid.foerdatid),

    ("at cykle til skole", Tid.bydeform),
    ("jeg cykler til skole", Tid.nutid),
    ("jeg cyklede til skole", Tid.datid),
    ("jeg har cyklet til skole", Tid.foernutid),
    ("jeg havde cyklet til skole", Tid.foerdatid),

    ("at hoppe i sengen", Tid.bydeform),
    ("jeg hopper i sengen", Tid.nutid),
    ("jeg hoppede i sengen", Tid.datid),
    ("jeg har hoppet i sengen", Tid.foernutid),
    ("jeg havde hoppet i sengen", Tid.foerdatid),

    ("at styre det hele", Tid.bydeform),
    ("jeg styrer det hele", Tid.nutid),
    ("jeg styrede det hele", Tid.datid),
    ("jeg har styret det hele", Tid.foernutid),
    ("jeg havde styret det hele", Tid.foerdatid),

    ("På det seneste har man i medierne kunnet læse om biologistuderende", Tid.foernutid),
    ("der har følt sig krænkede over", Tid.foernutid),
    ("at deres underviser kategoriserede data efter køn i forbindelse med nogle statistiske eksempler", Tid.datid),
    ("Tidligere er det også beskrevet", Tid.foerdatid),
    ("hvordan en mørklødet forsker på CBS havde følt sig krænket over", Tid.foerdatid),
    ("at man havde sunget en sang fra Højskolesangbogen med strofen: »Den danske sang er en ung blond pige«", Tid.foerdatid),
    ("Man kunne få det indtryk", Tid.foernutid),
    ("at der på universiteterne er opstået en kultur med normer og værdier", Tid.foernutid),
    ("der afviger stærkt fra det omgivende samfund", Tid.nutid),
    ("hvor det ellers er kutyme at inddele mennesker efter køn", Tid.nutid),
    ("Hvilket her sker velvidende", Tid.nutid),
    ("at der også findes få gråzoner og mellemvarianter f.eks. hermafroditter", Tid.bydeform),
    ("som er i gang med et kønsskifte", Tid.nutid),
    ("at det skulle være forkert eller ligefrem krænkende at kategorisere personer efter køn", Tid.bydeform),
    ("er i tråd med nogle ideer fra Sverige", Tid.nutid),
    ("Der taler man om ikke at bruge begreberne ‘han’ og ‘hun’ i forbindelse med børneopdragelse", Tid.nutid),
    ("men i stedet den kønsneutrale betegnelse ‘hen’", Tid.nutid),
    ("Denne opfattelse af kønsforskelle harmonerer bedst med ideen om køn som en primært kulturel eller social konstruktion", Tid.nutid),
    ("Videnskabelige grundvilkår Har man dog at gøre med et fag som biologi", Tid.bydeform),
    ("kommer man ikke uden om også at betragte køn som noget fysisk og mere objektivt", Tid.nutid),
    ("I biologien handler kønsforskelle om forskelle i gennemsnitshøjde", Tid.nutid),
    ("Videnskaben bruger kategoriseringer og dualistisk tænkning som hunkøn og hankøn", Tid.nutid),
    ("og det er ikke noget tilfælde", Tid.nutid),
    ("Det er en del af en meget gammel tradition", Tid.nutid),
    ("som kan spores tilbage til den tidlige videnskab i oldtidens Grækenland", Tid.bydeform),
    ("som var elev af Platon og naturvidenskabsmand", Tid.datid),
    ("Han udførte et omfattende arbejde med registrering og kategorisering af dyrearter og racer.", Tid.datid),
    ("er det ikke for at fornærme nogen eller for at negligere", Tid.bydeform),
    ("at der også kan eksistere noget", Tid.bydeform),


    ("Demokratisk politik kræver dramatik", Tid.nutid),
    ("Valghandlinger kan ses som terapisessioner", Tid.bydeform),
    ("hvor vælgere konfronteres med deres værste skrækscenarier – en ny krig", Tid.bydeform),
    ("at de i stemmeboksen får magt til at afværge disse scenarier", Tid.nutid),
    ("»Når valget nærmer sig,« bemærkede den franske politiske tænker Alexis de Tocqueville under en af sine rejser i USA i begyndelsen af 1800-tallet", Tid.datid),
    ("og agitationen bliver livlig og omfattende", Tid.nutid),
    ("Hele nationen henfalder i feberagtig tilstand ..", Tid.datid),
    ("men så såre et resultat foreligger", Tid.nutid),
    ("falder der atter ro på", Tid.datid),
    ("der før gik over sine bredder", Tid.datid),
    ("genfinder sit naturlige leje.« Har Tocqueville ret", Tid.nutid),
    ("er Den Europæiske Union i disse dage ved at forvandle sig til et ægte demokrati", Tid.bydeform),
    ("Hvor europaparlamentsvalg før var kedelige og trivielle", Tid.foerdatid),
    ("ser vi nu begyndelsen til en valgkamp", Tid.nutid),

    # twitter
    ("en katastrofisk kurs sat af de ledende skikkelser", Tid.datid),
    ("Om jeg BEGRIBER folk, der kun har én oplader til deres computer.", Tid.nutid),
    ("Tror vi skal forsøge at tage Jacinda Arderns kloge ord til os", Tid.bydeform),
    ("DF får egenhændigt lov til at flytte @24syv til Jylland.", Tid.nutid),
    ("Regeringen agerer flyttefirma.", Tid.nutid),
    ("Jeg er fortsat fuldstændig målløs.", Tid.nutid),
    ("Jeg kan lissågodt lade være med at få påtrykt Prins Henrik med en slange på hovedet på mit nye VISA-kort", Tid.nutid),
    ("kan man få data ud af disken fra en NAS", Tid.bydeform),
    ("Jeg har prøvet Googles umiddelbare forslag om pc bootet op på en linux dist", Tid.foernutid),
    ("Starthjælpen har gjort flygtninge til de fattigste mennesker i Danmark", Tid.foernutid),
    ("Den har været en menneskelig og social katastrofe", Tid.foernutid),
    ("Det kunne egentlig være sjovt", Tid.foerdatid),
    ("hvis det nu var en mand", Tid.foerdatid),
    ("der havde haft sin baby med i Folketinget", Tid.foerdatid),
    ("Var babyen så også blevet sendt ud", Tid.foerdatid),
    ("eller var manden blevet hyldet for at være en far", Tid.foerdatid),
    ("der havde overskud til i situationen at overkomme både job og barn", Tid.foerdatid),
    ("Det er satire", Tid.nutid),
    ("Men det er ikke satire", Tid.nutid),
    ("Det er da verdens mindste nyhed", Tid.nutid),
    ("at DF fører smålig", Tid.nutid),
    ("populistisk og hævngerrig politik og derfor ønsker at nedlægge Radio 24syv", Tid.nutid),
    ("I mine øjne er tragedien", Tid.nutid),
    ("at regeringen lader dem gøre det", Tid.nutid),
    ("I det mindste har DF en kultur- og mediepolitik", Tid.nutid),
    ("om man så kan lide den eller ej", Tid.nutid),
    ("Mange er sure over", Tid.nutid),
    ("at DF dræber @24syv men", Tid.nutid),
    ("Det kan ikke komme som en overraskelse for nogen", Tid.bydeform),
    ("DF har ikke flertal alene", Tid.nutid),
    ("Det er liberale politikere der svinger øksen", Tid.nutid),

]