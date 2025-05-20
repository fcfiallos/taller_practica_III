package com.talleri.reddit;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

public class RedditMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
    private final static IntWritable one = new IntWritable(1);
    private Text word = new Text();

    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        for (String token : value.toString().split("\\s+")) {
            word.set(token.toLowerCase().replaceAll("[^a-zA-Z]", ""));
            if (!word.toString().isEmpty()) {
                context.write(word, one);
            }
        }
    }
}

