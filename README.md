# StructureFromMotion

Explicare de manera detallada como usar las librerías Colmap, OpenMVG y OpenMVS para los proyectos de su necesidad.<br>
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

## Uso de Colmap SFM

Para poder usar Colmap SFM se debe tener instalado Colmap en la computadora, para instalar Colmap puede seguir los pasos de esta pagina [Colmap](https://colmap.github.io/install.html). Una vez instlado podra usar todas las herramientas necesarias para la reconstruccion 3D.
Las funciones que puede usar para generar la nube de puntos son las siguientes:

    1. Feature Extraction

Extrae características visuales de las imágenes de entrada. Estas características son puntos clave que se utilizarán para emparejar las imágenes y reconstruir la escena en 3D.

    2. Feature Matching

Encuentra coincidencias entre las características extraídas de las imágenes. Estas coincidencias se utilizan para calcular la estructura 3D de la escena.

    3. Incremental/Sequential Structure-from-Motion

Realiza la reconstrucción incremental (o secuencial) de la estructura 3D de la escena. Utiliza las coincidencias de características y los parámetros de cámara para construir la estructura tridimensional.

    4. Global Structure-from-Motion

Realiza la reconstrucción global de la estructura 3D de la escena. Utiliza todas las imágenes de entrada para calcular la estructura tridimensional de la escena.

## Uso de OpenMVS

Para poder usar OpenMVS se debe tener instalado OpenMVS en la computadora, para instalar OpenMVS puede seguir los pasos de esta pagina [OpenMVS](https://hackmd.io/@weichenpai/S126TudDn). Una vez instlado podra usar todas las herramientas necesarias para la reconstruccion 3D.

Las funciones que puede usar para generar la malla 3D son las siguientes:

    1. Densify Point Cloud

Genera una nube de puntos densa a partir de la nube de puntos generada en el paso anterior. Utiliza la información de las imágenes y la nube de puntos para calcular la posición tridimensional de los puntos de la escena.

    2. Mesh Reconstruction

Genera una malla 3D a partir de la nube de puntos densa. Utiliza la información de la nube de puntos para construir una malla tridimensional que representa la forma de la escena.

    3. Refine Mesh

Refina la malla 3D generada en el paso anterior. Utiliza algoritmos de optimización para mejorar la calidad de la malla y eliminar artefactos.

    4. Texture Mapping

Mapea texturas a la malla 3D generada. Utiliza las imágenes de entrada para asignar texturas a la malla, creando un modelo 3D texturizado.

## ¿Cómo reconstruir el proyecto con el Dockerfile del proyecto?

En el proyecto se encuentra un archivo de nombre Dockerfile, este archivo contiene las instrucciones necesarias para crear una imagen de docker con todas las librerias necesarias para poder ejecutar los scripts de python de OpenMVG, OpenMVS y Colmap. Para poder crear la imagen de docker se debe ejecutar el siguiente comando en la terminal:

```bash
docker run -it --rm \
    -v /path/to/imagenes:/app/images \
    my_project_image
```

En esta parte del comando se debe cambiar /path/to/imagenes por la ruta a las imagenes que se desean usar para la reconstruccion 3D, y my_project_image por el nombre que se le desea dar a la imagen de docker. Una vez ejecutado el comando se creara la imagen de docker con todas las librerias necesarias para poder ejecutar los scripts de python de OpenMVG, OpenMVS y Colmap.
se ejecutara automaticamente el archivo de python apy.py debera indicar la ruta donde se encuentra las imagenes, la carpeta images es donde se encontrara las imagenes no cambiar este nombre **images** porque el script de python esta configurado para buscar las imagenes en esa carpeta, si desea montar el proyecto donde se ejecutara poner el nombre del proyecto dentro de app/<name_project> y dentro de esa carpeta poner la carpeta images con las imagenes.
La estructura del proyecto debe ser la siguiente:

```bash
app/
    images/
        image1.jpg
        image2.jpg
        ...
    OpenMVG.py
    OpenMVS.py
    Colmap.py
    app.py
```

o si desea montar el proyecto en una carpeta diferente a app, la estructura del proyecto debe ser la siguiente:

```bash
app/
    <name_project>/
        images/
            image1.jpg
            image2.jpg
            ...
    OpenMVG.py
    OpenMVS.py
    Colmap.py
    app.py
```

El proyecto se creara en la carpeta app/<name_project> con los archivos generados por los scripts de python de OpenMVG, OpenMVS y Colmap, para ejecutar este ultimo con docker sera asi:

```bash
docker run -it --rm \
    -v /path/to/project:/app/<name_project> \
    my_project_image
```

Para ingresar al contenedor de docker se debe ejecutar el siguiente comando en la terminal:

```bash
docker images
```

Este comando mostrara una lista con todas las imagenes de docker que se han creado, se debe buscar la imagen que se creo con el comando anterior y copiar el id de la imagen, una vez copiado el id se debe ejecutar el siguiente comando en la terminal:

```bash
docker run -it my_project_image bash
```

si el contenedor ya esta creado se puede ingresar con el siguiente comando:

```bash
docker exec -it <container_id> bash
```

Para hacer las pruebas de los scripts de python de OpenMVG, OpenMVS y Colmap se debe ejecutar el siguiente comando en la terminal:

```bash
curl -X POST http://localhost:5000/run_colmap -H "Content-Type: application/json" -d '{"project_path": "/app/<name_project>"}'
```

Que significa que se debe hacer una peticion POST a la url http://localhost:5000/run_colmap con el parametro project_path que es la ruta al proyecto que se desea reconstruir, en este caso se debe cambiar /app/<name_project> por la ruta al proyecto que se desea reconstruir.

Luego de ejecutar el comando anterior se generara la malla 3D del proyecto en la carpeta app/<name_project> con los archivos generados por los scripts de python de OpenMVG, OpenMVS y Colmap.

```bash
curl -X POST http://localhost:5000/run_openmvs -H "Content-Type: application/json" -d '{"project_path": "/app/<name_project>"}'
```

## ¿Cómo generar la malla de un conjunto de fotos?

Este trabajo se ve enfocado en eso que alguien que dese usar las librerias OpenMVG, OpenMVS y Colmap pueda hacerlo de manera sencilla, por lo que se ha creado un script de python que permite generar la malla 3D de un conjunto de fotos, solo debe pasar la ruta a las imagenes y el script se encargara de hacer todo el proceso.
En el script de python de nombre Colmap.py se encuentra el script para generar la nube de puntos a partir de un conjunto de imagenes, solo debe pasar la ruta a las imagenes. En el archivo de nombre OpenMVS.py se encuentra el script para generar la malla 3D a partir de la nube de puntos generada en el paso anterior, solo debe pasar la ruta del proyecto generado del anterior paso.

Muchas gracias por leer este documento, espero que les haya sido de ayuda y que puedan usar las librerias OpenMVG, OpenMVS y Colmap, para sus proyectos de necesidad.
:)
