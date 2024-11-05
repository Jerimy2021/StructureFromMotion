# StructureFromMotion

Explicare de manera detallada como usar las librerías OpenMVG y OpenMVS para los proyectos de su necesidad.<br>
![Portada](https://lh3.googleusercontent.com/proxy/Bsv-VPwcmOMYo0J5iP00iZ8jJ44eNotuxGvDogiU0dXgeaTVRL2lbX_Q92fEksYss2Hc2lOtRaRIt0EpY7rq-7c7ng)

## Especiaciones Tecnicas

Para poder ejecutar los proyectos de OpenMVG y OpenMVS, se debe tener una computadora con las siguientes características:

-   Procesador: Intel Core i5 o superior
-   Memoria RAM: 32 GB o superior
-   Sistema Operativo: Ubuntu 18.04 o superior
-   Espacio en Disco: 1 TB o superior
-   Tener disponibilidad de gpu para el uso de OpenMVS(laptop con cuda para OpenMVS).

## Instalación de OpenMVG

Para instalar OpenMVG puede seguir los pasos de esta pagina [OpenMVG](https://github.com/openMVG/openMVG/blob/develop/BUILD.md)

## Instalación de OpenMVS

Para instalar OpenMVS puede seguir los pasos de esta pagina [OpenMVS](https://hackmd.io/@weichenpai/S126TudDn) en este link tambien se encuentra informacion de como instalar OpenMVG, en caso de tener porblemas con la instalacion de la primera parte.

## Uso de OpenMVG

En el script de python de nombre OpenMVG.py se encuentra el script para generar una nube de puntos a partir de un conjunto de imagenes, solo debe pasar la ruta a las imagenes.

Las funciones de OpenMVG para generar la nube de puntos es la siguiente:

    1.	Intrinsics Analysis (openMVG_main_SfMInit_ImageListing)

Realiza el análisis de los parámetros intrínsecos de la cámara. Crea un archivo sfm_data.json con información sobre las cámaras y sus parámetros intrínsecos (como la focal y las dimensiones del sensor). Este archivo es esencial para los pasos posteriores.

    2.	Compute Features (openMVG_main_ComputeFeatures)

Calcula características visuales de cada imagen en el directorio de entrada, utilizando el algoritmo SIFT. Estas características permiten identificar puntos clave únicos en las imágenes, lo cual es fundamental para el emparejamiento de imágenes en 3D.

    3.	Compute Matching Pairs (openMVG_main_PairGenerator)

Genera pares de imágenes que posiblemente coincidan (es decir, vistas de la misma escena). Este paso reduce la cantidad de emparejamientos que deben calcularse, agilizando el proceso de reconstrucción.

    4. Compute Matches (openMVG_main_ComputeMatches)

Encuentra coincidencias entre los puntos clave detectados en los pares de imágenes. Genera un archivo de coincidencias iniciales (matches.putative.bin), que indica qué puntos de dos imágenes podrían representar la misma ubicación en la escena.

    5. Filter Matches (openMVG_main_GeometricFilter)

Filtra las coincidencias detectadas utilizando un filtro geométrico para eliminar los emparejamientos incorrectos, generando un archivo más preciso (matches.f.bin) que se usará en la reconstrucción.

    6. Sequential/Incremental Reconstruction (openMVG_main_SfM)

Realiza la reconstrucción incremental (o secuencial) de la estructura 3D de la escena. Utiliza los emparejamientos de imágenes y los parámetros de cámara para construir la estructura tridimensional, almacenando la información en sfm_data.bin.

    7. Colorize Structure (openMVG_main_ComputeSfM_DataColor)

Asigna color a la estructura 3D generada. Exporta el archivo colorized.ply, un modelo 3D en formato PLY que contiene puntos de la estructura con color.
