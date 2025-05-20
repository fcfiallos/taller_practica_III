package com.talleri.student;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

public class StudentMapper extends Mapper<Object, Text, Text, IntWritable> {
    private static final IntWritable one = new IntWritable(1);
    private Text label = new Text();

    public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
        // Saltar el encabezado
        if (value.toString().startsWith("Gender")) return;

        String[] fields = value.toString().split(",");
        if (fields.length >= 5) {
            String depressionStatus = fields[4].trim();
            if (!depressionStatus.isEmpty()) {
                label.set(depressionStatus); // "Yes" o "No"
                context.write(label, one);
            }
        }
    }
}
