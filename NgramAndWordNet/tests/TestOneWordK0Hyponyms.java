import browser.NgordnetQuery;
import browser.NgordnetQueryHandler;
import org.junit.jupiter.api.Test;
import main.AutograderBuddy;

import java.util.ArrayList;
import java.util.List;

import static com.google.common.truth.Truth.assertThat;

/** Tests the most basic case for Hyponyms where the list of words is one word long, and k = 0.*/
public class TestOneWordK0Hyponyms {
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

    @Test
    public void testActK0() {
        NgordnetQueryHandler studentHandler = AutograderBuddy.getHyponymsHandler(
                WORDS_FILE, TOTAL_COUNTS_FILE, SMALL_SYNSET_FILE, SMALL_HYPONYM_FILE);
        List<String> words = new ArrayList<>();
        words.add("act");

        NgordnetQuery nq = new NgordnetQuery(words, 0, 0, 0);
        String actual = studentHandler.handle(nq);
        String expected = "[act, action, change, demotion, human_action, human_activity, variation]";
        assertThat(actual).isEqualTo(expected);
    }

    // TODO: Add more unit tests (including edge case tests) here.

@Test

    public void test52() {
        NgordnetQueryHandler studentHandler = AutograderBuddy.getHyponymsHandler(
                SMALL_WORDS_FILE, TOTAL_COUNTS_FILE, SYNSETS_FILE_SUBSET, HYPONYMS_FILE_SUBSET);
        List<String> words = new ArrayList<>();
        words.add("scrap");

        NgordnetQuery nq = new NgordnetQuery(words, 1470, 2019, 3);
        String actual = studentHandler.handle(nq);
        String expected = "[bit, scale, scrap]";
        assertThat(actual).isEqualTo(expected);
    }



    @Test
    public void test53() {
        NgordnetQueryHandler studentHandler = AutograderBuddy.getHyponymsHandler(
                FREQUENCY_EECS_FILE, TOTAL_COUNTS_FILE, SYNSETS_EECS_FILE, HYPONYMS_EECS_FILE);
        List<String> words = new ArrayList<>();
        words.add("CS61A");

        NgordnetQuery nq = new NgordnetQuery(words, 2000, 2020, 4);
        String actual = studentHandler.handle(nq);
        String expected = "[CS170, CS61A, CS61B, CS61C]";
        assertThat(actual).isEqualTo(expected);
    }


    @Test
    public void test57() {
        NgordnetQueryHandler studentHandler = AutograderBuddy.getHyponymsHandler(
                FREQUENCY_EECS_FILE, TOTAL_COUNTS_FILE, SYNSETS_EECS_FILE, HYPONYMS_EECS_FILE);
        List<String> words = new ArrayList<>();
        words.add("CS61A");

        NgordnetQuery nq = new NgordnetQuery(words, 2000, 2020, 19);
        String actual = studentHandler.handle(nq);
        String expected = "[CS152, CS160, CS161, CS162, CS164, CS168, CS169, CS170, CS172, CS174, CS176, CS184, CS186, CS188, CS189, CS191, CS61A, CS61B, CS61C]";
        assertThat(actual).isEqualTo(expected);
    }

}