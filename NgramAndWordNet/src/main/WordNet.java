package main;

import edu.princeton.cs.algs4.In;

import java.util.*;

public class WordNet {
Graph <Integer,Integer> hyponymGraph;
Graph <String, Integer> nounGraph;
Map<Integer, String[]> idToSynset;
public WordNet(String synFile, String hypoFile ) {
    this.hyponymGraph = new Graph<>();
    this.nounGraph = new Graph<>();
    this.idToSynset = new HashMap<>();
    parseSyn(synFile);
    parsHypo(hypoFile);



}


public void parseSyn(String syn) {
    In reader = new In(syn);
    while(!reader.isEmpty()) {
        String line = reader.readLine();
        String[] parts = line.split(",");
        int synId = Integer.parseInt(parts[0]);
        String[] nouns = parts[1].split(" ");
        idToSynset.put(synId, nouns);
        for (String noun : nouns) {
            nounGraph.addVertex(noun);
            nounGraph.addEdge(noun, synId);
        }


    }


}

// we ball similar to the last function
public void parsHypo(String hypo) {
    In reader = new In(hypo);
    while (!reader.isEmpty()) {
        String line = reader.readLine();
        String[] parts = line.split(",");
        int synid = Integer.parseInt(parts[0]);
        for (int i = 1;i < parts.length; i++ ) {
            int hypoId;
            hypoId = Integer.parseInt(parts[i]);
            hyponymGraph.addVertex(synid);
            hyponymGraph.addVertex(hypoId);
            hyponymGraph.addEdge(synid,hypoId);
        }

    }

}


//public List<String> givemehyponyms(String n) {
//    List<String> hyponyms = new ArrayList<>();
//    //null check!!
//    if (nounGraph.getEdges(n) == null) {
//        return hyponyms;
//    }
//    // for this part I coudlnt figure it out so I used a combo of overflow and gemini to structure
//    //this part of the code
//for (int synid: nounGraph.getEdges(n)) {
//    for (int hypoid: hyponymGraph.getEdges(synid)) {
//        String[] hypoNouns = idToSynset.get(hypoid);
//        hyponyms.addAll(Arrays.asList(hypoNouns));
//    }
//}
//return  hyponyms;


//    public Set<String> givemehyponyms(String noun) {
//        Set<String> allHyponyms = new HashSet<>();
//        Set<Integer> visitedSynsets = new HashSet<>();
//
//        // Get all synset IDs for the given noun
//        List<Integer> synsetIds = nounGraph.getEdges(noun);
//
//        // For each synset ID, gather all hyponyms recursively
//        for (int synsetId : synsetIds) {
//            gatherHyponyms(synsetId, allHyponyms, visitedSynsets);
//        }
//
//        return allHyponyms;
//    }
//
//    private void gatherHyponyms(int synsetId, Set<String> hyponyms, Set<Integer> visited) {
//        if (visited.contains(synsetId)) return; // Avoid cycles
//        visited.add(synsetId);
//
//        // Add the words in this synset to the hyponyms set
//        String[] words = idToSynset.get(synsetId);
//        if (words != null) {
//            hyponyms.addAll(Arrays.asList(words));
//        }
//
//        // Recurse on all connected hyponyms in hyponymGraph
//        List<Integer> hyponymIds = hypo nymGraph.getEdges(synsetId);
//        for (int hyponymId : hyponymIds) {
//            gatherHyponyms(hyponymId, hyponyms, visited);
//        }
//    }



    public Set<String> givemehyponyms(String noun) {
        Set<String> allHyponyms = new HashSet<>();
        Set<Integer> visitedSynsets = new HashSet<>();

        List<Integer> synsetIds = nounGraph.getEdges(noun);

        for (int synsetId : synsetIds) {
            gatherHyponyms(synsetId, allHyponyms, visitedSynsets);
        }

        return allHyponyms;
    }

    private void gatherHyponyms(int synsetId, Set<String> hyponyms, Set<Integer> visited) {
        if (visited.contains(synsetId)) return;
        visited.add(synsetId);

        String[] words = idToSynset.get(synsetId);
        if (words != null) {
            hyponyms.addAll(Arrays.asList(words));
        }

        List<Integer> hyponymIds = hyponymGraph.getEdges(synsetId);
        for (int hyponymId : hyponymIds) {
            gatherHyponyms(hyponymId, hyponyms, visited);
        }
    }







}
