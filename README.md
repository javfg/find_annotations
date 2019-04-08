# Práctica de Análisis de Secuencias

Miguel Ángel Gutierrez Medina  
Osvaldas Vainauskas  
Javier Ferrer Gómez  


## Trabajo 3

### Enunciado

Implementación de un método de análisis de un grupo de proteínas similares a una dada, usando delta-blast como herramienta para identificación de similitudes. El objetivo es sugerir anotaciones *GO* y rutas *KEGG* a partir de las asociadas de proteínas similares. Solo se podrán sugerir resultados soportados por un porcentaje de identidad mínimo y un grado de apoyo mínimo. Ambos valores serán especificados por el usuario en tiempo de ejecución. Un apoyo 10 significa que al menos 10 secuencias deben tener esa anotación GO o la ruta KEGG asociada.

### Ayuda

```
usage: find_annotations.py [-h] [-f FILE] [-o PATH] [protein] min_identity min_support

Find similar proteins using Delta Blast and suggests GO annotations and KEGG
routes associated to them.

positional arguments:
  protein                 File with Protein accession ID or fasta sequence to analyze.
  min_identity            Minimum identity score to consider (Default: 75).
  min_support             Minimum support degree to consider (amount of
                          sequences sharing an annotation (Default: 10).

optional arguments:
  -h, --help              Show this help message and exit.
  -f FILE, --file FILE    Specify dblast output file with list of similar
                          proteins.
  -o PATH, --outfile PATH Specify output filename and path. An additional .svg file will be
                          created.
                         
```

### Descripción del proceso

1. Lee un archivo con la ID/secuencia de una proteina y realiza un Delta Blast o lee un archivo de resultado de Delta Blast directamente.
2. Busca las IDs de proteinas similares en UniProt.
3. Extrae los términos GO.
4. Extrae las KEGG IDs.
5. Busca las Ids KEGG en la base de datos KEGG.
6. Recupera los Pathways KEGG.
7. Dibuja un diagrama con los términos GO y KEGG.


### Instalación y uso

Requiere `pipenv` y `ncbi-blast+`.



#### Instalar [pipenv](https://pipenv.readthedocs.io/en/latest/)

```bash
pip install pipenv
```
#### Instalar [ncbi-blast+](https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/) [Opcional si se utilizan archivos con resultados de busquedas Delta Blast previas]

```sudo apt install ncbi-blast+```

#### Preparar *virtual enviroment*

Después de clonar el repositorio, ir al directorio raíz del mismo y ejecutar: ```pipenv install``` para crear el entorno e instalar todas las dependencias.

#### Ejecución

Para ejecutar el programa, hay que entrar en el entorno virtual:  
_Ejemplo con grado de identidad mínimo del 90% y soporte mínimo de 10 anotaciones, usando un archivo delta-blast_

```bash
pipenv shell
./src/find_annotations.py -f tsv/O14733.tsv 90 10
```


