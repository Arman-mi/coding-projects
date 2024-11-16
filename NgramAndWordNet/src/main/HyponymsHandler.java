package main;

import browser.NgordnetQuery;
import browser.NgordnetQueryHandler;
import ngrams.NGramMap;

import java.util.*;

public class HyponymsHandler extends NgordnetQueryHandler {

    WordNet wordNet;
    NGramMap ngramMap;
    public HyponymsHandler(WordNet w, NGramMap n) {
        this.wordNet = w;
        this.ngramMap = n;
    }
    @Override
    public String handle(NgordnetQuery q) {
        List<String> words = q.words();
        int k;
        int startyear;
        int endyear;
        startyear = q.startYear();
        endyear = q.endYear();
        k = q.k();
        if (words.isEmpty()) {
            return "no words";
        }

        Set<String> commonhypo;
        commonhypo = new HashSet<>(wordNet.givemehyponyms(words.get(0)));
        for (int i = 1; i < words.size(); i++) {
            Set<String> hyponymsForWord = new HashSet<>(wordNet.givemehyponyms(words.get(i)));
            commonhypo.retainAll(hyponymsForWord);

        }
        if (k == 0) {
            List<String> hyponymlist = new ArrayList<>(commonhypo);
            Collections.sort(hyponymlist);
            return hyponymlist.toString();

        } else {
            Map<String, Long> hypopop;
            hypopop = new HashMap<>();
            for (String hyponym : commonhypo) {
                long count = ngramMap.getcountsForRange(hyponym, startyear, endyear);
                if (count > 0) {
                    hypopop.put(hyponym, count);
                }
            }
            //NGL I used Artifical boys for this last part, it was beyond me.
            List<String> sortedHyponyms = hypopop.entrySet().stream().sorted((a, b) -> {
                int countCompare = Long.compare(b.getValue(), a.getValue());
                return countCompare != 0
                                ? countCompare
                                :
                                a.getKey().compareTo(b.getKey());
            }).map(Map.Entry::getKey).limit(k).sorted().toList();
            return sortedHyponyms.toString();
        }
        //        hyponymsSet = new HashSet<>(wordNet.givemehyponyms(word));
        //        hyponymsList = new ArrayList<>(hyponymsSet);
        //        Collections.sort(hyponymsList);
        //        List<String> result;
        //        result = new ArrayList<>(commonhypo);
        //        return result.toString();
    }
}
