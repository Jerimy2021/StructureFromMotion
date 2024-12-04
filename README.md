# StructureFromMotion

Explicare de manera detallada como usar las librerías Colmap, OpenMVG y OpenMVS para los proyectos de su necesidad.<br>
![Portada](https://lh3.googleusercontent.com/proxy/Bsv-VPwcmOMYo0J5iP00iZ8jJ44eNotuxGvDogiU0dXgeaTVRL2lbX_Q92fEksYss2Hc2lOtRaRIt0EpY7rq-7c7ng)

## Especificaciones Técnicas

Para poder ejecutar los proyectos de OpenMVG y OpenMVS, se debe tener una computadora con las siguientes características:

-   Procesador: Intel Core i5 o superior
-   Memoria RAM: 32 GB o superior
-   Sistema Operativo: Ubuntu 18.04 o superior
-   Espacio en Disco: 1 TB o superior
-   Tener disponibilidad de GPU para el uso de OpenMVS(laptop con cuda para OpenMVS).

## Instalación de OpenMVS

Para instalar OpenMVS puede seguir los pasos de esta página [OpenMVS](https://hackmd.io/@weichenpai/S126TudDn) en este link también se encuentra información de como instalar OpenMVG, en caso de tener problemas con la instalación de la primera parte.

## Uso de Colmap SFM

Para poder usar Colmap SFM se debe tener instalado Colmap en la computadora, para instalar Colmap puede seguir los pasos de esta página [Colmap](https://colmap.github.io/install.html). Una vez instalado podrá usar todas las herramientas necesarias para la reconstrucción 3D.
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

Para poder usar OpenMVS se debe tener instalado OpenMVS en la computadora, para instalar OpenMVS puede seguir los pasos de esta página [OpenMVS](https://hackmd.io/@weichenpai/S126TudDn). Una vez instalado podrá usar todas las herramientas necesarias para la reconstruccion 3D.

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

En esta parte del comando se debe cambiar /path/to/imagenes por la ruta a las imágenes que se desean usar para la reconstrucción 3D, y my_project_image por el nombre que se le desea dar a la imagen de docker. Una vez ejecutado el comando se creara la imagen de docker con todas las librerias necesarias para poder ejecutar los scripts de python de OpenMVG, OpenMVS y Colmap.
se ejecutará automáticamente el archivo de python apy.py debera indicar la ruta donde se encuentra las imágenes, la carpeta images es donde se encontrara las imágenes no cambiar este nombre **images** porque el script de python esta configurado para buscar las imágenes en esa carpeta, si desea montar el proyecto donde se ejecutara poner el nombre del proyecto dentro de app/<name_project> y dentro de esa carpeta poner la carpeta images con las imágenes.
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

El proyecto se creara en la carpeta app/<name_project> con los archivos generados por los scripts de python de OpenMVG, OpenMVS y Colmap, para ejecutar este último con docker sera asi:

```bash
docker run -it --rm \
    -v /path/to/project:/app/<name_project> \
    my_project_image
```

Para ingresar al contenedor de docker se debe ejecutar el siguiente comando en la terminal:

```bash
docker images
```

Este comando mostrará una lista con todas las imágenes de docker que se han creado, se debe buscar la imagen que se creo con el comando anterior y copiar el id de la imagen, una vez copiado el id se debe ejecutar el siguiente comando en la terminal:

```bash
docker run -it my_project_image bash
```

si el contenedor ya está creado se puede ingresar con el siguiente comando:

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

Este trabajo se ve enfocado en eso que alguien que dese usar las librerias OpenMVG, OpenMVS y Colmap pueda hacerlo de manera sencilla, por lo que se ha creado un script de python que permite generar la malla 3D de un conjunto de fotos, solo debe pasar la ruta a las imágenes y el script se encargará de hacer todo el proceso.
En el script de python de nombre Colmap.py se encuentra el script para generar la nube de puntos a partir de un conjunto de imágenes, solo debe pasar la ruta a las imágenes. En el archivo de nombre OpenMVS.py se encuentra el script para generar la malla 3D a partir de la nube de puntos generada en el paso anterior, solo debe pasar la ruta del proyecto generado del anterior paso.

Muchas gracias por leer este documento, espero que les haya sido de ayuda y que puedan usar las librerías OpenMVG, OpenMVS y Colmap, para sus proyectos de necesidad.
:)
