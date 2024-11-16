package main;
import browser.NgordnetQuery;
import browser.NgordnetQueryHandler;
import ngrams.NGramMap;
import ngrams.TimeSeries;
import plotting.Plotter;
import org.knowm.xchart.XYChart;

import java.util.ArrayList;
import java.util.List;


public class HistoryHandler extends NgordnetQueryHandler  {
    NGramMap ngram;
    public HistoryHandler(NGramMap ngram) {
        this.ngram = ngram;
    }
    @Override
    public String handle(NgordnetQuery q) {
        List<String> words = q.words();
        int startYear = q.startYear();
        int endYear = q.endYear();
        List<TimeSeries> timeSeriesList = new ArrayList<>();
        List<String> labels = new ArrayList<>();
        for (String word : words) {
            TimeSeries ts = ngram.weightHistory(word, startYear, endYear);
            timeSeriesList.add(ts);
            labels.add(word);
        }
        XYChart chart = Plotter.generateTimeSeriesChart(labels, timeSeriesList);
        String encodedImage = Plotter.encodeChartAsString(chart);
        return encodedImage;


    }


}

