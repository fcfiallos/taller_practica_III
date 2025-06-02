package com.talleri.student;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;

public class StudentMapper extends Mapper<LongWritable, Text, LongWritable, Text> {

    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        String line = value.toString();

        // Saltar encabezado
        if (line.startsWith("id,")) return;

        String[] fields = line.split(",", -1); // -1 mantiene campos vacíos

        // Validar que estén todas las columnas y que no haya valores faltantes
        if (fields.length == 18) {
            for (String field : fields) {
                if (field.trim().isEmpty()) return; // Saltar fila con campo vacío
            }

            try {
                // Codificación
                int gender = fields[1].trim().equalsIgnoreCase("Male") ? 0 : 1;
                int profession = fields[4].trim().equalsIgnoreCase("Student") ? 0 : 1;
                int depression = fields[17].trim().equalsIgnoreCase("Yes") ? 1 : 0;

                // Puedes extender estos encodings para más campos

                // Construcción de línea numérica
                StringBuilder cleanLine = new StringBuilder();
                cleanLine.append(fields[0].trim()).append(",");           // id
                cleanLine.append(gender).append(",");                     // Gender (0/1)
                cleanLine.append(fields[2].trim()).append(",");           // Age
                cleanLine.append(fields[3].trim()).append(",");           // City (como texto)
                cleanLine.append(profession).append(",");                 // Profession (0/1)
                cleanLine.append(fields[5].trim()).append(",");           // Academic Pressure
                cleanLine.append(fields[6].trim()).append(",");           // Work Pressure
                cleanLine.append(fields[7].trim()).append(",");           // CGPA
                cleanLine.append(fields[8].trim()).append(",");           // Study Satisfaction
                cleanLine.append(fields[9].trim()).append(",");           // Job Satisfaction
                cleanLine.append(fields[10].trim()).append(",");          // Sleep Duration
                cleanLine.append(fields[11].trim()).append(",");          // Dietary Habits
                cleanLine.append(fields[12].trim()).append(",");          // Degree
                cleanLine.append(fields[13].trim()).append(",");          // Suicidal thoughts
                cleanLine.append(fields[14].trim()).append(",");          // Work/Study Hours
                cleanLine.append(fields[15].trim()).append(",");          // Financial Stress
                cleanLine.append(fields[16].trim()).append(",");          // Family History
                cleanLine.append(depression);                             // Depression (0/1)

                // Emitir línea
                context.write(key, new Text(cleanLine.toString()));
            } catch (Exception e) {
                // Si ocurre algún error inesperado en los datos, se omite la fila
            }
        }
    }
}
