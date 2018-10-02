"""
    testing.default_user_content
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Create default user content.
"""
from app.extensions import db
from app.users.models import User, Post


class DefaultUserContent:
    default_users = [
        ('Daniel', 'Lindegren'),
        ('Sheree', 'Score'),
        ('Mike', 'Johnson'),
        ('Susan', 'Roberts'),
        ('Jennifer', 'Michaels'),
        ('Tammy', 'Fowler'),
        ('Jordan', 'Smith'),
        ('Sam', 'Jennings')
    ]

    def __init__(self):
        user_count = 0
        for first, last in self.default_users:
            user = User.query.filter_by(first_name=first).first()
            if user:
                user_count += 1
            setattr(self, first.lower(), user)
        if user_count == 0:
            print('*** Warning: No default users. Use :meth:`create_users`.')

    def create_users(self):
        for first, last in self.default_users:
            first_lower = first.lower()
            email = '{}@testing.com'.format(first_lower)
            user = User(email=email, first_name=first, last_name=last,
                        username=first_lower)
            user.set_password('testing')
            user_object = user.commit()
            setattr(self, first_lower, user_object)

    def create_posts(self):
        post_msg = 'Hey Tammy, how\'s it going?'
        post = Post(body=post_msg, author=self.daniel, recipient=self.tammy)
        db.session.add(post)

        post_msg = (
            'Hey guys this is Daniel. You shouldn\'t see this post because '
            'it should be inactive.')
        post = Post(body=post_msg, author=self.daniel, recipient=self.daniel,
                    active=False)

        post_msg = (
            'Hey guys, it\'s Jennifer. No one should see this, since I\'m '
            'a disabled user.')
        post = Post(body=post_msg, author=self.jennifer,
                    recipient=self.jennifer)
        db.session.add(post)

        post_msg = (
            'Hey Daniel. You should\'t see this message on your wall, '
            'since I\'m a disabled user.')
        post = Post(body=post_msg, author=self.jennifer,
                    recipient=self.daniel)
        db.session.add(post)

        post_msg = (
            'The American Center or the former United States Chancery are '
            'currently used as the offices of USAid in Colombo, Sri Lanka. '
            'The building is located on Galle Road, Colombo. The building '
            'was originally built by J. H. Meedeniya Adigar, which he named '
            'Rickman House. It was the home of D. R. Wijewardena (the '
            'founder of the Lake House newspaper group), who married '
            'Meedeniya\'s eldest daughter Alice.[1][2] The property is '
            'relatively unique as its land title, under the original old '
            'Dutch deed, extends down to the ocean, only one of a few such '
            'cases in Colombo.')
        post = Post(body=post_msg, author=self.daniel, recipient=self.daniel)
        db.session.add(post)

        post_msg = (
            'The D.L. Serventy Medal may be awarded annually by the '
            'Birdlife Australia for outstanding published work on birds in '
            'the Australasian region. It commemorates Dr Dominic Serventy '
            '(1904–1988) and was first awarded in 1991.[1] Source: Birdlife '
            'Australia Protogyrinus sculpturatus is a species of beetle in '
            'the family Gyrinidae, the only species in the genus '
            'Protogyrinus.')
        post = Post(body=post_msg, author=self.sheree, recipient=self.sheree)
        db.session.add(post)

        post_msg = (
            'Garner first worked for the Conservative Party as an '
            'organiser for the Young Conservatives in Yorkshire in '
            '1948.[1] He revived the membership by organising '
            'fundraising weekends at Filey Holiday Camp.[1] By 1951, he '
            'became a Conservative Party agent in Halifax, West '
            'Yorkshire.')
        post = Post(body=post_msg, author=self.mike, recipient=self.mike)
        db.session.add(post)

        post_msg = (
            'In 1903 the building was purchased by Wijewardena\'s mother, '
            'Helena, who subsequently demolished the existing residence and '
            'rebuilt a new dwelling, Sri Ramya.[4] The new dwelling was '
            'designed by Herbert Henry Reid.[4] Wijewardena occupied the '
            'residence until her death in 1940. In May 1934, the Indian '
            'poet, Rabindranath Tagore and the Indian painter, Nandalal '
            'Bose, stayed at the house for a fortnight, when Tagore brought '
            'a troupe of Bengali dancers to Ceylon.')
        post = Post(body=post_msg, author=self.susan, recipient=self.susan)
        db.session.add(post)

        post_msg = (
            'Swenson and actress Audra McDonald became engaged in January '
            '2012[10] and were married on October 6, 2012. [11] In October '
            '2016, McDonald and Swenson welcomed their first child, Sally. '
            'The Flaxbourne River is a river in the Marlborough region of '
            'New Zealand. It arises in the Inland Kaikoura Range and Halden '
            'Hills and flows east and then south-east into the South Pacific '
            'Ocean near Ward.')
        post = Post(body=post_msg, author=self.daniel, recipient=self.daniel)
        db.session.add(post)

        post_msg = (
            'In 1951 the building was purchased by the Government of the '
            'United States to serve as the chancery of its Embassy in Sri '
            'Lanka.[4] It functioned in that capacity until the United '
            'States Embassy moved to a new premises in 1984 and the building '
            'was transferred to USAid, for use as their offices.[5][6] '
            'Gamekeeper\'s thumb (also known as skier\'s thumb or UCL tear) '
            'is a type of injury to the ulnar collateral ligament (UCL) of '
            'the thumb.')
        post = Post(body=post_msg, author=self.sam, recipient=self.sam)
        db.session.add(post)

        post_msg = (
            'Traffic classification describes the methods of '
            'classifying traffic by observing features passively in the '
            'traffic, and in line to particular classification goals. '
            'There might be some that only have a vulgar classification '
            'goal. For example, whether it is bulk transfer, peer to '
            'peer file sharing or transaction-orientated.')
        post = Post(body=post_msg, author=self.sheree, recipient=self.sheree)
        db.session.add(post)

        post_msg = (
            'The basis of categorizing work is to classify the type of '
            'Internet traffic; this is done by putting common groups of '
            'applications into different categories, e.g., "normal" '
            'versus "malicious", or more complex definitions, e.g., the '
            'identification of specific applications or specific '
            'Transmission Control Protocol (TCP) implementations.')
        post = Post(body=post_msg, author=self.jordan, recipient=self.jordan)
        db.session.add(post)

        post_msg = (
            'The village itself is a designated conservation area, '
            'whilst the entire parish is located within the Dedham Vale '
            'Area of Outstanding Natural Beauty. It also contains Rowley '
            'Grove, a nature reserve classed as Ancient Woodland and a '
            'point to point racecourse which is home to the Waveney '
            'Harriers.')
        post = Post(body=post_msg, author=self.daniel, recipient=self.daniel)
        db.session.add(post)

        post_msg = (
            'Sir Anthony Stuart Garner (28 January 1927 – 22 March '
            '2015) was a political organiser for the British '
            'Conservative Party. Anthony Garner was born on 28 February '
            '1927 in Liverpool, England.[1][2] He was educated at '
            'Liverpool College.')
        post = Post(body=post_msg, author=self.susan, recipient=self.susan)
        db.session.add(post)

        post_msg = (
            'Symptoms of gamekeeper\'s thumb are instability of the MCP '
            'joint of the thumb, accompanied by pain and weakness of the '
            'pinch grasp. The severity of the symptoms are related to the '
            'extent of the initial tear of the UCL (in the case of Skier\'s '
            'thumb), or how long the injury has been allowed to progress '
            '(in the case of gamekeeper\'s thumb). Characteristic signs '
            'include pain, swelling, and ecchymosis around the '
            'thenar eminence, and especially over the MCP joint of '
            'the thumb.')
        post = Post(body=post_msg, author=self.susan, recipient=self.susan)
        db.session.add(post)

        post_msg = (
            'Some people argue that the new plan on Internet tax would '
            'prove disadvantageous to the country’s economic '
            'development, limit access to information and hinder the '
            'freedom of expression.[7] Approximately 36,000 people have '
            'signed up to take part in an event on Facebook to be held '
            'outside the Economy Ministry to protest against the '
            'possible tax.')
        post = Post(body=post_msg, author=self.tammy, recipient=self.tammy)
        db.session.add(post)

        post_msg = (
            'In October 2013, Swenson was cast as Inspector Javert in the '
            '2014 Broadway revival of Les Misérables, which opened in March '
            '2014 at New York\'s Imperial Theatre, where the musical had '
            'previously run for 13 years.[9] In 2018, Swenson played Satan '
            'in the New Group\'s off-Broadway production of "Jerry Springer: '
            'The Opera." Swenson met his first wife Amy (née Westerby) '
            'while they were both in one of his grandmother\'s comedies, '
            'Hopsville Holiday.')
        post = Post(body=post_msg, author=self.sam, recipient=self.sam)
        db.session.add(post)

        post_msg = (
            'According to Yahoo News, economy minister Mihály Varga '
            'defended the move saying "the tax was fair as it reflected '
            'a shift by consumers to the Internet away from phone lines" '
            'and that "150 forints on each transferred gigabyte of data '
            '– was needed to plug holes in the 2015 budget of one of the '
            'EU’s most indebted nations".')
        post = Post(body=post_msg, author=self.daniel, recipient=self.daniel)
        db.session.add(post)

        post_msg = (
            'Hey Tammy! I just wanted to post on your wall. '
            'Curabitur eleifend himenaeos lorem ad lectus pulvinar cubilia '
            'tellus, erat ad tempus aenean urna nostra sapien mauris eleifen '
            'tempor convallis fames taciti nam lectus lacinia.')
        post = Post(body=post_msg, author=self.daniel, recipient=self.tammy)
        db.session.add(post)

        post_msg = (
            'Hey Jordan, how\'s it going? I just wanted to see how are? '
            'Nulla fringilla tempus ante litora sit diam et adipiscing '
            'ultricies eu, duis a nisi dictumst interdum mauris aliquam '
            'etiam senectus quis leo nam.')
        post = Post(body=post_msg, author=self.mike, recipient=self.jordan)
        db.session.add(post)

        post_msg = (
            'Hey baby! How\'s it going? What are you going to do tonight? ')
        post = Post(body=post_msg, author=self.sheree, recipient=self.daniel)
        db.session.add(post)

        post_msg = (
            'Hey Sheree! I\'m doing well. I don\'t know what I\'m going to '
            'do yet. Let\'s definitely hang out though.')
        post = Post(body=post_msg, author=self.daniel, recipient=self.sheree)
        db.session.add(post)

        post_msg = (
            'A planned tax on Internet use in Hungary introduced a '
            '150-forint (US$0.62, €0.47) tax per gigabyte of data traffic, '
            'in a move intended to reduce Internet traffic and also assist '
            'companies to offset corporate income tax against the new '
            'levy.[5] Hungary achieved 1.')
        post = Post(body=post_msg, author=self.sheree, recipient=self.sheree)
        db.session.add(post)

        post_msg = (
            'The Food Safety Act 1990[1][2] is an Act of the Parliament of '
            'the United Kingdom. It is the statutory obligation to treat '
            'food intended for human consumption in a controlled and managed '
            'way. The key requirements of the Act are that food must comply '
            'with food safety requirements, must be "of the nature, '
            'substance and quality demanded", and must be correctly '
            'described (labelled).')
        post = Post(body=post_msg, author=self.sam, recipient=self.sam)
        db.session.add(post)

        post_msg = (
            'The patient will often manifest a weakened ability to grasp '
            'objects or perform such tasks as tying shoes and tearing a '
            'piece of paper. Other complaints include intense pain '
            'experienced upon catching the thumb on an object, such as when '
            'reaching into a pants pocket. Gamekeeper\'s thumb and skier\'s '
            'thumb are two similar conditions, both of which involve '
            'insufficiency of the ulnar collateral ligament (UCL) of the '
            'thumb. The chief difference between these two conditions is '
            'that Skier\'s thumb is generally considered to be an acute '
            'condition acquired after a fall or similar abduction injury to '
            'the metacarpophalangeal (MCP) joint of the thumb, whereas '
            'gamekeeper\'s thumb typically refers to a chronic condition '
            'which has developed as a result of repeated episodes of '
            'lower-grade hyperabduction over a period of time.')
        post = Post(body=post_msg, author=self.susan, recipient=self.susan)
        db.session.add(post)

        db.session.commit()

    def create_defaults(self):
        self.daniel.follow(self.sheree)
        self.daniel.follow(self.jennifer)
        self.sheree.follow(self.jordan)
        self.jordan.follow(self.daniel)
        self.jennifer.active = False
        self.daniel.posts_per_page = 5
        db.session.commit()
