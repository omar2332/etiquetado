# Programa de Etiquetado
## _Etiqueta y descarga imágenes de s3_

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

![S3](data:image/png;base64,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)

## Introducción
El software esta diseñado para hacer una clasificación binaria de imagenes almacenadas en S3, originalmente fue pensado para caracterizar torres eléctricas, pero puede ser usado para clasificar distintos elementos en las imágenes, se etiqueta con 1 si hay torre y 0 si no hay torre. Una vez terminado de clasificar la imagenes se genera automáticamente un archivo csv con las imágenes etiquetadas.

Adicionalmente  las imágenes pueden ser descargadas de su bucket de s3 para su posterior manipulación, pero sólo se descargaran las imágenes etiquetadas con 1.

## Instalación 
Para poder hacer uso del software es recomendable usar una versión de python 3  e instalar los siguientes paquetes:

			pip install tqdm
			pip install boto3
			pip install tk

Luego de instalar los paquetes anteriores se debe clonar el proyecto en la carpeta de su preferencia mediante la instrucción:

	 git clone "url_del_proyecto_sin_comillas"

> Importante: Verifique que se encuentre la carpeta **CSVs** como se muestra en la imagen, de no ser asi, cree la carpeta manualmente.

![Imgur](https://i.imgur.com/8KaZx0f.png)

Para iniciar el programa se debe ir a el directorio donde se clono el proyecto y ejecutar la instrucción:

	python app.py

Si la instalación fue correcta, el programa iniciará.


## Etiquetado de Imágenes
Para empezar a utilizar el programa se deben seguir los siguientes pasos

#### 1 Paso
Colocar las credenciales de AWS en los campos correspondientes y acceder.

![Primer Inicio](https://i.ibb.co/1bRcFpx/p1.png)

#### 2 Paso

Se abrirá la siguiente ventana, se debe seleccionar bucket y folder donde se encuentran las imágenes.

![Primer Inicio](https://i.ibb.co/C2C6Z2B/p2.png)

Luego de colocar esos campos pulsar "Login" y se abrira una ventana de que los datos se cargaron correctamente.
![Log 3](https://i.imgur.com/qu59fvf.png)

#### 3 Paso
Se mostrará una ventana como la siguiente 
![Imgur](https://i.imgur.com/O3v88Va.png)

Puede desplazarse con las teclas de dirección o con los botones de *next* y *back*. Para indicar cuando hay una torre pulse la barra espaciadora o marque con el mouse *¿Torre?*. Para guardar de clic en *guardar*, la próxima vez que ingrese a a la aplicación está iniciaria en la última imagen guardada.

#### Paso 4
Cuando se terminen las imágenes, se mostrará un mensaje de completitud, para detener la aplicación primero debe cerrar la aplicación y luego la terminal. En la carpeta de **etiquetas** aparecerá el csv generado.

## Descarga de Imágenes

Para descargar las imágenes considere lo siguiente:

1. Coloque las credenciales como se indica en el **Paso 1**, pero no de clic en **login**.
2.  Pulse la opción **select directory to save images**, e indique el directorio donde se van a descargar las imágenes.
3.  Seleccione la opción **select directory to csv files** e indique el csv que se utilizará.
4.  De clic en **start** y espere mientras se descargan las imágenes, luego de unos segundos aparecerán las imágenes descargadas en la carpeta que se eligió.
