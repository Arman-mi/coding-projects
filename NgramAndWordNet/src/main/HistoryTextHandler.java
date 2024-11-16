package main;

import browser.NgordnetQuery;
import browser.NgordnetQueryHandler;
import ngrams.NGramMap;
import ngrams.TimeSeries;

import java.util.List;


public class HistoryTextHandler extends NgordnetQueryHandler {
    NGramMap ngram;

    public HistoryTextHandler(NGramMap ngram) {
        this.ngram = ngram;
    }

    @Override
    public String handle(NgordnetQuery q) {
        StringBuilder result = new StringBuilder();

        List<String> words = q.words();
        int startyear = q.startYear();
        int endyear = q.endYear();
        for (String word: words) {
            TimeSeries times = ngram.weightHistory(word, startyear, endyear);
            result.append(word).append(": ").append(times.toString()).append("\n");

        }

        String azsharab = result.toString();

        return azsharab;
    }
}
