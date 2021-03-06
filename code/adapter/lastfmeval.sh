#!/bin/sh

# run the evaluation- recommendations. parameters 
# novel -> NovelArtistRecommender, 
# nenovel -> ArtistRecommender
# dontbuild-> don't build

BUILD=true
EVAL=''
REC=''

for param in $*;
do    
    case $param in
    'novel')
        EVAL='NovelArtistRankEvaluator'
        REC='NovelArtistRecommender'
        ;;
    'nenovel')
        EVAL='ArtistRankEvaluator'
        REC='ArtistRecommender'
        ;;
    'dontbuild')
        BUILD=false
        ;;
    esac
done

if [ $BUILD = true ]
then
    # build
    echo "Building..."
    echo "from lastfm.recommender import *; $REC.build()" | python ./manage.py shell
fi

echo "Evaluating recommendations..."
echo "from lastfm.evaluation import *; from lastfm.recommender import *; $EVAL.evaluate_predictions($REC)"| python ./manage.py shell

echo ""

