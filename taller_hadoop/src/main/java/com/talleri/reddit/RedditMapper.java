package com.talleri.reddit;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

public class RedditMapper extends Mapper<LongWritable, Text, LongWritable, Text> {

    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String line = value.toString();

        // Saltar encabezado
        if (line.startsWith("count") || line.trim().isEmpty()) return;

        // Dividir por coma, con manejo de campos de texto con comas
        String[] fields = line.split(",(?=([^\"]*\"[^\"]*\")*[^\"]*$)", -1);

        if (fields.length >= 7) {
            for (String field : fields) {
                if (field.trim().isEmpty()) return; // Omitir fila con campos vacíos
            }

            try {
                String subreddit = fields[1].trim().replaceAll("\"", "");
                String title = fields[2].trim().replaceAll("\"", "");
                String body = fields[3].trim().replaceAll("\"", "");

                // Limpieza básica de texto (puedes mejorar esto con NLP posterior)
                title = title.replaceAll("[\\r\\n]+", " ").replaceAll(",", " ");
                body = body.replaceAll("[\\r\\n]+", " ").replaceAll(",", " ");

                int upvotes = Integer.parseInt(fields[4].trim());
                long createdUTC = Long.parseLong(fields[5].trim());
                int numComments = Integer.parseInt(fields[6].trim());
                int label = Integer.parseInt(fields[7].trim());

                // Construcción de línea de salida
                StringBuilder out = new StringBuilder();
                out.append(subreddit).append(",");
                out.append("\"").append(title).append("\"").append(",");
                out.append("\"").append(body).append("\"").append(",");
                out.append(upvotes).append(",");
                out.append(createdUTC).append(",");
                out.append(numComments).append(",");
                out.append(label);

                context.write(key, new Text(out.toString()));
            } catch (Exception e) {
                // Error al parsear números u otros: omitir línea
            }
        }
    }
}
