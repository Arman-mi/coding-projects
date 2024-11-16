import browser.NgordnetQuery;
import browser.NgordnetQueryHandler;
import edu.princeton.cs.algs4.StdRandom;
import main.AutograderBuddy;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import static com.google.common.truth.Truth.assertThat;
import static com.google.common.truth.Truth.assertWithMessage;

/** Tests the case where the list of words is length greater than 1, but k is still zero. */
public class TestMultiWordK0Hyponyms {
    // this case doesn't use the NGrams dataset at all, so the choice of files is irrelevant
    // ngrams files
    public static final String VERY_SHORT_WORDS_FILE = "data/ngrams/very_short.csv";
    public static final String TOTAL_COUNTS_FILE = "data/ngrams/total_counts.csv";
    private static final String SMALL_WORDS_FILE = "data/ngrams/top_14377_words.csv";
    private static final String WORDS_FILE = "data/ngrams/top_49887_words.csv";

    // wordnet Files
    public static final String SMALL_SYNSET_FILE = "data/wordnet/synsets16.txt";
    public static final String SMALL_HYPONYM_FILE = "data/wordnet/hyponyms16.txt";
    public static final String LARGE_SYNSET_FILE = "data/wordnet/synsets.txt";
    public static final String LARGE_HYPONYM_FILE = "data/wordnet/hyponyms.txt";
    private static final String HYPONYMS_FILE_SUBSET = "data/wordnet/hyponyms1000-subgraph.txt";
    private static final String SYNSETS_FILE_SUBSET = "data/wordnet/synsets1000-subgraph.txt";

    // EECS files
    private static final String FREQUENCY_EECS_FILE = "data/ngrams/frequency-EECS.csv";
    private static final String HYPONYMS_EECS_FILE = "data/wordnet/hyponyms-EECS.txt";
    private static final String SYNSETS_EECS_FILE = "data/wordnet/synsets-EECS.txt";


    /** This is an example from the spec.*/
    @Test
    public void testOccurrenceAndChangeK0() {
        NgordnetQueryHandler studentHandler = AutograderBuddy.getHyponymsHandler(
                VERY_SHORT_WORDS_FILE, TOTAL_COUNTS_FILE, SMALL_SYNSET_FILE, SMALL_HYPONYM_FILE);
        List<String> words = new ArrayList<>();
        words.add("occurrence");
        words.add("change");

        NgordnetQuery nq = new NgordnetQuery(words, 0, 0, 0);
        String actual = studentHandler.handle(nq);
        String expected = "[alteration, change, increase, jump, leap, modification, saltation, transition]";
        assertThat(actual).isEqualTo(expected);
    }

   @Test
    public void testChangeK0() {
        NgordnetQueryHandler studentHandler = AutograderBuddy.getHyponymsHandler(
                WORDS_FILE, TOTAL_COUNTS_FILE, SMALL_SYNSET_FILE, SMALL_HYPONYM_FILE);
        List<String> words = new ArrayList<>();
        words.add("change");

        NgordnetQuery nq = new NgordnetQuery(words, 0, 0, 0); // k = 0, so we get all hyponyms
        String actual = studentHandler.handle(nq);
        String expected = "[alteration, change, conversion, demotion, modification, mutation, transition, variation]";
        assertThat(actual).isEqualTo(expected);
    }
    @Test
    public void testMultipleWordsK0() {
        NgordnetQueryHandler studentHandler = AutograderBuddy.getHyponymsHandler(
                WORDS_FILE, TOTAL_COUNTS_FILE, SMALL_SYNSET_FILE, SMALL_HYPONYM_FILE);
        List<String> words = Arrays.asList("change", "transition");

        NgordnetQuery nq = new NgordnetQuery(words, 0, 0, 0); // k = 0 to get all common hyponyms
        String actual = studentHandler.handle(nq);
        String expected = "[jump, leap, saltation, transition]";
        assertThat(actual).isEqualTo(expected);
    }
    @Test
    public void testActionK3() {
        NgordnetQueryHandler studentHandler = AutograderBuddy.getHyponymsHandler(
                WORDS_FILE, TOTAL_COUNTS_FILE, SMALL_SYNSET_FILE, SMALL_HYPONYM_FILE);
        List<String> words = new ArrayList<>();
        words.add("act");

        NgordnetQuery nq = new NgordnetQuery(words, 0, 0, 3); // k = 3, so we get only 3 most popular hyponyms
        String actual = studentHandler.handle(nq);
        String expected = "[action, change, demotion]"; // Adjust based on actual popularity in your data
        assertThat(actual).isEqualTo(expected);
    }
    @Test
    public void testNoHyponyms() {
        NgordnetQueryHandler studentHandler = AutograderBuddy.getHyponymsHandler(
                WORDS_FILE, TOTAL_COUNTS_FILE, SMALL_SYNSET_FILE, SMALL_HYPONYM_FILE);
        List<String> words = new ArrayList<>();
        words.add("nonexistent_word");

        NgordnetQuery nq = new NgordnetQuery(words, 0, 0, 0); // k = 0, no hyponyms should exist
        String actual = studentHandler.handle(nq);
        String expected = "[]"; // Expect an empty list if no hyponyms exist
        assertThat(actual).isEqualTo(expected);
    }

    @Test
    public void testHyponymsInTimeRange() {
        NgordnetQueryHandler studentHandler = AutograderBuddy.getHyponymsHandler(
                WORDS_FILE, TOTAL_COUNTS_FILE, SMALL_SYNSET_FILE, SMALL_HYPONYM_FILE);
        List<String> words = new ArrayList<>();
        words.add("act");

        // Assume the range includes only some years with counts > 0
        NgordnetQuery nq = new NgordnetQuery(words, 1950, 2000, 0); // Specify time range
        String actual = studentHandler.handle(nq);
        String expected = "[action, change]"; // Example output, adjust based on actual data and counts
        assertThat(actual).isEqualTo(expected);
    }


    @Test
    public void testMultipleWordsK00() {
        NgordnetQueryHandler studentHandler = AutograderBuddy.getHyponymsHandler(
                WORDS_FILE, TOTAL_COUNTS_FILE, SMALL_SYNSET_FILE, SMALL_HYPONYM_FILE);
        List<String> words = Arrays.asList("change", "occurrence");

        NgordnetQuery nq = new NgordnetQuery(words, 0, 0, 0); // k = 0 to get all common hyponyms
        String actual = studentHandler.handle(nq);
        String expected = "[alteration, change, increase, jump, leap, modification, saltation, transition]";
        assertThat(actual).isEqualTo(expected);
    }


}
