    rules = (  
    
        # don't recommend artists with male-specific tags to females
        SubjectObjectRule(
            name="Don't recommend male music to female users.",

            # the user is a female and the artist was tagged by
            # a male-specific tag
            condition=lambda user, artist: user.gender == 'f' and \
                artist.artisttag_set.filter(tag__gender_specific='m').exists()
            
            # it's a negative rule
            is_positive=False,
            
            weight=0.5,
            
            # the more male-specific tags the artist has, the higher is 
            # the rule confidence. Normalized by the artist tag count
            confidence=lambda user, artist: float(
                artist.artisttag_set.filter(tag__gender_specific='m').count())/ \
                    artist.artisttag_set.count(),
                    
            description="Artist %(object)s isn't recommended to %(subject)s, " +
                "because the artist is considered male-specific."
        )
                
                
        # users of similar age are similar
        SubjectSimilarityRule(
            name="Users with similar age.",
            
            # both users have given their age and the difference 
            # is lower than five
            condition=lambda user1, user2: 
                user1.age and user2.age and abs(user1.age - user2.age) <= 5,
                
            is_positive=True,   
                
            weight=0.5,
            
            # a magic linear confidence function
            confidence=lambda user1, user2: 
                1 - float(abs(user1.age - user2.age))/AGE_DIFFERENCE,
            
            description="Users %(subject1)s and %(subject2)s are about " + 
                "the same age."
        ),        
        
        # artists sharing some tags are similar
        ObjectSimilarityRule(
            name="Artists sharing some tags.",

            # both artists have some tags and they share at least one tag
            # generator - take artists having some tags, compare them one to one
            generator=_tag_similarity_generator,
            
            
            # it's a positive rule
            is_positive=True,
            
            weight=0.5,
            
            # The more tags the artists have in common, the higher is  
            # the similarity confidence
            confidence=lambda artist1, artist2: \
                float(artist1.artisttag_set.filter(
                    tag__id__in=artist2.artisttag_set.values_list('tag__id')
                ).count()) / \
                min(artist1.artisttag_set.count(), artist2.artisttag_set.count()),
            
            description="Artists %(object1)s and %(object2)s are similar " + \
             "because they share some tags."
        ), 
    
        
        # if the users were registered in a similar period, the're similar
        SubjectSimilarityRule(
            name='Users registered in similar time.',
            
            condition=lambda s1, s2:
                s1.registered and s2.registered and \
                abs(s1.registered.toordinal() - s2.registered.toordinal()) < REGISTERED_DIFFERENCE / 5,
            
            is_positive=True,
            weight=0.5,
            
            confidence=lambda s1, s2:
                1 - float(abs(s1.registered.toordinal() - s2.registered.toordinal()))/REGISTERED_DIFFERENCE,
                
            description="Users %(subject1)s and %(subject2)s were registered in similar times",
        ),
    )
    
    cluster_sets = (

        
        # user - gender
        SubjectClusterSet(
            
            name='User gender.',
            
            weight=0.5,
            
            # users that have a gender (filled)
            filter_entities=User.objects.exclude(gender=''),
            
            get_cluster_confidence_pairs=lambda user: ((user.gender, 1),),
            
            description="%(subject)s's gender is %(cluster)s."
        
        ),
        
        # user - country
        SubjectClusterSet(
            
            name='User country.',
            
            weight=0.5,
            
            # users that have country filled
            filter_entities=User.objects.filter(country__isnull=False),
            
            get_cluster_confidence_pairs=lambda user: ((user.country.name, 1),),
            
            description="%(subject)s is from %(cluster)s."
        ),
    )
    
    biases = (
        ObjectBias(
            name="Artists whose tracks were listened the most.",
            description="%(object)s is much listened.",
            weight=0.5,
            is_positive=True,
            # users whose tracks were listened more than the half of the most listened
            generator=lambda: Artist.objects.annotate(listen_count=Count('track__scrobble')).filter(listen_count__gt=MAX_SCROBBLE_COUNT/7),
            
            # the number of scrobbles for the artist divided by the max.
            confidence=lambda a: float(a.track_set.annotate(scrobble_count=Count('scrobble')).aggregate(Sum('scrobble_count')))/MAX_SCROBBLE_COUNT
        ),
        
    )            
    
    
    
    
    
    
    
            # tag clusters
        ObjectClusterSet(

            name="Artist tags.",

            weight=0.5,
            
            # artists that are tagged by a tag that another artist also has
            filter_entities=Artist.objects.annotate(shared_count=Count('artisttag__tag__artisttag')).filter(shared_count__gt=1).distinct(),
            
            get_cluster_confidence_pairs=_get_artist_tag_pairs,
            
            description="%(object)s was tagged as %(cluster)s.",
        ),
