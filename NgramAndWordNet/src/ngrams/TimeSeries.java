package ngrams;

import java.util.*;

/**
 * An object for mapping a year number (e.g. 1996) to numerical data. Provides
 * utility methods useful for data analysis.
 *
 * @author Josh Hug
 */
public class TimeSeries extends TreeMap<Integer, Double> {

    /** If it helps speed up your code, you can assume year arguments to your NGramMap
     * are between 1400 and 2100. We've stored these values as the constants
     * MIN_YEAR and MAX_YEAR here. */
    public static final int MIN_YEAR = 1400;
    public static final int MAX_YEAR = 2100;

    /**
     * Constructs a new empty TimeSeries.
     */
    public TimeSeries() {
        super();
    }

    /**
     * Creates a copy of TS, but only between STARTYEAR and ENDYEAR,
     * inclusive of both end points.
     */
    public TimeSeries(TimeSeries ts, int startYear, int endYear) {
        super();
        Set<Integer> allYears = ts.keySet();
        for (Integer y : allYears) {
            if (y >= startYear && y <= endYear) {
                this.put(y, ts.get(y));
            }
        }

    }

    /**
     *  Returns all years for this time series in ascending order.
     */
    public List<Integer> years() {
        Set<Integer> allYearssboi = this.keySet();
        return new ArrayList<>(allYearssboi);
    }

    /**
     *  Returns all data for this time series. Must correspond to the
     *  order of years().
     */
    public List<Double> data() {
        Collection<Double> alldata = this.values();
        ArrayList<Double> alldatabutarray = new ArrayList<>(alldata);
        return alldatabutarray;
    }

    /**
     * Returns the year-wise sum of this TimeSeries with the given TS. In other words, for
     * each year, sum the data from this TimeSeries with the data from TS. Should return a
     * new TimeSeries (does not modify this TimeSeries).
     *
     * If both TimeSeries don't contain any years, return an empty TimeSeries.
     * If one TimeSeries contains a year that the other one doesn't, the returned TimeSeries
     * should store the value from the TimeSeries that contains that year.
     */
    public TimeSeries plus(TimeSeries ts) {
        TimeSeries newSeries = new TimeSeries();
        // I looked the putall function up online, handy little bastard.
        newSeries.putAll(this);

        for (Map.Entry<Integer, Double> data : ts.entrySet()) {
            int year = data.getKey();
            double value;

            value = data.getValue();
            if (newSeries.containsKey(year)) {
                double newseriesValue = newSeries.get(year);
                newSeries.put(year, value + newseriesValue);

            } else {
                newSeries.put(year, value);


            }
        }
        return newSeries;

    }

    public boolean containsYear(int year) {
        return this.containsKey(year);
    }

    /**
     * Returns the quotient of the value for each year this TimeSeries divided by the
     * value for the same year in TS. Should return a new TimeSeries (does not modify this
     * TimeSeries).
     *
     * If TS is missing a year that exists in this TimeSeries, throw an
     * IllegalArgumentException.
     * If TS has a year that is not in this TimeSeries, ignore it.
     */
    public TimeSeries dividedBy(TimeSeries ts) {
        // Version 3 of the code, more efficent and elegant. as josh hug likes to say
        // beautiful solution... not so beautiful if it takes you 3 hours tho...
        TimeSeries newSeries = new TimeSeries();
        newSeries.putAll(this);

        for (Map.Entry<Integer, Double> datapair: newSeries.entrySet()) {
            int currentyear = datapair.getKey();



            Double currnetValue = datapair.getValue();

            if (ts.containsKey(currentyear)) {

                newSeries.put(currentyear, currnetValue /  ts.get(currentyear));

            } else {
                throw new IllegalArgumentException("something is wrong, the math aint mathing");
            }

        }






        return newSeries;


    }


}