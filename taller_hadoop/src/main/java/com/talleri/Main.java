package com.talleri;

public class Main {
    public static void main(String[] args) {
        System.out.println("Este es el lanzador de jobs MapReduce. Ejecuta los jobs directamente con: ");
        System.out.println("hadoop jar target/taller_hadoop-1.0-SNAPSHOT.jar com.talleri.reddit.RedditJob /ruta/input /ruta/output");
    }
}
