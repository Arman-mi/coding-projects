package main;


import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class Graph<K,V> {
    HashMap<K, List<V>> storage;
    int size;
    public Graph(){
        this.storage = new HashMap<>();
        size = 0;

    }

    public void addVertex(K key) {
        if (!storage.containsKey(key)) {
            storage.put(key, new ArrayList<>());
        }
        size++;

    }
    public void addEdge(K key , V value) {
        List<V> edge = storage.get(key);
        if(edge == null) {
            edge = new ArrayList<>();
            storage.put(key,edge);
        }
        edge.add(value);


        
    }

    public List<V> getEdges(K key) {
        return storage.getOrDefault(key, new ArrayList<>());
    }

    public int getSize () {
        return size;
    }








}
