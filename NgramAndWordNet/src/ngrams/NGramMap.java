package ngrams;

import edu.princeton.cs.algs4.In;


import java.util.Collection;
import java.util.Map;
import java.util.TreeMap;

import static ngrams.TimeSeries.MAX_YEAR;
import static ngrams.TimeSeries.MIN_YEAR;

/**
 * An object that provides utility methods for making queries on the
 * Google NGrams dataset (or a subset thereof).
 *
 * An NGramMap stores pertinent data from a "words file" and a "counts
 * file". It is not a map in the strict sense, but it does provide additional
 * functionality.
 *
 * @author Josh Hug
 */
public class NGramMap {
    Map<String, TimeSeries> wordmap;

    TimeSeries counts;

    /**
     * Constructs an NGramMap from WORDSFILENAME and COUNTSFILENAME.
     */
    public NGramMap(String wordsFilename, String countsFilename) {

        wordmap = new TreeMap<>();
        counts = new TimeSeries();

        //        CompletableFuture<Void> wordsTask = CompletableFuture.runAsync(() -> loadwordsfile(wordsFilename));
        //        CompletableFuture<Void> countsTask = CompletableFuture.runAsync(() -> loadcountfiles(countsFilename));
        //        CompletableFuture.allOf(wordsTask, countsTask).join();
        loadwordsfile(wordsFilename);
        loadcountfiles(countsFilename);




    }

    /**
     * Provides the history of WORD between STARTYEAR and ENDYEAR, inclusive of both ends. The
     * returned TimeSeries should be a copy, not a link to this NGramMap's TimeSeries. In other
     * words, changes made to the object returned by this function should not also affect the
     * NGramMap. This is also known as a "defensive copy". If the word is not in the data files,
     * returns an empty TimeSeries.
     */
    public TimeSeries countHistory(String word, int startYear, int endYear) {
        if (!wordmap.containsKey(word)) {
            return new TimeSeries();
        }
        TimeSeries kosegav = wordmap.get(word);
        return new TimeSeries(kosegav, startYear, endYear);



    }

    /**
     * Provides the history of WORD. The returned TimeSeries should be a copy, not a link to this
     * NGramMap's TimeSeries. In other words, changes made to the object returned by this function
     * should not also affect the NGramMap. This is also known as a "defensive copy". If the word
     * is not in the data files, returns an empty TimeSeries.
     */
    public TimeSeries countHistory(String word) {
        if (!wordmap.containsKey(word)) {
            // this is version 2
            return new TimeSeries();
        }
        TimeSeries kosekhar = wordmap.get(word);
        return new TimeSeries(kosekhar, MIN_YEAR, MAX_YEAR);


        //version1:
        //     return Collections.unmodifiableMap(wordMap.get(word));


    }

    /**
     * Returns a defensive copy of the total number of words recorded per year in all volumes.
     */
    public TimeSeries totalCountHistory() {
        return new TimeSeries(counts, MIN_YEAR, MAX_YEAR);
    }

    /**
     * Provides a TimeSeries containing the relative frequency per year of WORD between STARTYEAR
     * and ENDYEAR, inclusive of both ends. If the word is not in the data files, returns an empty
     * TimeSeries.
     */
    public TimeSeries weightHistory(String word, int startYear, int endYear) {
        TimeSeries result = new TimeSeries();
        if (!wordmap.containsKey(word)) {
            return new TimeSeries();
        }


        TimeSeries wordcounts = wordmap.get(word);



        for (int i : wordcounts.subMap(startYear, true, endYear, true).keySet()) {
            addrelfreq(result, i, wordcounts.get(i));
        }
        return result;


    }

    /**
     * Provides a TimeSeries containing the relative frequency per year of WORD compared to all
     * words recorded in that year. If the word is not in the data files, returns an empty
     * TimeSeries.
     */
    public TimeSeries weightHistory(String word) {
        return weightHistory(word, TimeSeries.MIN_YEAR, TimeSeries.MAX_YEAR);

    }

    /**
     * Provides the summed relative frequency per year of all words in WORDS between STARTYEAR and
     * ENDYEAR, inclusive of both ends. If a word does not exist in this time frame, ignore it
     * rather than throwing an exception.
     */
    public TimeSeries summedWeightHistory(Collection<String> words,
                                          int startYear, int endYear) {

        TimeSeries result  = new TimeSeries();
        for (String word : words) {
            TimeSeries wwh = weightHistory(word, startYear, endYear);
            result = result.plus(wwh);
        }
        return result;
    }

    /**
     * Returns the summed relative frequency per year of all words in WORDS. If a word does not
     * exist in this time frame, ignore it rather than throwing an exception.
     */
    public TimeSeries summedWeightHistory(Collection<String> words) {
        return summedWeightHistory(words, MIN_YEAR, TimeSeries.MAX_YEAR);

    }

    // I used google and some searching to write this function. not purely my own work but then again
    // Josh Hug said its okay to use online resources and that we will use lots of online resouces for this project.
    private void loadcountfiles(String filename) {
        //        String L;
        //        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
        //            String L;
        //
        //            while ((L = reader.readLine()) != null) {
        //                String[] parts = L.split(",");
        //
        //                if (parts.length < 2) {
        //                    System.err.println("Skipping invalid line: " + L);
        //                    continue;
        //                }
        //                int year = Integer.parseInt(parts[0]);
        //                double totalCount = Double.parseDouble(parts[1]);
        //                counts.put(year, totalCount);
        //
        //            }
        //        } catch (IOException | NumberFormatException expection) {
        //            expection.printStackTrace();
        //        }
        In in = new In(filename);
        while (!in.isEmpty()) {
            String nextLine = in.readLine();
            String[] splitLine = nextLine.split(",");
            int year;
            double totalcount;
            year = Integer.parseInt(splitLine[0]);
            totalcount = Double.parseDouble(splitLine[1]);
            counts.put(year, totalcount);

        }
    }


    private void loadwordsfile(String filename) {
        //            String lama;
        //        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
        //            String lama;
        //            while ((lama = reader.readLine()) != null) {
        //                String[] parts = lama.split("\t");
        //                if (parts.length < 3) {
        //                    System.err.println("Skipping invalid line: " + lama);
        //                    continue;
        //                }
        //                String word = parts[0];
        //                int year = Integer.parseInt(parts[1]);
        //                double count = Double.parseDouble(parts[2]);
        //
        //                wordmap.computeIfAbsent(word, k -> new TimeSeries()).put(year, count);
        //            }
        //        } catch (IOException | NumberFormatException e) {
        //            e.printStackTrace();
        //        }
        In in = new In(filename);
        while (!in.isEmpty()) {
            String nextLine = in.readLine();
            String[] splitLine = nextLine.split("\t");
            if (splitLine.length < 3) {
                System.out.println("invalid line");
                continue;
            }
            String word = splitLine[0];
            int year = Integer.parseInt(splitLine[1]);
            double count = Double.parseDouble(splitLine[2]);
            TimeSeries hugTime;
            if (wordmap.containsKey(word)) {

                hugTime = wordmap.get(word);
            } else {
                hugTime = new TimeSeries();
                wordmap.put(word, hugTime);

            }

            hugTime.put(year, count);

        }




    }

    private void addrelfreq(TimeSeries result, int year, double wordcount) {
        if (counts.containsKey(year) && counts.get(year) > 0) {
            double totalcount = counts.get(year);
            result.put(year, wordcount / totalcount);



        }

    }

    public long getcountsForRange (String word, int startYear, int endYear) {
        TimeSeries wordHisstory = getWordCountHistory(word);
        long total = 0;
        for (int year = startYear; year <= endYear; year++){
            if (wordHisstory.containsYear(year)) {
                total += wordHisstory.get(year);
            }
        }
        return total;
    }


    //private void print(int x){
    //        return System.out.println(x);
    //}


    public TimeSeries getWordCountHistory(String word) {
        return wordmap.getOrDefault(word, new TimeSeries());
    }

}
